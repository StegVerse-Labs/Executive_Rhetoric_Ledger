#!/usr/bin/env python3
"""Validate ERL durable task-state registries without network access."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

REQUIRED_STATES = {
    "COMPLETE",
    "BLOCKED",
    "RETRY",
    "REVIEW_REQUIRED",
    "FAILED",
    "CLAIMED",
    "SUPERSEDED",
    "MERGED",
}
TERMINAL_STATES = {"COMPLETE", "SUPERSEDED", "MERGED"}


def parse_time(value: str, field: str, errors: list[str]) -> datetime | None:
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (TypeError, ValueError):
        errors.append(f"{field} must be an ISO-8601 timestamp: {value!r}")
        return None


def require_text(obj: dict[str, Any], field: str, errors: list[str], prefix: str = "") -> None:
    value = obj.get(field)
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{prefix}{field} must be a non-empty string")


def validate_registry(path: Path, repo_root: Path) -> list[str]:
    errors: list[str] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"unable to read valid JSON from {path}: {exc}"]

    if not isinstance(data, dict):
        return ["registry root must be an object"]

    for field in ("registry_version", "goal_id", "originating_goal", "repository", "branch", "canonical_handoff"):
        require_text(data, field, errors)

    issue = data.get("canonical_issue")
    if not isinstance(issue, int) or issue <= 0:
        errors.append("canonical_issue must be a positive integer")

    declared_states = data.get("allowed_states")
    if not isinstance(declared_states, list) or set(declared_states) != REQUIRED_STATES:
        errors.append("allowed_states must exactly match the governed state set")

    tasks = data.get("tasks")
    if not isinstance(tasks, list) or not tasks:
        errors.append("tasks must be a non-empty array")
        return errors

    ids: set[str] = set()
    known_ids: set[str] = set()
    for task in tasks:
        if isinstance(task, dict) and isinstance(task.get("task_id"), str):
            known_ids.add(task["task_id"])

    for index, task in enumerate(tasks):
        prefix = f"tasks[{index}]."
        if not isinstance(task, dict):
            errors.append(f"tasks[{index}] must be an object")
            continue
        for field in ("task_id", "title", "state", "owner", "surface"):
            require_text(task, field, errors, prefix)
        task_id = task.get("task_id")
        if isinstance(task_id, str):
            if task_id in ids:
                errors.append(f"duplicate task_id: {task_id}")
            ids.add(task_id)

        state = task.get("state")
        if state not in REQUIRED_STATES:
            errors.append(f"{prefix}state is not governed: {state!r}")

        surface = task.get("surface")
        if isinstance(surface, str) and state in TERMINAL_STATES and not (repo_root / surface).exists():
            errors.append(f"{prefix}terminal surface does not exist: {surface}")

        if state == "COMPLETE":
            evidence = task.get("evidence")
            if not isinstance(evidence, list) or not evidence or not all(isinstance(item, str) and item.strip() for item in evidence):
                errors.append(f"{prefix}COMPLETE requires non-empty evidence")

        if state in {"BLOCKED", "REVIEW_REQUIRED", "RETRY"}:
            require_text(task, "release_condition", errors, prefix)

        if state == "CLAIMED":
            for field in ("claim_created_at", "claim_expires_at", "release_condition"):
                require_text(task, field, errors, prefix)
            created = parse_time(task.get("claim_created_at", ""), prefix + "claim_created_at", errors)
            expires = parse_time(task.get("claim_expires_at", ""), prefix + "claim_expires_at", errors)
            if created and expires and expires <= created:
                errors.append(f"{prefix}claim_expires_at must be later than claim_created_at")
            boundary = task.get("collision_boundary")
            if not isinstance(boundary, list) or not boundary:
                errors.append(f"{prefix}CLAIMED requires a non-empty collision_boundary")

        next_task = task.get("next_task")
        if next_task is not None and next_task not in known_ids:
            errors.append(f"{prefix}next_task references unknown task: {next_task!r}")

    consolidation = data.get("session_consolidation")
    if not isinstance(consolidation, dict):
        errors.append("session_consolidation must be an object")
    else:
        if consolidation.get("state") != "MERGED":
            errors.append("session_consolidation.state must be MERGED")
        require_text(consolidation, "archive_condition", errors, "session_consolidation.")
        merged_into = consolidation.get("merged_into")
        if not isinstance(merged_into, list) or len(merged_into) < 2:
            errors.append("session_consolidation.merged_into must identify at least two durable canonical locations")
        transferred = consolidation.get("unique_session_requirements_transferred")
        total = consolidation.get("unique_session_requirements_total")
        if not isinstance(transferred, int) or not isinstance(total, int) or transferred < 0 or total <= 0 or transferred > total:
            errors.append("session consolidation counts are invalid")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("registry", nargs="?", default="task-state/ERL-2026-07-24-MULTIANGLE-001.json")
    parser.add_argument("--repo-root", default=".")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    path = (repo_root / args.registry).resolve()
    errors = validate_registry(path, repo_root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"VALID: {path.relative_to(repo_root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
