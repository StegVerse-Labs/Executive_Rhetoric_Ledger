#!/usr/bin/env python3
"""Materialize the latest valid Issue #26 review comment into a governed receipt."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "producer-reviewed-receipt.schema.json"
INTAKE_ID = "ADMINISTRATIONS-EXPORT-EO14179-ACTION-001"
MARKER = "ERL-PRODUCER-REVIEW-V1"
ALLOWED = {"approved-action-record", "needs-primary-source", "needs-context-revision", "rejected-unsupported", "rejected-out-of-scope"}


def parse(body: str) -> dict[str, str] | None:
    if MARKER not in body:
        return None
    fields: dict[str, str] = {}
    for line in body.splitlines():
        m = re.match(r"^([a-z-]+):\s*(.+?)\s*$", line.strip())
        if m:
            fields[m.group(1)] = m.group(2)
    if not {"disposition", "rationale", "documents-issuance-and-text"}.issubset(fields):
        return None
    if fields["disposition"] not in ALLOWED:
        return None
    if fields["documents-issuance-and-text"].lower() not in {"true", "false"}:
        return None
    return fields


def find_sha(value: object) -> str | None:
    if isinstance(value, dict):
        if value.get("ingestion_id") == INTAKE_ID or value.get("intake_id") == INTAKE_ID:
            for key in ("sha256", "export_sha256", "record_sha256"):
                candidate = value.get(key)
                if isinstance(candidate, str) and re.fullmatch(r"[a-f0-9]{64}", candidate):
                    return candidate
        for child in value.values():
            found = find_sha(child)
            if found:
                return found
    elif isinstance(value, list):
        for child in value:
            found = find_sha(child)
            if found:
                return found
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--comments", required=True)
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--receipt", required=True)
    ap.add_argument("--state", required=True)
    args = ap.parse_args()

    comments = json.loads(Path(args.comments).read_text())
    valid = []
    for comment in comments:
        parsed = parse(str(comment.get("body", "")))
        if parsed:
            valid.append((str(comment["created_at"]), int(comment["id"]), comment, parsed))
    state = {"review_issue": 26, "intake_id": INTAKE_ID, "status": "awaiting-governed-review", "receipt_created": False, "manual_mechanics_remaining": False, "human_authority_remaining": True}
    if valid:
        _, comment_id, comment, fields = sorted(valid)[-1]
        export_sha = find_sha(json.loads(Path(args.manifest).read_text()))
        if not export_sha:
            state["status"] = "retry-pending-manifest-hash"
        else:
            disposition = fields["disposition"]
            issuance = fields["documents-issuance-and-text"].lower() == "true"
            if disposition == "approved-action-record" and not issuance:
                raise SystemExit("approved-action-record requires documents-issuance-and-text: true")
            receipt = {
                "review_receipt_id": f"ERL-ISSUE26-COMMENT-{comment_id}",
                "review_issue": 26,
                "reviewer": str(comment.get("user", {}).get("login", "")),
                "reviewed_at": str(comment["created_at"]),
                "producer_repository": "StegVerse-Labs/Administrations",
                "intake_id": INTAKE_ID,
                "export_sha256": export_sha,
                "disposition": disposition,
                "rationale": fields["rationale"],
                "scope": {"documents_issuance_and_text": issuance, "proves_embedded_rhetoric_truth": False, "permits_broader_causation_claim": False},
                "authority": {"human_reviewed": True, "automation_may_verify": True, "automation_may_create_decision": False, "automation_may_expand_scope": False}
            }
            errors = list(Draft202012Validator(json.loads(SCHEMA.read_text()), format_checker=FormatChecker()).iter_errors(receipt))
            if errors:
                raise SystemExit(errors[0].message)
            out = Path(args.receipt); out.parent.mkdir(parents=True, exist_ok=True); out.write_text(json.dumps(receipt, indent=2) + "\n")
            state.update({"status": "governed-review-receipt-ready", "receipt_created": True, "human_authority_remaining": False, "disposition": disposition})
    state_path = Path(args.state); state_path.parent.mkdir(parents=True, exist_ok=True); state_path.write_text(json.dumps(state, indent=2) + "\n")
    print(json.dumps(state, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
