#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas/erl-kv-artifact.schema.json"
FIXTURE = ROOT / "fixtures/erl-kv/sample-manifest.json"


def main() -> None:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    errors = sorted(
        Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(fixture),
        key=lambda error: list(error.path),
    )
    if errors:
        raise SystemExit("\n".join(error.message for error in errors))
    subprocess.run(
        [sys.executable, str(ROOT / "scripts/test_erl_kv_writer.py")],
        cwd=ROOT,
        check=True,
    )
    print("ERL KnowledgeVault storage contract validation passed.")


if __name__ == "__main__":
    main()
