import importlib.util
import json
from pathlib import Path


def load_module():
    path = Path(__file__).resolve().parents[1] / "scripts" / "generate_active_research_dispatch.py"
    spec = importlib.util.spec_from_file_location("active_dispatch", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def write_json(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value), encoding="utf-8")


def test_active_ready_queue_requires_mykv(tmp_path):
    write_json(tmp_path / "coordination/research-candidate-activation-registry.v1.json", {
        "groups": [{
            "group_id": "ERL-RC-TEST-001",
            "title": "test",
            "active": True,
            "state": "RESEARCH_ACTIVE",
            "durable_owner": "issue:1",
            "artifact_paths": ["config/test-source-queue.json"],
            "next_executable_task": "Acquire public evidence."
        }]
    })
    write_json(tmp_path / "config/test-source-queue.json", {
        "goal_id": "ERL-TEST-001",
        "network_policy": "PUBLIC_HTTPS_ONLY_NO_AUTH",
        "credential_requirement": "NONE",
        "finding_authority": "NONE",
        "items": [{
            "source_id": "SRC-1",
            "state": "READY",
            "url": "https://example.com/evidence",
            "destination": "evidence/example.native",
            "evidence_class": "official-record"
        }]
    })

    doc = load_module().build_dispatch(tmp_path, "2026-09-10T23:59:00Z")
    lane = doc["lanes"][0]
    assert lane["dispatch_state"] == "ELIGIBLE_FOR_AUTOMATED_ACQUISITION"
    assert lane["mykv"]["required"] is True
    assert lane["mykv"]["lane"] == "02_Research/ERL"
    assert doc["mykv_coordination"]["github_storage_satisfies_persistence"] is False
    assert lane["queues"][0]["executable_items"][0]["persistence_required"] is True
    assert lane["finding_authorized"] is False
    assert lane["publication_authorized"] is False


def test_active_lane_without_queue_is_deferred_not_dropped(tmp_path):
    write_json(tmp_path / "coordination/research-candidate-activation-registry.v1.json", {
        "groups": [{
            "group_id": "ERL-RC-MANUAL-001",
            "title": "manual",
            "active": True,
            "state": "RESEARCH_ACTIVE",
            "durable_owner": "issue:2",
            "artifact_paths": [],
            "next_executable_task": "Acquire unavailable primary record."
        }]
    })

    doc = load_module().build_dispatch(tmp_path, "2026-09-10T23:59:00Z")
    lane = doc["lanes"][0]
    assert lane["dispatch_state"] == "RESEARCH_ACTIVE_NO_AUTOMATED_ACQUISITION"
    assert lane["mykv"]["required"] is False
