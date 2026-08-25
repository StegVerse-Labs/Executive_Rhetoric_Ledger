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


normalizer = load_module("event_normalizer", "scripts/normalize_existing_market_events.py")


def test_generic_event_requires_real_timestamp_or_capture_date():
    payload = {"schema": "example.event.v1", "status": "candidate"}
    try:
        normalizer.normalize_known_event(payload, "example.json")
    except ValueError as exc:
        assert "timestamp" in str(exc)
    else:
        raise AssertionError("missing timestamp must fail closed")


def test_generic_event_preserves_non_authority_and_does_not_invent_hypotheses():
    payload = {
        "schema": "example.event.v1",
        "captured_on": "2026-08-20",
        "status": "candidate",
        "finding_authorized": False,
        "note": "source-specific interpretation remains unresolved"
    }
    observation = normalizer.normalize_known_event(payload, "research-data/example.json")
    schema = json.loads((ROOT / "schemas/market-observation.schema.json").read_text())
    errors = list(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(observation))
    assert errors == []
    assert observation["status"] == "PARTIAL"
    assert observation["facts"]["finding_authorized"] is False
    assert observation["hypotheses"] == []
    assert observation["execution_authority"] == "NONE"
    assert observation["may_authorize_order"] is False
