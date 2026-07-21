#!/usr/bin/env python3
"""Verify a human-authored producer review receipt and emit bounded activation state.

This script validates a decision; it never creates, changes, or broadens one.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas/producer-reviewed-receipt.schema.json"
DEFAULT_RECEIPT = ROOT / "producer_intake/reviewed-receipts/ADMINISTRATIONS-EXPORT-EO14179-ACTION-001.json"
DEFAULT_OUTPUT = ROOT / "producer_intake/review-activation/ADMINISTRATIONS-EXPORT-EO14179-ACTION-001.json"


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", type=Path, default=DEFAULT_RECEIPT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    if not args.receipt.exists():
        write_json(args.output, {
            "intake_id": "ADMINISTRATIONS-EXPORT-EO14179-ACTION-001",
            "status": "awaiting-governed-review",
            "review_issue": 26,
            "compendium_eligible": False,
            "propagation_eligible": False,
            "authority": {
                "automation_created_decision": False,
                "automation_may_verify": True,
                "automation_may_publish_without_approval": False
            }
        })
        print("No governed review receipt exists; activation remains blocked.")
        return 0

    receipt_bytes = args.receipt.read_bytes()
    receipt = json.loads(receipt_bytes)
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    errors = sorted(
        Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(receipt),
        key=lambda error: list(error.path),
    )
    if errors:
        raise SystemExit(f"Governed review receipt invalid: {errors[0].message}")

    approved = receipt["disposition"] == "approved-action-record"
    if approved and not receipt["scope"]["documents_issuance_and_text"]:
        raise SystemExit("Approved action record must affirm bounded issuance/text scope")

    write_json(args.output, {
        "intake_id": receipt["intake_id"],
        "review_issue": receipt["review_issue"],
        "review_receipt_id": receipt["review_receipt_id"],
        "review_receipt_sha256": hashlib.sha256(receipt_bytes).hexdigest(),
        "disposition": receipt["disposition"],
        "status": "reviewed-approved" if approved else "reviewed-not-approved",
        "compendium_eligible": approved,
        "propagation_eligible": approved,
        "scope": receipt["scope"],
        "authority": {
            "automation_created_decision": False,
            "automation_may_verify": True,
            "automation_may_publish_without_approval": False,
            "automation_may_expand_scope": False
        }
    })
    print(f"Verified governed review disposition: {receipt['disposition']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
