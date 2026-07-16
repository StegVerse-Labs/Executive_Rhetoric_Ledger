#!/usr/bin/env python3
"""Validate standalone Source Posture receipts."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "source-posture.schema.json"
RECEIPT_DIRS = [
    ROOT / "assessments" / "evidence" / "receipts",
]


def load_json(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Unable to load {path.relative_to(ROOT)}: {exc}") from exc


def main() -> int:
    schema = load_json(SCHEMA_PATH)
    validator = Draft202012Validator(schema)
    files = sorted(
        path
        for directory in RECEIPT_DIRS
        if directory.exists()
        for path in directory.glob("*.json")
    )

    if not files:
        print("FAIL: no standalone source receipts found", file=sys.stderr)
        return 1

    failures: list[str] = []
    source_ids: list[str] = []

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

        if isinstance(document, dict):
            source_id = str(document.get("source_id", "")).strip()
            if source_id:
                source_ids.append(source_id)
            expected_name = f"{source_id}.json" if source_id else ""
            if expected_name and path.name != expected_name:
                failures.append(
                    f"{path.relative_to(ROOT)}: filename must match source_id ({expected_name})"
                )

        print(f"CHECKED {path.relative_to(ROOT)}")

    duplicates = sorted({source_id for source_id in source_ids if source_ids.count(source_id) > 1})
    for duplicate in duplicates:
        failures.append(f"duplicate standalone source_id {duplicate}")

    if failures:
        print("Standalone source receipt validation failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    print(f"Validated {len(files)} standalone source receipt(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
