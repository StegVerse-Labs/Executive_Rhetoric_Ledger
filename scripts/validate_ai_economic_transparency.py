#!/usr/bin/env python3
import json
import sys
from pathlib import Path

REQUIRED = {
    "schema","task_id","provider","protocol_complete",
    "actual_request_cost_directly_exposed","request_usage_directly_exposed",
    "research_steps_required","provider_surfaces_consulted",
    "account_or_privilege_required","support_required","external_research_required",
    "reconstructable_actual_cost","unresolved_cost_components",
    "disclosure_burden_rating","scale_sensitivity_state","activation_authorized"
}

def validate(obj):
    errors = []
    missing = sorted(REQUIRED - set(obj))
    if missing:
        errors.append("missing:" + ",".join(missing))
        return errors

    if obj["schema"] != "stegverse.erl.ai-economic-transparency-observation/v1":
        errors.append("schema")
    if obj["task_id"] != "ERL-AI-ECON-TRANSPARENCY-001":
        errors.append("task_id")
    if obj["activation_authorized"] is not False:
        errors.append("activation_authorized_must_be_false")
    if not isinstance(obj["research_steps_required"], int) or obj["research_steps_required"] < 0:
        errors.append("research_steps_required")
    rating = obj["disclosure_burden_rating"]
    if rating is not None and (not isinstance(rating, int) or rating < 0 or rating > 5):
        errors.append("disclosure_burden_rating")
    if rating == 5 and obj["protocol_complete"] is not True:
        errors.append("rating_5_requires_protocol_complete")
    if rating is not None and obj["protocol_complete"] is not True and rating != 0:
        errors.append("final_rating_requires_protocol_complete")
    if obj["actual_request_cost_directly_exposed"] is True and rating not in (None, 0):
        errors.append("direct_cost_conflicts_with_rating")
    if obj["reconstructable_actual_cost"] is False and obj.get("literal_request_cost_usd") is not None:
        errors.append("literal_cost_without_reconstructability")

    scenarios = obj.get("scale_scenarios", [])
    allowed_states = {"EXACT","BOUNDED","UNBOUNDED_UNKNOWN","NOT_APPLICABLE"}
    for i, s in enumerate(scenarios):
        if s.get("state") not in allowed_states:
            errors.append(f"scale_scenarios[{i}].state")
            continue
        state=s["state"]
        if state=="EXACT" and s.get("known_total_cost_usd") is None:
            errors.append(f"scale_scenarios[{i}].exact_missing_total")
        if state=="BOUNDED":
            lo=s.get("lower_bound_usd"); hi=s.get("upper_bound_usd")
            if lo is None or hi is None or hi < lo:
                errors.append(f"scale_scenarios[{i}].invalid_bounds")
        if state=="UNBOUNDED_UNKNOWN" and any(s.get(k) is not None for k in ("known_total_cost_usd","lower_bound_usd","upper_bound_usd")):
            errors.append(f"scale_scenarios[{i}].unknown_has_numeric_claim")
    return errors

def main():
    if len(sys.argv) != 2:
        print("usage: validate_ai_economic_transparency.py <json>", file=sys.stderr)
        return 2
    obj=json.loads(Path(sys.argv[1]).read_text())
    errors=validate(obj)
    if errors:
        print(json.dumps({"valid":False,"errors":errors}, separators=(",",":")))
        return 1
    print('{"valid":true,"errors":[]}')
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
