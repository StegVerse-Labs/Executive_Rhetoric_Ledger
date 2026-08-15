import copy
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import process_uap_source_queue as worker


class UapSourceQueueTests(unittest.TestCase):
    def setUp(self):
        self.queue = json.loads((ROOT / "config" / "uap-media-source-queue.json").read_text())

    def test_canonical_queue_is_valid(self):
        self.assertEqual(worker.validate_queue(self.queue), [])

    def test_wrong_class_destination_fails(self):
        bad = copy.deepcopy(self.queue)
        bad["items"][0]["destination"] = "assessments/uap-media/evidence/media-primary/misfiled.native"
        errors = worker.validate_queue(bad)
        self.assertTrue(any("destination must remain under" in error for error in errors), errors)

    def test_non_https_url_fails(self):
        bad = copy.deepcopy(self.queue)
        bad["items"][0]["url"] = "http://science.nasa.gov/uap/"
        errors = worker.validate_queue(bad)
        self.assertTrue(any("public HTTPS" in error for error in errors), errors)

    def test_unallowlisted_host_fails(self):
        bad = copy.deepcopy(self.queue)
        bad["items"][0]["url"] = "https://example.com/uap"
        errors = worker.validate_queue(bad)
        self.assertTrue(any("host is not allowlisted" in error for error in errors), errors)

    def test_validate_only_requires_no_network_and_strips_tokens(self):
        with tempfile.TemporaryDirectory() as tmp:
            receipt = Path(tmp) / "receipt.json"
            env = os.environ.copy()
            env["GITHUB_TOKEN"] = "SHOULD_NOT_BE_USED"
            env["GH_TOKEN"] = "SHOULD_NOT_BE_USED"
            proc = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "process_uap_source_queue.py"), "--receipt", str(receipt)],
                cwd=ROOT,
                env=env,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            data = json.loads(receipt.read_text())
            self.assertEqual(data["execution_status"], "VALIDATED_ONLY")
            self.assertFalse(data["github_token_used"])
            self.assertTrue(data["inherited_token_presence_removed_before_network"]["GITHUB_TOKEN"])
            self.assertTrue(data["inherited_token_presence_removed_before_network"]["GH_TOKEN"])
            self.assertEqual(data["results"], [])


if __name__ == "__main__":
    unittest.main()
