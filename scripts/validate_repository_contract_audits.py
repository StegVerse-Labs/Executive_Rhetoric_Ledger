#!/usr/bin/env python3
"""Validate machine-readable repository contract audits and activation boundaries."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "repository-contract-audit.schema.json"
REGISTRY_PATH = ROOT / "integration" / "repository-contract-audits.json"
CAPABILITY_PATH = ROOT / "integration" / "repository-capabilities.json"


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)


def main() -> int:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    capabilities = json.loads(CAPABILITY_PATH.read_text(encoding="utf-8"))

    errors = sorted(
        Draft202012Validator(schema).iter_errors(registry),
        key=lambda error: list(error.path),
    )
    if errors:
        for error in errors:
            path = ".".join(str(part) for part in error.path) or "<root>"
            fail(f"{path}: {error.message}")
        return 1

    capability_repositories = {
        item["repository"] for item in capabilities.get("repositories", [])
    }
    seen: set[str] = set()
    failed = False

    for audit in registry.get("audits", []):
        repository = audit["repository"]
        if repository in seen:
            fail(f"duplicate contract audit for {repository}")
            failed = True
        seen.add(repository)

        if repository not in capability_repositories:
            fail(f"contract audit repository missing from capability registry: {repository}")
            failed = True

        audit_ref = ROOT / audit["audit_ref"]
        if not audit_ref.is_file():
            fail(f"audit_ref does not exist for {repository}: {audit['audit_ref']}")
            failed = True

        contract_state = audit["contract_state"]
        adapter_state = audit["adapter_state"]

        if contract_state == "verified":
            required_nonempty = [
                "verified_inputs",
                "verified_outputs",
                "verified_receipts",
                "verified_consumers",
                "verified_failure_handling",
            ]
            for field in required_nonempty:
                if not audit.get(field):
                    fail(f"verified contract for {repository} requires non-empty {field}")
                    failed = True
            if audit.get("blockers"):
                fail(f"verified contract for {repository} cannot retain blockers")
                failed = True

        if adapter_state in {"ready", "active"} and contract_state != "verified":
            fail(f"{repository} adapter_state {adapter_state} requires verified contract")
            failed = True

        if adapter_state == "active" and audit.get("blockers"):
            fail(f"active adapter for {repository} cannot retain blockers")
            failed = True

        if audit["audit_state"] == "repaired-partial" and not audit.get("repairs"):
            fail(f"repaired-partial audit for {repository} requires repair records")
            failed = True

    if failed:
        return 1

    print(
        "OK: repository contract audit registry passed "
        f"({len(registry.get('audits', []))} audit record(s))"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
