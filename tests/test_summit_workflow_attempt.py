import json
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from run_summit_workflow_attempt import execute, GROUP


class AttemptTests(unittest.TestCase):
    def exercise(self, mode):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            old = root / "assessments/us-china-ai-summit/research-cycles/old.json"
            old.parent.mkdir(parents=True)
            old.write_text('{"historical":true}')
            calls = []
            def invoke(cmd, cwd):
                calls.append(cmd)
                if "generate_active" in cmd[1]:
                    if mode == "generator_failure":
                        return SimpleNamespace(returncode=1)
                    lane = {"group_id": GROUP, "dispatch_state": "ELIGIBLE_FOR_AUTOMATED_ACQUISITION",
                            "finding_authorized": False, "publication_authorized": False,
                            "queues": [{"executable_items": [1] * (0 if mode == "empty" else 6)}]}
                    if mode == "denied": lane["dispatch_state"] = "DENIED"
                    if mode == "authority": lane["publication_authorized"] = True
                    Path(cmd[-1]).write_text(json.dumps({"lanes": [lane]}))
                    return SimpleNamespace(returncode=0)
                timestamp = cmd[cmd.index("--timestamp") + 1]
                Path(cmd[-1]).write_text(json.dumps({"generated_at": timestamp,
                    "execution_state": "NOT_SCANNED" if mode == "runner_gap" else "FIXTURE_SUCCESS"}))
                return SimpleNamespace(returncode=2 if mode == "runner_gap" else 0)
            code = execute(root, "123", "2", invoke)
            audit = root / "_audit/summit-123-2"
            receipt = json.loads((audit / "preflight.json").read_text())
            self.assertEqual(old.read_text(), '{"historical":true}')
            self.assertFalse(receipt["publication_authorized"])
            self.assertEqual(receipt["run_attempt"], "2")
            if mode in {"denied", "empty", "authority", "generator_failure"}:
                self.assertEqual(code, 2)
                self.assertEqual(len(calls), 1)
                self.assertEqual(receipt["state"], "PREFLIGHT_REFUSED")
                self.assertFalse((audit / "cycle.json").exists())
            else:
                self.assertEqual(len(calls), 2)
                self.assertTrue((audit / "cycle.json").exists())
                self.assertEqual(code, 2 if mode == "runner_gap" else 0)
                self.assertEqual(len(list(old.parent.glob("*.json"))), 1 if mode == "runner_gap" else 2)
            with self.assertRaises(FileExistsError):
                execute(root, "123", "2", invoke)
            self.assertEqual(len(calls), 1 if mode in {"denied", "empty", "authority", "generator_failure"} else 2)

    def test_generator_failure_retains_gap(self): self.exercise("generator_failure")
    def test_denied_never_invokes_acquisition(self): self.exercise("denied")
    def test_empty_never_invokes_acquisition(self): self.exercise("empty")
    def test_authority_never_invokes_acquisition(self): self.exercise("authority")
    def test_runner_gap_retained_without_daily_promotion(self): self.exercise("runner_gap")
    def test_success_preserves_current_and_daily_receipts(self): self.exercise("success")
