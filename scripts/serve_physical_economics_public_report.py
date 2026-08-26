#!/usr/bin/env python3
"""Fail-closed HTTP transport for the ERL Physical Economics report transaction.

This adapter does not acquire evidence. It selects only a pre-admitted prepared
snapshot template, rebinds request identity/as-of metadata, invokes the existing
report transaction, and returns the report document plus portable verification.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from datetime import date
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
REQUEST_SCHEMA = ROOT / "schemas" / "physical-economics-report-request.schema.json"
REGISTRY_SCHEMA = ROOT / "schemas" / "physical-economics-report-snapshot-registry.schema.json"
REPORT_TRANSACTION = ROOT / "scripts" / "generate_physical_economics_public_report.py"
POST_PATH = "/v1/physical-economics/reports"
HEALTH_PATH = "/healthz"
READY_PATH = "/readyz"
MAX_BODY_BYTES = 1024 * 1024


class AdapterError(RuntimeError):
    def __init__(self, code: str, message: str, status: int = 503):
        super().__init__(message)
        self.code = code
        self.status = status


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_schema(value: Any, schema_path: Path, label: str) -> None:
    validator = Draft202012Validator(load_json(schema_path), format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(value), key=lambda e: list(e.absolute_path))
    if errors:
        detail = "; ".join(error.message for error in errors[:5])
        raise AdapterError("INVALID_" + label.upper(), detail, 400)


def normalized_claim_classes(request: dict[str, Any]) -> tuple[str, ...]:
    return tuple(sorted(request["claim_classes"]))


def scope_matches(entry_scope: dict[str, Any], request_scope: dict[str, Any]) -> bool:
    required = ("subject", "economic_domain", "geography", "population_scope")
    if any(entry_scope.get(k) != request_scope.get(k) for k in required):
        return False
    for optional in ("essential_or_discretionary_class", "unit_definition"):
        if optional in entry_scope and entry_scope.get(optional) != request_scope.get(optional):
            return False
    return True


def entry_matches(entry: dict[str, Any], request: dict[str, Any]) -> bool:
    if entry["state"] != "ADMITTED":
        return False
    if not scope_matches(entry["scope"], request["scope"]):
        return False
    if tuple(sorted(entry["claim_classes"])) != normalized_claim_classes(request):
        return False
    if entry["pertinence_matrix_version"] != request["pertinence_policy"]["required_attribute_sets_version"]:
        return False
    vintage = request.get("vintage_policy", "CURRENT_VINTAGE")
    return vintage in entry["allowed_vintage_policies"]


def select_registry_entry(registry: dict[str, Any], request: dict[str, Any]) -> dict[str, Any]:
    matches = [entry for entry in registry["entries"] if entry_matches(entry, request)]
    if not matches:
        raise AdapterError(
            "NO_ADMITTED_SNAPSHOT",
            "No admitted prepared evidence snapshot matches the request.",
            503,
        )
    if len(matches) != 1:
        raise AdapterError(
            "AMBIGUOUS_ADMITTED_SNAPSHOT",
            "Multiple admitted prepared evidence snapshots match the request.",
            503,
        )
    return matches[0]


def resolve_snapshot_path(entry: dict[str, Any]) -> Path:
    candidate = (ROOT / entry["snapshot_template_path"]).resolve()
    root = ROOT.resolve()
    if candidate != root and root not in candidate.parents:
        raise AdapterError("INVALID_SNAPSHOT_PATH", "Snapshot path escapes repository root.", 503)
    if not candidate.is_file():
        raise AdapterError("SNAPSHOT_UNAVAILABLE", "Admitted snapshot template is unavailable.", 503)
    return candidate


def enforce_historical_vintage(snapshot: dict[str, Any], request: dict[str, Any]) -> None:
    if request.get("vintage_policy", "CURRENT_VINTAGE") != "AS_KNOWN_AT_REQUESTED_TIME":
        return
    as_of = date.fromisoformat(request["requested_as_of_time"][:10])
    later_dates: list[str] = []
    for receipt in snapshot.get("source_receipts", []):
        release_date = receipt.get("release_date")
        if release_date and date.fromisoformat(release_date) > as_of:
            later_dates.append(f"source:{receipt.get('source_receipt_id', 'UNKNOWN')}={release_date}")
    for attribute in snapshot.get("attributes", []):
        release_date = attribute.get("source_release_date")
        if release_date and date.fromisoformat(release_date) > as_of:
            later_dates.append(f"attribute:{attribute.get('attribute_id', 'UNKNOWN')}={release_date}")
    if later_dates:
        raise AdapterError(
            "HISTORICAL_VINTAGE_VIOLATION",
            "Prepared evidence contains releases later than the requested as-of time.",
            503,
        )


def bind_snapshot(template: dict[str, Any], request: dict[str, Any]) -> dict[str, Any]:
    snapshot = copy.deepcopy(template)
    snapshot["report_request_id"] = request["report_request_id"]
    snapshot["requested_as_of_time"] = request["requested_as_of_time"]
    snapshot["snapshot_hash"] = "PENDING"
    enforce_historical_vintage(snapshot, request)
    return snapshot


def report_id_for_request(request: dict[str, Any]) -> str:
    digest = hashlib.sha256(
        json.dumps(request, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    ).hexdigest()[:16]
    return f"PE-HTTP-{digest}"


def generate_response(request: dict[str, Any], registry_path: Path) -> dict[str, Any]:
    validate_schema(request, REQUEST_SCHEMA, "request")
    registry = load_json(registry_path)
    validate_schema(registry, REGISTRY_SCHEMA, "registry")
    entry = select_registry_entry(registry, request)
    template = load_json(resolve_snapshot_path(entry))
    snapshot = bind_snapshot(template, request)

    if snapshot.get("pertinence_matrix_version") != request["pertinence_policy"]["required_attribute_sets_version"]:
        raise AdapterError(
            "SNAPSHOT_PERTINENCE_MISMATCH",
            "Admitted snapshot pertinence matrix does not match request.",
            503,
        )

    with tempfile.TemporaryDirectory(prefix="pe-report-http-") as temp_name:
        temp = Path(temp_name)
        request_path = temp / "request.json"
        snapshot_path = temp / "snapshot-draft.json"
        output_dir = temp / "output"
        request_path.write_text(json.dumps(request, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        snapshot_path.write_text(json.dumps(snapshot, indent=2, sort_keys=True) + "\n", encoding="utf-8")

        result = subprocess.run(
            [
                sys.executable,
                str(REPORT_TRANSACTION),
                str(request_path),
                str(snapshot_path),
                "--report-id",
                report_id_for_request(request),
                "--output-dir",
                str(output_dir),
            ],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=60,
            check=False,
        )
        if result.returncode != 0:
            raise AdapterError(
                "REPORT_TRANSACTION_FAILED",
                "The governed report transaction failed closed.",
                503,
            )

        try:
            transaction = json.loads(result.stdout)
            document = load_json(output_dir / "report-document.json")
            receipt = load_json(output_dir / "verification-receipt.json")
            markdown = (output_dir / "report.md").read_text(encoding="utf-8")
        except (json.JSONDecodeError, OSError, KeyError) as exc:
            raise AdapterError(
                "REPORT_TRANSACTION_INVALID_OUTPUT",
                "The governed report transaction returned incomplete output.",
                503,
            ) from exc

    if transaction.get("state") != "GENERATED_NOT_PUBLICLY_ACTIVATED":
        raise AdapterError("REPORT_STATE_NOT_ADMISSIBLE", "Report state is not admissible.", 503)
    if receipt.get("verification_state") != "VERIFIABLE":
        raise AdapterError("REPORT_NOT_VERIFIABLE", "Portable verification did not pass.", 503)
    if receipt.get("report_id") != document.get("report_id"):
        raise AdapterError("REPORT_ID_MISMATCH", "Report document and receipt identifiers differ.", 503)

    return {
        "state": transaction["state"],
        "report_document": document,
        "verification_receipt": receipt,
        "report_markdown": markdown,
    }


def make_handler(registry_path: Path, allowed_origin: str | None):
    class Handler(BaseHTTPRequestHandler):
        server_version = "StegVersePhysicalEconomicsHTTP/0.1"

        def _origin_allowed(self) -> bool:
            origin = self.headers.get("Origin")
            if not origin:
                return True
            return bool(allowed_origin and origin == allowed_origin)

        def _headers(self, status: int, content_type: str = "application/json") -> None:
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Referrer-Policy", "no-referrer")
            if allowed_origin:
                self.send_header("Access-Control-Allow-Origin", allowed_origin)
                self.send_header("Vary", "Origin")
            self.end_headers()

        def _json(self, status: int, payload: dict[str, Any]) -> None:
            encoded = json.dumps(payload, sort_keys=True).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(encoded)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Referrer-Policy", "no-referrer")
            if allowed_origin:
                self.send_header("Access-Control-Allow-Origin", allowed_origin)
                self.send_header("Vary", "Origin")
            self.end_headers()
            self.wfile.write(encoded)

        def do_OPTIONS(self) -> None:
            if self.path != POST_PATH or not self._origin_allowed():
                self._json(403, {"state": "FAIL_CLOSED", "code": "ORIGIN_NOT_ALLOWED"})
                return
            self.send_response(204)
            if allowed_origin:
                self.send_header("Access-Control-Allow-Origin", allowed_origin)
                self.send_header("Vary", "Origin")
            self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type, Accept")
            self.send_header("Access-Control-Max-Age", "300")
            self.end_headers()

        def do_GET(self) -> None:
            if self.path == HEALTH_PATH:
                self._json(200, {"state": "LIVE", "service": "physical-economics-report-http"})
                return
            if self.path == READY_PATH:
                try:
                    registry = load_json(registry_path)
                    validate_schema(registry, REGISTRY_SCHEMA, "registry")
                    admitted = sum(entry["state"] == "ADMITTED" for entry in registry["entries"])
                    state = "READY" if admitted else "NOT_READY"
                    self._json(200 if admitted else 503, {"state": state, "admitted_snapshot_count": admitted})
                except Exception:
                    self._json(503, {"state": "NOT_READY"})
                return
            self._json(404, {"state": "FAIL_CLOSED", "code": "NOT_FOUND"})

        def do_POST(self) -> None:
            if self.path != POST_PATH:
                self._json(404, {"state": "FAIL_CLOSED", "code": "NOT_FOUND"})
                return
            if not self._origin_allowed():
                self._json(403, {"state": "FAIL_CLOSED", "code": "ORIGIN_NOT_ALLOWED"})
                return
            if self.headers.get("Content-Type", "").split(";", 1)[0].strip().lower() != "application/json":
                self._json(415, {"state": "FAIL_CLOSED", "code": "CONTENT_TYPE_REQUIRED"})
                return
            try:
                length = int(self.headers.get("Content-Length", "0"))
            except ValueError:
                length = -1
            if length <= 0 or length > MAX_BODY_BYTES:
                self._json(413, {"state": "FAIL_CLOSED", "code": "INVALID_BODY_SIZE"})
                return
            try:
                request = json.loads(self.rfile.read(length))
                response = generate_response(request, registry_path)
                self._json(200, response)
            except json.JSONDecodeError:
                self._json(400, {"state": "FAIL_CLOSED", "code": "INVALID_JSON"})
            except AdapterError as exc:
                self._json(exc.status, {"state": "FAIL_CLOSED", "code": exc.code, "message": str(exc)})
            except Exception:
                self._json(503, {"state": "FAIL_CLOSED", "code": "UNEXPECTED_FAIL_CLOSED"})

        def log_message(self, fmt: str, *args: Any) -> None:
            sys.stderr.write("physical-economics-http: " + (fmt % args) + "\n")

    return Handler


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--registry",
        type=Path,
        default=Path(os.environ.get("PE_REPORT_SNAPSHOT_REGISTRY", "")),
        help="Path to admitted snapshot registry.",
    )
    parser.add_argument("--host", default=os.environ.get("PE_REPORT_HOST", "127.0.0.1"))
    parser.add_argument("--port", type=int, default=int(os.environ.get("PE_REPORT_PORT", "8080")))
    parser.add_argument("--allowed-origin", default=os.environ.get("PE_REPORT_ALLOWED_ORIGIN") or None)
    args = parser.parse_args()

    if not str(args.registry):
        print("FAIL PE_REPORT_SNAPSHOT_REGISTRY or --registry is required", file=sys.stderr)
        return 2
    registry_path = args.registry if args.registry.is_absolute() else (ROOT / args.registry)
    registry_path = registry_path.resolve()
    try:
        registry = load_json(registry_path)
        validate_schema(registry, REGISTRY_SCHEMA, "registry")
    except Exception as exc:
        print(f"FAIL registry unavailable or invalid: {exc}", file=sys.stderr)
        return 2

    server = ThreadingHTTPServer((args.host, args.port), make_handler(registry_path, args.allowed_origin))
    print(f"LISTEN physical-economics-report-http {args.host}:{args.port}", file=sys.stderr)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
