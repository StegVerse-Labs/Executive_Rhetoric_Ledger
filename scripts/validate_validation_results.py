#!/usr/bin/env python3
"""Validate Executive Rhetoric Ledger validation-result receipts.

Default target:
  validation_results/*.json

Optional usage:
  python scripts/validate_validation_results.py path/to/result.json
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
SCHEMA_PATH = ROOT / "schemas" / "validation-result.schema.json"
DEFAULT_RECEIPT_DIR = ROOT / "validation_results"


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}") from exc


def default_receipt_files() -> list[Path]:
    if not DEFAULT_RECEIPT_DIR.exists():
        return []
    return sorted(DEFAULT_RECEIPT_DIR.glob("*.json"))


def receipt_files_from_args(args: Iterable[str]) -> list[Path]:
    paths = [Path(arg).resolve() for arg in args]
    if paths:
        return paths
    return default_receipt_files()


def main(argv: list[str]) -> int:
    schema = load_json(SCHEMA_PATH)
    receipt_files = receipt_files_from_args(argv)

    if not receipt_files:
        print("No validation-result JSON receipts found.")
        return 1

    failures: list[str] = []

    for path in receipt_files:
        try:
            data = load_json(path)
            jsonschema.validate(instance=data, schema=schema)
            print(f"PASS {path}")
        except Exception as exc:  # noqa: BLE001 - CLI should report all failures
            failures.append(f"FAIL {path}: {exc}")

    if failures:
        print("\n".join(failures), file=sys.stderr)
        return 1

    print(f"Validated {len(receipt_files)} validation-result receipt(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
