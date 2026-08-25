#!/usr/bin/env python3
"""Validate ERL forecast-calibration records and conditional state logic."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "forecast-calibration.schema.json"
FIXTURES = ROOT / "tests" / "transition-calculus"
CALIBRATIONS = ROOT / "assessments" / "forecast-calibration"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def governance_errors(data: dict) -> list[str]:
    errors: list[str] = []
    source_ids = {s["source_id"] for s in data["source_receipts"]}
    for forecast in data["forecasts"]:
        fid = forecast["forecast_id"]
        refs = set(forecast["source_ids"])
        for contingency in forecast["contingencies"]:
            refs.update(contingency["source_ids"])
        for state_event in forecast["state_history"]:
            refs.update(state_event["source_ids"])
        missing = sorted(refs - source_ids)
        if missing:
            errors.append(f"{fid}: missing source receipts: {', '.join(missing)}")

        if forecast["state_history"][-1]["state"] != forecast["state"]:
            errors.append(f"{fid}: current state must equal final state_history entry")

        occurred_effects = {c["effect"] for c in forecast["contingencies"] if c["status"] == "occurred"}
        if forecast["state"] == "DELAYED_BY_STATED_CONTINGENCY" and "delay" not in occurred_effects:
            errors.append(f"{fid}: delayed state requires an occurred delay contingency")
        if forecast["state"] == "ACCELERATED_BY_STATED_CONTINGENCY" and "accelerate" not in occurred_effects:
            errors.append(f"{fid}: accelerated state requires an occurred acceleration contingency")
        if forecast["state"] == "INVALIDATED" and "invalidate" not in occurred_effects:
            # Invalidity can also arise from contrary outcome evidence, but it must be stated explicitly.
            if "invalidat" not in forecast["state_history"][-1]["reason"].lower() and "contrary" not in forecast["state_history"][-1]["reason"].lower():
                errors.append(f"{fid}: invalidated state requires an occurred invalidating contingency or explicit contrary-evidence reason")

        if forecast["state"] in {"RESOLVED_CORRECT", "RESOLVED_INCORRECT"} and not forecast["world_event_links"]:
            errors.append(f"{fid}: resolved forecast requires linked world-state evidence")

    return errors


def calibration_files() -> list[Path]:
    files = list(FIXTURES.glob("*.forecast.json"))
    if CALIBRATIONS.exists():
        files.extend(CALIBRATIONS.rglob("*.forecast.json"))
    return sorted(set(files))


def main() -> int:
    schema = load(SCHEMA)
    files = calibration_files()
    if not files:
        print("No forecast calibration fixtures or live records found.", file=sys.stderr)
        return 1
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    failures = 0
    for path in files:
        data = load(path)
        schema_errors = list(validator.iter_errors(data))
        if schema_errors:
            failures += 1
            for exc in schema_errors:
                print(f"FAIL {path}: schema: {exc.message}")
            continue
        errors = governance_errors(data)
        if errors:
            failures += 1
            for error in errors:
                print(f"FAIL {path}: governance: {error}")
        else:
            print(f"PASS {path}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
