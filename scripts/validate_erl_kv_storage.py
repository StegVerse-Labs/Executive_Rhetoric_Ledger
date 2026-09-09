#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
VALID_FIXTURES = [
    (ROOT / "schemas/erl-kv-artifact.schema.json", ROOT / "fixtures/erl-kv/sample-manifest.json"),
    (ROOT / "schemas/erl-kv-write-receipt.schema.json", ROOT / "fixtures/erl-kv/sample-write-receipt.json"),
    (ROOT / "schemas/erl-kv-provider-write-observation.schema.json", ROOT / "fixtures/erl-kv/sample-provider-write-observation.json"),
]
INVALID_FIXTURES = [
    (ROOT / "schemas/erl-kv-provider-write-observation.schema.json", ROOT / "fixtures/erl-kv/invalid-provider-observation-overclaims.json"),
]


def main() -> None:
    for schema_path, fixture_path in VALID_FIXTURES:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
        errors = sorted(
            Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(fixture),
            key=lambda error: list(error.path),
        )
        if errors:
            raise SystemExit(f"{fixture_path.name}: " + "\n".join(error.message for error in errors))

    for schema_path, fixture_path in INVALID_FIXTURES:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
        errors = list(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(fixture))
        if not errors:
            raise SystemExit(f"{fixture_path.name}: invalid fixture unexpectedly passed")
    subprocess.run(
        [sys.executable, str(ROOT / "scripts/test_erl_kv_writer.py")],
        cwd=ROOT,
        check=True,
    )
    print("ERL KnowledgeVault storage contract validation passed.")


if __name__ == "__main__":
    main()
