#!/usr/bin/env python3
"""Validate producer adapter schema, discovery configuration, and discovered declarations."""
import json
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
schema = json.loads((ROOT / "schemas/producer-adapter.schema.json").read_text(encoding="utf-8"))
Draft202012Validator.check_schema(schema)
validator = Draft202012Validator(schema)
config = json.loads((ROOT / "config/producer-discovery.json").read_text(encoding="utf-8"))

if config["authority"] != {
    "discovery_may_register": False,
    "discovery_may_promote": False,
    "governed_deprecation_required": True,
}:
    raise SystemExit("Producer discovery authority boundary is invalid.")
if len(config["organization_scopes"]) != len(set(config["organization_scopes"])):
    raise SystemExit("Producer discovery organization scopes must be unique.")
if config["contract_path"] != ".stegverse/executive-rhetoric-ledger-producer.json":
    raise SystemExit("Producer declaration path is not canonical.")

path = ROOT / config["output_path"]
if path.exists():
    document = json.loads(path.read_text(encoding="utf-8"))
    if document["authority"] != {"may_discover": True, "may_register": False, "may_promote": False}:
        raise SystemExit("Discovered producer registry exceeded discovery authority.")
    seen = set()
    for row in document["producers"]:
        repository = row["repository"]
        if repository in seen:
            raise SystemExit(f"Duplicate producer declaration: {repository}")
        seen.add(repository)
        declaration = row["declaration"]
        errors = list(validator.iter_errors(declaration))
        if errors:
            raise SystemExit(f"Producer declaration failed schema validation: {repository}")
        if declaration["producer"]["repository"] != repository:
            raise SystemExit(f"Producer identity mismatch: {repository}")
        authority = declaration["authority"]
        if authority["may_claim_truth"] or authority["may_classify_final"] or authority["may_promote"]:
            raise SystemExit(f"Producer exceeded ledger authority: {repository}")

print("Validated producer adapter schema, discovery configuration, identities, and authority boundaries.")
