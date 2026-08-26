#!/usr/bin/env python3
"""Validate snapshot hashing, source-conflict handling, and portable verification receipts."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT_HASHER = ROOT / "scripts" / "finalize_physical_economics_evidence_snapshot.py"
CONFLICT_RUNTIME = ROOT / "scripts" / "physical_economics_source_conflicts.py"
VERIFIER_RUNTIME = ROOT / "scripts" / "generate_physical_economics_report_verification_receipt.py"
VERIFIER_SCHEMA = ROOT / "schemas" / "physical-economics-report-verification-receipt.schema.json"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    hasher = load_module(SNAPSHOT_HASHER, "pe_snapshot_hasher")
    conflicts = load_module(CONFLICT_RUNTIME, "pe_source_conflicts")
    verifier = load_module(VERIFIER_RUNTIME, "pe_report_verifier")
    verifier_schema = load(VERIFIER_SCHEMA)
    failures: list[str] = []

    snapshot = {
        "evidence_snapshot_id": "SNAP-INTEGRITY",
        "created_at": "2026-08-26T01:00:00-05:00",
        "report_request_id": "REQ-INTEGRITY",
        "requested_as_of_time": "2026-08-26T00:30:00-05:00",
        "pertinence_matrix_version": "0.1",
        "attributes": [],
        "source_receipts": [],
        "snapshot_hash": "PENDING"
    }
    finalized = hasher.finalize(snapshot)
    valid, expected = hasher.verify(finalized)
    if not valid or finalized["snapshot_hash"] != expected or not expected.startswith("sha256:"):
        failures.append("snapshot hashing: finalized snapshot did not self-verify")
    tampered = dict(finalized)
    tampered["report_request_id"] = "REQ-TAMPERED"
    valid, _ = hasher.verify(tampered)
    if valid:
        failures.append("snapshot hashing: tampered snapshot remained verifiable")

    source_receipts = [
        {
            "source_receipt_id": "SRC-OLD",
            "revision_status": "CURRENT_VINTAGE",
            "supersedes_source_receipt_id": None
        },
        {
            "source_receipt_id": "SRC-CORRECTED",
            "revision_status": "CORRECTED",
            "supersedes_source_receipt_id": "SRC-OLD"
        }
    ]
    explicit = conflicts.resolve_conflict(
        {"conflict_id": "C1", "source_receipt_ids": ["SRC-OLD", "SRC-CORRECTED"], "status": "UNRESOLVED"},
        source_receipts,
    )
    if explicit.get("status") != "RESOLVED_BY_OFFICIAL_CORRECTION":
        failures.append("source conflicts: explicit correction chain did not resolve")
    unresolved = conflicts.resolve_conflict(
        {"conflict_id": "C2", "source_receipt_ids": ["SRC-OLD", "SRC-CORRECTED"], "status": "UNRESOLVED"},
        [dict(source_receipts[0]), {**source_receipts[1], "revision_status": "CURRENT_VINTAGE", "supersedes_source_receipt_id": None}],
    )
    if unresolved.get("status") != "UNRESOLVED":
        failures.append("source conflicts: ambiguous values were reconciled without explicit basis")

    snapshot_for_receipt = {
        "evidence_snapshot_id": "SNAP-VR",
        "snapshot_hash": "sha256:abc123",
        "source_receipts": [{"source_receipt_id": "SRC-1"}]
    }
    request = {"report_request_id": "REQ-VR"}
    boundary = {
        "boundary_manifest_id": "BM-VR",
        "evidence_snapshot_id": "SNAP-VR",
        "receipts": {
            "report_request_hash": "sha256:req",
            "evidence_snapshot_hash": "sha256:abc123",
            "boundary_manifest_hash": "sha256:bm",
            "source_receipt_set": ["SRC-1"],
            "contract_version": "physical-economics-report-generation.v0.1",
            "pertinence_matrix_version": "0.1"
        }
    }
    receipt = verifier.generate("REPORT-VR", b"portable report bytes", request, snapshot_for_receipt, boundary, "renderer.v0.1")
    errors = list(Draft202012Validator(verifier_schema, format_checker=FormatChecker()).iter_errors(receipt))
    if errors:
        failures.extend(f"verification receipt schema: {error.message}" for error in errors)
    if receipt.get("verification_state") != "VERIFIABLE" or not receipt.get("report_content_hash", "").startswith("sha256:"):
        failures.append("portable verification: consistent inputs did not produce VERIFIABLE receipt")
    broken_boundary = json.loads(json.dumps(boundary))
    broken_boundary["receipts"]["evidence_snapshot_hash"] = "sha256:different"
    broken = verifier.generate("REPORT-VR", b"portable report bytes", request, snapshot_for_receipt, broken_boundary, "renderer.v0.1")
    if broken.get("verification_state") != "FAIL_CLOSED_HASH_MISMATCH":
        failures.append("portable verification: snapshot hash mismatch did not fail closed")

    if failures:
        for failure in failures:
            print(f"FAIL {failure}")
        return 1

    print("PASS immutable snapshot self-verification")
    print("PASS fail-closed source conflict handling")
    print("PASS portable report verification receipts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
