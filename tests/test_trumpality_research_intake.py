import importlib.util
import hashlib
import io
import json
import tempfile
import unittest
from unittest import mock
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

    def segment_producer(self, root, split=1):
        legacy = root / "research/research_receipts.jsonl"
        lines = legacy.read_bytes().splitlines(keepends=True)
        directory = root / "research/research_receipts"
        directory.mkdir()
        (directory / "research_receipts-000000.jsonl").write_bytes(b"".join(lines[:split]))
        (directory / "research_receipts-000001.jsonl").write_bytes(b"".join(lines[split:]))
        legacy.unlink()
        return directory

    def test_legacy_to_segments_preserves_intake_hashes_and_retry_idempotency(self):
        p = self.tmp / "producer"
        write_producer(p, [candidate("C1")], [receipt("R1", "REQ-1", "CANDIDATES_IDENTIFIED")])
        first = self.mod.intake(self.erl, COMMIT_1, p)
        prior = (self.erl / self.mod.PENDING).read_bytes()
        write_producer(p, [candidate("C1"), candidate("C2", pointer="R2")], [
            receipt("R1", "REQ-1", "CANDIDATES_IDENTIFIED"), receipt("R2", "REQ-1", "CANDIDATES_IDENTIFIED"),
            receipt("R0", "REQ-2", "NO_UPDATE")])
        logical = (p / "research/research_receipts.jsonl").read_bytes()
        self.segment_producer(p)
        second = self.mod.intake(self.erl, COMMIT_2, p)
        retry = self.mod.intake(self.erl, COMMIT_2, p)
        self.assertEqual((second["accepted"], second["scan_records_added"]), (1, 2))
        self.assertEqual((retry["accepted"], retry["duplicates"], retry["scan_records_added"]), (0, 2, 0))
        self.assertEqual(second["producer_files_sha256"]["receipts"], hashlib.sha256(logical).hexdigest())
        self.assertEqual([e["rows"] for e in second["producer_receipt_segments"]], [1, 2])
        self.assertTrue((self.erl / self.mod.PENDING).read_bytes().startswith(prior))
        self.assertEqual(first["producer_receipt_segments"][0]["path"], "research/research_receipts.jsonl")
        rb = self.mod.readback(self.erl)
        self.assertEqual((rb["pending_candidate_count"], rb["scan_record_count"]), (2, 3))
        self.assertTrue(rb["append_only_verified"])
        self.assertFalse(rb["finding_authorized"])

    def test_bad_segment_streams_fail_before_intake_effects(self):
        for case in ("gap", "bad_name", "mixed", "missing", "interior_no_lf", "invalid_json", "duplicate_id", "symlink"):
            with self.subTest(case=case):
                p = self.tmp / case
                write_producer(p, [candidate("C1")], [receipt("R1", "REQ-1", "CANDIDATES_IDENTIFIED"), receipt("R0", "REQ-2", "NO_UPDATE")])
                d = self.segment_producer(p)
                first = d / "research_receipts-000000.jsonl"
                last = d / "research_receipts-000001.jsonl"
                if case == "gap": last.rename(d / "research_receipts-000002.jsonl")
                elif case == "bad_name": last.rename(d / "research_receipts-tail.jsonl")
                elif case == "mixed": (p / "research/research_receipts.jsonl").write_bytes(first.read_bytes())
                elif case == "missing": first.unlink(); last.unlink()
                elif case == "interior_no_lf": first.write_bytes(first.read_bytes().rstrip(b"\n"))
                elif case == "invalid_json": last.write_bytes(b"{bad}\n")
                elif case == "duplicate_id": last.write_bytes(first.read_bytes())
                elif case == "symlink": last.unlink(); last.symlink_to(first)
                before = {name: (self.erl / name).read_bytes() if (self.erl / name).exists() else None
                          for name in (self.mod.PENDING, self.mod.SCANS, self.mod.RECEIPTS, self.mod.QUARANTINE)}
                with self.assertRaisesRegex(SystemExit, "FAIL_CLOSED"):
                    self.mod.intake(self.erl, COMMIT_1, p)
                after = {name: (self.erl / name).read_bytes() if (self.erl / name).exists() else None for name in before}
                self.assertEqual(before, after)
                failure = self.dispositions()[-1]
                self.assertFalse(failure["consequence_committed"])
                self.assertTrue(all(failure.get(k) for k in ACTIONABLE))

    def remote_fixture(self):
        parts = {"research/research_receipts/research_receipts-000000.jsonl": b'{"receipt_id":"R1"}\n',
                 "research/research_receipts/research_receipts-000001.jsonl": b'{"receipt_id":"R2"}\n'}
        entries = [{"path": path, "size": len(data), "type": "blob", "mode": "100644",
                    "sha": hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()}
                   for path, data in parts.items()]
        return parts, {"tree": list(reversed(entries)), "truncated": False}

    def remote_read(self, parts, tree, calls):
        def read(request, timeout):
            calls.append(request.full_url)
            if request.full_url == f"https://api.github.com/repos/{self.mod.PRODUCER_REPO}/git/trees/{COMMIT_1}?recursive=1":
                return io.BytesIO(json.dumps(tree).encode())
            prefix = f"https://raw.githubusercontent.com/{self.mod.PRODUCER_REPO}/{COMMIT_1}/"
            self.assertTrue(request.full_url.startswith(prefix))
            return io.BytesIO(parts[request.full_url[len(prefix):]])
        return read

    def test_remote_tree_pins_order_size_and_blob_hash(self):
        parts, tree = self.remote_fixture()
        calls = []
        with mock.patch.object(self.mod.urllib.request, "urlopen", side_effect=self.remote_read(parts, tree, calls)):
            data, manifest = self.mod.fetch_receipts(COMMIT_1, None)
        self.assertEqual(data, b"".join(parts.values()))
        self.assertEqual([e["path"] for e in manifest], list(parts))
        self.assertEqual(len(calls), 3)
        for entry in manifest:
            self.assertEqual(entry["sha256"], hashlib.sha256(parts[entry["path"]]).hexdigest())

    def test_remote_incomplete_or_corrupted_tree_never_fetches_unpinned_data(self):
        for case in ("truncated", "duplicate", "gap", "mixed", "wrong_size", "wrong_hash", "oversized", "symlink_mode"):
            with self.subTest(case=case):
                parts, tree = self.remote_fixture()
                e = tree["tree"][0]
                if case == "truncated": tree["truncated"] = True
                elif case == "duplicate": tree["tree"].append(dict(e))
                elif case == "gap": e["path"] = e["path"].replace("000001", "000002")
                elif case == "mixed": tree["tree"].append({**e, "path": "research/research_receipts.jsonl"})
                elif case == "wrong_size": e["size"] += 1
                elif case == "wrong_hash": e["sha"] = "0" * 40
                elif case == "oversized": e["size"] = self.mod.MAX_RECEIPT_BYTES + 1
                elif case == "symlink_mode": e["mode"] = "120000"
                calls = []
                with mock.patch.object(self.mod.urllib.request, "urlopen", side_effect=self.remote_read(parts, tree, calls)):
                    with self.assertRaises(ValueError): self.mod.fetch_receipts(COMMIT_1, None)

    def test_remote_legacy_file_remains_supported_and_response_is_closed(self):
        path = "research/research_receipts.jsonl"
        data = b'{"receipt_id":"old"}'  # A complete final record need not end with LF.
        parts = {path: data}
        tree = {"truncated": False, "tree": [{"path": path, "type": "blob", "mode": "100644", "size": len(data),
                 "sha": hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()}]}
        handles = []
        reader = self.remote_read(parts, tree, [])
        def read(request, timeout):
            response = reader(request, timeout)
            handles.append(response)
            return response
        with mock.patch.object(self.mod.urllib.request, "urlopen", side_effect=read):
            actual, manifest = self.mod.fetch_receipts(COMMIT_1, None)
        self.assertEqual(actual, data)
        self.assertEqual(manifest[0]["path"], path)
        self.assertTrue(all(h.closed for h in handles))


if __name__ == "__main__":
    unittest.main()
