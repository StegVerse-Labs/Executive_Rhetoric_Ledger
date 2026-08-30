#!/usr/bin/env python3
"""Validate an ERL-governed research surface checkout.

Usage:
  python scripts/validate_research_surface.py /path/to/repository

This validator is intentionally local/deterministic. It does not search the web,
mutate candidate ledgers, or confer evidentiary standing.
"""
from __future__ import annotations
import json
import pathlib
import sys

REQUIRED = [
    "research/README.md",
    "research/frontier.json",
    "research/acquisition_requests.jsonl",
    "research/source_candidates.jsonl",
    "research/research_receipts.jsonl",
]

ALLOWED_TRAJECTORY_STATES = {"OPEN", "ACTIVE", "BLOCKED", "SATURATED", "SUPERSEDED", "MERGED"}
ALLOWED_REQUEST_STATES = {"OPEN", "ACTIVE", "RETRY", "COMPLETE", "BLOCKED", "FAILED", "SUPERSEDED", "MERGED"}


def fail(msg: str) -> None:
    raise SystemExit(f"FAIL: {msg}")


def read_json(path: pathlib.Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"invalid JSON {path}: {exc}")


def read_jsonl(path: pathlib.Path):
    out = []
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            out.append(json.loads(line))
        except Exception as exc:
            fail(f"invalid JSONL {path}:{i}: {exc}")
    return out


def main() -> int:
    base = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    missing = [p for p in REQUIRED if not (base / p).exists()]
    if missing:
        fail("missing required files: " + ", ".join(missing))

    frontier = read_json(base / "research/frontier.json")
    if frontier.get("schema") != "stegverse.erl.research_frontier.v1":
        fail("wrong frontier schema")
    if frontier.get("evaluation_authority") != "StegVerse-Labs/Executive_Rhetoric_Ledger":
        fail("ERL must remain evaluation authority")
    rules = frontier.get("rules") or {}
    required_rules = {
        "all_trajectories_required": True,
        "new_trajectory_discovery_allowed": True,
        "binary_support_refute_forbidden": True,
        "local_conclusion_promotion": False,
    }
    for k, v in required_rules.items():
        if rules.get(k) is not v:
            fail(f"frontier rule {k} must be {v}")

    ids = set()
    for t in frontier.get("trajectories", []):
        tid = t.get("trajectory_id")
        if not tid or tid in ids:
            fail("trajectory IDs must be present and unique")
        ids.add(tid)
        if t.get("state") not in ALLOWED_TRAJECTORY_STATES:
            fail(f"invalid trajectory state for {tid}")

    requests = read_jsonl(base / "research/acquisition_requests.jsonl")
    request_ids = set()
    for r in requests:
        rid = r.get("request_id")
        if not rid or rid in request_ids:
            fail("request IDs must be present and unique")
        request_ids.add(rid)
        if r.get("state", "ACTIVE") not in ALLOWED_REQUEST_STATES:
            fail(f"invalid request state for {rid}")
        if not r.get("trajectory_ids"):
            fail(f"request {rid} has no trajectory IDs")
        if not r.get("query"):
            fail(f"request {rid} has no query")

    candidates = read_jsonl(base / "research/source_candidates.jsonl")
    candidate_ids = set()
    for c in candidates:
        cid = c.get("candidate_id")
        if not cid or cid in candidate_ids:
            fail("candidate IDs must be present and unique")
        candidate_ids.add(cid)
        if c.get("evidence_role") not in {"lead-only", "context-only"}:
            fail(f"candidate {cid} illegally exceeds candidate evidence posture")
        if c.get("evaluation_changed") is True:
            fail(f"candidate {cid} claims local evaluation change")
        if c.get("native_records_mutated") is True:
            fail(f"candidate {cid} claims native mutation during research acquisition")
        if not c.get("trajectory_ids"):
            fail(f"candidate {cid} has no trajectory linkage")
        if not c.get("source_url"):
            fail(f"candidate {cid} has no source URL")

    read_jsonl(base / "research/research_receipts.jsonl")
    print(json.dumps({
        "status": "PASS",
        "repository": frontier.get("repository"),
        "trajectories": len(frontier.get("trajectories", [])),
        "requests": len(requests),
        "candidates": len(candidates),
        "evaluation_authority": frontier.get("evaluation_authority"),
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
