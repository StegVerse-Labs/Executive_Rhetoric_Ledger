#!/usr/bin/env python3
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BINDINGS = ROOT / "research-data/household-economic-conditions/official-series-bindings.v1.json"
ACQUIRE = ROOT / "scripts/acquire_household_economic_conditions.py"
GOAL = "ERL-HOUSEHOLD-ECONOMIC-CONDITIONS-SITE-001"

spec = importlib.util.spec_from_file_location("household_acquire", ACQUIRE)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)

doc = json.loads(BINDINGS.read_text(encoding="utf-8"))
assert doc["goal_task_id"] == GOAL
assert doc["public_activation_authorized"] is False
assert doc["binding_state"] == "IDENTIFIERS_BOUND_ACQUISITION_PARTIAL"
assert doc["rules"]["raw_source_bytes_retained_before_normalization"] is True
assert doc["rules"]["missing_or_failed_source_remains_unknown"] is True
assert doc["rules"]["no_cross_method_splicing"] is True

bindings = {row["inventory_series_id"]: row for row in doc["bindings"]}
assert bindings["BLS_CES_PE_REAL_HOURLY_EARNINGS"]["official_series_id"] == "CES0500000032"
assert bindings["BLS_CES_PE_REAL_WEEKLY_EARNINGS"]["official_series_id"] == "CES0500000031"
assert bindings["BLS_CPI_U_ALL_ITEMS"]["official_series_id"] == "CUUR0000SA0"
assert bindings["BEA_DPI_CURRENT_DOLLARS"]["table_name"] == "T20600"
assert bindings["BEA_DPI_CURRENT_DOLLARS"]["line_number"] == 27
assert bindings["BEA_PCE_TOTAL"]["line_number"] == 29
assert bindings["BEA_PERSONAL_SAVING_RATE"]["line_number"] == 35
assert bindings["BEA_REAL_DPI"]["line_number"] == 37
assert bindings["FRB_DSR_CURRENT_TOTAL"]["official_series_id"] == "TDSP"
assert bindings["FRB_DSR_CURRENT_MORTGAGE"]["official_series_id"] == "MDSP"
assert bindings["FRB_DSR_CURRENT_CONSUMER"]["official_series_id"] == "CDSP"
assert bindings["FRB_DSR_CURRENT_TOTAL"]["earliest_current_method"] == "2005-01-01"
assert bindings["CENSUS_ACS_HOUSING_COST_BURDEN"]["group"] == "B25140"
assert 2020 in bindings["CENSUS_ACS_HOUSING_COST_BURDEN"]["excluded_standard_comparison_years"]
assert bindings["CENSUS_ACS_HOUSING_COST_BURDEN"]["credential_required"] is False
assert bindings["CENSUS_ACS_HOUSING_COST_BURDEN"]["earliest_standard_acs1_year"] == 2005
assert bindings["CENSUS_ACS_HOUSING_COST_BURDEN"]["required_cost_scope"] == "HOUSING_COST_BURDEN_ONLY"
assert set(bindings["CENSUS_ACS_HOUSING_COST_BURDEN"]["derived_measures"]) == {"owned_with_mortgage_over_30_share_pct","owned_with_mortgage_over_50_share_pct","owned_without_mortgage_over_30_share_pct","owned_without_mortgage_over_50_share_pct","rented_over_30_share_pct","rented_over_50_share_pct"}
assert bindings["NYFED_CCP_DEBT_BALANCE_BY_CLASS"]["current_release_id"] == "2026Q2"
assert bindings["NYFED_CCP_DEBT_BALANCE_BY_CLASS"]["normalization"]["parser_state"] == "WORKBOOK_COLUMN_BINDING_PENDING"

bls_payload = {"Results":{"series":[{"seriesID":"CES0500000032","data":[{"year":"2026","period":"M08","value":"10.50"},{"year":"2026","period":"M13","value":"999"},{"year":"2026","period":"M07","value":"10.40"}]}]}}
bls = module.normalize_bls(bindings["BLS_CES_PE_REAL_HOURLY_EARNINGS"], bls_payload)
assert bls == [
    {"period":"2026-07","value":10.4,"evidence_class":"DIRECT_OBSERVATION"},
    {"period":"2026-08","value":10.5,"evidence_class":"DIRECT_OBSERVATION"},
]

fred_raw = b"DATE,TDSP\n2026-01-01,11.16414\n2026-04-01,.\n"
fred = module.normalize_fred_csv(bindings["FRB_DSR_CURRENT_TOTAL"], fred_raw)
assert fred == [{"period":"2026-01-01","value":11.16414,"evidence_class":"DIRECT_OBSERVATION"}]

bea_payload = {"BEAAPI":{"Results":{"Data":[
    {"LineNumber":"27","TimePeriod":"2026M07","DataValue":"23,858.1","UNIT_MULT":"9"},
    {"LineNumber":"29","TimePeriod":"2026M07","DataValue":"22,250.4","UNIT_MULT":"9"}
]}}}
bea = module.normalize_bea(bindings["BEA_DPI_CURRENT_DOLLARS"], bea_payload)
assert bea == [{"period":"2026M07","value":23858.1,"evidence_class":"DIRECT_OBSERVATION"}]

census_binding = bindings["CENSUS_ACS_HOUSING_COST_BURDEN"]
variables = census_binding["variables"]
header = ["NAME"] + list(variables.values()) + ["us"]
values = ["United States"] + [str(index + 100) for index in range(len(variables))] + ["1"]
census = module.normalize_census(census_binding, [header, values], 2024)
assert len(census) == len(variables) + 6
assert sum(row["evidence_class"] == "DIRECT_OBSERVATION" for row in census) == len(variables)
derived = {row["measure"]: row for row in census if row["evidence_class"] == "DERIVED_FROM_DIRECT_OBSERVATIONS"}
assert set(derived) == set(census_binding["derived_measures"])
assert all(row["finding_authority"] is False for row in derived.values())
assert derived["owned_with_mortgage_over_30_share_pct"]["value"] == ((102.0 / 101.0) * 100.0)
try:
    module.normalize_census(census_binding, [header, values], 2020)
except ValueError:
    pass
else:
    raise AssertionError("ACS 2020 noncomparable year was accepted")

candidate = module.make_candidate(bindings["FRB_DSR_CURRENT_TOTAL"], fred_raw, fred, "2026-09-16T00:00:00Z")
assert candidate["finding_authority"] is False
assert candidate["public_activation_authorized"] is False
assert candidate["raw_sha256"] == module.sha256_bytes(fred_raw)

print("HOUSEHOLD_ECONOMIC_SOURCE_BINDINGS=PASS")
print("HOUSEHOLD_ECONOMIC_NORMALIZERS=PASS")
print("NYFED_WORKBOOK_NORMALIZATION=PENDING_EXACT_COLUMN_BINDING")
print("HOUSEHOLD_ECONOMIC_SOURCE_PUBLIC_ACTIVATION=false")
