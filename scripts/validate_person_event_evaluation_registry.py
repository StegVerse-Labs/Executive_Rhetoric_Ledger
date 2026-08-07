#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "coordination" / "person-event-evaluation-registry.json"
STANDARD = ROOT / "standards" / "person-event-current-state-evaluation.v1.md"

ALLOWED_STATES = {"CONFORMING", "PENDING_ADMISSION", "EXEMPT_REVIEWED", "SUPERSEDED"}
REQUIRED_PAGE_SET = {
    "Overview / Current State",
    "Evidence",
    "DPOIs",
    "Chronology & Authority",
    "Analysis",
    "Evidence Gaps",
    "Method",
}


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def main() -> None:
    if not REGISTRY.exists():
        fail(f"missing registry: {REGISTRY.relative_to(ROOT)}")
    if not STANDARD.exists():
        fail(f"missing standard: {STANDARD.relative_to(ROOT)}")

    data = json.loads(REGISTRY.read_text())
    if data.get("schema") != "stegverse.executive_rhetoric_ledger.person_event_evaluation_registry.v1":
        fail("unexpected registry schema")
    if data.get("standard") != "standards/person-event-current-state-evaluation.v1.md":
        fail("registry does not bind canonical standard")

    entries = data.get("entries")
    if not isinstance(entries, list) or not entries:
        fail("registry must contain at least one entry")

    seen = set()
    for entry in entries:
        rid = entry.get("registry_id")
        if not rid or rid in seen:
            fail("registry_id missing or duplicated")
        seen.add(rid)

        state = entry.get("state")
        if state not in ALLOWED_STATES:
            fail(f"{rid}: invalid state {state}")
        if entry.get("evaluation_authority") != "StegVerse-Labs/Executive_Rhetoric_Ledger":
            fail(f"{rid}: ERL must remain evaluation authority")

        if state == "CONFORMING":
            for key in ("consumer_contract", "append_only_update_ledger", "current_state_index"):
                if not entry.get(key):
                    fail(f"{rid}: conforming entry missing {key}")
            if entry.get("reviewed_only") is not True:
                fail(f"{rid}: conforming consumer must be reviewed_only")
            if entry.get("native_record_mutation_authorized") is not False:
                fail(f"{rid}: native mutation must remain false absent separate authority")

        if entry.get("subject_type") == "person_event_cluster" and entry.get("repository") == "StegVerse-Labs/Site":
            pages = set(entry.get("required_pages", []))
            if pages != REQUIRED_PAGE_SET:
                fail(f"{rid}: Site cluster page set is incomplete")
            if entry.get("home_page_evidence_update_ledger_required") is not True:
                fail(f"{rid}: Site cluster must require home-page Evidence Update Ledger")
            if entry.get("public_no_update_state_required") is not True:
                fail(f"{rid}: Site cluster must expose NO UPDATE")
            if state == "PENDING_ADMISSION" and not entry.get("release_condition"):
                fail(f"{rid}: pending Site admission requires release condition")

    print(f"PASS: validated {len(entries)} person/event evaluation registry entries")


if __name__ == "__main__":
    main()
