#!/usr/bin/env python3
"""Validate recurring-search configurations and generated discovery-cycle manifests."""

from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    from jsonschema import Draft202012Validator
except ImportError as exc:  # pragma: no cover
    raise SystemExit("Missing dependency: jsonschema") from exc

ROOT = Path(__file__).resolve().parents[1]
CONFIG_SCHEMA = ROOT / "schemas" / "recurring-search-config.schema.json"
CYCLE_SCHEMA = ROOT / "schemas" / "discovery-cycle.schema.json"
CONFIG_DIR = ROOT / "config"
CYCLE_DIR = ROOT / "discovery_cycles" / "generated"


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in {path}: {exc}") from exc


def validate_file(path: Path, schema: dict) -> list[str]:
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(load_json(path)), key=lambda error: list(error.path))
    return [
        f"{path}: {'.'.join(str(part) for part in error.path) or '<root>'}: {error.message}"
        for error in errors
    ]


def main() -> int:
    config_schema = load_json(CONFIG_SCHEMA)
    cycle_schema = load_json(CYCLE_SCHEMA)
    config_files = sorted(CONFIG_DIR.glob("recurring-searches*.json"))
    cycle_files = sorted(CYCLE_DIR.glob("*.json"))

    if not config_files:
        print("No recurring-search configuration files found.", file=sys.stderr)
        return 1
    if not cycle_files:
        print("No generated discovery-cycle manifests found.", file=sys.stderr)
        return 1

    failures: list[str] = []
    for path in config_files:
        failures.extend(validate_file(path, config_schema))
    for path in cycle_files:
        failures.extend(validate_file(path, cycle_schema))

    if failures:
        print("\n".join(failures), file=sys.stderr)
        return 1

    print(f"Validated {len(config_files)} recurring-search configuration file(s).")
    print(f"Validated {len(cycle_files)} discovery-cycle manifest file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
