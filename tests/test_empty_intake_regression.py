"""Regression controls: zero eligible sources must leave an honest gap receipt."""
import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from run_us_china_ai_summit_research import run

class EmptyIntakeRegression(unittest.TestCase):
    def setUp(self):
        self.queue = json.loads((ROOT / "config/us-china-ai-summit-source-queue.v1.json").read_text())

    def no_fetch(self, *args):
        raise AssertionError("No request may occur for an empty eligible plan")

    def check_gap(self, result):
        self.assertEqual(result["execution_state"], "ACQUISITION_NOT_ATTEMPTED_NO_ELIGIBLE_SOURCES")
        self.assertEqual(result["coverage_state"], "NOT_SCANNED")
        self.assertEqual(result["source_attempted_count"], 0)
        self.assertEqual(result["source_captured_count"], 0)
        self.assertEqual(result["source_unavailable_count"], 0)
        self.assertEqual(result["no_result_effect"], "no-update")
        self.assertEqual(result["items"], [])
        for key in ("finding_authorized", "publication_authorized", "original_intr_receipts_observed", "mykv_persistence_verified"):
            self.assertIs(result[key], False)

    def test_empty_queue_preserves_gap(self):
        self.queue["items"] = []
        with tempfile.TemporaryDirectory() as temp:
            self.check_gap(run(Path(temp), self.queue, "2026-10-29T05:18:58Z", fetch=self.no_fetch))

    def test_all_ineligible_preserves_gap(self):
        for item in self.queue["items"]:
            item["state"] = "REVIEW_REQUIRED"
        with tempfile.TemporaryDirectory() as temp:
            result = run(Path(temp), self.queue, "2026-10-29T05:18:58Z", fetch=self.no_fetch)
        self.check_gap(result)
        self.assertEqual(result["source_skipped_count"], len(self.queue["items"]))

    def test_cli_writes_gap_then_returns_nonzero(self):
        self.queue["items"] = []
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            queue = root / "queue.json"
            queue.write_text(json.dumps(self.queue))
            report = root / "cycle.json"
            report.write_text('{"execution_state":"STALE_PRIOR_SUCCESS"}')
            proc = subprocess.run([sys.executable, str(ROOT / "scripts/run_us_china_ai_summit_research.py"),
                "--root", str(root), "--queue", str(queue), "--report", str(report),
                "--timestamp", "2026-10-29T05:18:58Z"], capture_output=True, text=True)
            self.assertEqual(proc.returncode, 2)
            self.check_gap(json.loads(report.read_text()))
            self.assertEqual(json.loads(proc.stdout)["execution_state"], "ACQUISITION_NOT_ATTEMPTED_NO_ELIGIBLE_SOURCES")

    def test_eligible_failed_attempt_is_not_unscanned(self):
        self.queue["items"] = self.queue["items"][:1]
        def unavailable(*args):
            raise RuntimeError("fixture source unavailable")
        with tempfile.TemporaryDirectory() as temp:
            result = run(Path(temp), self.queue, "2026-10-29T05:18:58Z", fetch=unavailable)
        self.assertEqual(result["source_attempted_count"], 1)
        self.assertEqual(result["source_unavailable_count"], 1)
        self.assertEqual(result["execution_state"], "ACQUISITION_CYCLE_COMPLETED_WITH_SOURCE_FAILURES")
        self.assertEqual(result["coverage_state"], "BOUNDED_CONFIGURED_URL_ATTEMPTS")
        self.assertTrue(result["items"][0]["retry_eligible"])

    def test_invalid_authority_is_still_rejected(self):
        self.queue["items"] = []
        self.queue["publication_authority"] = "AUTO"
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaises(ValueError):
                run(Path(temp), self.queue, "2026-10-29T05:18:58Z", fetch=self.no_fetch)
