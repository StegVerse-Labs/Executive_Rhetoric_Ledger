import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
COMMIT_1 = "1" * 40
COMMIT_2 = "2" * 40


def load_module():
    path = ROOT / "scripts" / "intake_trumpality_research_candidates.py"
    spec = importlib.util.spec_from_file_location("trumpality_intake", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def receipt(rid, request, result, digest="h1"):
    return {"receipt_id": rid, "request_id": request, "trajectory_ids": ["melania-token-preannouncement-wallets"],
            "source_scanned": "https://fixture.local/feed", "result": result, "response_hash": digest}


def candidate(cid, pointer="R1", digest="h1", **overrides):
    row = {
        "schema": "stegverse.erl.research_source_candidate.v1",
        "candidate_id": cid,
        "repository": "StegVerse-Labs/Trumpality",
        "trajectory_ids": ["melania-token-preannouncement-wallets"],
        "acquisition_request_id": "REQ-1",
        "query": "announcement timestamp",
        "source_url": f"https://fixture.local/{cid}",
        "source_title": cid,
        "listing_response_sha256": digest,
        "custody_pointer": pointer,
        "verification_state": "UNVERIFIED",
        "evidence_role": "lead-only",
        "native_records_mutated": False,
        "evaluation_changed": False,
        "transport": {"destination_repository": "StegVerse-Labs/Executive_Rhetoric_Ledger",
                      "authority_effect": "NONE", "github_token_authority": "NONE"},
    }
    row.update(overrides)
    return row


def write_producer(base: Path, candidates, receipts):
    research = base / "research"
    research.mkdir(parents=True, exist_ok=True)
    (research / "source_candidates.jsonl").write_text("".join(json.dumps(c) + "\n" for c in candidates))
    (research / "research_receipts.jsonl").write_text("".join(json.dumps(r) + "\n" for r in receipts))
    (research / "frontier.json").write_text(json.dumps({"trajectories": [
        {"id": "melania-token-preannouncement-wallets", "state": "ACTIVE"},
        {"id": "wlf-positive-adoption-radar", "state": "ACTIVE"},
    ]}))


@pytest.fixture
def erl(tmp_path):
    root = tmp_path / "erl"
    doc = root / "research-candidates/2026-08-21-trump-family-crypto-rhetoric-market-impact.md"
    doc.parent.mkdir(parents=True)
    doc.write_text("## Lane J — Trumpality mapping\n\n1. `melania-token-preannouncement-wallets`\n\n## Next\n")
    return root


def test_two_cycles_append_only_with_provenance_and_nulls(erl, tmp_path):
    mod = load_module()
    p1 = tmp_path / "p1"
    write_producer(p1, [candidate("C1")], [receipt("R1", "REQ-1", "CANDIDATES_IDENTIFIED"), receipt("R0", "REQ-2", "NO_UPDATE")])
    first = mod.intake(erl, COMMIT_1, p1)
    assert (first["accepted"], first["quarantined"], first["scan_records_added"]) == (1, 0, 2)
    before = (erl / mod.PENDING).read_bytes()

    p2 = tmp_path / "p2"
    write_producer(p2, [candidate("C1"), candidate("C2", pointer="R2", digest="h2")],
                   [receipt("R1", "REQ-1", "CANDIDATES_IDENTIFIED"), receipt("R0", "REQ-2", "NO_UPDATE"),
                    receipt("R2", "REQ-1", "CANDIDATES_IDENTIFIED", "h2")])
    second = mod.intake(erl, COMMIT_2, p2)
    assert (second["accepted"], second["duplicates"], second["scan_records_added"]) == (1, 1, 1)
    assert (erl / mod.PENDING).read_bytes().startswith(before)

    rb = mod.readback(erl)
    assert rb["intake_cycles"] == 2 and rb["append_only_verified"] is True
    lane = rb["trajectories"]["melania-token-preannouncement-wallets"]
    assert [c["candidate_id"] for c in lane["pending_candidates"]] == ["C1", "C2"]
    assert {c["producer_commit"] for c in lane["pending_candidates"]} == {COMMIT_1, COMMIT_2}
    assert lane["scan_results"] == {"CANDIDATES_IDENTIFIED": 2, "NO_UPDATE": 1}
    assert lane["movement"] == "no-update" and rb["finding_authorized"] is False
    accepted = [json.loads(x) for x in (erl / mod.PENDING).read_text().splitlines()]
    assert all(c["erl_intake"]["review_status"] == "PENDING_REVIEW" for c in accepted)
    assert accepted[0]["erl_intake"]["erl_lane_mapped_trajectories"] == ["melania-token-preannouncement-wallets"]


def test_missing_provenance_and_authority_violations_quarantine(erl, tmp_path):
    mod = load_module()
    p = tmp_path / "p"
    write_producer(p, [
        candidate("NOPTR", pointer="MISSING"),
        candidate("BADHASH", digest="other"),
        candidate("PROMOTED", verification_state="VERIFIED"),
        candidate("TOKEN", transport={"destination_repository": "StegVerse-Labs/Executive_Rhetoric_Ledger",
                                      "authority_effect": "NONE", "github_token_authority": "WRITE"}),
        candidate("UNKNOWNT", trajectory_ids=["not-in-frontier"]),
    ], [receipt("R1", "REQ-1", "CANDIDATES_IDENTIFIED")])
    result = mod.intake(erl, COMMIT_1, p)
    assert result["accepted"] == 0 and result["quarantined"] == 5
    q = {row["candidate_id"]: row["errors"] for row in map(json.loads, (erl / mod.QUARANTINE).read_text().splitlines())}
    assert q["NOPTR"] == ["custody_pointer:unresolved"]
    assert q["BADHASH"] == ["custody_pointer:hash_mismatch"]
    assert any(e.startswith("verification_state") for e in q["PROMOTED"])
    assert q["TOKEN"] == ["transport.authority"]
    assert q["UNKNOWNT"][0].startswith("trajectory_ids:not_active_in_producer_frontier")
    # Re-running the same producer commit must not duplicate quarantine records.
    mod.intake(erl, COMMIT_1, p)
    assert len((erl / mod.QUARANTINE).read_text().splitlines()) == 5


def test_unpinned_commit_and_rewritten_history_fail_closed(erl, tmp_path):
    mod = load_module()
    with pytest.raises(SystemExit, match="FAIL_CLOSED"):
        mod.intake(erl, "main", None)
    p = tmp_path / "p"
    write_producer(p, [candidate("C1")], [receipt("R1", "REQ-1", "CANDIDATES_IDENTIFIED")])
    mod.intake(erl, COMMIT_1, p)
    (erl / mod.PENDING).write_text("{}\n")
    with pytest.raises(SystemExit, match="diverges"):
        mod.readback(erl)
