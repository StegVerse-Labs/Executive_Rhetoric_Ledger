#!/usr/bin/env python3
"""Reconcile producer chronology, acknowledgment consumption, and reviewed-output eligibility.

This process may verify mechanical completion and identify reviewed-only eligibility. It may
not approve review, promote candidates, or publish unresolved producer records.
"""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HEALTH = ROOT / "producer_intake/producer-health.json"
RESULTS = ROOT / "producer_intake/results"
ACKS = ROOT / "producer_intake/acknowledgments"
REVIEW = ROOT / "producer_intake/review-queue"
REVIEWED = ROOT / "reviewed_receipts"
OUTPUT = ROOT / "producer_intake/completion-state.json"


def generated_at() -> str:
    value = os.environ.get("RECONCILIATION_TIME")
    return value or datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def load_many(root: Path, pattern: str) -> list[dict]:
    documents = []
    if not root.exists():
        return documents
    for path in sorted(root.rglob(pattern)):
        try:
            documents.append(json.loads(path.read_text(encoding="utf-8")))
        except Exception:
            continue
    return documents


def chronology_state(rows: list[dict]) -> str:
    if not rows:
        return "empty"
    ids = {row.get("intake_id") for row in rows}
    edges: dict[str, set[str]] = {item: set() for item in ids if item}
    unresolved = False
    for row in rows:
        source = row.get("intake_id")
        chronology = row.get("chronology") or {}
        for key in ("supersedes", "corrects"):
            target = chronology.get(key)
            if not target:
                continue
            if target not in ids:
                unresolved = True
            elif source:
                edges.setdefault(source, set()).add(target)
    visiting: set[str] = set()
    visited: set[str] = set()

    def cyclic(node: str) -> bool:
        if node in visiting:
            return True
        if node in visited:
            return False
        visiting.add(node)
        for target in edges.get(node, set()):
            if cyclic(target):
                return True
        visiting.remove(node)
        visited.add(node)
        return False

    if any(cyclic(node) for node in edges):
        return "cycle-detected"
    return "unresolved-reference" if unresolved else "consistent"


def main() -> int:
    health = json.loads(HEALTH.read_text(encoding="utf-8")) if HEALTH.exists() else {"producers": []}
    results = load_many(RESULTS, "ERL-INTAKE-*.json")
    acknowledgments = load_many(ACKS, "*.json")
    review_packets = load_many(REVIEW, "*.json")
    reviewed = load_many(REVIEWED, "*.json")
    reviewed_ids = {
        value
        for document in reviewed
        for value in (document.get("intake_id"), document.get("source_intake_id"))
        if value
    }

    producer_rows = []
    eligibility = []
    repositories = sorted({row.get("repository") for row in health.get("producers", []) if row.get("repository")} | {row.get("producer_repository") for row in results if row.get("producer_repository")})
    for repository in repositories:
        producer_results = [row for row in results if row.get("producer_repository") == repository]
        producer_acks = [row for row in acknowledgments if row.get("producer_repository") == repository]
        producer_packets = [row for row in review_packets if row.get("producer_repository") == repository]
        health_row = next((row for row in health.get("producers", []) if row.get("repository") == repository), {})
        state = chronology_state(producer_results)
        seen = len(producer_results)
        acknowledged = len({row.get("intake_id") for row in producer_acks if row.get("intake_id")})
        routed = len({row.get("intake_result") for row in producer_packets if row.get("intake_result")})
        ack_state = "none" if acknowledged == 0 else ("complete" if acknowledged >= seen else "available")
        capability_complete = bool(health_row.get("status") == "healthy" and state in {"empty", "consistent"} and acknowledged >= seen and routed >= sum(1 for row in producer_results if row.get("status") == "review-required"))
        producer_rows.append({
            "repository": repository,
            "manifest_live": health_row.get("status") in {"healthy", "quarantined"},
            "records_seen": seen,
            "records_acknowledged": acknowledged,
            "records_review_routed": routed,
            "chronology_state": state,
            "acknowledgment_consumption": ack_state,
            "capability_complete": capability_complete,
        })
        for row in producer_results:
            intake_id = row.get("intake_id")
            is_reviewed = intake_id in reviewed_ids
            eligibility.append({
                "intake_id": intake_id,
                "producer_repository": repository,
                "status": "eligible-reviewed-only" if is_reviewed else "ineligible-unreviewed",
                "reason": "durable reviewed receipt found" if is_reviewed else "pending final evidentiary review; automation cannot approve",
            })

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps({
        "generated_at": generated_at(),
        "producers": producer_rows,
        "reviewed_output_eligibility": sorted(eligibility, key=lambda row: (row["producer_repository"], row["intake_id"] or "")),
        "authority": {
            "may_reconcile_chronology": True,
            "may_record_ack_consumption": True,
            "may_mark_reviewed_eligibility": True,
            "may_approve_review": False,
            "may_promote": False,
            "may_publish": False,
        },
    }, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Reconciled completion state for {len(producer_rows)} producers")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
