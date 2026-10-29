"""Run the existing summit commands with attempt-specific audit retention."""
import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

GROUP = "ERL-RC-US-CN-AI-SUMMIT-2026"


def execute(root, run_id, attempt, invoke=subprocess.run):
    if not str(run_id).isdigit() or not str(attempt).isdigit():
        raise ValueError("numeric GitHub run and attempt identities required")
    root = Path(root).resolve()
    audit = root / "_audit" / f"summit-{run_id}-{attempt}"
    # Refuse reuse rather than accepting stale output as this attempt's evidence.
    audit.mkdir(parents=True, exist_ok=False)
    timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    receipt = {"schema": "stegverse.erl.summit-preflight/v1", "run_id": str(run_id),
               "run_attempt": str(attempt), "generated_at": timestamp,
               "scope": "DISPATCH_PREFLIGHT_ONLY", "coverage_state": "NOT_SCANNED",
               "acquisition_invocation_requested": False, "finding_authorized": False,
               "publication_authorized": False, "mykv_persistence_verified": False,
               "state": "PREFLIGHT_STARTED", "reason": None}

    def save():
        (audit / "preflight.json").write_text(json.dumps(receipt, indent=2) + "\n")

    save()
    try:
        result = invoke([sys.executable, "scripts/generate_active_research_dispatch.py",
                         "--generated-at", timestamp, "--output", str(audit / "dispatch.json")], cwd=root)
        if result.returncode:
            raise ValueError("DISPATCH_COMMAND_FAILED")
        data = json.loads((audit / "dispatch.json").read_text())
        if not isinstance(data, dict) or not isinstance(data.get("lanes"), list):
            raise ValueError("DISPATCH_SCHEMA_INVALID")
        if not all(isinstance(x, dict) for x in data["lanes"]):
            raise ValueError("DISPATCH_LANE_SCHEMA_INVALID")
        lanes = [x for x in data["lanes"] if x.get("group_id") == GROUP]
        if len(lanes) != 1:
            raise ValueError("DISPATCH_LANE_NOT_UNIQUE")
        lane = lanes[0]
        if lane.get("dispatch_state") != "ELIGIBLE_FOR_AUTOMATED_ACQUISITION":
            raise ValueError("DISPATCH_NOT_ELIGIBLE")
        if lane.get("finding_authorized") is not False or lane.get("publication_authorized") is not False:
            raise ValueError("DISPATCH_AUTHORITY_INVALID")
        queues = lane.get("queues")
        if not isinstance(queues, list) or not all(
                isinstance(q, dict) and isinstance(q.get("executable_items"), list) for q in queues):
            raise ValueError("DISPATCH_QUEUE_SCHEMA_INVALID")
        if sum(len(q["executable_items"]) for q in queues) < 6:
            raise ValueError("INSUFFICIENT_EXECUTABLE_SOURCES")
    except (OSError, ValueError, KeyError, TypeError) as exc:
        receipt.update(state="PREFLIGHT_REFUSED", reason=type(exc).__name__ + ": " + str(exc)[:160])
        save()
        return 2
    receipt.update(state="PREFLIGHT_PASSED", acquisition_invocation_requested=True)
    save()
    result = invoke([sys.executable, "scripts/run_us_china_ai_summit_research.py",
                     "--timestamp", timestamp, "--report", str(audit / "cycle.json")], cwd=root)
    # Keep runner output at its own evidence boundary even when CLI returns 2.
    if result.returncode:
        return result.returncode
    cycle = json.loads((audit / "cycle.json").read_text())
    if cycle.get("generated_at") != timestamp:
        raise ValueError("runner receipt timestamp mismatch")
    target = root / "assessments/us-china-ai-summit/research-cycles" / (timestamp[:10] + ".json")
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(audit / "cycle.json", target)
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--attempt", required=True)
    args = parser.parse_args()
    raise SystemExit(execute(Path.cwd(), args.run_id, args.attempt))
