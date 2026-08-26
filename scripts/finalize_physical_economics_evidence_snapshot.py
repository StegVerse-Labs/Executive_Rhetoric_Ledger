#!/usr/bin/env python3
"""Finalize and verify immutable Physical Economics evidence-snapshot hashes."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "physical-economics-evidence-snapshot.schema.json"
PREFIX = "sha256:"


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def snapshot_digest(snapshot: dict[str, Any]) -> str:
    hashable = copy.deepcopy(snapshot)
    hashable["snapshot_hash"] = ""
    digest = hashlib.sha256(canonical_json(hashable).encode("utf-8")).hexdigest()
    return PREFIX + digest


def finalize(snapshot: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(snapshot)
    result["snapshot_hash"] = snapshot_digest(result)
    return result


def verify(snapshot: dict[str, Any]) -> tuple[bool, str]:
    declared = snapshot.get("snapshot_hash", "")
    expected = snapshot_digest(snapshot)
    return declared == expected, expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("snapshot", type=Path)
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    snapshot = load(args.snapshot)
    schema = load(SCHEMA_PATH)
    schema_errors = list(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(snapshot))
    if schema_errors:
        for error in schema_errors:
            print(f"FAIL snapshot schema: {error.message}", file=sys.stderr)
        return 1

    if args.verify:
        valid, expected = verify(snapshot)
        if not valid:
            print(
                f"FAIL snapshot hash mismatch: declared={snapshot.get('snapshot_hash')} expected={expected}",
                file=sys.stderr,
            )
            return 1
        print(f"PASS {expected}")
        return 0

    finalized = finalize(snapshot)
    encoded = json.dumps(finalized, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded, encoding="utf-8")
    else:
        print(encoded, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
