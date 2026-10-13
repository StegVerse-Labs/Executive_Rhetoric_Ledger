import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMIT_1 = "1" * 40
COMMIT_2 = "2" * 40
ACTIONABLE = ("failure_code", "failed_predicate", "required_evidence_or_repair", "retry_entrypoint", "owning_existing_goal", "next_attempt")


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


class TrumpalityIntakeTest(unittest.TestCase):
    def setUp(self):
        self.mod = load_module()
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.erl = self.tmp / "erl"
        doc = self.erl / "research-candidates/2026-08-21-trump-family-crypto-rhetoric-market-impact.md"
        doc.parent.mkdir(parents=True)
        doc.write_text("## Lane J — Trumpality mapping\n\n1. `melania-token-preannouncement-wallets`\n\n## Next\n")

    def tearDown(self):
        self._tmp.cleanup()

    def dispositions(self):
        return [json.loads(x) for x in (self.erl / self.mod.DISPOSITIONS).read_text().splitlines()]

    def test_two_cycles_append_only_with_provenance_and_nulls(self):
        mod, erl = self.mod, self.erl
        p1 = self.tmp / "p1"
        write_producer(p1, [candidate("C1")], [receipt("R1", "REQ-1", "CANDIDATES_IDENTIFIED"), receipt("R0", "REQ-2", "NO_UPDATE")])
        first = mod.intake(erl, COMMIT_1, p1)
        self.assertEqual((first["accepted"], first["quarantined"], first["scan_records_added"]), (1, 0, 2))
        before = (erl / mod.PENDING).read_bytes()

        p2 = self.tmp / "p2"
        write_producer(p2, [candidate("C1"), candidate("C2", pointer="R2", digest="h2")],
                       [receipt("R1", "REQ-1", "CANDIDATES_IDENTIFIED"), receipt("R0", "REQ-2", "NO_UPDATE"),
                        receipt("R2", "REQ-1", "CANDIDATES_IDENTIFIED", "h2")])
        second = mod.intake(erl, COMMIT_2, p2)
        self.assertEqual((second["accepted"], second["duplicates"], second["scan_records_added"]), (1, 1, 1))
        self.assertTrue((erl / mod.PENDING).read_bytes().startswith(before))

        rb = mod.readback(erl)
        self.assertEqual(rb["intake_cycles"], 2)
        self.assertTrue(rb["append_only_verified"])
        lane = rb["trajectories"]["melania-token-preannouncement-wallets"]
        self.assertEqual([c["candidate_id"] for c in lane["pending_candidates"]], ["C1", "C2"])
        self.assertEqual({c["producer_commit"] for c in lane["pending_candidates"]}, {COMMIT_1, COMMIT_2})
        self.assertEqual(lane["scan_results"], {"CANDIDATES_IDENTIFIED": 2, "NO_UPDATE": 1})
        self.assertEqual(lane["movement"], "no-update")
        self.assertFalse(rb["finding_authorized"])
        accepted = [json.loads(x) for x in (erl / mod.PENDING).read_text().splitlines()]
        self.assertTrue(all(c["erl_intake"]["review_status"] == "PENDING_REVIEW" for c in accepted))
        self.assertEqual(accepted[0]["erl_intake"]["erl_lane_mapped_trajectories"], ["melania-token-preannouncement-wallets"])

        d = self.dispositions()
        self.assertEqual([x["disposition"] for x in d], ["ALLOW", "ALLOW", "ALLOW"])
        # Each intake ALLOW chains: the second predecessor is the first successor.
        self.assertEqual(d[1]["predecessor"]["pending_sha256"], d[0]["successor"]["pending_sha256"])
        self.assertEqual(d[2]["requested_action"], "READ_BACK_LANE_EVIDENCE")

    def test_missing_provenance_and_authority_violations_quarantine(self):
        mod, erl = self.mod, self.erl
        p = self.tmp / "p"
        write_producer(p, [
            candidate("NOPTR", pointer="MISSING"),
            candidate("BADHASH", digest="other"),
            candidate("PROMOTED", verification_state="VERIFIED"),
            candidate("TOKEN", transport={"destination_repository": "StegVerse-Labs/Executive_Rhetoric_Ledger",
                                          "authority_effect": "NONE", "github_token_authority": "WRITE"}),
            candidate("UNKNOWNT", trajectory_ids=["not-in-frontier"]),
        ], [receipt("R1", "REQ-1", "CANDIDATES_IDENTIFIED")])
        result = mod.intake(erl, COMMIT_1, p)
        self.assertEqual((result["accepted"], result["quarantined"]), (0, 5))
        q = {row["candidate_id"]: row["errors"] for row in map(json.loads, (erl / mod.QUARANTINE).read_text().splitlines())}
        self.assertEqual(q["NOPTR"], ["custody_pointer:unresolved"])
        self.assertEqual(q["BADHASH"], ["custody_pointer:hash_mismatch"])
        self.assertTrue(any(e.startswith("verification_state") for e in q["PROMOTED"]))
        self.assertEqual(q["TOKEN"], ["transport.authority"])
        self.assertTrue(q["UNKNOWNT"][0].startswith("trajectory_ids:not_active_in_producer_frontier"))
        # Re-running the same producer commit must not duplicate quarantine records.
        mod.intake(erl, COMMIT_1, p)
        self.assertEqual(len((erl / mod.QUARANTINE).read_text().splitlines()), 5)

    def test_failures_are_actionable_fail_closed_transitions(self):
        mod, erl = self.mod, self.erl
        with self.assertRaisesRegex(SystemExit, "FAIL_CLOSED"):
            mod.intake(erl, "main", None)
        with self.assertRaisesRegex(SystemExit, "FAIL_CLOSED"):
            mod.intake(erl, COMMIT_1, self.tmp / "absent")
        with self.assertRaisesRegex(SystemExit, "FAIL_CLOSED"):
            mod.readback(erl)
        p = self.tmp / "p"
        write_producer(p, [candidate("C1")], [receipt("R1", "REQ-1", "CANDIDATES_IDENTIFIED")])
        mod.intake(erl, COMMIT_1, p)
        (erl / mod.PENDING).write_text("{}\n")
        with self.assertRaisesRegex(SystemExit, "diverges"):
            mod.readback(erl)
        failed = [x for x in self.dispositions() if x["disposition"] == "FAIL_CLOSED"]
        self.assertEqual([x["failure_code"] for x in failed],
                         ["PRODUCER_COMMIT_NOT_PINNED", "PRODUCER_FETCH_FAILED", "NO_INTAKE_RECEIPTS", "PENDING_HISTORY_DIVERGED"])
        for record in failed:
            self.assertFalse(record["consequence_committed"])
            self.assertTrue(all(record.get(k) for k in ACTIONABLE), record)


if __name__ == "__main__":
    unittest.main()
