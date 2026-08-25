import importlib.util
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
    doc = {
        "research_authority": "ERL",
        "execution_authority": "TVC",
        "may_authorize_order": True,
    }
    errors = validator.validate_document(doc, schema)
    assert any("execution_authority" in error for error in errors)
    assert any("may_authorize_order" in error for error in errors)


def test_low_coverage_cannot_emit_prefer():
    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "additionalProperties": True,
    }
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
    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "additionalProperties": True,
    }
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
