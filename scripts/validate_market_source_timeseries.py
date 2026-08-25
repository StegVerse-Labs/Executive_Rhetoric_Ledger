#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker


def _utc(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("timestamp must be timezone-aware")
    return parsed


def validate(payload: dict, schema: dict) -> list[str]:
    errors = [error.message for error in Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(payload)]
    if errors:
        return sorted(errors)
    metrics = set(payload["metrics"])
    previous = None
    for index, observation in enumerate(payload["observations"]):
        current = _utc(observation["as_of_utc"])
        if previous is not None and current <= previous:
            errors.append(f"observations[{index}] timestamp must be strictly increasing")
        previous = current
        unknown = set(observation["values"]) - metrics
        if unknown:
            errors.append(f"observations[{index}] contains undeclared metrics: {sorted(unknown)}")
        missing = metrics - set(observation["values"])
        if missing:
            errors.append(f"observations[{index}] omits declared metrics: {sorted(missing)}")
    if payload.get("execution_authority") != "NONE" or payload.get("may_authorize_order") is not False:
        errors.append("market source timeseries must be research-only")
    return sorted(errors)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("document")
    parser.add_argument("--schema", default="schemas/market-source-timeseries.schema.json")
    args = parser.parse_args()
    payload = json.loads(Path(args.document).read_text())
    schema = json.loads(Path(args.schema).read_text())
    errors = validate(payload, schema)
    print(json.dumps({"status": "PASS" if not errors else "FAIL", "errors": errors, "execution_authority": "NONE"}, sort_keys=True))
    return 0 if not errors else 2


if __name__ == "__main__":
    raise SystemExit(main())
