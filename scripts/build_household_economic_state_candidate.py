#!/usr/bin/env python3
"""Build a non-authorizing household-state candidate from bounded source candidates."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

GOAL = "ERL-HOUSEHOLD-ECONOMIC-CONDITIONS-SITE-001"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def latest(candidate: dict) -> dict | None:
    rows = candidate.get("observations", [])
    return max(rows, key=lambda row: row.get("period", "")) if rows else None


def evidence_ref(candidate: dict) -> str:
    return f"sha256:{candidate['raw_sha256']}"


def component(state: str, coverage: str, value=None, unit=None, refs=None, notes=None) -> dict:
    return {
        "state": state,
        "coverage": coverage,
        "value": value,
        "unit": unit,
        "evidence_refs": refs or [],
        "notes": notes or [],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    by_id = {}
    for path in args.candidate_root.rglob("*.candidate.json"):
        body = load(path)
        if body.get("goal_task_id") != GOAL:
            continue
        if body.get("finding_authority") is not False or body.get("public_activation_authorized") is not False:
            raise SystemExit(f"authorizing source candidate refused: {path}")
        by_id[body["inventory_series_id"]] = body

    required = [
        "BLS_CES_PE_REAL_WEEKLY_EARNINGS",
        "BLS_CES_PE_REAL_HOURLY_EARNINGS",
        "BLS_CPI_U_ALL_ITEMS",
        "FRB_DSR_CURRENT_TOTAL",
        "FRB_DSR_CURRENT_MORTGAGE",
        "FRB_DSR_CURRENT_CONSUMER",
        "CENSUS_ACS_HOUSING_COST_BURDEN",
    ]
    missing = [key for key in required if key not in by_id]
    if missing:
        raise SystemExit(f"required current source candidates missing: {missing}")

    weekly = latest(by_id["BLS_CES_PE_REAL_WEEKLY_EARNINGS"])
    hourly = latest(by_id["BLS_CES_PE_REAL_HOURLY_EARNINGS"])
    cpi = latest(by_id["BLS_CPI_U_ALL_ITEMS"])
    tdsp = latest(by_id["FRB_DSR_CURRENT_TOTAL"])
    mdsp = latest(by_id["FRB_DSR_CURRENT_MORTGAGE"])
    cdsp = latest(by_id["FRB_DSR_CURRENT_CONSUMER"])
    acs = by_id["CENSUS_ACS_HOUSING_COST_BURDEN"]
    if not all((weekly, hourly, cpi, tdsp, mdsp, cdsp)):
        raise SystemExit("one or more required normalized current observations are absent")

    acquired_times = sorted({body["acquired_at"] for body in by_id.values()})
    as_of = acquired_times[-1]

    output = {
        "schema": "stegverse.erl.household-economic-conditions-output/v1",
        "goal_task_id": GOAL,
        "generated_at": as_of,
        "evidence_state": "PARTIAL",
        "freshness": {"as_of": as_of, "max_age_seconds": 86400, "is_stale": False},
        "household_state": {
            "gross_labor_income": component(
                "PARTIAL",
                "BLS production/nonsupervisory private-payroll real earnings context only; not household gross income or take-home pay",
                weekly["value"],
                "1982-84 dollars per week",
                [evidence_ref(by_id["BLS_CES_PE_REAL_WEEKLY_EARNINGS"]), evidence_ref(by_id["BLS_CES_PE_REAL_HOURLY_EARNINGS"])],
                [f"Latest weekly observation: {weekly['period']}", f"Latest hourly observation: {hourly['period']}", "Composition and hours effects remain possible."],
            ),
            "net_disposable_resources": component("UNKNOWN", "No governed household-level net/take-home resource measure bound", notes=["BEA aggregate DPI is not household take-home pay; governed BEA credential availability remains unresolved."]),
            "required_cost_burden": component("UNKNOWN", "ACS housing-cost burden is available as one component, but no complete governed required-cost composite exists", refs=[evidence_ref(acs)], notes=["Housing burden alone must not be promoted to total required-cost burden."]),
            "debt_service": component(
                "PARTIAL",
                "Federal Reserve current-method aggregate DSR context; not household/cohort debt stress",
                tdsp["value"],
                "percent of disposable personal income",
                [evidence_ref(by_id["FRB_DSR_CURRENT_TOTAL"]), evidence_ref(by_id["FRB_DSR_CURRENT_MORTGAGE"]), evidence_ref(by_id["FRB_DSR_CURRENT_CONSUMER"])],
                [f"Latest total DSR: {tdsp['period']}", f"Mortgage={mdsp['value']}; consumer={cdsp['value']}", "Distribution and debt-class borrower exposure remain unresolved."],
            ),
            "necessary_consumption": component("UNKNOWN", "No governed necessary-consumption quantity/need-satisfaction measure bound"),
            "discretionary_residual": component("UNKNOWN", "Cannot derive without governed net resources and required costs"),
            "saving_dissaving": component("UNKNOWN", "No governed current saving/dissaving candidate admitted in this run"),
            "new_borrowing": component("UNKNOWN", "NY Fed debt-stock workbook capture is not equivalent to new borrowing and workbook normalization is not yet admitted"),
            "delinquency_arrears": component("UNKNOWN", "NY Fed serious-delinquency workbook normalization is not yet admitted"),
            "unmet_foregone_consumption": component("UNKNOWN", "No governed unmet-need/foregone-consumption measure bound"),
        },
        "series": [
            {
                "series_id": "BLS_CES_PE_REAL_WEEKLY_EARNINGS",
                "label": "Real weekly earnings, production and nonsupervisory employees",
                "source_agency": "U.S. Bureau of Labor Statistics",
                "frequency": "MONTHLY",
                "unit": "1982-84 dollars per week",
                "earliest_comparable_date": "1964-01-01",
                "vintage": by_id["BLS_CES_PE_REAL_WEEKLY_EARNINGS"]["source_vintage"],
                "revision_timestamp": by_id["BLS_CES_PE_REAL_WEEKLY_EARNINGS"]["acquired_at"],
                "comparison_mode": "ABSOLUTE",
                "same_axis_group": "BLS_REAL_WEEKLY_EARNINGS",
                "observations": by_id["BLS_CES_PE_REAL_WEEKLY_EARNINGS"]["observations"],
                "structural_breaks": [],
                "source_url": "https://api.bls.gov/publicAPI/v2/timeseries/data/",
                "methodology_url": "https://www.bls.gov/web/empsit/cesfaq.htm",
            },
            {
                "series_id": "FRB_DSR_CURRENT_TOTAL",
                "label": "Household debt service payments as a percent of disposable personal income",
                "source_agency": "Board of Governors of the Federal Reserve System",
                "frequency": "QUARTERLY",
                "unit": "percent of disposable personal income",
                "earliest_comparable_date": "2005-01-01",
                "vintage": by_id["FRB_DSR_CURRENT_TOTAL"]["source_vintage"],
                "revision_timestamp": by_id["FRB_DSR_CURRENT_TOTAL"]["acquired_at"],
                "comparison_mode": "ABSOLUTE",
                "same_axis_group": "FRB_DSR_CURRENT_METHOD",
                "observations": by_id["FRB_DSR_CURRENT_TOTAL"]["observations"],
                "structural_breaks": [{"date":"2024-09-25","type":"METHODOLOGY_REPLACEMENT","description":"Current credit-bureau methodology is a separate series from the archived prior-method DSR."}],
                "source_url": "https://fred.stlouisfed.org/series/TDSP",
                "methodology_url": "https://www.federalreserve.gov/releases/DSR/about.htm",
            },
        ],
        "interpretation": {
            "what_changed": [],
            "what_it_may_mean": [],
            "prohibited_inferences": [
                "Do not infer household welfare from gross real earnings.",
                "Do not infer household take-home resources from BLS payroll earnings.",
                "Do not infer low household stress from aggregate DSR alone.",
                "Do not infer total required-cost burden from housing burden alone.",
                "Do not infer new borrowing from debt-stock balances.",
            ],
        },
        "public_activation_authorized": False,
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("HOUSEHOLD_MULTI_SOURCE_STATE_CANDIDATE=PARTIAL_NONAUTHORIZING")
    print("PUBLIC_ACTIVATION_AUTHORIZED=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
