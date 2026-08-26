#!/usr/bin/env python3
"""Resolve deterministic Physical Economics report boundaries.

Inputs are a report request and an immutable evidence snapshot. Claim-to-attribute
pertinence comes only from the versioned matrix. The resolver never fills missing
required evidence with contextual evidence and never manufactures a common window
when required attributes do not support one.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from datetime import date
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
REQUEST_SCHEMA = ROOT / "schemas" / "physical-economics-report-request.schema.json"
SNAPSHOT_SCHEMA = ROOT / "schemas" / "physical-economics-evidence-snapshot.schema.json"
BOUNDARY_SCHEMA = ROOT / "schemas" / "physical-economics-report-boundary-manifest.schema.json"
PERTINENCE_MATRIX = ROOT / "contracts" / "physical-economics-report-pertinence.matrix.v0.1.json"
CONTRACT_VERSION = "physical-economics-report-generation.v0.1"

BLOCKING_STATES = {"PENDING_RELEASE", "UNAVAILABLE", "OPAQUE"}
PARTIAL_STATES = {"PARTIAL_CURRENT_PERIOD", "METHODOLOGY_BREAK"}
COMPARABLE_STATES = {"COMPARABLE", "BRIDGED", "NO_PRIOR_REGIME"}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def validate(data: Any, schema: dict[str, Any], label: str) -> list[str]:
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    return [f"{label}: {error.message}" for error in validator.iter_errors(data)]


def union_in_order(groups: list[list[str]]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for group in groups:
        for item in group:
            if item not in seen:
                seen.add(item)
                result.append(item)
    return result


def resolve_pertinence(request: dict[str, Any], matrix: dict[str, Any]) -> tuple[list[str], list[str], list[str]]:
    requested_version = request["pertinence_policy"]["required_attribute_sets_version"]
    matrix_version = matrix["contract_version"]
    errors: list[str] = []
    if requested_version != matrix_version:
        errors.append(
            f"pertinence matrix version mismatch: request={requested_version} matrix={matrix_version}"
        )

    claim_map = matrix["claim_classes"]
    missing_claims = [claim for claim in request["claim_classes"] if claim not in claim_map]
    if missing_claims:
        errors.append("claim classes absent from pertinence matrix: " + ", ".join(sorted(missing_claims)))

    if errors:
        return [], [], errors

    required = union_in_order([claim_map[c]["required"] for c in request["claim_classes"]])
    contextual = union_in_order([claim_map[c].get("contextual", []) for c in request["claim_classes"]])

    user_requested = request["pertinence_policy"].get("user_requested_attributes", [])
    if request["pertinence_policy"]["allow_optional_context_attributes"]:
        contextual = union_in_order([contextual, user_requested])

    excluded = set(request["pertinence_policy"].get("excluded_attributes", []))
    excluded_required = sorted(excluded.intersection(required))
    if excluded_required:
        errors.append(
            "request excludes required attributes and therefore fails closed: "
            + ", ".join(excluded_required)
        )

    contextual = [item for item in contextual if item not in excluded and item not in required]
    return required, contextual, errors


def opaque_boundary(attribute_id: str) -> dict[str, Any]:
    return {
        "attribute_id": attribute_id,
        "required_for_claim_class": True,
        "earliest_admissible_date": None,
        "latest_observed_date": None,
        "latest_complete_date": None,
        "current_period_state": "OPAQUE",
        "release_or_observation_lag_days": None,
        "methodology_regime_id": "UNKNOWN",
        "comparability_with_prior_regime": "UNRESOLVED",
        "revision_vintage": "UNKNOWN",
        "source_release_date": None,
        "observation_reference_period": None,
        "geography_scope": "UNKNOWN",
        "population_scope": "UNKNOWN",
        "unit_scope": "UNKNOWN",
        "source_authority": "UNKNOWN",
        "provenance_posture": "UNKNOWN",
        "missingness_posture": "OPAQUE",
        "uncertainty": None,
        "opaque_elements": [f"required attribute {attribute_id} absent from evidence snapshot"],
    }


def snapshot_to_boundary(attribute: dict[str, Any], required: bool) -> dict[str, Any]:
    return {
        "attribute_id": attribute["attribute_id"],
        "required_for_claim_class": required,
        "earliest_admissible_date": attribute["earliest_admissible_date"],
        "latest_observed_date": attribute["latest_observed_date"],
        "latest_complete_date": attribute["latest_complete_date"],
        "current_period_state": attribute["current_period_state"],
        "release_or_observation_lag_days": attribute.get("release_or_observation_lag_days"),
        "methodology_regime_id": attribute["methodology_regime_id"],
        "comparability_with_prior_regime": attribute["comparability_with_prior_regime"],
        "revision_vintage": attribute["revision_vintage"],
        "source_release_date": attribute.get("source_release_date"),
        "observation_reference_period": attribute.get("observation_reference_period"),
        "geography_scope": attribute["geography_scope"],
        "population_scope": attribute["population_scope"],
        "unit_scope": attribute["unit_scope"],
        "source_authority": attribute["source_authority"],
        "provenance_posture": attribute["provenance_posture"],
        "missingness_posture": attribute["missingness_posture"],
        "uncertainty": copy.deepcopy(attribute.get("uncertainty")),
        "opaque_elements": copy.deepcopy(attribute.get("opaque_elements", [])),
    }


def parse_date(value: str | None) -> date | None:
    return date.fromisoformat(value) if value else None


def date_max(values: list[str]) -> str | None:
    return max(values, key=parse_date) if values else None


def date_min(values: list[str]) -> str | None:
    return min(values, key=parse_date) if values else None


def classify_completeness(required_boundaries: list[dict[str, Any]]) -> str:
    if not required_boundaries:
        return "NOT_GENERATABLE_FAIL_CLOSED"
    opaque = [
        b for b in required_boundaries
        if b["current_period_state"] in BLOCKING_STATES
        or b["missingness_posture"] in {"MISSING", "OPAQUE"}
    ]
    observed_count = sum(b["missingness_posture"] in {"OBSERVED", "PARTIAL"} for b in required_boundaries)
    if opaque:
        return "MATERIAL_ATTRIBUTES_OPAQUE" if observed_count else "NOT_GENERATABLE_FAIL_CLOSED"
    if any(
        b["current_period_state"] in PARTIAL_STATES or b["missingness_posture"] == "PARTIAL"
        for b in required_boundaries
    ):
        return "PARTIAL_WITH_DISCLOSED_GAPS"
    if any(b["comparability_with_prior_regime"] not in COMPARABLE_STATES for b in required_boundaries):
        return "PARTIAL_WITH_DISCLOSED_GAPS"
    return "COMPLETE_WITHIN_BOUNDARY"


def build_boundary_statement(
    completeness: str,
    earliest_common: str | None,
    latest_complete: str | None,
    missing_required: list[str],
    partial_required: list[str],
    methodology_breaks: list[str],
) -> str:
    pieces = [f"Report completeness: {completeness}."]
    if earliest_common and latest_complete:
        pieces.append(
            f"Common required-attribute comparable/complete window: {earliest_common} through {latest_complete}."
        )
    else:
        pieces.append("No single common comparable and complete window is established across all required attributes.")
    if missing_required:
        pieces.append("Required attributes currently unavailable or opaque: " + ", ".join(missing_required) + ".")
    if partial_required:
        pieces.append("Required attributes with incomplete current-period evidence: " + ", ".join(partial_required) + ".")
    if methodology_breaks:
        pieces.append("Methodology/comparability boundaries remain visible for: " + ", ".join(methodology_breaks) + ".")
    pieces.append(
        "Longer attribute-specific history may be shown as context but does not extend the admissible conclusion window."
    )
    return " ".join(pieces)


def resolve(
    request: dict[str, Any], snapshot: dict[str, Any], matrix: dict[str, Any]
) -> tuple[dict[str, Any] | None, list[str]]:
    required, contextual, errors = resolve_pertinence(request, matrix)
    if errors:
        return None, errors
    if snapshot["report_request_id"] != request["report_request_id"]:
        return None, ["evidence snapshot report_request_id does not match request"]
    if snapshot["requested_as_of_time"] != request["requested_as_of_time"]:
        return None, ["evidence snapshot requested_as_of_time does not match request"]
    if snapshot["pertinence_matrix_version"] != matrix["contract_version"]:
        return None, ["evidence snapshot pertinence_matrix_version does not match active matrix"]

    by_id = {item["attribute_id"]: item for item in snapshot["attributes"]}
    boundaries: list[dict[str, Any]] = []
    for attribute_id in required:
        boundaries.append(
            snapshot_to_boundary(by_id[attribute_id], True)
            if attribute_id in by_id
            else opaque_boundary(attribute_id)
        )
    for attribute_id in contextual:
        if attribute_id in by_id:
            boundaries.append(snapshot_to_boundary(by_id[attribute_id], False))

    required_boundaries = [b for b in boundaries if b["required_for_claim_class"]]
    missing_required = [
        b["attribute_id"]
        for b in required_boundaries
        if b["current_period_state"] in BLOCKING_STATES
        or b["missingness_posture"] in {"MISSING", "OPAQUE"}
    ]
    partial_required = [
        b["attribute_id"]
        for b in required_boundaries
        if b["current_period_state"] in PARTIAL_STATES or b["missingness_posture"] == "PARTIAL"
    ]
    methodology_breaks = [
        b["attribute_id"]
        for b in required_boundaries
        if b["current_period_state"] == "METHODOLOGY_BREAK"
        or b["comparability_with_prior_regime"] in {"NOT_COMPARABLE", "UNRESOLVED"}
    ]

    comparable_required = [
        b for b in required_boundaries
        if b["comparability_with_prior_regime"] in COMPARABLE_STATES
        and b["missingness_posture"] in {"OBSERVED", "PARTIAL"}
        and b["current_period_state"] not in BLOCKING_STATES
    ]
    all_required_comparable = len(comparable_required) == len(required_boundaries)
    earliest_values = [
        b["earliest_admissible_date"] for b in comparable_required if b["earliest_admissible_date"]
    ]
    complete_values = [b["latest_complete_date"] for b in comparable_required if b["latest_complete_date"]]
    earliest_common = (
        date_max(earliest_values)
        if all_required_comparable and len(earliest_values) == len(required_boundaries)
        else None
    )
    latest_complete = (
        date_min(complete_values)
        if all_required_comparable and len(complete_values) == len(required_boundaries)
        else None
    )

    report_as_of_date = request["requested_as_of_time"][:10]
    historical_depth: dict[str, int | None] = {}
    for boundary in boundaries:
        start = parse_date(boundary["earliest_admissible_date"])
        historical_depth[boundary["attribute_id"]] = (
            (date.fromisoformat(report_as_of_date) - start).days if start else None
        )

    completeness = classify_completeness(required_boundaries)
    statement = build_boundary_statement(
        completeness,
        earliest_common,
        latest_complete,
        missing_required,
        partial_required,
        methodology_breaks,
    )

    request_hash = digest(request)
    manifest: dict[str, Any] = {
        "boundary_manifest_id": f"PE-BM-{request_hash[:16]}",
        "report_request_id": request["report_request_id"],
        "report_as_of_time": request["requested_as_of_time"],
        "evidence_snapshot_id": snapshot["evidence_snapshot_id"],
        "attribute_boundaries": boundaries,
        "report_boundaries": {
            "earliest_common_comparable_date": earliest_common,
            "latest_common_complete_date": latest_complete,
            "historical_depth_by_attribute": historical_depth,
            "partial_current_period_components": partial_required,
            "methodology_breaks": methodology_breaks,
            "revision_vintages": sorted({b["revision_vintage"] for b in boundaries}),
            "unsupported_requested_dimensions": missing_required,
        },
        "completeness_state": completeness,
        "boundary_statement": statement,
        "receipts": {
            "report_request_hash": request_hash,
            "evidence_snapshot_hash": snapshot["snapshot_hash"],
            "boundary_manifest_hash": "PENDING",
            "source_receipt_set": [item["source_receipt_id"] for item in snapshot["source_receipts"]],
            "renderer_version": None,
            "contract_version": CONTRACT_VERSION,
            "pertinence_matrix_version": matrix["contract_version"],
        },
    }
    hashable = copy.deepcopy(manifest)
    hashable["receipts"]["boundary_manifest_hash"] = ""
    manifest["receipts"]["boundary_manifest_hash"] = digest(hashable)
    return manifest, []


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("request", type=Path)
    parser.add_argument("snapshot", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    request = load(args.request)
    snapshot = load(args.snapshot)
    request_schema = load(REQUEST_SCHEMA)
    snapshot_schema = load(SNAPSHOT_SCHEMA)
    boundary_schema = load(BOUNDARY_SCHEMA)
    matrix = load(PERTINENCE_MATRIX)

    failures = validate(request, request_schema, "request") + validate(snapshot, snapshot_schema, "snapshot")
    if failures:
        for failure in failures:
            print(f"FAIL {failure}", file=sys.stderr)
        return 1

    manifest, failures = resolve(request, snapshot, matrix)
    if failures or manifest is None:
        for failure in failures:
            print(f"FAIL {failure}", file=sys.stderr)
        return 1

    failures = validate(manifest, boundary_schema, "boundary manifest")
    if failures:
        for failure in failures:
            print(f"FAIL {failure}", file=sys.stderr)
        return 1

    encoded = json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded, encoding="utf-8")
    else:
        print(encoded, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
