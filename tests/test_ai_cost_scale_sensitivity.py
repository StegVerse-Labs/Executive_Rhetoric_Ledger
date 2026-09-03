import importlib.util
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("scale", ROOT / "scripts" / "calculate_ai_cost_scale_sensitivity.py")
scale = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scale)

class TestScaleSensitivity(unittest.TestCase):
    def test_exact(self):
        rows = scale.scenarios(exact_per_request=0.01)
        self.assertEqual(rows[0]["known_total_cost_usd"], 10.0)
        self.assertEqual(rows[-1]["known_total_cost_usd"], 10000.0)
        self.assertTrue(all(r["state"] == "EXACT" for r in rows))

    def test_bounded(self):
        rows = scale.scenarios(lower_per_request=0.005, upper_per_request=0.02)
        self.assertEqual(rows[0]["lower_bound_usd"], 5.0)
        self.assertEqual(rows[0]["upper_bound_usd"], 20.0)
        self.assertEqual(rows[-1]["lower_bound_usd"], 5000.0)
        self.assertEqual(rows[-1]["upper_bound_usd"], 20000.0)

    def test_unknown_stays_unknown(self):
        rows = scale.scenarios()
        self.assertTrue(all(r["state"] == "UNBOUNDED_UNKNOWN" for r in rows))
        self.assertTrue(all(r["known_total_cost_usd"] is None for r in rows))

    def test_reject_partial_bounds(self):
        with self.assertRaises(ValueError):
            scale.scenarios(lower_per_request=0.01)

    def test_reject_inverted_bounds(self):
        with self.assertRaises(ValueError):
            scale.scenarios(lower_per_request=0.02, upper_per_request=0.01)

if __name__ == "__main__":
    unittest.main()
