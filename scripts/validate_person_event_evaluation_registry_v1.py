#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "coordination" / "person-event-evaluation-registry.v1.json"
STANDARD = ROOT / "standards" / "person-event-current-state-evaluation.v1.md"
ALLOWED_STATES = {"CONFORMING", "PENDING_ADMISSION", "EXEMPT_REVIEWED", "SUPERSEDED"}
REQUIRED_PAGES = {
    "Overview / Current State", "Evidence", "DPOIs", "Chronology & Authority",
    "Analysis", "Evidence Gaps", "Method"
}

def fail(message):
    raise SystemExit(f"FAIL: {message}")

def main():
    if not REGISTRY.exists() or not STANDARD.exists():
        fail("canonical standard/registry missing")
    data = json.loads(REGISTRY.read_text())
    if data.get("schema") != "stegverse.executive_rhetoric_ledger.person_event_evaluation_registry.v1":
        fail("unexpected schema")
    if data.get("standard") != "standards/person-event-current-state-evaluation.v1.md":
        fail("registry not bound to canonical standard")
    entries = data.get("entries") or []
    if not entries:
        fail("registry must contain entries")
    ids = set()
    for e in entries:
        rid = e.get("registry_id")
        if not rid or rid in ids:
            fail("missing/duplicate registry_id")
        ids.add(rid)
        if e.get("state") not in ALLOWED_STATES:
            fail(f"{rid}: invalid state")
        if e.get("evaluation_authority") != "StegVerse-Labs/Executive_Rhetoric_Ledger":
            fail(f"{rid}: ERL evaluation authority missing")
        if e.get("state") == "CONFORMING":
            for key in ("consumer_contract", "append_only_update_ledger", "current_state_index"):
                if not e.get(key):
                    fail(f"{rid}: missing {key}")
            if e.get("reviewed_only") is not True or e.get("native_record_mutation_authorized") is not False:
                fail(f"{rid}: consumer authority boundary invalid")
        if e.get("repository") == "StegVerse-Labs/Site":
            if set(e.get("required_pages", [])) != REQUIRED_PAGES:
                fail(f"{rid}: Site page cluster incomplete")
            if e.get("home_page_evidence_update_ledger_required") is not True:
                fail(f"{rid}: home ledger required")
            if e.get("public_no_update_state_required") is not True:
                fail(f"{rid}: NO UPDATE visibility required")
            if e.get("state") == "PENDING_ADMISSION" and not e.get("site_candidate_issue"):
                fail(f"{rid}: pending Site workload needs durable issue")
    print(f"PASS: {len(entries)} person/event evaluation registry entries")

if __name__ == "__main__":
    main()
