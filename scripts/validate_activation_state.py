#!/usr/bin/env python3
"""Validate the Executive Rhetoric Ledger activation-state manifest.

Default target:
  release/activation-state.json

Optional usage:
  python scripts/validate_activation_state.py path/to/activation-state.json
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    import jsonschema
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "Missing dependency: jsonschema. Install with `python -m pip install jsonschema`."
    ) from exc

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "activation-state.schema.json"
DEFAULT_STATE_PATH = ROOT / "release" / "activation-state.json"


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}") from exc


def state_path_from_args(args: list[str]) -> Path:
    if args:
        return Path(args[0]).resolve()
    return DEFAULT_STATE_PATH


def main(argv: list[str]) -> int:
    schema = load_json(SCHEMA_PATH)
    state_path = state_path_from_args(argv)

    if not state_path.exists():
        print(f"Activation-state manifest not found: {state_path}", file=sys.stderr)
        return 1

    try:
        data = load_json(state_path)
        jsonschema.validate(instance=data, schema=schema)
        print(f"PASS {state_path}")
    except Exception as exc:  # noqa: BLE001 - CLI should report schema failure
        print(f"FAIL {state_path}: {exc}", file=sys.stderr)
        return 1

    print("Validated activation-state manifest.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
