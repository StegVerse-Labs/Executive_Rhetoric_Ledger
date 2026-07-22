from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "generate_compendium_and_deliveries.py"


def load_module():
    spec = importlib.util.spec_from_file_location("generate_compendium_and_deliveries", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_trumpality_receipt_is_explicitly_related() -> None:
    module = load_module()
    path = ROOT / "ledger_receipts" / "reviewed" / "PIT-MODERN-2025-AI-EO-14179__action-record.reviewed.md"
    entry = {"_source_text": path.read_text(encoding="utf-8")}
    assert module.explicitly_related(entry, "StegVerse-Labs/Trumpality") is True
    assert module.explicitly_related(entry, "StegVerse-Labs/Giuffre-ality") is False
    assert module.explicitly_related(entry, "StegVerse-Labs/Maxwellality") is False
    assert module.explicitly_related(entry, "StegVerse-Labs/Epsteinality") is False


def test_person_specific_projection_is_reviewed_only_and_non_authorizing(tmp_path, monkeypatch) -> None:
    module = load_module()
    monkeypatch.setattr(module, "ROOT", tmp_path)
    monkeypatch.setattr(module, "RELATED_REPOSITORIES", tmp_path / "integration" / "related-repositories.json")
    (tmp_path / "integration").mkdir()
    (tmp_path / "integration" / "related-repositories.json").write_text(
        json.dumps(
            {
                "repositories": [
                    {
                        "repository": "StegVerse-Labs/Trumpality",
                        "roles": ["person-or-network-specific-record"],
                        "evidence_boundary": "Distinguish rhetoric, action, allegation, finding, and outcome.",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    entries = [
        {
            "entry_id": "ENTRY-1",
            "title": "Reviewed action",
            "receipt_path": "ledger_receipts/reviewed/example.md",
            "receipt_sha256": "a" * 64,
            "review_status": "reviewed",
            "search_text": "reviewed action",
            "_source_text": 'producer_repo: "StegVerse-Labs/Trumpality"',
        },
        {
            "entry_id": "ENTRY-2",
            "title": "Unrelated reviewed action",
            "receipt_path": "ledger_receipts/reviewed/unrelated.md",
            "receipt_sha256": "b" * 64,
            "review_status": "reviewed",
            "search_text": "unrelated",
            "_source_text": 'producer_repo: "StegVerse-Labs/Administrations"',
        },
    ]

    destinations = module.write_person_specific_projections(entries, "2026-07-22T00:00:00Z")
    assert len(destinations) == 1
    projection_path = tmp_path / destinations[0]["source_path"]
    projection = json.loads(projection_path.read_text(encoding="utf-8"))
    assert projection["destination_repository"] == "StegVerse-Labs/Trumpality"
    assert [item["entry_id"] for item in projection["entries"]] == ["ENTRY-1"]
    assert projection["authority"] == {
        "reviewed_only": True,
        "may_include_candidates": False,
        "may_change_native_source_records": False,
        "may_change_destination_verification_labels": False,
        "may_establish_culpability": False,
        "may_claim_delivery": False,
        "may_claim_acknowledgment": False,
    }
    material = dict(projection)
    expected = material.pop("projection_sha256")
    import hashlib
    actual = hashlib.sha256(json.dumps(material, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    assert expected == actual
