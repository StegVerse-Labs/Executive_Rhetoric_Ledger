#!/usr/bin/env python3
"""Validate repository-neutral federal force-event packets and authority boundaries."""
from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / "schemas/federal-force-event.schema.json").read_text(encoding="utf-8"))


def main() -> int:
    validator = Draft202012Validator(SCHEMA, format_checker=FormatChecker())
    paths = sorted((ROOT / "assessments/events").glob("RRM-FORCE-*.json"))
    if len(paths) != 3:
        raise SystemExit(f"Expected three Ruben Ray Martinez force-event packets; found {len(paths)}")
    ids: set[str] = set()
    for path in paths:
        document = json.loads(path.read_text(encoding="utf-8"))
        errors = sorted(validator.iter_errors(document), key=lambda error: list(error.path))
        if errors:
            raise SystemExit(f"{path}: {errors[0].message}")
        if document["event_id"] in ids:
            raise SystemExit(f"Duplicate event ID: {document['event_id']}")
        ids.add(document["event_id"])
        if document["case_id"] != "RRM-SPI-2025-03-15":
            raise SystemExit("Martinez packet escaped its case boundary")
        if document["event_status"] != "candidate-review-required":
            raise SystemExit("Unreviewed Martinez packet changed review status")
        if document["classification"]["official_account_reconciled"]:
            raise SystemExit("Automation falsely reconciled the official account")
        authority = document["authority"]
        if authority["automation_may_decide_liability"] or authority["automation_may_find_constitutional_violation"] or authority["automation_may_publish"]:
            raise SystemExit("Federal force-event automation exceeded authority")
        if document["review_routing"]["minimum_quorum"] < 2:
            raise SystemExit("Critical civil-rights review requires quorum >= 2")
    print(f"Validated {len(paths)} Ruben Ray Martinez federal force-event packets.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
