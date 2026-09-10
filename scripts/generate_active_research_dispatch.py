#!/usr/bin/env python3
"""Generate restartable ERL active-research dispatch state with required MyKV persistence."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

BASE_REGISTRY = Path("coordination/research-candidate-activation-registry.v1.json")
OVERLAY_GLOB = "research-candidate-activation-registry.overlay.*.json"
EXECUTABLE_ITEM_STATES = {"READY", "CONTINUING", "REFRESH"}
MYKV_LANE = "02_Research/ERL"
SCHEMA = "stegverse.executive_rhetoric_ledger.active_research_dispatch.v1"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_groups(root: Path) -> list[dict[str, Any]]:
    groups = list(load_json(root / BASE_REGISTRY).get("groups", []))
    for overlay in sorted((root / "coordination").glob(OVERLAY_GLOB)):
        groups.extend(load_json(overlay).get("groups", []))
    return groups


def queue_candidates(root: Path, group: dict[str, Any]) -> list[Path]:
    candidates: list[Path] = []
    for raw in group.get("artifact_paths", []):
        if not isinstance(raw, str) or not raw.endswith(".json"):
            continue
        lowered = raw.lower()
        if "queue" not in lowered and "research-lane" not in lowered and "recurring-search" not in lowered:
            continue
        path = root / raw
        if path.is_file():
            candidates.append(path)
    return candidates


def inspect_queue(root: Path, queue: Path) -> dict[str, Any]:
    doc = load_json(queue)
    items = doc.get("items")
    executable = []
    if isinstance(items, list):
        for item in items:
            if not isinstance(item, dict):
                continue
            state = str(item.get("state", "")).upper()
            url = item.get("url")
            if state in EXECUTABLE_ITEM_STATES and isinstance(url, str) and url.startswith(("https://", "http://")):
                executable.append({
                    "source_id": item.get("source_id"),
                    "state": state,
                    "url": url,
                    "destination": item.get("destination"),
                    "evidence_class": item.get("evidence_class"),
                    "persistence_required": True,
                    "required_storage_lane": MYKV_LANE,
                })
    enabled = doc.get("enabled") is True
    return {
        "queue_path": queue.relative_to(root).as_posix(),
        "queue_goal_id": doc.get("goal_id") or doc.get("lane_id") or doc.get("config_id"),
        "network_policy": doc.get("network_policy"),
        "credential_requirement": doc.get("credential_requirement"),
        "finding_authority": doc.get("finding_authority"),
        "executable_items": executable,
        "config_enabled": enabled,
    }


def build_dispatch(root: Path, generated_at: str) -> dict[str, Any]:
    lanes = []
    for group in load_groups(root):
        if group.get("active") is not True:
            continue
        queues = [inspect_queue(root, p) for p in queue_candidates(root, group)]
        executable_count = sum(len(q["executable_items"]) for q in queues)
        if executable_count:
            state = "ELIGIBLE_FOR_AUTOMATED_ACQUISITION"
        elif queues:
            state = "RESEARCH_ACTIVE_NO_READY_ACQUISITION_ITEMS"
        else:
            state = "RESEARCH_ACTIVE_NO_AUTOMATED_ACQUISITION"
        lanes.append({
            "group_id": group.get("group_id"),
            "title": group.get("title"),
            "research_state": group.get("state"),
            "durable_owner": group.get("durable_owner"),
            "next_executable_task": group.get("next_executable_task"),
            "dispatch_state": state,
            "queues": queues,
            "mykv": {
                "required": executable_count > 0,
                "lane": MYKV_LANE,
                "completion_states": [
                    "KV_STORED_AND_READBACK_VERIFIED",
                    "KV_ALREADY_PRESENT_AND_HASH_MATCHED",
                ],
                "deferred_states": ["KV_PERSISTENCE_PENDING", "KV_UNAVAILABLE"],
            },
            "finding_authorized": False,
            "publication_authorized": False,
        })
    return {
        "schema": SCHEMA,
        "generated_at": generated_at,
        "registry": BASE_REGISTRY.as_posix(),
        "restart_basis": "ACTIVE_REGISTRY_PLUS_LATEST_ACQUISITION_AND_MYKV_RECEIPTS",
        "mykv_coordination": {
            "required_lane": MYKV_LANE,
            "github_storage_satisfies_persistence": False,
            "exact_byte_readback_required": True,
            "cross_lane_source_reuse_by_hash": True,
            "cross_lane_finding_state_reuse": False,
        },
        "lanes": lanes,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--generated-at", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    document = build_dispatch(args.root.resolve(), args.generated_at)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(args.output)


if __name__ == "__main__":
    main()
