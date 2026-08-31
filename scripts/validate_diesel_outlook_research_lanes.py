#!/usr/bin/env python3
"""Validate governed ERL three-to-six-week diesel outlook research lanes."""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "diesel-outlook-research-lanes.schema.json"
RECORDS = ROOT / "assessments" / "forecast-calibration"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def close(actual: float, expected: float, tolerance: float = 0.001) -> bool:
    return math.isclose(actual, expected, abs_tol=tolerance)


def governance_errors(data: dict) -> list[str]:
    errors: list[str] = []
    lane_ids = [lane["lane_id"] for lane in data["research_lanes"]]
    duplicates = sorted({lane_id for lane_id in lane_ids if lane_ids.count(lane_id) > 1})
    if duplicates:
        errors.append(f"duplicate research lane ids: {', '.join(duplicates)}")

    states = {lane["state"] for lane in data["research_lanes"]}
    if not ({"EXISTING", "EXISTING_EXPANDED"} & states):
        errors.append("registry must bind at least one existing research lane")
    if "ADDED" not in states:
        errors.append("registry must identify at least one added research lane")

    source_record = ROOT / data["existing_lane_validation"]["source_record"]
    if not source_record.is_file():
        errors.append(f"existing lane source record does not exist: {source_record.relative_to(ROOT)}")

    handoff = ROOT / data["owner"]["handoff"]
    if not handoff.is_file():
        errors.append(f"owner handoff does not exist: {handoff.relative_to(ROOT)}")

    observations = data["latest_baseline"]["observations"]
    derived = data["latest_baseline"]["derived"]
    expected_net_exports = observations["distillate_exports_kbd"] - observations["distillate_imports_kbd"]
    if not close(derived["net_exports_kbd"], expected_net_exports):
        errors.append(
            "net_exports_kbd must equal distillate_exports_kbd minus distillate_imports_kbd"
        )

    materiality = data["materiality_evaluation"]
    is_material = materiality["current_state"] != "NO_MATERIAL_CHANGE"
    if materiality["alert_authorized"] != is_material:
        errors.append("alert_authorized must match whether current_state is material")
    if is_material and not materiality["assumptions_for_recalibration"]:
        errors.append("material change requires assumptions_for_recalibration")
    if not materiality["countervailing_signals"]:
        errors.append("materiality evaluation must preserve countervailing signals")

    baseline = data["latest_baseline"]
    if not baseline["observed_summary"] or not baseline["inference_summary"]:
        errors.append("baseline must separate observed summaries from inference summaries")
    if data["governance"]["finding_authorized"] or data["governance"]["publication_authorized"]:
        errors.append("this research-lane registry cannot authorize findings or publication")

    required_series = {
        "refinery_utilization_pct",
        "distillate_net_production_kbd",
        "distillate_imports_kbd",
        "distillate_exports_kbd",
    }
    aligned = set(data["existing_lane_validation"]["aligned_series"])
    missing = sorted(required_series - aligned)
    if missing:
        errors.append(f"existing lane validation missing required aligned series: {', '.join(missing)}")

    return errors


def record_files() -> list[Path]:
    if not RECORDS.exists():
        return []
    return sorted(RECORDS.rglob("diesel-outlook-*.json"))


def main() -> int:
    schema = load(SCHEMA)
    files = record_files()
    if not files:
        print("No diesel outlook research-lane records found.", file=sys.stderr)
        return 1

    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    failures = 0
    for path in files:
        data = load(path)
        schema_errors = sorted(validator.iter_errors(data), key=lambda exc: list(exc.path))
        if schema_errors:
            failures += 1
            for exc in schema_errors:
                location = ".".join(str(part) for part in exc.path) or "<root>"
                print(f"FAIL {path}: schema {location}: {exc.message}")
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
