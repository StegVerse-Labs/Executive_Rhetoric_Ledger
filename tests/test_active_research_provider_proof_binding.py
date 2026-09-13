from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.verify_active_research_provider_proof_binding import verify

ROOT = Path(__file__).resolve().parents[1]
PROOF = ROOT / "evidence/active-research/ERL-CYBER-CISA-IRAN-2025-JOINT-FACT-SHEET.provider-readback-proof.json"


def envelope():
    return {
        "schema": "stegverse.erl.active-research-acquisition-envelope/v1",
        "group_id": "ERL-RC-CYBER-SABOTAGE-LINEAGE-2026",
        "source_id": "ERL-CYBER-CISA-IRAN-2025-JOINT-FACT-SHEET",
        "source_url": "https://www.cisa.gov/news-events/cybersecurity-advisories/aa25-176a",
        "required_storage_lane": "02_Research/ERL",
        "finding_authorized": False,
        "publication_authorized": False,
    }


class ActiveResearchProviderProofBindingTests(unittest.TestCase):
    def test_binds_source_identity_to_existing_exact_provider_readback(self):
        proof = json.loads(PROOF.read_text(encoding="utf-8"))
        result = verify(envelope(), proof)
        self.assertEqual(result["state"], "SOURCE_IDENTITY_BOUND_TO_EXISTING_PROVIDER_PROOF")
        self.assertEqual(result["provider_exact_sha256"], "94470c58db24e544c3edfcd390cca395375a348879ec3c53451ba517ff917763")
        self.assertEqual(result["provider_exact_size_bytes"], 1015)
        self.assertFalse(result["provider_operation_reexecution_authorized"])
        self.assertFalse(result["provider_operation_attempted"])
        self.assertFalse(result["universal_intr_traversal_proven_by_provider_proof"])

    def test_rejects_source_identity_mismatch(self):
        proof = json.loads(PROOF.read_text(encoding="utf-8"))
        bad = envelope()
        bad["source_id"] = "different"
        with self.assertRaisesRegex(ValueError, "source_id_binding_mismatch"):
            verify(bad, proof)

    def test_rejects_any_reexecution_authorization(self):
        proof = json.loads(PROOF.read_text(encoding="utf-8"))
        proof["provider_operation_reexecution_authorized"] = True
        with self.assertRaisesRegex(ValueError, "reexecution"):
            verify(envelope(), proof)


if __name__ == "__main__":
    unittest.main()
