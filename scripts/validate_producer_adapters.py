#!/usr/bin/env python3
"""Validate producer adapter schema, fixture, discovery configuration, and discovered declarations."""
import json
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
schema = json.loads((ROOT / "schemas/producer-adapter.schema.json").read_text(encoding="utf-8"))
validator = Draft202012Validator(schema)
sample = json.loads((ROOT / "samples/producer-adapter.sample.json").read_text(encoding="utf-8"))
sample_errors = sorted(validator.iter_errors(sample), key=lambda error: list(error.path))
if sample_errors:
    detail = "; ".join(error.message for error in sample_errors)
    raise SystemExit(f"Canonical producer adapter fixture failed validation: {detail}")

config = json.loads((ROOT / "config/producer-discovery.json").read_text(encoding="utf-8"))
authority = config.get("authority", {})
if authority.get("discovery_may_register") is not False:
    raise SystemExit("Producer discovery may not register producers.")
if authority.get("discovery_may_promote") is not False:
    raise SystemExit("Producer discovery may not promote records.")
if authority.get("governed_deprecation_required") is not True:
    raise SystemExit("Producer deprecation must require a governed record.")
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
        if repository in seen:
            raise SystemExit(f"Duplicate producer declaration: {repository}")
        seen.add(repository)
        declaration = row["declaration"]
        errors = sorted(validator.iter_errors(declaration), key=lambda error: list(error.path))
        if errors:
            detail = "; ".join(error.message for error in errors)
            raise SystemExit(f"Producer declaration failed schema validation: {repository}: {detail}")
        if declaration["producer"]["repository"] != repository:
            raise SystemExit(f"Producer identity mismatch: {repository}")
        producer_authority = declaration["authority"]
        if producer_authority["may_claim_truth"] or producer_authority["may_classify_final"] or producer_authority["may_promote"]:
            raise SystemExit(f"Producer exceeded ledger authority: {repository}")

print("Validated producer adapter fixture, discovery configuration, identities, retry posture, and authority boundaries.")
