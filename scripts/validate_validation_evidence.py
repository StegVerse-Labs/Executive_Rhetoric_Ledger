#!/usr/bin/env python3
"""Validate governed validator manifests, execution receipts, and fixture expectations."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_SCHEMA = ROOT / "schemas/validation-evidence-manifest.schema.json"
RECEIPT_SCHEMA = ROOT / "schemas/validation-execution-receipt.schema.json"
FIXTURE_ROOT = ROOT / "validation_fixtures/validation-evidence"


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_json(instance: Any, schema_path: Path, label: str) -> list[str]:
    validator = Draft202012Validator(load(schema_path), format_checker=FormatChecker())
    return [f"{label}: {error.message}" for error in sorted(validator.iter_errors(instance), key=lambda e: list(e.path))]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def validate_receipt_semantics(receipt: dict[str, Any], path: Path) -> list[str]:
    errors: list[str] = []
    validators = receipt.get("validators", [])
    required_failures = [entry for entry in validators if entry.get("required", True) and entry.get("exit_code") != 0]
    expected = "failure" if required_failures else "success"
    if receipt.get("overall_conclusion") in {"success", "failure"} and receipt.get("overall_conclusion") != expected:
        errors.append(f"{path}: overall_conclusion disagrees with required validator outcomes")
    authority = receipt.get("authority", {})
    if any(authority.get(key) is not False for key in (
        "may_promote_publication",
        "may_assert_primary_source_completion",
        "may_change_chain_node_confidence",
    )):
        errors.append(f"{path}: authority boundary must remain false")
    for entry in validators:
        log_path = entry.get("log_path")
        if log_path and Path(log_path).is_absolute():
            errors.append(f"{path}: log_path must be artifact-relative")
    return errors


def validate_fixtures() -> list[str]:
    errors: list[str] = []
    index_path = FIXTURE_ROOT / "fixture-index.json"
    index = load(index_path)
    for fixture in index["fixtures"]:
        fixture_path = FIXTURE_ROOT / fixture["path"]
        payload = load(fixture_path)
        errors.extend(validate_json(payload, RECEIPT_SCHEMA, fixture["id"]))
        errors.extend(validate_receipt_semantics(payload, fixture_path))
        if payload.get("overall_conclusion") != fixture["expected_conclusion"]:
            errors.append(f"{fixture['id']}: expected {fixture['expected_conclusion']} but found {payload.get('overall_conclusion')}")
        if fixture.get("expected_activation_effect") and payload.get("activation_effect") != fixture["expected_activation_effect"]:
            errors.append(f"{fixture['id']}: activation_effect mismatch")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", default="validation_manifests/repository-core.json")
    parser.add_argument("--receipt")
    parser.add_argument("--fixtures", action="store_true")
    args = parser.parse_args()

    errors: list[str] = []
    manifest_path = ROOT / args.manifest
    errors.extend(validate_json(load(manifest_path), MANIFEST_SCHEMA, str(manifest_path)))

    if args.receipt:
        receipt_path = ROOT / args.receipt
        receipt = load(receipt_path)
        errors.extend(validate_json(receipt, RECEIPT_SCHEMA, str(receipt_path)))
        errors.extend(validate_receipt_semantics(receipt, receipt_path))

    if args.fixtures:
        errors.extend(validate_fixtures())

    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1

    print(f"PASS: validation evidence contracts verified; manifest_sha256={sha256(manifest_path)}")
    print("NOTE: contract validity does not establish source completeness, factual truth, admissibility, or publication authority")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
