#!/usr/bin/env python3
"""Validate Physical Economics public-reporting contracts and runtime behavior."""

from __future__ import annotations

import importlib.util
import json
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
DELTA_RUNTIME_PATH = ROOT / "scripts" / "generate_physical_economics_report_delta.py"
UNCERTAINTY_PATH = ROOT / "scripts" / "physical_economics_uncertainty.py"


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to load {path}")
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
    if request_claims != matrix_claims:
        errors.append(
            "claim-class mismatch: request-only="
            + ",".join(sorted(request_claims - matrix_claims))
            + " matrix-only="
            + ",".join(sorted(matrix_claims - request_claims))
        )
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
    seen: set[str] = set()
    for attribute in snapshot["attributes"]:
        attribute_id = attribute["attribute_id"]
        if attribute_id in seen:
            errors.append(f"{snapshot['evidence_snapshot_id']}: duplicate attribute {attribute_id}")
        seen.add(attribute_id)
        missing = sorted(set(attribute["source_receipt_ids"]) - receipt_ids)
        if missing:
            errors.append(f"{snapshot['evidence_snapshot_id']}: {attribute_id} missing receipts {missing}")
        uncertainty = attribute.get("uncertainty") or {}
        if uncertainty.get("dependence_posture") == "UNKNOWN_DEPENDENCE" and uncertainty.get("propagation_authorized"):
            errors.append(f"{snapshot['evidence_snapshot_id']}: {attribute_id} propagates unknown dependence")
        if uncertainty.get("measure_type") == "STANDARD_ERROR" and uncertainty.get("standard_error") is None:
            errors.append(f"{snapshot['evidence_snapshot_id']}: {attribute_id} lacks standard-error value")
    for conflict in snapshot.get("conflicts", []):
        missing = sorted(set(conflict["source_receipt_ids"]) - receipt_ids)
        if missing:
            errors.append(f"{snapshot['evidence_snapshot_id']}: conflict {conflict['conflict_id']} missing receipts {missing}")
    return errors


def validate_case(case: dict[str, Any], resolver, schemas: dict[str, dict[str, Any]], matrix: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    case_id = case["case_id"]
    request = case["request"]
    snapshot = case["snapshot"]
    expect = case["expect"]
    errors.extend(schema_errors(request, schemas["request"], f"{case_id}: request"))
    errors.extend(schema_errors(snapshot, schemas["snapshot"], f"{case_id}: snapshot"))
    errors.extend(validate_snapshot_semantics(snapshot))
    if errors:
        return errors

    manifest, resolve_errors = resolver.resolve(request, snapshot, matrix)
    if expect["resolver_success"]:
        if resolve_errors or manifest is None:
            return [f"{case_id}: expected success, got {resolve_errors}"]
        errors.extend(schema_errors(manifest, schemas["boundary"], f"{case_id}: boundary"))
        if manifest["completeness_state"] != expect.get("completeness_state"):
            errors.append(f"{case_id}: completeness mismatch")
        bounds = manifest["report_boundaries"]
        if bounds["earliest_common_comparable_date"] != expect.get("earliest_common_comparable_date"):
            errors.append(f"{case_id}: earliest common boundary mismatch")
        if bounds["latest_common_complete_date"] != expect.get("latest_common_complete_date"):
            errors.append(f"{case_id}: latest common boundary mismatch")
        unsupported = expect.get("unsupported_contains")
        if unsupported and unsupported not in bounds["unsupported_requested_dimensions"]:
            errors.append(f"{case_id}: expected unsupported attribute {unsupported}")
        if manifest["receipts"]["evidence_snapshot_hash"] != snapshot["snapshot_hash"]:
            errors.append(f"{case_id}: boundary receipt does not bind snapshot hash")
        if manifest["receipts"]["pertinence_matrix_version"] != matrix["contract_version"]:
            errors.append(f"{case_id}: boundary receipt does not bind pertinence version")
        replay, replay_errors = resolver.resolve(request, snapshot, matrix)
        if replay_errors or replay is None or replay["receipts"]["boundary_manifest_hash"] != manifest["receipts"]["boundary_manifest_hash"]:
            errors.append(f"{case_id}: deterministic replay changed boundary hash")
    else:
        if not resolve_errors:
            errors.append(f"{case_id}: expected fail-closed resolution")
        needle = expect.get("error_contains")
        if needle and not any(needle in item for item in resolve_errors):
            errors.append(f"{case_id}: expected error containing {needle!r}; got {resolve_errors}")
    return errors


def validate_uncertainty_runtime(uncertainty) -> list[str]:
    errors: list[str] = []
    independent = [
        {"uncertainty": {"measure_type": "STANDARD_ERROR", "standard_error": 2.0, "dependence_posture": "KNOWN_INDEPENDENT"}},
        {"uncertainty": {"measure_type": "STANDARD_ERROR", "standard_error": 3.0, "dependence_posture": "KNOWN_INDEPENDENT"}},
    ]
    result = uncertainty.propagate_linear_standard_error(independent, [1.0, 1.0])
    if result.get("status") != "PROPAGATED" or abs(result.get("standard_error", 0) - (13 ** 0.5)) > 1e-12:
        errors.append("uncertainty: independent propagation failed")
    unknown = [dict(independent[0]), dict(independent[1])]
    unknown[1] = {"uncertainty": {"measure_type": "STANDARD_ERROR", "standard_error": 3.0, "dependence_posture": "UNKNOWN_DEPENDENCE"}}
    result = uncertainty.propagate_linear_standard_error(unknown, [1.0, 1.0])
    if result.get("status") != "UNRESOLVED":
        errors.append("uncertainty: unknown dependence did not fail closed")
    bounded = uncertainty.combine_interval_bounds(
        [{"uncertainty": {"lower_bound": 1, "upper_bound": 2}}, {"uncertainty": {"lower_bound": 3, "upper_bound": 5}}],
        [1.0, -1.0],
    )
    if bounded.get("status") != "BOUNDED" or bounded.get("lower_bound") != -4.0 or bounded.get("upper_bound") != -1.0:
        errors.append("uncertainty: interval arithmetic failed")
    return errors


def validate_delta_runtime(delta_runtime, delta_schema: dict[str, Any]) -> list[str]:
    prior_snapshot = {
        "evidence_snapshot_id": "SNAP-A",
        "attributes": [{"attribute_id": "nominal_price", "latest_observed_date": "2026-06-30", "latest_complete_date": "2026-06-30", "methodology_regime_id": "V1", "revision_vintage": "R1", "missingness_posture": "OBSERVED", "uncertainty": None, "source_receipt_ids": ["SRC-A"]}],
        "source_receipts": [{"source_receipt_id": "SRC-A", "revision_status": "CURRENT_VINTAGE"}],
        "conflicts": [],
    }
    current_snapshot = {
        "evidence_snapshot_id": "SNAP-B",
        "attributes": [{"attribute_id": "nominal_price", "latest_observed_date": "2026-07-31", "latest_complete_date": "2026-07-31", "methodology_regime_id": "V1", "revision_vintage": "R2", "missingness_posture": "OBSERVED", "uncertainty": None, "source_receipt_ids": ["SRC-B"]}],
        "source_receipts": [{"source_receipt_id": "SRC-B", "revision_status": "CURRENT_VINTAGE"}],
        "conflicts": [],
    }
    prior_manifest = {"receipts": {"pertinence_matrix_version": "0.1", "contract_version": "v1", "renderer_version": None}}
    current_manifest = {"receipts": {"pertinence_matrix_version": "0.1", "contract_version": "v1", "renderer_version": None}}
    delta = delta_runtime.generate("REPORT-A", "REPORT-B", prior_snapshot, current_snapshot, prior_manifest, current_manifest)
    errors = schema_errors(delta, delta_schema, "delta runtime")
    classes = {item["change_class"] for item in delta["changes"]}
    if "NEW_OBSERVATION" not in classes or "PRIOR_PERIOD_COMPLETED" not in classes or "ROUTINE_REVISION" not in classes:
        errors.append("delta runtime: expected observation/completion/revision changes not emitted")
    return errors


def main() -> int:
    request_schema = load(REQUEST_SCHEMA)
    snapshot_schema = load(SNAPSHOT_SCHEMA)
    boundary_schema = load(BOUNDARY_SCHEMA)
    delta_schema = load(DELTA_SCHEMA)
    matrix = load(MATRIX_PATH)
    cases = load(CASES_PATH)["cases"]
    resolver = load_module(RESOLVER_PATH, "physical_economics_boundary_resolver")
    delta_runtime = load_module(DELTA_RUNTIME_PATH, "physical_economics_report_delta")
    uncertainty = load_module(UNCERTAINTY_PATH, "physical_economics_uncertainty")

    failures: list[str] = []
    failures.extend(validate_matrix_alignment(request_schema, matrix))
    schemas = {"request": request_schema, "snapshot": snapshot_schema, "boundary": boundary_schema}
    for case in cases:
        failures.extend(validate_case(case, resolver, schemas, matrix))
    failures.extend(validate_uncertainty_runtime(uncertainty))
    failures.extend(validate_delta_runtime(delta_runtime, delta_schema))

    if failures:
        for failure in failures:
            print(f"FAIL {failure}")
        return 1

    print(f"PASS claim-class alignment ({len(matrix['claim_classes'])} classes)")
    print(f"PASS boundary resolver fixtures ({len(cases)} cases)")
    print("PASS evidence snapshot semantics")
    print("PASS uncertainty fail-closed runtime")
    print("PASS report delta runtime")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
