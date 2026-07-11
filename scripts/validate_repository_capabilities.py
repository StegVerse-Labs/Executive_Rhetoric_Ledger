#!/usr/bin/env python3
"""Validate the related-repository capability and contract-audit registry."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "repository-capability-registry.schema.json"
REGISTRY_PATH = ROOT / "integration" / "repository-capabilities.json"
NETWORK_PATH = ROOT / "integration" / "related-repositories.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    issues: list[str] = []

    for path in (SCHEMA_PATH, REGISTRY_PATH, NETWORK_PATH):
        if not path.exists():
            issues.append(f"missing required file: {path.relative_to(ROOT)}")

    if issues:
        for issue in issues:
            print(f"- {issue}", file=sys.stderr)
        return 1

    schema = load_json(SCHEMA_PATH)
    registry = load_json(REGISTRY_PATH)
    network = load_json(NETWORK_PATH)

    validator = Draft202012Validator(schema)
    for error in sorted(validator.iter_errors(registry), key=lambda item: list(item.path)):
        location = ".".join(str(part) for part in error.path) or "<root>"
        issues.append(f"schema {location}: {error.message}")

    registry_entries = registry.get("repositories", [])
    registry_names = [entry.get("repository") for entry in registry_entries]
    network_names = [entry.get("repository") for entry in network.get("repositories", [])]

    if len(registry_names) != len(set(registry_names)):
        issues.append("duplicate repository entries in capability registry")

    if set(registry_names) != set(network_names):
        missing = sorted(set(network_names) - set(registry_names))
        extra = sorted(set(registry_names) - set(network_names))
        if missing:
            issues.append(f"registry missing related repositories: {missing}")
        if extra:
            issues.append(f"registry contains undeclared repositories: {extra}")

    for entry in registry_entries:
        repository = entry.get("repository", "<unknown>")
        audit_refs = entry.get("audit_refs", [])
        for audit_ref in audit_refs:
            target = ROOT / audit_ref
            if not target.exists():
                issues.append(f"{repository}: audit reference not found: {audit_ref}")

        if entry.get("adapter_state") in {"ready", "active"} and entry.get("contract_state") != "verified":
            issues.append(f"{repository}: ready or active adapter requires verified contract_state")

        if entry.get("contract_state") == "verified":
            if not entry.get("verified_inputs"):
                issues.append(f"{repository}: verified contract requires verified_inputs")
            if not entry.get("verified_outputs"):
                issues.append(f"{repository}: verified contract requires verified_outputs")

        if entry.get("privacy_posture") != "public" and not entry.get("prohibited_changes"):
            issues.append(f"{repository}: non-public posture requires prohibited_changes")

    if issues:
        print("Repository capability registry validation failed:")
        for issue in issues:
            print(f"- {issue}")
        return 1

    print(f"OK: validated {len(registry_entries)} repository capability records")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
