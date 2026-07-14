#!/usr/bin/env python3
"""Validate decision-attribution receipts against the repository schema."""

from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    import jsonschema
except ImportError as exc:  # pragma: no cover
    raise SystemExit("jsonschema is required: python -m pip install jsonschema") from exc

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "decision-attribution-receipt.schema.json"
RECEIPT_ROOT = ROOT / "decision-attribution-receipts"


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def semantic_checks(receipt: dict, path: Path) -> list[str]:
    errors: list[str] = []

    authority = receipt.get("authority_chain", [])
    responsibility = receipt.get("responsibility_chain", [])

    authority_sequences = [item.get("sequence") for item in authority]
    if authority_sequences != list(range(1, len(authority_sequences) + 1)):
        errors.append(f"{path}: authority_chain sequence must be contiguous from 1")

    responsibility_sequences = [item.get("sequence") for item in responsibility]
    if responsibility_sequences != list(range(1, len(responsibility_sequences) + 1)):
        errors.append(f"{path}: responsibility_chain sequence must be contiguous from 1")

    if receipt.get("decision_time") is None and receipt.get("decision_time_status") not in {
        "period-only",
        "unknown",
    }:
        errors.append(f"{path}: null decision_time requires period-only or unknown status")

    override = receipt.get("override")
    if override and override.get("occurred"):
        if not override.get("override_authority") or not override.get("override_reason"):
            errors.append(f"{path}: occurred override requires authority and reason")

    if receipt.get("promotion_state") != "fixture-only" and receipt.get("verification_status") == "fixture":
        errors.append(f"{path}: fixture verification cannot be promoted beyond fixture-only")

    if receipt.get("final_legal_finding") is not None and receipt.get("promotion_state") != "promoted":
        errors.append(f"{path}: final_legal_finding requires promoted state")

    return errors


def main() -> int:
    schema = load_json(SCHEMA_PATH)
    validator = jsonschema.Draft202012Validator(schema)
    files = sorted(RECEIPT_ROOT.rglob("*.json"))

    if not files:
        print("No decision-attribution receipts found.", file=sys.stderr)
        return 1

    failures: list[str] = []
    for path in files:
        receipt = load_json(path)
        for error in sorted(validator.iter_errors(receipt), key=lambda item: list(item.path)):
            location = ".".join(str(part) for part in error.path) or "<root>"
            failures.append(f"{path}: {location}: {error.message}")
        if isinstance(receipt, dict):
            failures.extend(semantic_checks(receipt, path))

    if failures:
        print("Decision-attribution receipt validation failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    print(f"Validated {len(files)} decision-attribution receipt(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
