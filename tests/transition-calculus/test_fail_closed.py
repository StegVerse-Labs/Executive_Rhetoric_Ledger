#!/usr/bin/env python3
"""Negative tests proving transition-calculus governance fails closed."""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIXTURES = ROOT / "tests" / "transition-calculus"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_json(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def require_error(errors: list[str], needle: str, case: str) -> None:
    if not any(needle in error for error in errors):
        raise AssertionError(f"{case}: expected error containing {needle!r}; got {errors!r}")
    print(f"PASS negative {case}")


def main() -> int:
    transition = load_module("transition_validator", ROOT / "scripts" / "validate_transition_calculus.py")
    forecast = load_module("forecast_validator", ROOT / "scripts" / "validate_forecast_calibration.py")

    base_transition = load_json("opaque-resolution.transition.json")

    # Canonical continuity may never be silently downgraded from ESTABLISHED.
    case = copy.deepcopy(base_transition)
    case["continuity"]["posture"] = "UNRESOLVED"
    require_error(transition.governance_errors(case), "requires ESTABLISHED continuity", "canonical-continuity-gate")

    # Every continuity claim must preserve an evidence receipt.
    case = copy.deepcopy(base_transition)
    case["continuity"]["evidence_ids"] = []
    require_error(transition.governance_errors(case), "canonical continuity requires evidence", "continuity-evidence-gate")

    # Resolution cannot erase its historical opaque slot event.
    case = copy.deepcopy(base_transition)
    resolved = next(item for item in case["opaque_elements"] if item["resolution_state"] == "RESOLVED")
    case["resolution_history"] = [
        item for item in case["resolution_history"]
        if not (item["event_type"] == "RESOLVE_OPAQUE" and item.get("opaque_id") == resolved["opaque_id"])
    ]
    require_error(transition.governance_errors(case), "lacks preserved RESOLVE_OPAQUE history", "opacity-history-preservation")

    # Known dependency may not masquerade as independent confirmation.
    case = copy.deepcopy(base_transition)
    if not case["provenance_relations"]:
        raise AssertionError("fixture must contain a provenance relation for negative testing")
    case["provenance_relations"][0]["posture"] = "known_dependency"
    case["provenance_relations"][0]["independent_confirmation_weight"] = 1.0
    require_error(transition.governance_errors(case), "must have weight 0", "dependency-double-counting")

    # Unknown provenance receives bounded, not full, independence weight.
    case = copy.deepcopy(base_transition)
    case["provenance_relations"][0]["posture"] = "unknown_provenance"
    case["provenance_relations"][0]["independent_confirmation_weight"] = 1.0
    require_error(transition.governance_errors(case), "unknown provenance weight exceeds 0.5", "unknown-provenance-boundedness")

    base_forecast = load_json("conditional-delay.forecast.json")
    case = copy.deepcopy(base_forecast)
    f = case["forecasts"][0]
    # A delay classification requires an originally stated contingency that actually occurred.
    for contingency in f["contingencies"]:
        if contingency["effect"] == "delay":
            contingency["status"] = "not_occurred"
    f["state"] = "DELAYED_BY_STATED_CONTINGENCY"
    f["state_history"][-1]["state"] = "DELAYED_BY_STATED_CONTINGENCY"
    require_error(forecast.governance_errors(case), "requires an occurred delay contingency", "forecast-delay-contingency")

    # A resolved forecast must bind to observed world-state evidence.
    case = copy.deepcopy(base_forecast)
    f = case["forecasts"][0]
    f["state"] = "RESOLVED_CORRECT"
    f["state_history"][-1]["state"] = "RESOLVED_CORRECT"
    f["world_event_links"] = []
    require_error(forecast.governance_errors(case), "resolved forecast requires linked world-state evidence", "forecast-world-evidence")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
