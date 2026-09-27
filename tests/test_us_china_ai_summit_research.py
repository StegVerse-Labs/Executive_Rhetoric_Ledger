"""Regression tests for autonomous, nonauthorizing ERL summit research acquisition."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from run_us_china_ai_summit_research import GROUP, evaluate, run  # noqa: E402


class SummitResearchTest(unittest.TestCase):
    def setUp(self):
        self.queue = json.loads((ROOT / "config/us-china-ai-summit-source-queue.v1.json").read_text())
        self.timestamp = "2026-09-27T20:00:00Z"

    def test_all_six_live_configured_sources_are_executable(self):
        self.assertEqual(self.queue["lane_id"], GROUP)
        self.assertGreaterEqual(len(self.queue["items"]), 8)
        self.assertTrue(all(x["state"] == "READY" and x["url"].startswith("https://") for x in self.queue["items"]))
        self.assertEqual(self.queue["credential_requirement"], "NONE")
        self.assertEqual(self.queue["finding_authority"], "NONE")

    def test_acquires_sources_and_produces_source_bound_candidates(self):
        def fetch(url, allowed_hosts, timeout):
            self.assertIn(url.split("/")[2], allowed_hosts)
            return (b"<html><body>The two countries established the U.S.-China Super Intelligence (SI) Dialogue to exchange views. They agreed to establish a bilateral communication channel for SI incidents.</body></html>", url, "text/html")
        with tempfile.TemporaryDirectory() as tmp:
            result = run(Path(tmp), self.queue, self.timestamp, fetch=fetch)
            self.assertEqual(result["source_captured_count"], len(self.queue["items"]))
            self.assertEqual(result["source_unavailable_count"], 0)
            self.assertFalse(result["finding_authorized"])
            self.assertFalse(result["publication_authorized"])
            self.assertFalse(result["mykv_persistence_verified"])
            incident = next(x for x in result["items"] if x["lane"] == "INCIDENT")
            self.assertTrue(any(x["state"] == "SOURCE_TEXT_MATCH_REVIEW_REQUIRED" for x in incident["proposition_candidates"]))
            for item in result["items"]:
                path = Path(tmp) / item["source_capture_path"]
                self.assertTrue(path.exists())
                import hashlib
                self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), item["source_sha256"])

    def test_one_http_failure_does_not_suppress_other_sources(self):
        first = self.queue["items"][0]["url"]
        def fetch(url, allowed_hosts, timeout):
            if url == first:
                raise RuntimeError("HTTP 503")
            return (b"<html>State visit on September 24, 2026.</html>", url, "text/html")
        with tempfile.TemporaryDirectory() as tmp:
            result = run(Path(tmp), self.queue, self.timestamp, fetch=fetch)
            self.assertEqual(result["source_unavailable_count"], 1)
            self.assertEqual(result["source_captured_count"], len(self.queue["items"]) - 1)
            self.assertEqual(result["items"][0]["acquisition_state"], "SOURCE_UNAVAILABLE")
            self.assertTrue(result["items"][0]["retry_eligible"])
            self.assertEqual(result["execution_state"], "ACQUISITION_CYCLE_COMPLETED_WITH_SOURCE_FAILURES")

    def test_chinese_primary_language_does_not_depend_on_english_translation(self):
        original = "双方同意建立中美人工智能对话，交流人工智能相关风险和惠益。双方同意建立人工智能事件的沟通渠道。"
        propositions = evaluate(original, "INCIDENT")
        hit = {x["proposition_id"] for x in propositions if x["state"] == "SOURCE_TEXT_MATCH_REVIEW_REQUIRED"}
        self.assertIn("PRC-CHINESE-AI-DIALOGUE", hit)
        self.assertIn("PRC-CHINESE-INCIDENT-CHANNEL", hit)
        self.assertFalse(any(x["interpretation_authorized"] for x in propositions))

    def test_security_and_unverified_claim_boundaries(self):
        bad = dict(self.queue)
        bad["finding_authority"] = "AUTO"
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                run(Path(tmp), bad, self.timestamp, fetch=lambda *args: None)
        candidates = evaluate("This document says nothing about any agreement.", "INCIDENT")
        self.assertTrue(candidates)
        self.assertTrue(all(x["state"] == "NO_MATCH_IN_CAPTURED_TEXT" for x in candidates))


if __name__ == "__main__":
    unittest.main()
