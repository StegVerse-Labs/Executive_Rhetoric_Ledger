import importlib.util
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("validator", ROOT / "scripts" / "validate_ai_economic_transparency.py")
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)

def base():
    return {
        "schema":"stegverse.erl.ai-economic-transparency-observation/v1",
        "task_id":"ERL-AI-ECON-TRANSPARENCY-001",
        "provider":"example",
        "model":None,
        "surface_class":"CONSUMER_NON_ACCOUNT_ATTRIBUTED",
        "rating_scope":"SURFACE_SPECIFIC",
        "protocol_complete":False,
        "actual_request_cost_directly_exposed":False,
        "request_usage_directly_exposed":False,
        "research_steps_required":1,
        "provider_surfaces_consulted":["request"],
        "account_or_privilege_required":False,
        "support_required":False,
        "external_research_required":False,
        "reconstructable_actual_cost":False,
        "literal_request_cost_usd":None,
        "unresolved_cost_components":["request cost"],
        "disclosure_burden_rating":None,
        "scale_scenarios":[
            {"equivalent_requests":1000,"state":"UNBOUNDED_UNKNOWN","known_total_cost_usd":None,"lower_bound_usd":None,"upper_bound_usd":None}
        ],
        "scale_sensitivity_state":"UNBOUNDED_UNKNOWN",
        "activation_authorized":False
    }

class TestTransparencyValidator(unittest.TestCase):
    def test_incomplete_unscored_valid(self):
        self.assertEqual(validator.validate(base()), [])

    def test_provider_wide_rating_forbidden(self):
        o=base(); o["rating_scope"]="PROVIDER_WIDE"
        self.assertIn("provider_wide_rating_forbidden", validator.validate(o))

    def test_rating_five_requires_complete_protocol(self):
        o=base(); o["disclosure_burden_rating"]=5
        self.assertIn("rating_5_requires_protocol_complete", validator.validate(o))

    def test_complete_nonreconstructable_can_rate_five(self):
        o=base(); o["protocol_complete"]=True; o["disclosure_burden_rating"]=5
        self.assertEqual(validator.validate(o), [])

    def test_unknown_scale_cannot_claim_numeric_total(self):
        o=base(); o["scale_scenarios"][0]["known_total_cost_usd"]=10
        self.assertTrue(any("unknown_has_numeric_claim" in e for e in validator.validate(o)))

    def test_exact_scale_requires_total(self):
        o=base(); o["scale_scenarios"][0]["state"]="EXACT"
        self.assertTrue(any("exact_missing_total" in e for e in validator.validate(o)))

if __name__ == "__main__":
    unittest.main()
