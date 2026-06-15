#!/usr/bin/env python3
"""Validate Executive Rhetoric Ledger producer export objects.

This script validates:
1. producer export JSON files against schemas/producer-export.schema.json
2. embedded source receipts against schemas/source-posture.schema.json

Default target:
  producer_exports/example/*.json

Optional usage:
  python scripts/validate_producer_exports.py path/to/export.json another/export.json
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Iterable

try:
    import jsonschema
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "Missing dependency: jsonschema. Install with `python -m pip install jsonschema`."
    ) from exc

ROOT = Path(__file__).resolve().parents[1]
PRODUCER_SCHEMA_PATH = ROOT / "schemas" / "producer-export.schema.json"
SOURCE_SCHEMA_PATH = ROOT / "schemas" / "source-posture.schema.json"
DEFAULT_EXPORT_GLOB = ROOT / "producer_exports" / "example"


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}") from exc


def default_export_files() -> list[Path]:
    if not DEFAULT_EXPORT_GLOB.exists():
        return []
    return sorted(DEFAULT_EXPORT_GLOB.glob("*.json"))


def export_files_from_args(args: Iterable[str]) -> list[Path]:
    paths = [Path(arg).resolve() for arg in args]
    if paths:
        return paths
    return default_export_files()


def validate_export(path: Path, producer_schema: dict, source_schema: dict) -> None:
    data = load_json(path)

    jsonschema.validate(instance=data, schema=producer_schema)

    receipts = data.get("source_receipts", [])
    if not receipts:
        raise jsonschema.ValidationError(f"{path}: source_receipts must not be empty")

    for index, receipt in enumerate(receipts):
        try:
            jsonschema.validate(instance=receipt, schema=source_schema)
        except jsonschema.ValidationError as exc:
            raise jsonschema.ValidationError(
                f"{path}: source_receipts[{index}] failed source-posture validation: {exc.message}"
            ) from exc


def main(argv: list[str]) -> int:
    producer_schema = load_json(PRODUCER_SCHEMA_PATH)
    source_schema = load_json(SOURCE_SCHEMA_PATH)
    export_files = export_files_from_args(argv)

    if not export_files:
        print("No producer export JSON files found.")
        return 1

    failures: list[str] = []

    for path in export_files:
        try:
            validate_export(path, producer_schema, source_schema)
            print(f"PASS {path}")
        except Exception as exc:  # noqa: BLE001 - CLI should report all validation failures
            failures.append(f"FAIL {path}: {exc}")

    if failures:
        print("\n".join(failures), file=sys.stderr)
        return 1

    print(f"Validated {len(export_files)} producer export file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
