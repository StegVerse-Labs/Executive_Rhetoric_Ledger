#!/usr/bin/env python3
"""Intake and read back Trumpality research source candidates for an ERL research lane.

Trumpality's ERL adapter (scripts/erl_research_agent.py) appends lead-only
`stegverse.erl.research_source_candidate.v1` packets and per-scan receipts. This
script pulls those files at a pinned Trumpality commit, validates provenance,
and appends accepted candidates to the lane's pending intake file. Nothing here
creates a finding: every accepted candidate stays PENDING_REVIEW with evidence
movement `no-update`, and zero-result scans are recorded as no-update nulls.

Subcommands:
  intake    --producer-commit <40-hex sha> [--source-dir DIR]
  readback  [--output FILE]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import urllib.request
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

PRODUCER_REPO = "StegVerse-Labs/Trumpality"
ERL_REPO = "StegVerse-Labs/Executive_Rhetoric_Ledger"
CANDIDATE_SCHEMA = "stegverse.erl.research_source_candidate.v1"
GROUP_ID = "ERL-RC-TRUMP-FAMILY-CRYPTO-MARKET-2026"
LANE_DOC = Path("research-candidates/2026-08-21-trump-family-crypto-rhetoric-market-impact.md")
LANE_DIR = Path("research-data/trumpality-acquisition") / GROUP_ID
PENDING = LANE_DIR / "pending-candidates.jsonl"
SCANS = LANE_DIR / "scan-ledger.jsonl"
QUARANTINE = LANE_DIR / "quarantine.jsonl"
RECEIPTS = LANE_DIR / "intake-receipts.jsonl"
READBACK = LANE_DIR / "readback.json"
PRODUCER_FILES = {
    "candidates": "research/source_candidates.jsonl",
    "receipts": "research/research_receipts.jsonl",
    "frontier": "research/frontier.json",
}
SHA_RE = re.compile(r"^[0-9a-f]{40}$")


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def parse_jsonl(data: bytes) -> list[dict[str, Any]]:
    return [json.loads(line) for line in data.decode("utf-8").splitlines() if line.strip()]


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return parse_jsonl(path.read_bytes()) if path.exists() else []


def append_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True) + "\n")


def fetch_producer(commit: str, source_dir: Path | None) -> dict[str, bytes]:
    out = {}
    for key, rel in PRODUCER_FILES.items():
        if source_dir is not None:
            out[key] = (source_dir / rel).read_bytes()
        else:
            url = f"https://raw.githubusercontent.com/{PRODUCER_REPO}/{commit}/{rel}"
            request = urllib.request.Request(url, headers={"User-Agent": "StegVerse-ERL-Intake/1.0"})
            out[key] = urllib.request.urlopen(request, timeout=30).read()
    return out


def erl_mapped_trajectories(root: Path) -> set[str]:
    text = (root / LANE_DOC).read_text(encoding="utf-8")
    section = text.split("## Lane J", 1)[1].split("\n## ", 1)[0] if "## Lane J" in text else ""
    return set(re.findall(r"`([a-z0-9-]+)`", section))


def validate(candidate: dict[str, Any], receipts: dict[str, dict[str, Any]], active: set[str]) -> list[str]:
    errors = []
    transport = candidate.get("transport") or {}
    expected = {
        "schema": CANDIDATE_SCHEMA,
        "repository": PRODUCER_REPO,
        "verification_state": "UNVERIFIED",
        "evidence_role": "lead-only",
        "native_records_mutated": False,
        "evaluation_changed": False,
    }
    for key, value in expected.items():
        if candidate.get(key) != value:
            errors.append(f"{key}!={value}")
    if transport.get("destination_repository") != ERL_REPO:
        errors.append("transport.destination_repository")
    if transport.get("authority_effect") != "NONE" or transport.get("github_token_authority") != "NONE":
        errors.append("transport.authority")
    url = candidate.get("source_url") or ""
    if urlsplit(url).scheme not in {"http", "https"} or not urlsplit(url).hostname:
        errors.append("source_url")
    trajectories = candidate.get("trajectory_ids") or []
    if not trajectories:
        errors.append("trajectory_ids:empty")
    unknown = [t for t in trajectories if t not in active]
    if unknown:
        errors.append("trajectory_ids:not_active_in_producer_frontier:" + ",".join(unknown))
    # Provenance: the candidate must point at the scan receipt that produced it.
    receipt = receipts.get(candidate.get("custody_pointer") or "")
    if receipt is None:
        errors.append("custody_pointer:unresolved")
    else:
        if receipt.get("result") != "CANDIDATES_IDENTIFIED":
            errors.append("custody_pointer:receipt_result")
        if receipt.get("request_id") != candidate.get("acquisition_request_id"):
            errors.append("custody_pointer:request_mismatch")
        if not receipt.get("response_hash") or receipt.get("response_hash") != candidate.get("listing_response_sha256"):
            errors.append("custody_pointer:hash_mismatch")
    return errors


def intake(root: Path, commit: str, source_dir: Path | None) -> dict[str, Any]:
    if not SHA_RE.match(commit):
        raise SystemExit("FAIL_CLOSED: --producer-commit must be a full 40-hex commit SHA")
    raw = fetch_producer(commit, source_dir)
    candidates = parse_jsonl(raw["candidates"])
    producer_receipts = parse_jsonl(raw["receipts"])
    frontier = json.loads(raw["frontier"])
    active = {t.get("id") or t.get("trajectory_id") for t in frontier.get("trajectories", []) if t.get("state") in {"OPEN", "ACTIVE"}}
    mapped = erl_mapped_trajectories(root)
    by_receipt = {r.get("receipt_id"): r for r in producer_receipts}

    pending_path, scans_path = root / PENDING, root / SCANS
    before = pending_path.read_bytes() if pending_path.exists() else b""
    known = {row["candidate_id"] for row in parse_jsonl(before)} if before else set()
    quarantined_ids = {row.get("candidate_id") for row in read_jsonl(root / QUARANTINE)}
    known_scans = {row["receipt_id"] for row in read_jsonl(scans_path)}

    provenance = {
        "producer_repository": PRODUCER_REPO,
        "producer_commit": commit,
        "producer_files_sha256": {key: sha256(raw[key]) for key in PRODUCER_FILES},
    }
    accepted, quarantined, duplicates = [], [], 0
    for candidate in candidates:
        cid = candidate.get("candidate_id")
        if cid in known:
            duplicates += 1
            continue
        errors = validate(candidate, by_receipt, active)
        if errors:
            if cid not in quarantined_ids:
                quarantined.append({"candidate_id": cid, "errors": errors, "quarantined_at": now(), **provenance})
                quarantined_ids.add(cid)
            continue
        accepted.append({
            **candidate,
            "erl_intake": {
                **provenance,
                "group_id": GROUP_ID,
                "lane_document": LANE_DOC.as_posix(),
                "erl_lane_mapped_trajectories": sorted(t for t in candidate["trajectory_ids"] if t in mapped),
                "review_status": "PENDING_REVIEW",
                "evidence_movement": "no-update",
                "finding_authorized": False,
                "publication_authorized": False,
                "accepted_at": now(),
            },
        })
        known.add(cid)

    # Null and failed scans are evidence of search coverage, not of absence.
    new_scans = [
        {
            "receipt_id": r["receipt_id"],
            "trajectory_ids": r.get("trajectory_ids", []),
            "request_id": r.get("request_id"),
            "source_scanned": r.get("source_scanned"),
            "result": r.get("result"),
            "response_hash": r.get("response_hash"),
            "retrieved_at": r.get("retrieved_at"),
            "evidence_movement": "no-update",
            "producer_commit": commit,
        }
        for r in producer_receipts
        if r.get("receipt_id") and r["receipt_id"] not in known_scans
    ]

    append_jsonl(pending_path, accepted)
    append_jsonl(root / QUARANTINE, quarantined)
    append_jsonl(scans_path, new_scans)
    after = pending_path.read_bytes() if pending_path.exists() else b""
    if not after.startswith(before):
        raise SystemExit("FAIL_CLOSED: pending candidate history was rewritten")
    receipt = {
        "schema": "stegverse.erl.trumpality_research_intake_receipt.v1",
        "intake_at": now(),
        **provenance,
        "group_id": GROUP_ID,
        "producer_candidates": len(candidates),
        "producer_scan_receipts": len(producer_receipts),
        "accepted": len(accepted),
        "duplicates": duplicates,
        "quarantined": len(quarantined),
        "scan_records_added": len(new_scans),
        "pending_bytes_before": len(before),
        "pending_sha256_before": sha256(before),
        "pending_bytes_after": len(after),
        "pending_sha256_after": sha256(after),
        "disposition": "ALLOW" if candidates or new_scans else "FAIL_CLOSED",
        "finding_authorized": False,
    }
    append_jsonl(root / RECEIPTS, [receipt])
    return receipt


def readback(root: Path) -> dict[str, Any]:
    pending_bytes = (root / PENDING).read_bytes() if (root / PENDING).exists() else b""
    intake_receipts = read_jsonl(root / RECEIPTS)
    if not intake_receipts:
        raise SystemExit("FAIL_CLOSED: no intake receipts to read back")
    # Every recorded intake must still be an exact byte prefix of the current file.
    for r in intake_receipts:
        prefix = pending_bytes[: r["pending_bytes_after"]]
        if len(prefix) != r["pending_bytes_after"] or sha256(prefix) != r["pending_sha256_after"]:
            raise SystemExit(f"FAIL_CLOSED: pending history diverges from intake at {r['producer_commit']}")
    candidates = parse_jsonl(pending_bytes)
    scans = read_jsonl(root / SCANS)
    lanes: dict[str, dict[str, Any]] = defaultdict(lambda: {"pending_candidates": [], "scan_results": Counter()})
    for c in candidates:
        for t in c["trajectory_ids"]:
            lanes[t]["pending_candidates"].append({
                "candidate_id": c["candidate_id"],
                "source_url": c["source_url"],
                "source_title": c.get("source_title"),
                "query": c.get("query"),
                "custody_pointer": c.get("custody_pointer"),
                "producer_commit": c["erl_intake"]["producer_commit"],
                "review_status": c["erl_intake"]["review_status"],
            })
    for s in scans:
        for t in s.get("trajectory_ids", []):
            lanes[t]["scan_results"][s.get("result") or "UNKNOWN"] += 1
    trajectories = {}
    for t, lane in sorted(lanes.items()):
        results = dict(lane["scan_results"])
        trajectories[t] = {
            "pending_candidate_count": len(lane["pending_candidates"]),
            "pending_candidates": lane["pending_candidates"],
            "scan_results": results,
            # A trajectory with scans and no leads is a recorded null, not a refutation.
            "movement": "no-update",
            "null_scan_only": not lane["pending_candidates"] and bool(results),
        }
    return {
        "schema": "stegverse.erl.trumpality_research_readback.v1",
        "group_id": GROUP_ID,
        "producer_commits": [r["producer_commit"] for r in intake_receipts],
        "intake_cycles": len(intake_receipts),
        "pending_candidate_count": len(candidates),
        "scan_record_count": len(scans),
        "pending_sha256": sha256(pending_bytes),
        "append_only_verified": True,
        "trajectories": trajectories,
        "finding_authorized": False,
        "publication_authorized": False,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", type=Path, default=Path("."))
    sub = parser.add_subparsers(dest="command", required=True)
    p_in = sub.add_parser("intake")
    p_in.add_argument("--producer-commit", required=True)
    p_in.add_argument("--source-dir", type=Path)
    p_rb = sub.add_parser("readback")
    p_rb.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    root = args.root.resolve()
    if args.command == "intake":
        result = intake(root, args.producer_commit, args.source_dir)
    else:
        result = readback(root)
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    summary = {k: v for k, v in result.items() if k != "trajectories"}
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
