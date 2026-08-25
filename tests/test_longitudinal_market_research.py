import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_module(name, relative_path):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


analogue = load_module("analogue", "scripts/find_historical_market_analogues.py")
validator = load_module("validator", "scripts/validate_longitudinal_market_evidence.py")
labeler = load_module("labeler", "scripts/label_market_forward_outcomes.py")
preference = load_module("preference", "scripts/build_trade_preference_evidence.py")
indexer = load_module("indexer", "scripts/index_existing_crypto_market_panel.py")


def state(state_id, ts, **features):
    return {
        "schema": "stegverse.erl.market_state_vector.v1",
        "state_id": state_id,
        "as_of_utc": ts,
        "feature_version": "v1",
        "features": features,
        "source_coverage": {
            "coverage_score": 1.0,
            "missing_families": [],
            "stale_families": [],
            "source_refs": ["fixture"],
        },
        "research_authority": "ERL",
        "execution_authority": "NONE",
        "may_authorize_order": False,
    }


def test_canonical_panel_indexes_without_fabricating_missing_families():
    source = ROOT / "research-data/2026-08-13_2026-08-21_crypto_market_panel.coingecko.utc.json"
    panel = json.loads(source.read_text())
    indexed = indexer.build_states(panel, str(source))
    assert len(indexed["states"]) == 9
    final = indexed["states"][-1]
    assert final["prices"]["XRP-USD"] == 1.45
    assert final["features"]["xrp_xlm_ratio"] > 7.18
    assert "derivatives" in final["source_coverage"]["missing_families"]
    assert final["source_coverage"]["coverage_score"] == 1.0
    assert final["execution_authority"] == "NONE"
    schema = json.loads((ROOT / "schemas/market-state-vector.schema.json").read_text())
    state_without_prices = {key: value for key, value in final.items() if key != "prices"}
    assert validator.validate_document(state_without_prices, schema) == []


def test_nearest_analogue_is_ranked_first_and_deterministic():
    current = state("current", "2026-08-25T18:00:00Z", btc_return=0.05, breadth=0.80, funding=0.01)
    history = [
        state("far", "2026-08-20T18:00:00Z", btc_return=-0.08, breadth=0.20, funding=-0.02),
        state("near", "2026-08-21T18:00:00Z", btc_return=0.045, breadth=0.76, funding=0.012),
        state("mid", "2026-08-22T18:00:00Z", btc_return=0.02, breadth=0.60, funding=0.005),
    ]
    first = analogue.find_analogues(current, history, top_k=3)
    second = analogue.find_analogues(current, history, top_k=3)
    assert first == second
    assert first["historical_analogues"][0]["analogue_id"] == "near"
    assert first["as_of_utc"] == current["as_of_utc"]
    assert first["execution_authority"] == "NONE"
    assert first["may_authorize_order"] is False


def test_missing_feature_is_penalized_and_exposed():
    current = state("current", "2026-08-25T18:00:00Z", btc_return=0.05, breadth=0.80)
    incomplete = state("incomplete", "2026-08-20T18:00:00Z", btc_return=0.05)
    complete = state("complete", "2026-08-21T18:00:00Z", btc_return=0.04, breadth=0.75)
    result = analogue.find_analogues(current, [incomplete, complete])
    rows = {row["analogue_id"]: row for row in result["historical_analogues"]}
    assert "breadth" in rows["incomplete"]["missing_dimensions"]
    assert rows["complete"]["similarity_score"] > rows["incomplete"]["similarity_score"]


def test_forward_outcomes_are_observed_without_lookahead_in_state_features():
    panel = [
        {"state_id": "s0", "as_of_utc": "2026-08-25T00:00:00Z", "prices": {"BTC-USD": 100.0, "ETH-USD": 50.0}},
        {"state_id": "s1", "as_of_utc": "2026-08-25T01:00:00Z", "prices": {"BTC-USD": 102.0, "ETH-USD": 49.0}},
        {"state_id": "s2", "as_of_utc": "2026-08-25T02:00:00Z", "prices": {"BTC-USD": 103.0, "ETH-USD": 51.0}},
    ]
    result = labeler.label_forward_outcomes(panel, [1, 2])
    first = result["records"][0]
    assert first["horizons"]["step_1"]["returns_pct"]["BTC-USD"] == 2.0
    assert first["horizons"]["step_2"]["returns_pct"]["ETH-USD"] == 2.0
    assert result["execution_authority"] == "NONE"


def test_trade_preference_builder_can_choose_candidate_or_forego_from_analogue_outcomes():
    current = state("current", "2026-08-25T18:00:00Z", btc_return=0.05)
    history = [state(f"s{i}", f"2026-08-{10+i:02d}T18:00:00Z", btc_return=0.05 + i * 0.0001) for i in range(12)]
    analogue_set = analogue.find_analogues(current, history, top_k=12)
    records = []
    for i, historical in enumerate(history):
        records.append({
            "state_id": historical["state_id"],
            "as_of_utc": historical["as_of_utc"],
            "horizons": {"step_1": {"status": "OBSERVED", "returns_pct": {"BTC-USD": 1.0 + i * 0.01, "ETH-USD": 0.2}}},
        })
    outcome_panel = {"records": records, "execution_authority": "NONE", "may_authorize_order": False}
    packet = preference.build_trade_preference_evidence(
        analogue_set=analogue_set,
        outcome_panel=outcome_panel,
        candidate_instrument="BTC-USD",
        candidate_side="BUY",
        comparison_instruments=["ETH-USD"],
        horizon="step_1",
        source_coverage={"coverage_score": 1.0, "missing_families": [], "stale_families": []},
        minimum_observations=10,
    )
    assert packet["preference"] == "PREFER"
    assert packet["execution_authority"] == "NONE"
    assert packet["may_authorize_order"] is False
    schema = json.loads((ROOT / "schemas/trade-preference-evidence.schema.json").read_text())
    assert validator.validate_document(packet, schema) == []


def test_trade_preference_validator_rejects_execution_authority():
    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "properties": {
            "research_authority": {"const": "ERL"},
            "execution_authority": {"const": "NONE"},
            "may_authorize_order": {"const": False},
        },
    }
    doc = {"research_authority": "ERL", "execution_authority": "TVC", "may_authorize_order": True}
    errors = validator.validate_document(doc, schema)
    assert any("execution_authority" in error for error in errors)
    assert any("may_authorize_order" in error for error in errors)


def test_low_coverage_cannot_emit_prefer():
    schema = {"$schema": "https://json-schema.org/draft/2020-12/schema", "type": "object", "additionalProperties": True}
    doc = {
        "schema": "stegverse.erl.trade_preference_evidence.v1",
        "research_authority": "ERL",
        "execution_authority": "NONE",
        "may_authorize_order": False,
        "source_coverage": {"coverage_score": 0.40},
        "confidence": 0.90,
        "historical_analogues": [{"analogue_id": "x"}],
        "preference": "PREFER",
    }
    errors = validator.validate_document(doc, schema)
    assert "evidence:prefer_forbidden_when_source_coverage_below_0_5" in errors


def test_zero_analogues_forces_nonpositive_preference():
    schema = {"$schema": "https://json-schema.org/draft/2020-12/schema", "type": "object", "additionalProperties": True}
    doc = {
        "schema": "stegverse.erl.trade_preference_evidence.v1",
        "research_authority": "ERL",
        "execution_authority": "NONE",
        "may_authorize_order": False,
        "source_coverage": {"coverage_score": 1.0},
        "confidence": 0.90,
        "historical_analogues": [],
        "preference": "PREFER",
    }
    errors = validator.validate_document(doc, schema)
    assert "evidence:nonempty_analogue_set_required_for_positive_preference" in errors
