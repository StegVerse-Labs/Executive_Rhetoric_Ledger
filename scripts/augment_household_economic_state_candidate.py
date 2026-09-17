#!/usr/bin/env python3
"""Admit only exact-bound distribution/required-cost context into a partial household-state candidate."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

GOAL = "ERL-HOUSEHOLD-ECONOMIC-CONDITIONS-SITE-001"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def evidence_ref(body: dict) -> str:
    return f"sha256:{body['raw_sha256']}"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--state", type=Path, required=True)
    ap.add_argument("--candidate-root", type=Path, required=True)
    ap.add_argument("--nyfed-distribution", type=Path, required=True)
    args = ap.parse_args()

    state = load(args.state)
    if state.get("goal_task_id") != GOAL or state.get("public_activation_authorized") is not False:
        raise SystemExit("household state authority boundary invalid")

    census_path = next(args.candidate_root.rglob("census_acs_housing_cost_burden.candidate.json"), None)
    if census_path is None:
        raise SystemExit("Census housing-cost candidate missing")
    census = load(census_path)
    if census.get("finding_authority") is not False or census.get("public_activation_authorized") is not False:
        raise SystemExit("Census candidate gained authority")

    distribution = load(args.nyfed_distribution)
    if distribution.get("goal_task_id") != GOAL or distribution.get("finding_authority") is not False or distribution.get("public_activation_authorized") is not False:
        raise SystemExit("NY Fed distribution context gained authority")
    boundaries = distribution["semantic_boundaries"]
    if boundaries.get("debt_stock_is_new_borrowing") is not False or boundaries.get("aggregate_or_age_delinquency_is_complete_household_stress") is not False:
        raise SystemExit("NY Fed semantic boundary invalid")

    census_obs = census.get("observations", [])
    if not census_obs:
        raise SystemExit("Census housing-cost observations missing")
    measures = {row.get("measure"): row for row in census_obs}
    required = ["owned_with_mortgage_over_30", "owned_without_mortgage_over_30", "rented_over_30"]
    if any(name not in measures for name in required):
        raise SystemExit("Census tenure housing-burden measures incomplete")

    hs = state["household_state"]
    hs["required_cost_burden"] = {
        "state": "PARTIAL",
        "coverage": "Official ACS housing-cost burden by tenure only; not a complete required-cost composite",
        "value": None,
        "unit": "occupied housing units by tenure with housing costs over 30/50 percent of household income",
        "evidence_refs": [evidence_ref(census)],
        "notes": [
            f"ACS period: {census_obs[0]['period']}",
            "Housing cost burden is an exact required-cost component, not total household required costs.",
            "Food, medical, insurance, transportation, utilities, taxes and other mandatory costs remain unresolved unless separately evidenced."
        ],
    }

    series_by_id = {row["series_id"]: row for row in distribution["series"]}
    age_debt = series_by_id["NYFED_CCP_DEBT_BALANCE_BY_AGE"]
    age_delinq = series_by_id["NYFED_CCP_SERIOUS_DELINQUENCY_BY_AGE"]
    latest_period = max(row["period"] for row in age_delinq["observations"])
    latest_age = [row for row in age_delinq["observations"] if row["period"] == latest_period and row["category"] != "all"]
    hs["delinquency_arrears"] = {
        "state": "PARTIAL",
        "coverage": "New York Fed CCP age-distributed transition into serious delinquency (90+) only; not complete arrears or household-stress state",
        "value": None,
        "unit": "percent, four-quarter moving sum",
        "evidence_refs": [f"sha256:{distribution['raw_sha256']}"],
        "notes": [
            f"Latest age-distributed period: {latest_period}",
            "Age cohorts provide distributional evidence that the aggregate rate cannot provide.",
            "This does not establish income/wealth distribution, missed essential payments, or complete household stress."
        ] + [f"{row['category']}={row['value']:.4f}%" for row in latest_age],
    }

    hs["new_borrowing"] = {
        "state": "UNKNOWN",
        "coverage": "Debt-stock balances by class and age are admitted only as debt-stock/distribution context; they are not new borrowing",
        "value": None,
        "unit": None,
        "evidence_refs": [f"sha256:{distribution['raw_sha256']}"],
        "notes": ["Mortgage/auto originations may later support bounded flow context, but no complete governed new-borrowing measure is admitted here."]
    }

    state["series"].extend([age_debt, age_delinq])
    state["interpretation"]["prohibited_inferences"].extend([
        "Do not infer new borrowing from New York Fed debt-stock balances by age.",
        "Do not infer complete household stress from serious-delinquency transition rates by age.",
        "Do not infer total required-cost burden from ACS housing-cost burden by tenure."
    ])
    state["public_activation_authorized"] = False
    args.state.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("HOUSEHOLD_REQUIRED_COST_BURDEN=PARTIAL_HOUSING_ONLY")
    print("HOUSEHOLD_DELINQUENCY_ARREARS=PARTIAL_AGE_DISTRIBUTIONAL_CONTEXT")
    print("HOUSEHOLD_NEW_BORROWING=UNKNOWN")
    print("PUBLIC_ACTIVATION_AUTHORIZED=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
