#!/usr/bin/env python3
"""Validate producer adapter schema, fixture, configuration, and discovered declarations."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
schema = json.loads((ROOT / "schemas/producer-adapter.schema.json").read_text(encoding="utf-8"))
sample = json.loads((ROOT / "samples/producer-adapter.sample.json").read_text(encoding="utf-8"))
config = json.loads((ROOT / "config/producer-discovery.json").read_text(encoding="utf-8"))

required_top = {"contract_version", "producer", "consumer", "exports", "preservation", "authority", "lifecycle"}
if set(schema.get("required", [])) != required_top:
    raise SystemExit("Producer adapter schema required-field contract changed unexpectedly.")
if sample.get("contract_version") != "1.0.0" or sample.get("consumer") != "StegVerse-Labs/Executive_Rhetoric_Ledger":
    raise SystemExit("Canonical producer adapter fixture identity is invalid.")
if not required_top.issubset(sample):
    raise SystemExit("Canonical producer adapter fixture is incomplete.")
if len(sample["preservation"]) < 8 or len(sample["preservation"]) != len(set(sample["preservation"])):
    raise SystemExit("Canonical producer preservation contract is incomplete or duplicated.")

def validate_authority(authority, repository):
    expected = {
        "export_status": "candidate-only",
        "may_claim_truth": False,
        "may_classify_final": False,
        "may_promote": False,
        "requires_ledger_review": True,
    }
    if authority != expected:
        raise SystemExit(f"Producer exceeded ledger authority: {repository}")

validate_authority(sample["authority"], sample["producer"]["repository"])
retry = sample["lifecycle"]["retry_policy"]
if retry["max_attempts"] < 1 or not retry["backoff_seconds"] or any(value < 1 for value in retry["backoff_seconds"]):
    raise SystemExit("Canonical producer retry policy is invalid.")
if sample["lifecycle"]["deprecation_requires_governed_record"] is not True:
    raise SystemExit("Producer deprecation must require a governed record.")

if config.get("authority") != {"discovery_may_register": False, "discovery_may_promote": False, "governed_deprecation_required": True}:
    raise SystemExit("Producer discovery authority boundary is invalid.")
scopes = config.get("organization_scopes", [])
if not scopes or len(scopes) != len(set(scopes)):
    raise SystemExit("Producer discovery organization scopes must be non-empty and unique.")
if config.get("contract_path") != ".stegverse/executive-rhetoric-ledger-producer.json":
    raise SystemExit("Producer declaration path is not canonical.")

path = ROOT / config["output_path"]
if path.exists():
    document = json.loads(path.read_text(encoding="utf-8"))
    if document.get("authority") != {"may_discover": True, "may_register": False, "may_promote": False}:
        raise SystemExit("Discovered producer registry exceeded discovery authority.")
    seen = set()
    for row in document.get("producers", []):
        repository = row["repository"]
        declaration = row["declaration"]
        if repository in seen:
            raise SystemExit(f"Duplicate producer declaration: {repository}")
        seen.add(repository)
        if declaration.get("producer", {}).get("repository") != repository:
            raise SystemExit(f"Producer identity mismatch: {repository}")
        if declaration.get("consumer") != "StegVerse-Labs/Executive_Rhetoric_Ledger":
            raise SystemExit(f"Producer consumer mismatch: {repository}")
        if not required_top.issubset(declaration):
            raise SystemExit(f"Producer declaration is incomplete: {repository}")
        validate_authority(declaration["authority"], repository)
        lifecycle = declaration["lifecycle"]
        if lifecycle.get("deprecation_requires_governed_record") is not True:
            raise SystemExit(f"Producer deprecation boundary is invalid: {repository}")

print("Validated producer adapter identities, preservation, retry posture, discovery scope, and authority boundaries.")
