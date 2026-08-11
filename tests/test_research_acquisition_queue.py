#!/usr/bin/env python3
from __future__ import annotations
import json
import subprocess
import sys
import tempfile
from pathlib import Path


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    builder = repo / "scripts/build_research_acquisition_queue.py"
    with tempfile.TemporaryDirectory() as td:
        base = Path(td)
        frontier = base / "fixture-frontier.json"
        output = base / "requests.jsonl"
        frontier.write_text(json.dumps({
            "schema": "stegverse.erl.research_frontier.v1",
            "repository": "Fixture/Subject",
            "evaluation_authority": "StegVerse-Labs/Executive_Rhetoric_Ledger",
            "canonical_task": "fixture",
            "rules": {
                "all_trajectories_required": True,
                "new_trajectory_discovery_allowed": True,
                "binary_support_refute_forbidden": True,
                "local_conclusion_promotion": False
            },
            "trajectories": [
                {"trajectory_id": "T-A", "title": "Initial explanation", "state": "ACTIVE", "priority": "HIGH", "acquisition_queries": ["alpha evidence"]},
                {"trajectory_id": "T-B", "title": "Alternative explanation", "state": "ACTIVE", "priority": "HIGH", "acquisition_queries": ["beta evidence"]},
                {"trajectory_id": "T-C", "title": "Null trajectory", "state": "OPEN", "priority": "MEDIUM", "acquisition_queries": ["null evidence"]},
                {"trajectory_id": "T-D", "title": "Closed trajectory", "state": "SATURATED", "priority": "LOW", "acquisition_queries": ["must not schedule"]}
            ]
        }, indent=2) + "\n", encoding="utf-8")

        first = subprocess.run([sys.executable, str(builder), str(frontier), str(output)], check=True, capture_output=True, text=True)
        second = subprocess.run([sys.executable, str(builder), str(frontier), str(output)], check=True, capture_output=True, text=True)
        first_summary = json.loads(first.stdout)
        second_summary = json.loads(second.stdout)
        rows = [json.loads(line) for line in output.read_text(encoding="utf-8").splitlines() if line.strip()]

        assert first_summary["eligible_trajectories"] == 3
        assert first_summary["new_requests"] == 3
        assert second_summary["new_requests"] == 0
        assert len(rows) == 3
        assert {row["trajectory_ids"][0] for row in rows} == {"T-A", "T-B", "T-C"}
        assert all(row["state"] == "ACTIVE" for row in rows)
        assert len({row["request_id"] for row in rows}) == 3
        assert not any("T-D" in row["trajectory_ids"] for row in rows)

    print("PASS: all OPEN/ACTIVE trajectories scheduled once; SATURATED excluded; rerun idempotent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
