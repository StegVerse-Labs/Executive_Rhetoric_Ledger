import copy
import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("economic_lanes", ROOT / "scripts/run_economic_research_lanes.py")
lanes = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(lanes)


def inputs():
    registry = json.loads((ROOT / "economic-trajectories/research-lanes.v1.json").read_text())
    dictionary = json.loads((ROOT / "economic-trajectories/measurement-dictionary.v1.json").read_text())
    gaps = {
        "ERL-ECON-CA": json.loads((ROOT / "economic-trajectories/canada/gap-matrix.v1.json").read_text()),
        "ERL-ECON-US": json.loads((ROOT / "economic-trajectories/united-states/gap-matrix.v1.json").read_text()),
    }
    indicator_ids = {row["indicator_id"] for row in dictionary["indicators"]}
    gap_ids = {lane: {row["gap_id"] for row in matrix["rows"]} for lane, matrix in gaps.items()}
    return registry, gaps, indicator_ids, gap_ids


def fake_fetch(source):
    body = source["source_id"].encode()
    return {
        "ok": True,
        "http_status": 200,
        "final_url": source["url"],
        "content_type": "text/html",
        "etag": None,
        "last_modified": None,
        "sha256": lanes.hashlib.sha256(body).hexdigest(),
        "bytes": len(body),
    }


def test_registry_is_valid_and_overlay_has_no_source_adapters():
    registry, _, indicator_ids, gap_ids = inputs()
    assert lanes.validate_registry(registry, indicator_ids, gap_ids) == []
    overlay = next(row for row in registry["lanes"] if row["lane_id"] == "ERL-ECON-CA-US-OVERLAY")
    assert overlay["sources"] == []
    assert overlay["mode"] == "reviewed-findings-only"


def test_cross_country_source_is_rejected():
    registry, _, indicator_ids, gap_ids = inputs()
    invalid = copy.deepcopy(registry)
    invalid["lanes"][0]["sources"][0]["jurisdiction"] = "United States"
    assert any("crosses national lane" in error for error in lanes.validate_registry(invalid, indicator_ids, gap_ids))


def test_overlay_acquisition_is_rejected():
    registry, _, indicator_ids, gap_ids = inputs()
    invalid = copy.deepcopy(registry)
    invalid["lanes"][2]["sources"] = [copy.deepcopy(invalid["lanes"][0]["sources"][0])]
    assert any("overlay may not acquire" in error for error in lanes.validate_registry(invalid, indicator_ids, gap_ids))


def test_automatic_promotion_is_rejected():
    registry, _, indicator_ids, gap_ids = inputs()
    invalid = copy.deepcopy(registry)
    invalid["authority"]["may_create_findings"] = True
    assert any("deny findings" in error for error in lanes.validate_registry(invalid, indicator_ids, gap_ids))


def test_first_capture_routes_review_tasks_without_findings_or_comparisons():
    registry, gaps, _, _ = inputs()
    run, state = lanes.capture(registry, gaps, datetime(2026, 8, 25, tzinfo=timezone.utc), fetcher=fake_fetch)
    assert run["summary"] == {
        "sources": 6,
        "changed": 0,
        "baseline_captured": 6,
        "stale": 0,
        "unavailable": 0,
        "review_tasks": 6,
        "findings_created": 0,
        "comparisons_created": 0,
    }
    assert all(row["status"] == "REVIEW_REQUIRED" for row in run["review_tasks"])
    assert run["authority"] == {"finding_authorized": False, "comparison_authorized": False, "publication_authorized": False}
    assert len(state["sources"]) == 6


def test_unchanged_capture_is_deterministic_and_creates_no_tasks():
    registry, gaps, _, _ = inputs()
    when = datetime(2026, 8, 25, tzinfo=timezone.utc)
    first, state = lanes.capture(registry, gaps, when, fetcher=fake_fetch)
    second, _ = lanes.capture(registry, gaps, when, previous=state, fetcher=fake_fetch)
    third, _ = lanes.capture(registry, gaps, when, previous=state, fetcher=fake_fetch)
    assert second == third
    assert second["summary"]["changed"] == 0
    assert second["summary"]["review_tasks"] == 0
    assert all(row["state"] == "UNCHANGED" for row in second["receipts"])
    assert first["summary"]["findings_created"] == second["summary"]["findings_created"] == 0


def test_changed_source_routes_only_its_declared_national_gap():
    registry, gaps, _, _ = inputs()
    when = datetime(2026, 8, 25, tzinfo=timezone.utc)
    _, state = lanes.capture(registry, gaps, when, fetcher=fake_fetch)

    def one_change(source):
        result = fake_fetch(source)
        if source["source_id"] == "ERL-ECON-CA-SRC-STATCAN-TRADE":
            result["sha256"] = "f" * 64
        return result

    run, _ = lanes.capture(registry, gaps, when, previous=state, fetcher=one_change)
    assert run["summary"]["changed"] == 1
    assert len(run["review_tasks"]) == 1
    task = run["review_tasks"][0]
    assert task["lane_id"] == "ERL-ECON-CA"
    assert task["gap_id"] == "ERL-ECON-CA-GAP-DIVERSIFICATION-EFFECTS"
    assert task["may_create_finding"] is False


def test_unchanged_source_becomes_stale_and_routes_review_after_threshold():
    registry, gaps, _, _ = inputs()
    first_when = datetime(2026, 1, 1, tzinfo=timezone.utc)
    _, state = lanes.capture(registry, gaps, first_when, fetcher=fake_fetch)
    later = datetime(2027, 2, 15, tzinfo=timezone.utc)
    run, _ = lanes.capture(registry, gaps, later, previous=state, fetcher=fake_fetch)
    assert all(row["state"] == "STALE" for row in run["receipts"])
    assert len(run["review_tasks"]) == 6
    assert all(row["trigger"] == "STALE" for row in run["review_tasks"])
    assert run["summary"]["findings_created"] == 0
