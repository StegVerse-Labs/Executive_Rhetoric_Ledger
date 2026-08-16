#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "coordination" / "research-candidate-activation-registry.v1.json"
EXPECTED_SCHEMA = "stegverse.executive_rhetoric_ledger.research_candidate_activation_registry.v1"
TERMINAL_STATES = {"PROMOTED", "SUPERSEDED", "MERGED", "CLOSED_WITH_REASON"}


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def repo_candidate_paths() -> set[str]:
    paths = {
        p.relative_to(ROOT).as_posix()
        for p in (ROOT / "research-candidates").glob("*")
        if p.is_file()
    }
    paths.update(
        p.relative_to(ROOT).as_posix()
        for p in (ROOT / "assessments").rglob("*.research-candidate.json")
        if p.is_file()
    )
    return paths


def main() -> None:
    if not REGISTRY.exists():
        fail("research-candidate activation registry missing")

    data = json.loads(REGISTRY.read_text())
    if data.get("schema") != EXPECTED_SCHEMA:
        fail("unexpected registry schema")
    if data.get("repository") != "StegVerse-Labs/Executive_Rhetoric_Ledger":
        fail("registry repository binding invalid")
    if data.get("repository_authority") != "ERL_MIRROR_HANDOFF.md":
        fail("registry must bind to ERL_MIRROR_HANDOFF.md")
    if not data.get("umbrella_issue"):
        fail("umbrella durable issue missing")

    groups = data.get("groups") or []
    if not groups:
        fail("registry must contain candidate groups")

    ids: set[str] = set()
    registered_paths: set[str] = set()
    for group in groups:
        gid = group.get("group_id")
        if not gid or gid in ids:
            fail("missing or duplicate group_id")
        ids.add(gid)

        paths = group.get("candidate_paths") or []
        if not paths:
            fail(f"{gid}: candidate_paths missing")
        for path in paths:
            if path in registered_paths:
                fail(f"{gid}: duplicate candidate path {path}")
            registered_paths.add(path)
            if not (ROOT / path).is_file():
                fail(f"{gid}: candidate path missing: {path}")

        state = group.get("state")
        active = group.get("active")
        if active is True:
            if not group.get("durable_owner"):
                fail(f"{gid}: active group lacks durable_owner")
            if not group.get("next_executable_task"):
                fail(f"{gid}: active group lacks next_executable_task")
            if not group.get("terminal_condition"):
                fail(f"{gid}: active group lacks terminal_condition")
            if group.get("candidate_layer_finding_authorized") is not False:
                fail(f"{gid}: candidate layer cannot authorize a finding")
            if group.get("candidate_layer_publication_authorized") is not False:
                fail(f"{gid}: candidate layer cannot authorize publication")
        else:
            if state not in TERMINAL_STATES:
                fail(f"{gid}: inactive group lacks governed terminal state")
            if not group.get("terminal_reason"):
                fail(f"{gid}: terminal group lacks terminal_reason")

        for artifact in group.get("artifact_paths") or []:
            if not (ROOT / artifact).exists():
                fail(f"{gid}: registered artifact path missing: {artifact}")

    discovered = repo_candidate_paths()
    missing = sorted(discovered - registered_paths)
    stale = sorted(registered_paths - discovered)
    if missing:
        fail("unregistered research candidates: " + ", ".join(missing))
    if stale:
        fail("registry references non-candidate paths: " + ", ".join(stale))

    active_count = sum(1 for group in groups if group.get("active") is True)
    print(
        f"PASS: {len(groups)} research-candidate groups; "
        f"{len(discovered)} candidate files; {active_count} active groups"
    )


if __name__ == "__main__":
    main()
