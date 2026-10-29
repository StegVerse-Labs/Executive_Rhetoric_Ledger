"""Offline real-process integration; dispatch is explicitly a synthetic fixture."""
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

CANDIDATE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CANDIDATE / "scripts"))
from run_summit_workflow_attempt import execute, GROUP

class IntegrationTests(unittest.TestCase):
    def workspace(self, root, dispatch):
        (root / "scripts").mkdir()
        (root / "config").mkdir()
        for name in ["run_us_china_ai_summit_research.py", "process_uap_source_queue.py"]:
            shutil.copyfile(CANDIDATE / "scripts" / name, root / "scripts" / name)
        queue = json.loads((CANDIDATE / "config/us-china-ai-summit-source-queue.v1.json").read_text())
        queue["items"] = []  # Guarantees no source request even if wrapper invokes runner.
        (root / "config/us-china-ai-summit-source-queue.v1.json").write_text(json.dumps(queue))
        (root / "scripts/generate_active_research_dispatch.py").write_text(
            "import pathlib,sys\npathlib.Path(sys.argv[-1]).write_text(" + repr(json.dumps(dispatch)) + ")\n")

    def test_real_runner_zero_source_receipt_retained(self):
        dispatch = {"lanes": [{"group_id": GROUP, "dispatch_state": "ELIGIBLE_FOR_AUTOMATED_ACQUISITION",
                    "finding_authorized": False, "publication_authorized": False,
                    "queues": [{"executable_items": [1] * 6}]}]}
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.workspace(root, dispatch)
            self.assertEqual(execute(root, "777", "1"), 2)
            report = json.loads((root / "_audit/summit-777-1/cycle.json").read_text())
            self.assertEqual(report["coverage_state"], "NOT_SCANNED")
            self.assertEqual(report["source_attempted_count"], 0)
            self.assertEqual(report["items"], [])
            self.assertFalse(report["publication_authorized"])
            self.assertFalse((root / "assessments/us-china-ai-summit/research-cycles").exists())

    def malformed(self, dispatch):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.workspace(root, dispatch)
            self.assertEqual(execute(root, "888", "1"), 2)
            audit = root / "_audit/summit-888-1"
            receipt = json.loads((audit / "preflight.json").read_text())
            self.assertEqual(receipt["state"], "PREFLIGHT_REFUSED")
            self.assertFalse(receipt["acquisition_invocation_requested"])
            self.assertFalse((audit / "cycle.json").exists())

    def test_nonobject_lane_retains_refusal(self): self.malformed({"lanes": [None]})
    def test_nonobject_document_retains_refusal(self): self.malformed([])
    def test_nonlist_queues_retains_refusal(self):
        self.malformed({"lanes": [{"group_id": GROUP, "dispatch_state": "ELIGIBLE_FOR_AUTOMATED_ACQUISITION",
            "finding_authorized": False, "publication_authorized": False, "queues": {}}]})

if __name__ == "__main__": unittest.main()
