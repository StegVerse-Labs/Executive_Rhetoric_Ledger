#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "reclamation-kv-provider-operation-receipt.schema.json"
RECEIPT = ROOT / "evidence" / "reclamation-kv" / "2026-09-10-target-set-provider-operation.json"


def main() -> None:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
    errors = sorted(
        Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(receipt),
        key=lambda error: list(error.absolute_path),
    )
    if errors:
        raise SystemExit("; ".join(error.message for error in errors))
    if receipt["exact_provider_readback"] is not True:
        raise SystemExit("provider operation receipt must retain exact readback proof")
    if receipt["native_writer_executed"] is not False:
        raise SystemExit("provider operation must not manufacture native-writer proof")
    if receipt["provider_deletion_success"] is not False:
        raise SystemExit("KV custody must not manufacture deletion success")
    print("reclamation KV provider operation receipt: PASS")


if __name__ == "__main__":
    main()
