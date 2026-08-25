import importlib.util
import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "validate_market_source_timeseries.py"
SPEC = importlib.util.spec_from_file_location("validate_market_source_timeseries", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)
validate = MODULE.validate
SCHEMA = json.loads((ROOT / "schemas" / "market-source-timeseries.schema.json").read_text())


def _payload(family="derivatives"):
    return {
        "schema": "stegverse.erl.market_source_timeseries.v1",
        "series_id": "test-series",
        "source_family": family,
        "provider": "provider.example",
        "retrieved_at_utc": "2026-08-25T20:00:00Z",
        "granularity": "1h",
        "metrics": ["funding_rate", "open_interest_usd"],
        "observations": [
            {"as_of_utc": "2026-08-25T18:00:00Z", "instrument": "BTC-USD", "venue": "EXAMPLE", "values": {"funding_rate": 0.0001, "open_interest_usd": 1000.0}, "quality_flags": []},
            {"as_of_utc": "2026-08-25T19:00:00Z", "instrument": "BTC-USD", "venue": "EXAMPLE", "values": {"funding_rate": 0.0002, "open_interest_usd": 1010.0}, "quality_flags": []}
        ],
        "source_refs": ["https://provider.example/source"],
        "notes": [],
        "research_authority": "ERL",
        "execution_authority": "NONE",
        "may_authorize_order": False
    }


def test_valid_cross_family_series_passes():
    assert validate(_payload(), SCHEMA) == []


def test_schema_supports_every_numeric_source_family():
    for family in ["spot_market", "derivatives", "order_book_liquidity", "stablecoin_flows", "etf_fund_flows", "on_chain_flows", "macro_cross_market"]:
        assert validate(_payload(family), SCHEMA) == []


def test_rejects_out_of_order_timestamps():
    payload = _payload()
    payload["observations"].reverse()
    errors = validate(payload, SCHEMA)
    assert any("strictly increasing" in error for error in errors)


def test_rejects_undeclared_or_missing_metrics():
    payload = _payload()
    payload["observations"][0]["values"] = {"funding_rate": 0.1, "unexpected": 2.0}
    errors = validate(payload, SCHEMA)
    assert any("undeclared metrics" in error for error in errors)
    assert any("omits declared metrics" in error for error in errors)


def test_authority_boundary_is_schema_enforced():
    payload = _payload()
    payload["execution_authority"] = "BROKER"
    errors = validate(payload, SCHEMA)
    assert errors
    raw_errors = list(Draft202012Validator(SCHEMA, format_checker=FormatChecker()).iter_errors(payload))
    assert raw_errors
