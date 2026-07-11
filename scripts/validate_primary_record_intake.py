#!/usr/bin/env python3
"""Validate machine-readable primary-record intake queues."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "primary-record-intake.schema.json"
INTAKE_DIR = ROOT / "assessments" / "intake"


def load_json(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Unable to load {path.relative_to(ROOT)}: {exc}") from exc


def main() -> int:
    schema = load_json(SCHEMA_PATH)
    validator = Draft202012Validator(schema)
    files = sorted(INTAKE_DIR.glob("*.json"))
    if not files:
        print("FAIL: no machine-readable intake queues found", file=sys.stderr)
        return 1

    failures: list[str] = []
    for path in files:
        try:
            document = load_json(path)
        except ValueError as exc:
            failures.append(str(exc))
            continue

        errors = sorted(validator.iter_errors(document), key=lambda error: list(error.path))
        for error in errors:
            location = ".".join(str(part) for part in error.path) or "<root>"
            failures.append(f"{path.relative_to(ROOT)}:{location}: {error.message}")

        if not isinstance(document, dict):
            continue

        items = document.get("items", [])
        ids = [item.get("intake_id") for item in items if isinstance(item, dict)]
        duplicates = sorted({item_id for item_id in ids if ids.count(item_id) > 1})
        for duplicate in duplicates:
            failures.append(f"{path.relative_to(ROOT)}: duplicate intake_id {duplicate}")

        queue_status = document.get("queue_status")
        unresolved_states = {
            "requested",
            "located",
            "received-unverified",
            "conflicting-records",
            "restricted-or-sealed",
            "unavailable",
        }
        unresolved = [
            item for item in items
            if isinstance(item, dict) and item.get("state") in unresolved_states
        ]
        if queue_status == "complete" and unresolved:
            failures.append(
                f"{path.relative_to(ROOT)}: queue_status complete is invalid while {len(unresolved)} item(s) remain unresolved"
            )

        for item in items:
            if not isinstance(item, dict):
                continue
            state = item.get("state")
            receipts = item.get("source_receipt_ids", [])
            if state in {"verified-primary", "verified-secondary"} and not receipts:
                failures.append(
                    f"{path.relative_to(ROOT)}:{item.get('intake_id')}: verified state requires at least one source_receipt_id"
                )

        print(f"CHECKED {path.relative_to(ROOT)}")

    if failures:
        print("Primary-record intake validation failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    print(f"Validated {len(files)} primary-record intake queue(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
