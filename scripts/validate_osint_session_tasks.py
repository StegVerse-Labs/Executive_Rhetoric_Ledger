#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "coordination/osint-session-tasks.json"

REQUIRED = {
    "task_id",
    "originating_goal",
    "repository",
    "branch",
    "surfaces",
    "owner",
    "claim_state",
    "claim_created_at",
    "claim_expires_at",
    "release_condition",
    "expected_evidence",
    "collision_boundaries",
    "completion_state",
    "validation_state",
    "integration_state",
    "archival_dependency",
    "evidence_location",
    "next_executable_action",
}


def parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)


def main() -> int:
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    if data.get("schema") != "stegverse.executive_rhetoric_ledger.session_task_registry.v1":
        raise SystemExit("Unexpected session task registry schema")

    allowed_claims = set(data.get("allowed_claim_states", []))
    allowed_completion = set(data.get("allowed_completion_states", []))
    tasks = data.get("tasks")
    if not isinstance(tasks, list) or not tasks:
        raise SystemExit("Session task registry must contain tasks")

    seen_ids: set[str] = set()
    active_surfaces: dict[str, str] = {}
    now = datetime.now(timezone.utc)

    for task in tasks:
        missing = REQUIRED - set(task)
        if missing:
            raise SystemExit(f"{task.get('task_id', '<unknown>')} missing fields: {sorted(missing)}")
        task_id = task["task_id"]
        if task_id in seen_ids:
            raise SystemExit(f"Duplicate task_id: {task_id}")
        seen_ids.add(task_id)

        if task["claim_state"] not in allowed_claims:
            raise SystemExit(f"{task_id} has invalid claim_state")
        if task["completion_state"] not in allowed_completion:
            raise SystemExit(f"{task_id} has invalid completion_state")
        if not task["surfaces"] or not task["expected_evidence"] or not task["collision_boundaries"]:
            raise SystemExit(f"{task_id} lacks surfaces, evidence, or collision boundaries")
        if not task["release_condition"] or not task["next_executable_action"]:
            raise SystemExit(f"{task_id} lacks release condition or next action")

        expires = task["claim_expires_at"]
        active = task["claim_state"].startswith("CLAIMED_")
        if active:
            if not expires:
                raise SystemExit(f"{task_id} active claim has no expiration")
            if parse_time(expires) <= now:
                raise SystemExit(f"{task_id} active claim is stale; release, renew, or block it")
            for surface in task["surfaces"]:
                other = active_surfaces.get(surface)
                if other and other != task_id:
                    raise SystemExit(f"Conflicting active claims on {surface}: {other}, {task_id}")
                active_surfaces[surface] = task_id

        if task["claim_state"] == "COMPLETE":
            if task["completion_state"] != "COMPLETE":
                raise SystemExit(f"{task_id} COMPLETE claim lacks COMPLETE completion state")
            if task["archival_dependency"]:
                raise SystemExit(f"{task_id} complete task remains an archival dependency")

        if task["claim_state"] == "BLOCKED" and "release_condition" not in task:
            raise SystemExit(f"{task_id} blocked task lacks release condition")

    print(f"Validated {len(tasks)} session tasks; active claims: {len(active_surfaces)} surfaces.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
