#!/usr/bin/env python3
import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas/household-economic-conditions-output.schema.json"
FIXTURE = ROOT / "fixtures/household-economic-conditions/fail-closed.fixture.json"
INVENTORY = ROOT / "research-data/household-economic-conditions/official-series-inventory.v1.json"
GOAL = "ERL-HOUSEHOLD-ECONOMIC-CONDITIONS-SITE-001"

schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))

errors = sorted(
    Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(fixture),
    key=lambda error: list(error.path),
)
if errors:
    raise SystemExit("\n".join(f"{list(e.path)}: {e.message}" for e in errors))

assert fixture["goal_task_id"] == GOAL
assert fixture["evidence_state"] == "FIXTURE_ONLY"
assert fixture["public_activation_authorized"] is False
assert fixture["interpretation"]["what_changed"] == []
assert fixture["interpretation"]["what_it_may_mean"] == []
assert all(series["source_agency"] == "FIXTURE_ONLY" for series in fixture["series"])
assert all(series["comparison_mode"] == "NORMALIZED_INDEX_ONLY" for series in fixture["series"])

required_components = {
    "gross_labor_income", "net_disposable_resources", "required_cost_burden",
    "debt_service", "necessary_consumption", "discretionary_residual",
    "saving_dissaving", "new_borrowing", "delinquency_arrears",
    "unmet_foregone_consumption",
}
assert set(fixture["household_state"]) == required_components

assert inventory["goal_task_id"] == GOAL
rules = inventory["rules"]
assert rules["same_axis_requires_same_unit_and_definition"] is True
assert rules["cross_metric_comparison_requires_normalized_index"] is True
assert rules["methodology_breaks_must_be_visible"] is True
assert rules["incompatible_series_must_not_be_spliced"] is True
assert rules["historical_proxy_must_be_labeled"] == "DERIVED_HISTORICAL_PROXY"
assert rules["missing_history_remains_missing_without_governed_reconstruction"] is True

ids = {item["series_id"] for item in inventory["series"]}
for expected in {
    "BLS_CES_PE_REAL_HOURLY_EARNINGS", "BLS_CES_PE_REAL_WEEKLY_EARNINGS",
    "BLS_CPI_U_ALL_ITEMS", "BEA_DPI_CURRENT_DOLLARS", "BEA_REAL_DPI",
    "BEA_PCE_TOTAL", "BEA_PERSONAL_SAVING_RATE", "FRB_DSR_CURRENT_TOTAL",
    "FRB_DSR_CURRENT_MORTGAGE", "FRB_DSR_CURRENT_CONSUMER",
    "NYFED_CCP_DEBT_BALANCE_BY_CLASS", "NYFED_CCP_DELINQUENCY_BY_CLASS",
    "CENSUS_ACS_HOUSING_COST_BURDEN",
}:
    assert expected in ids, expected

frb = next(item for item in inventory["series"] if item["series_id"] == "FRB_DSR_CURRENT_TOTAL")
assert frb["earliest_comparable_date"] == "2005-01-01"
assert any(
    isinstance(br, dict) and br.get("type") == "METHODOLOGY_REPLACEMENT"
    for br in frb["structural_breaks"]
)
acs = next(item for item in inventory["series"] if item["series_id"] == "CENSUS_ACS_HOUSING_COST_BURDEN")
assert any(
    isinstance(br, dict) and br.get("type") == "NONCOMPARABLE_EXPERIMENTAL_RELEASE" and br.get("date") == "2020-01-01"
    for br in acs["structural_breaks"]
)

print("HOUSEHOLD_ECONOMIC_CONDITIONS_CONTRACT=PASS")
print("HOUSEHOLD_ECONOMIC_CONDITIONS_FIXTURE_FAIL_CLOSED=PASS")
print("HOUSEHOLD_ECONOMIC_CONDITIONS_PUBLIC_ACTIVATION=false")
