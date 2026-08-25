import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_module(name, relative_path):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


health = load_module("source_health", "scripts/build_longitudinal_source_health.py")


def test_observation_timestamp_extraction_does_not_use_arbitrary_future_windows():
    shock = ROOT / "research-data/2026-08-22_crypto_system_shock_transaction_reconstruction.v1.json"
    observed = health.source_latest_timestamp(shock)
    assert observed is not None
    assert observed.isoformat().replace("+00:00", "Z") == "2026-08-22T05:11:20Z"


def test_daily_panel_uses_last_observed_date():
    panel = ROOT / "research-data/2026-08-13_2026-08-21_crypto_market_panel.coingecko.utc.json"
    observed = health.source_latest_timestamp(panel)
    assert observed is not None
    assert observed.isoformat().replace("+00:00", "Z") == "2026-08-21T23:59:59Z"


def test_health_receipt_marks_missing_and_stale_families_without_imputation():
    registry = json.loads((ROOT / "research-data/longitudinal-market-source-registry.v1.json").read_text())
    policy = json.loads((ROOT / "research-data/longitudinal-market-source-health-policy.v1.json").read_text())
    as_of = datetime(2026, 8, 25, 20, 0, 0, tzinfo=timezone.utc)
    receipt = health.build_health(registry, policy, ROOT, as_of)
    families = {row["family"]: row for row in receipt["families"]}

    assert families["spot_market"]["health_state"] == "STALE"
    assert families["spot_market"]["age_hours"] > 48
    assert families["event_context"]["health_state"] == "FRESH"
    assert families["derivatives"]["health_state"] == "MISSING"
    assert families["order_book_liquidity"]["health_state"] == "MISSING"
    assert receipt["coverage_score"] < 0.25
    assert receipt["execution_authority"] == "NONE"
    assert receipt["may_authorize_order"] is False


def test_source_health_is_deterministic_for_fixed_as_of():
    registry = json.loads((ROOT / "research-data/longitudinal-market-source-registry.v1.json").read_text())
    policy = json.loads((ROOT / "research-data/longitudinal-market-source-health-policy.v1.json").read_text())
    as_of = datetime(2026, 8, 25, 20, 0, 0, tzinfo=timezone.utc)
    first = health.build_health(registry, policy, ROOT, as_of)
    second = health.build_health(registry, policy, ROOT, as_of)
    assert first == second
    assert first["receipt_digest"].startswith("sha256:")
