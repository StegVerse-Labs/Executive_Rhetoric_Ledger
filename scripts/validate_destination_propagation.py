#!/usr/bin/env python3
"""Validate destination adapter, acknowledgment, and propagation authority boundaries."""
import json
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
config = json.loads((ROOT / "config/destination-adapters.json").read_text(encoding="utf-8"))
repositories = [item["repository"] for item in config["destinations"]]
required = {
    "StegVerse-Labs/Site",
    "GCAT-BCAT-Engine/Publisher",
    "StegVerse-Labs/admissibility-wiki",
    "StegVerse-002/StegGuardian",
}
if set(repositories) != required or len(repositories) != len(set(repositories)):
    raise SystemExit("Destination adapter registry must contain each required destination exactly once.")
if config["authority"] != {"source_may_prepare": True, "destination_must_acknowledge": True, "source_may_self_acknowledge": False}:
    raise SystemExit("Destination adapter authority boundary is invalid.")

for schema_name in ["destination-acknowledgment.schema.json", "propagation-verification.schema.json"]:
    schema = json.loads((ROOT / "schemas" / schema_name).read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)

manifest_path = ROOT / "propagation" / "verification.json"
if manifest_path.exists():
    schema = json.loads((ROOT / "schemas/propagation-verification.schema.json").read_text(encoding="utf-8"))
    document = json.loads(manifest_path.read_text(encoding="utf-8"))
    errors = list(Draft202012Validator(schema).iter_errors(document))
    if errors:
        raise SystemExit("Propagation verification manifest failed schema validation.")
    if set(document["required_destinations"]) != required:
        raise SystemExit("Propagation verification required destinations do not match the authoritative adapter registry.")
    if document["authority"]["may_fabricate_acknowledgment"] or document["authority"]["may_close_issue"]:
        raise SystemExit("Propagation verifier exceeded its authority.")

print("Validated destination propagation contracts and authority boundaries.")
