import importlib.util
import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]


def load_module(name, relative_path):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


indexer = load_module("shock_indexer", "scripts/index_crypto_system_shock_event.py")


def test_system_shock_normalizes_to_unresolved_non_authoritative_observation():
    source = ROOT / "research-data/2026-08-22_crypto_system_shock_transaction_reconstruction.v1.json"
    payload = json.loads(source.read_text())
    observation = indexer.normalize_shock(payload, str(source))
    schema = json.loads((ROOT / "schemas/market-observation.schema.json").read_text())
    errors = list(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(observation))
    assert errors == []
    assert observation["observed_at_utc"] == "2026-08-22T05:11:20Z"
    assert observation["status"] == "UNRESOLVED"
    assert observation["facts"]["synchronized_cliff_observed"] is True
    assert observation["facts"]["finding_authorized"] is False
    assert observation["facts"]["xrp_vs_btc_display_change_amplitude_ratio"] == 8.56
    assert len(observation["hypotheses"]) == 6
    assert observation["execution_authority"] == "NONE"
    assert observation["may_authorize_order"] is False


def test_event_normalization_is_deterministic():
    source = ROOT / "research-data/2026-08-22_crypto_system_shock_transaction_reconstruction.v1.json"
    payload = json.loads(source.read_text())
    first = indexer.normalize_shock(payload, "canonical-shock-source")
    second = indexer.normalize_shock(payload, "canonical-shock-source")
    assert first == second
    assert first["observation_digest"].startswith("sha256:")


def test_unresolved_event_does_not_promote_hypothesis_to_fact():
    source = ROOT / "research-data/2026-08-22_crypto_system_shock_transaction_reconstruction.v1.json"
    payload = json.loads(source.read_text())
    observation = indexer.normalize_shock(payload, str(source))
    facts_text = json.dumps(observation["facts"], sort_keys=True)
    assert "derivatives_led" not in facts_text
    assert "spot_led" not in facts_text
    assert observation["status"] == "UNRESOLVED"
