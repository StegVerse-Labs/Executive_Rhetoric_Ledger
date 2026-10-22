import importlib.util
from pathlib import Path
import unittest
ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("market_validator", ROOT / "scripts/validate_nvidia_market_intelligence.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
class MarketIntelligenceTests(unittest.TestCase):
    def test_valid_inputs(self):
        self.assertEqual(module.validate(), (3, 3))
    def test_outreach_is_hard_disabled(self):
        self.assertFalse(module.load("opportunity-register.json")["outreach_enabled"])
if __name__ == "__main__":
    unittest.main()
