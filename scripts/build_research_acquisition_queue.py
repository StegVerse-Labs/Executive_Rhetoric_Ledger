#!/usr/bin/env python3
"""Build an append-only acquisition queue from every OPEN/ACTIVE ERL trajectory.

This is a planning/transport step only. It does not search, rank truth, or change an
assessment. Re-running is idempotent by deterministic request_id.
"""
from __future__ import annotations
import argparse, hashlib, json
from datetime import datetime, timezone
from pathlib import Path


def rid(frontier_id: str, trajectory_id: str, query: str) -> str:
    payload = f"{frontier_id}|{trajectory_id}|{query}".encode("utf-8")
    return "ARQ-" + hashlib.sha256(payload).hexdigest()[:24]


def load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("frontier")
    ap.add_argument("output")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    frontier_path = Path(args.frontier)
    output_path = Path(args.output)
    frontier = json.loads(frontier_path.read_text(encoding="utf-8"))
    frontier_id = frontier_path.stem
    existing = load_jsonl(output_path)
    existing_ids = {row.get("request_id") for row in existing}
    additions: list[dict] = []

    for trajectory in frontier.get("trajectories", []):
        if trajectory.get("state") not in {"OPEN", "ACTIVE"}:
            continue
        tid = trajectory.get("trajectory_id")
        for query in trajectory.get("acquisition_queries", []):
            request_id = rid(frontier_id, tid, query)
            if request_id in existing_ids:
                continue
            additions.append({
                "request_id": request_id,
                "trajectory_ids": [tid],
                "query": query,
                "state": "ACTIVE",
                "priority": trajectory.get("priority", "MEDIUM"),
                "source_classes": trajectory.get("source_classes", []),
                "created_at": datetime.now(timezone.utc).isoformat(),
                "originating_goal": frontier.get("canonical_task", ""),
                "collision_key": hashlib.sha256(f"{tid}|{query}".encode()).hexdigest()[:20],
                "release_condition": "candidate search completed with receipt or task reaches BLOCKED/FAILED/SUPERSEDED/MERGED state"
            })

    if not args.dry_run and additions:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("a", encoding="utf-8") as handle:
            for row in additions:
                handle.write(json.dumps(row, sort_keys=True) + "\n")

    print(json.dumps({
        "frontier": str(frontier_path),
        "eligible_trajectories": sum(1 for t in frontier.get("trajectories", []) if t.get("state") in {"OPEN", "ACTIVE"}),
        "existing_requests": len(existing),
        "new_requests": len(additions),
        "dry_run": args.dry_run
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
