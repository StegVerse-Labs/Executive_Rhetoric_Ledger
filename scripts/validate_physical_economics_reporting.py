#!/usr/bin/env python3
"""Validate Physical Economics public-reporting contracts and boundary behavior."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
REQUEST_SCHEMA = ROOT / "schemas" / "physical-economics-report-request.schema.json"
SNAPSHOT_SCHEMA = ROOT / "schemas" / "physical-economics-evidence-snapshot.schema.json"
BOUNDARY_SCHEMA = ROOT / "schemas" / "physical-economics-report-boundary-manifest.schema.json"
DELTA_SCHEMA = ROOT / "schemas" / "physical-economics-report-delta.schema.json"
MATRIX_PATH = ROOT / "contracts" / "physical-economics-report-pertinence.matrix.v0.1.json"
CASES_PATH = ROOT / "tests" / "physical-economics-reporting" / "boundary-resolver.cases.json"
RESOLVER_PATH = ROOT / "scripts" / "resolve_physical_economics_report_boundary.py"


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_resolver_module():
    spec = importlib.util.spec_from_file_location("physical_economics_boundary_resolver", RESOLVER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load boundary resolver")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def schema_errors(data: Any, schema: dict[str, Any], label: str) -> list[str]:
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    return [f"{label}: {error.message}" for error in validator.iter_errors(data)]


def validate_matrix_alignment(request_schema: dict[str, Any], matrix: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    request_claims = set(request_schema["properties"]["claim_classes"]["items"]["enum"])
    matrix_claims = set(matrix["claim_classes"])
    missing_in_matrix = sorted(request_claims - matrix_claims)
    missing_in_schema = sorted(matrix_claims - request_claims)
    if missing_in_matrix:
        errors.append("claim classes allowed by request schema but absent from matrix: " + ", ".join(missing_in_matrix))
    if missing_in_schema:
        errors.append("claim classes defined by matrix but absent from request schema: " + ", ".join(missing_in_schema))

    for claim, mapping in matrix["claim_classes"].items():
        required = mapping.get("required", [])
        contextual = mapping.get("contextual", [])
        if not required:
            errors.append(f"{claim}: required attribute set is empty")
        overlap = sorted(set(required).intersection(contextual))
        if overlap:
            errors.append(f"{claim}: required/contextual overlap: {', '.join(overlap)}")
        if len(required) != len(set(required)):
            errors.append(f"{claim}: duplicate required attributes")
        if len(contextual) != len(set(contextual)):
            errors.append(f"{claim}: duplicate contextual attributes")
    return errors


def validate_snapshot_semantics(snapshot: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    receipt_ids = {receipt["source_receipt_id"] for receipt in snapshot["source_receipts"]}
    attribute_ids: set[str] = set()
    for attribute in snapshot["attributes"]:
        attribute_id = attribute["attribute_id"]
        if attribute_id in attribute_ids:
            errors.append(f"{snapshot['evidence_snapshot_id']}: duplicate attribute {attribute_id}")
        attribute_ids.add(attribute_id)
        missing_receipts = sorted(set(attribute["source_receipt_ids"]) - receipt_ids)
        if missing_receipts:
            errors.append(
                f"{snapshot['evidence_snapshot_id']}: {attribute_id} references absent receipts: "
                + ", ".join(missing_receipts)
            )
        uncertainty = attribute.get("uncertainty")
        if uncertainty:
            dependence = uncertainty.get("dependence_posture")
            propagation = uncertainty.get("propagation_authorized", False)
            if dependence == "UNKNOWN_DEPENDENCE" and propagation:
                errors.append(
                    f"{snapshot['evidence_snapshot_id']}: {attribute_id} authorizes uncertainty propagation with unknown dependence"
                )
            if uncertainty.get("measure_type") == "STANDARD_ERROR" and uncertainty.get("standard_error") is None:
                errors.append(f"{snapshot['evidence_snapshot_id']}: {attribute_id} standard-error posture lacks value")

    for conflict in snapshot.get("conflicts", []):
        missing = sorted(set(conflict["source_receipt_ids"]) - receipt_ids)
        if missing:
            errors.append(
                f"{snapshot['evidence_snapshot_id']}: conflict {conflict['conflict_id']} references absent receipts: "
                + ", ".join(missing)
            )
    return errors


def validate_case(case: dict[str, Any], resolver, schemas: dict[str, dict[str, Any]], matrix: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    case_id = case["case_id"]
    request = case["request"]
    snapshot = case["snapshot"]
    expectation = case["expect"]

    errors.extend(schema_errors(request, schemas["request"], f"{case_id}: request schema"))
    errors.extend(schema_errors(snapshot, schemas["snapshot"], f"{case_id}: snapshot schema"))
    errors.extend(validate_snapshot_semantics(snapshot))
    if errors:
        return errors

    manifest, resolve_errors = resolver.resolve(request, snapshot, matrix)
    expected_success = expectation["resolver_success"]
    if expected_success and resolve_errors:
        errors.append(f"{case_id}: expected success but resolver failed: {'; '.join(resolve_errors)}")
        return errors
    if not expected_success:
        if not resolve_errors:
            errors.append(f"{case_id}: expected fail-closed resolver error but resolution succeeded")
            return errors
        needle = expectation.get("error_contains")
        if needle and not any(needle in item for item in resolve_errors):
            errors.append(f"{case_id}: expected error containing {needle!r}; got {resolve_errors}")
        return errors

    if manifest is None:
        errors.append(f"{case_id}: resolver returned no manifest")
        return errors
    errors.extend(schema_errors(manifest, schemas["boundary"], f"{case_id}: boundary schema"))
    if errors:
        return errors

    if manifest["completeness_state"] != expectation.get("completeness_state"):
        errors.append(
            f"{case_id}: completeness expected {expectation.get('completeness_state')} got {manifest['completeness_state']}"
        )
    boundaries = manifest["report_boundaries"]
    if boundaries["earliest_common_comparable_date"] != expectation.get("earliest_common_comparable_date"):
        errors.append(
            f"{case_id}: earliest common expected {expectation.get('earliest_common_comparable_date')} got {boundaries['earliest_common_comparable_date']}"
        )
    if boundaries["latest_common_complete_date"] != expectation.get("latest_common_complete_date"):
        errors.append(
            f"{case_id}: latest complete expected {expectation.get('latest_common_complete_date')} got {boundaries['latest_common_complete_date']}"
        )
    unsupported = expectation.get("unsupported_contains")
    if unsupported and unsupported not in boundaries["unsupported_requested_dimensions"]:
        errors.append(f"{case_id}: missing expected unsupported required attribute {unsupported}")

    # Determinism check: same request + same snapshot must hash identically.
    second, second_errors = resolver.resolve(request, snapshot, matrix)
    if second_errors or second is None:
        errors.append(f"{case_id}: deterministic replay failed")
    elif second["receipts"]["boundary_manifest_hash"] != manifest["receipts"]["boundary_manifest_hash"]:
        errors.append(f"{case_id}: deterministic replay changed manifest hash")
    return errors


def validate_delta_schema(schema: dict[str, Any]) -> list[str]:
    fixture = {
        "report_delta_id": "DELTA-TEST",
        "prior_report_id": "REPORT-A",
        "current_report_id": "REPORT-B",
        "prior_snapshot_id": "SNAP-A",
        "current_snapshot_id": "SNAP-B",
        "changes": [
            {
                "change_id": "CHANGE-1",
                "change_class": "NEW_OBSERVATION",
                "scope": "nominal_price",
                "attribute_id": "nominal_price",
                "prior_value_or_state": {"latest_observed_date": "2026-06-30"},
                "current_value_or_state": {"latest_observed_date": "2026-07-31"},
                "description": "July observation became available.",
                "finding_impact": "BOUNDARY_CHANGED",
                "source_receipt_ids": ["SRC-JULY"]
            }
        ],
        "material_change_state": "MATERIAL_BOUNDARY_CHANGE",
        "plain_language_summary": "The admissible report window advanced by one completed observation.",
        "delta_hash": "testhash"
    }
    return schema_errors(fixture, schema, "delta schema smoke test")


def main() -> int:
    request_schema = load(REQUEST_SCHEMA)
    snapshot_schema = load(SNAPSHOT_SCHEMA)
    boundary_schema = load(BOUNDARY_SCHEMA)
    delta_schema = load(DELTA_SCHEMA)
    matrix = load(MATRIX_PATH)
    cases = load(CASES_PATH)["cases"]
    resolver = load_resolver_module()

    failures: list[str] = []
    failures.extend(validate_matrix_alignment(request_schema, matrix))
    failures.extend(validate_delta_schema(delta_schema))
    schemas = {"request": request_schema, "snapshot": snapshot_schema, "boundary": boundary_schema}
    for case in cases:
        failures.extend(validate_case(case, resolver, schemas, matrix))

    if failures:
        for failure in failures:
            print(f"FAIL {failure}")
        return 1

    print(f"PASS claim-class alignment ({len(matrix['claim_classes'])} classes)")
    print(f"PASS boundary resolver fixtures ({len(cases)} cases)")
    print("PASS evidence snapshot semantics")
    print("PASS report delta schema smoke test")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
