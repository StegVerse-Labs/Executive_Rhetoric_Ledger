#!/usr/bin/env python3
"""Apply reviewed evidence movements to an ERL research frontier.

Only REVIEWED movements are accepted. Search candidates cannot directly change
conclusions; movements are trajectory-relative and may create newly discovered
trajectories only after review.
"""
from __future__ import annotations

import argparse
import copy
import json
import pathlib

ALLOWED = {"strengthen", "weaken", "disambiguate", "contextualize", "no-update"}
TRAJECTORY_STATES = {"OPEN", "ACTIVE", "BLOCKED", "SATURATED", "SUPERSEDED", "MERGED"}


def fail(message: str) -> None:
    raise SystemExit("FAIL: " + message)


def load_json(path: str):
    return json.loads(pathlib.Path(path).read_text(encoding="utf-8"))


def load_jsonl(path: str):
    rows = []
    for line_number, line in enumerate(pathlib.Path(path).read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except Exception as exc:
            fail(f"invalid JSONL line {line_number}: {exc}")
    return rows


def apply(frontier: dict, movements: list[dict]) -> dict:
    if frontier.get("schema") != "stegverse.erl.research_frontier.v1":
        fail("wrong frontier schema")
    if frontier.get("evaluation_authority") != "StegVerse-Labs/Executive_Rhetoric_Ledger":
        fail("wrong evaluation authority")

    output = copy.deepcopy(frontier)
    trajectories = {item["trajectory_id"]: item for item in output.get("trajectories", [])}
    history = output.setdefault("evidence_movement_history", [])
    seen = {item.get("movement_id") for item in history if item.get("movement_id")}

    for movement_record in movements:
        movement_id = movement_record.get("movement_id")
        if not movement_id:
            fail("missing movement_id")
        if movement_id in seen:
            continue
        if movement_record.get("review_state") != "REVIEWED":
            fail(f"{movement_id}: movement not REVIEWED")
        movement = movement_record.get("movement")
        if movement not in ALLOWED:
            fail(f"{movement_id}: invalid movement")
        if movement_record.get("authority_effect", "NONE") != "NONE":
            fail(f"{movement_id}: authority escalation")
        if movement_record.get("final_conclusion") is True:
            fail(f"{movement_id}: final conclusion forbidden")

        trajectory_ids = movement_record.get("trajectory_ids") or []
        if not trajectory_ids:
            fail(f"{movement_id}: no trajectory_ids")
        for trajectory_id in trajectory_ids:
            if trajectory_id not in trajectories:
                fail(f"{movement_id}: unknown trajectory {trajectory_id}")
            trajectory = trajectories[trajectory_id]
            counts = trajectory.setdefault("movement_counts", {key: 0 for key in sorted(ALLOWED)})
            counts[movement] = counts.get(movement, 0) + 1
            candidate_id = movement_record.get("candidate_id")
            refs = trajectory.setdefault("reviewed_candidate_ids", [])
            if candidate_id and candidate_id not in refs:
                refs.append(candidate_id)

        new_trajectory = movement_record.get("new_trajectory")
        if new_trajectory:
            if not isinstance(new_trajectory, dict):
                fail(f"{movement_id}: new_trajectory must be object")
            new_id = new_trajectory.get("trajectory_id")
            if not new_id or new_id in trajectories:
                fail(f"{movement_id}: duplicate/missing new trajectory_id")
            if new_trajectory.get("state") not in TRAJECTORY_STATES:
                fail(f"{movement_id}: invalid new trajectory state")
            new_trajectory = copy.deepcopy(new_trajectory)
            new_trajectory["parent_movement_id"] = movement_id
            output.setdefault("trajectories", []).append(new_trajectory)
            trajectories[new_id] = new_trajectory

        history.append(movement_record)
        seen.add(movement_id)

    return output


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("frontier")
    parser.add_argument("movements")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    movements = load_jsonl(args.movements)
    result = apply(load_json(args.frontier), movements)
    pathlib.Path(args.output).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": "PASS",
        "movements_applied": len(movements),
        "trajectory_count": len(result.get("trajectories", [])),
        "evaluation_authority": result.get("evaluation_authority"),
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
