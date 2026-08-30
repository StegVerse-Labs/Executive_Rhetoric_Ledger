#!/usr/bin/env python3
"""Validate bounded per-question authority assignments for the Fauci/HSGAC ledger."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "assessments" / "silence-causation"
LEDGER = BASE / "2026-07-29-fauci-hsgac-atomic-question-ledger.partial.json"
REGISTRY = BASE / "2026-07-29-fauci-hsgac-authority-source-registry.json"
ASSIGNMENTS = BASE / "2026-07-29-fauci-hsgac-authority-assignment.partial.json"

def fail(errors: list[str]) -> int:
    for error in errors:
        print(f"FAIL authority-assignment: {error}", file=sys.stderr)
    return 1

def main() -> int:
    ledger = json.loads(LEDGER.read_text())
    registry = json.loads(REGISTRY.read_text())
    data = json.loads(ASSIGNMENTS.read_text())
    errors: list[str] = []

    ledger_ids = {r["atomic_id"] for r in ledger["records"]}
    source_ids = {s["source_id"] for s in registry["sources"]}
    assigned: list[str] = []

    if data.get("state") not in {"ACTIVE_PARTIAL_NON_PROMOTIONAL","COMPLETE_NON_PROMOTIONAL"}:
        errors.append("assignment state must remain non-promotional")

    for group in data.get("assignments", []):
        ids = group.get("atomic_ids", [])
        if not ids:
            errors.append("assignment group missing atomic_ids")
            continue
        for aq in ids:
            if aq not in ledger_ids:
                errors.append(f"unknown atomic id {aq}")
            if aq in assigned:
                errors.append(f"duplicate authority assignment for {aq}")
            assigned.append(aq)
        for src in group.get("source_ids", []):
            if src not in source_ids:
                errors.append(f"unknown authority source {src}")

        domain = group.get("authority_domain")
        holder = str(group.get("formal_authority_holder_class",""))
        exact = group.get("exact_holder_state")
        if domain == "NIH_GRANT_OBLIGATION":
            if "Grants Management Officer" not in holder:
                errors.append("NIH grant obligation authority must resolve to award-specific GMO class")
            if exact != "PENDING_AWARD_SPECIFIC_NOTICE_OF_AWARD":
                errors.append("grant exact holder must remain pending until award-specific Notice of Award")
            if "Fauci" in holder:
                errors.append("Fauci cannot be asserted as sole NIH legal obligation authority without award-specific primary record")
        if domain == "PRESIDENTIAL_PARDON":
            if holder != "President of the United States":
                errors.append("formal pardon authority must be President of the United States")
        if group.get("factual_event_established") is True and domain != "NOT_APPLICABLE":
            errors.append(f"{domain}: authority mapping must not establish the questioned event")

    if len(assigned) != len(set(assigned)):
        errors.append("authority assignment IDs must be unique")

    coverage = data.get("coverage", {})
    if coverage.get("atomic_ids_assigned") != len(assigned):
        errors.append("coverage.atomic_ids_assigned does not match assigned count")
    if coverage.get("atomic_total") != len(ledger_ids):
        errors.append("coverage.atomic_total does not match ledger total")
    if coverage.get("coverage_complete") is True and set(assigned) != ledger_ids:
        errors.append("coverage_complete=true requires every ledger atomic id assigned")

    boundary = str(data.get("promotion_boundary","")).lower()
    for concept in ("motive","culpability","legal","publication"):
        if concept not in boundary:
            errors.append(f"promotion boundary must mention {concept}")

    if errors:
        return fail(errors)

    print(f"PASS authority assignments: {len(assigned)}/{len(ledger_ids)} atomics")
    print("PASS NIH grant obligation boundary: GMO/NoA preserved")
    print("PASS pardon boundary: presidential grant authority preserved")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
