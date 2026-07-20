#!/usr/bin/env python3
"""Deterministically validate producer adapter identity and authority constants."""
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
schema = json.loads((root / "schemas/producer-adapter.schema.json").read_text(encoding="utf-8"))
sample = json.loads((root / "samples/producer-adapter.sample.json").read_text(encoding="utf-8"))
config = json.loads((root / "config/producer-discovery.json").read_text(encoding="utf-8"))

assert schema["properties"]["consumer"]["const"] == "StegVerse-Labs/Executive_Rhetoric_Ledger"
assert schema["properties"]["authority"]["properties"]["may_claim_truth"]["const"] is False
assert schema["properties"]["authority"]["properties"]["may_classify_final"]["const"] is False
assert schema["properties"]["authority"]["properties"]["may_promote"]["const"] is False
assert schema["properties"]["authority"]["properties"]["requires_ledger_review"]["const"] is True
assert sample["consumer"] == "StegVerse-Labs/Executive_Rhetoric_Ledger"
assert sample["authority"] == {
    "export_status": "candidate-only",
    "may_claim_truth": False,
    "may_classify_final": False,
    "may_promote": False,
    "requires_ledger_review": True,
}
assert config["contract_path"] == ".stegverse/executive-rhetoric-ledger-producer.json"
assert config["authority"] == {
    "discovery_may_register": False,
    "discovery_may_promote": False,
    "governed_deprecation_required": True,
}
assert config["organization_scopes"] and len(config["organization_scopes"]) == len(set(config["organization_scopes"]))

registry = root / config["output_path"]
if registry.exists():
    document = json.loads(registry.read_text(encoding="utf-8"))
    assert document["authority"] == {"may_discover": True, "may_register": False, "may_promote": False}
    repositories = []
    for row in document.get("producers", []):
        repository = row["repository"]
        declaration = row["declaration"]
        assert declaration["producer"]["repository"] == repository
        assert declaration["consumer"] == "StegVerse-Labs/Executive_Rhetoric_Ledger"
        assert declaration["authority"] == sample["authority"]
        assert declaration["lifecycle"]["deprecation_requires_governed_record"] is True
        repositories.append(repository)
    assert len(repositories) == len(set(repositories))

print("Validated governed producer adapter identity and authority constants.")
