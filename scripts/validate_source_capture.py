#!/usr/bin/env python3
"""Validate source adapters, archive receipts, and generated review candidates."""

from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate(instance, schema_path: Path, label: str) -> None:
    validator = Draft202012Validator(load(schema_path), format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(instance), key=lambda error: list(error.path))
    if errors:
        for error in errors:
            path = ".".join(str(item) for item in error.path) or "<root>"
            print(f"{label} {path}: {error.message}")
        raise SystemExit(1)


def main() -> None:
    config = load(ROOT / "config/source-adapters.json")
    adapter_schema = ROOT / "schemas/source-adapter.schema.json"
    for adapter in config["adapters"]:
        validate(adapter, adapter_schema, adapter["adapter_id"])

    with tempfile.TemporaryDirectory() as temporary:
        sandbox = Path(temporary)
        command = ["python", str(ROOT / "scripts/run_source_capture.py"), "--captured-at", "2026-07-20T12:00:00Z"]
        subprocess.run(command, cwd=ROOT, check=True)

    receipt_schema = ROOT / "schemas/archive-capture.schema.json"
    receipts = sorted((ROOT / "archive/receipts/2026-07-20").glob("CAP-*.json"))
    if not receipts:
        raise SystemExit("Source capture generated no receipts.")
    for receipt_path in receipts:
        receipt = load(receipt_path)
        validate(receipt, receipt_schema, receipt_path.name)
        raw_path = ROOT / receipt["raw_archive_path"]
        candidate_path = ROOT / receipt["candidate_path"]
        if not raw_path.is_file() or not candidate_path.is_file():
            raise SystemExit(f"Missing retained output for {receipt_path}")
        candidate = load(candidate_path)
        if candidate["candidate_status"] != "candidate-review-required":
            raise SystemExit("Automation exceeded candidate-only authority.")
        if candidate["automation_authority"]["promoted"] is not False:
            raise SystemExit("Automation must not promote candidates.")
    print(f"Validated {len(receipts)} archive capture receipt(s) and retained candidate boundary.")


if __name__ == "__main__":
    main()
