#!/usr/bin/env python3
"""Deterministic validation for the Physical Economics fail-closed HTTP adapter."""

from __future__ import annotations

import copy
import importlib.util
import json
import tempfile
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
ADAPTER_PATH = ROOT / "scripts" / "serve_physical_economics_public_report.py"
REGISTRY_PATH = ROOT / "tests" / "physical-economics-reporting" / "http-adapter.registry.fixture.json"
REGISTRY_SCHEMA = ROOT / "schemas" / "physical-economics-report-snapshot-registry.schema.json"
SNAPSHOT_PATH = ROOT / "tests" / "physical-economics-reporting" / "http-adapter.snapshot.fixture.json"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def request(
    request_id: str = "REQ-HTTP-001",
    *,
    as_of: str = "2026-08-26T20:35:00Z",
    vintage: str = "CURRENT_VINTAGE",
    geography: str = "US",
) -> dict[str, Any]:
    return {
        "report_request_id": request_id,
        "question": "How did the effective nominal price change?",
        "requested_as_of_time": as_of,
        "scope": {
            "subject": "test basket",
            "economic_domain": "food",
            "geography": geography,
            "population_scope": "all consumer units",
            "essential_or_discretionary_class": "ESSENTIAL",
            "unit_definition": "standardized unit",
            "requested_start_date": "2024-01-01",
            "requested_end_date": "2026-07-31",
        },
        "claim_classes": ["PRICE_CHANGE"],
        "pertinence_policy": {
            "mode": "DETERMINISTIC_CLAIM_CLASS_MAPPING",
            "required_attribute_sets_version": "0.1",
            "allow_optional_context_attributes": True,
            "user_requested_attributes": [],
            "excluded_attributes": [],
        },
        "vintage_policy": vintage,
        "output_preferences": {
            "include_state_vector": True,
            "include_data_coverage_matrix": True,
            "include_prospective_evidence_gates": True,
            "include_source_receipts": True,
            "include_uncertainty_surface": True,
        },
    }


def expect_adapter_error(adapter, code: str, fn, failures: list[str]) -> None:
    try:
        fn()
    except adapter.AdapterError as exc:
        if exc.code != code:
            failures.append(f"expected {code}, received {exc.code}")
    else:
        failures.append(f"expected fail-closed error {code}")


def main() -> int:
    adapter = load_module(ADAPTER_PATH, "pe_http_adapter")
    failures: list[str] = []

    registry = load(REGISTRY_PATH)
    schema = load(REGISTRY_SCHEMA)
    schema_errors = list(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(registry))
    if schema_errors:
        failures.extend(f"registry schema: {error.message}" for error in schema_errors)

    canonical_request = request()
    selected = adapter.select_registry_entry(registry, canonical_request)
    if selected.get("registry_entry_id") != "PE-HTTP-FIXTURE-PRICE-US":
        failures.append("exact registry selection did not return the admitted fixture")

    template = load(SNAPSHOT_PATH)
    bound = adapter.bind_snapshot(template, canonical_request)
    if bound["report_request_id"] != canonical_request["report_request_id"]:
        failures.append("snapshot request identity was not rebound")
    if bound["requested_as_of_time"] != canonical_request["requested_as_of_time"]:
        failures.append("snapshot as-of time was not rebound")
    if bound["attributes"] != template["attributes"]:
        failures.append("transport mutated evidence attributes while binding request identity")
    if bound["source_receipts"] != template["source_receipts"]:
        failures.append("transport mutated source receipts while binding request identity")

    expect_adapter_error(
        adapter,
        "NO_ADMITTED_SNAPSHOT",
        lambda: adapter.select_registry_entry(registry, request(geography="CA")),
        failures,
    )

    duplicate_registry = copy.deepcopy(registry)
    duplicate = copy.deepcopy(duplicate_registry["entries"][0])
    duplicate["registry_entry_id"] = "PE-HTTP-FIXTURE-DUPLICATE"
    duplicate_registry["entries"].append(duplicate)
    expect_adapter_error(
        adapter,
        "AMBIGUOUS_ADMITTED_SNAPSHOT",
        lambda: adapter.select_registry_entry(duplicate_registry, canonical_request),
        failures,
    )

    expect_adapter_error(
        adapter,
        "HISTORICAL_VINTAGE_VIOLATION",
        lambda: adapter.bind_snapshot(
            template,
            request(
                request_id="REQ-HTTP-HISTORICAL",
                as_of="2026-08-01T00:00:00Z",
                vintage="AS_KNOWN_AT_REQUESTED_TIME",
            ),
        ),
        failures,
    )

    response = adapter.generate_response(canonical_request, REGISTRY_PATH)
    if response.get("state") != "GENERATED_NOT_PUBLICLY_ACTIVATED":
        failures.append("successful adapter transaction returned an inadmissible backend state")
    document = response.get("report_document")
    receipt = response.get("verification_receipt")
    if not isinstance(document, dict):
        failures.append("adapter did not return report_document object")
    if not isinstance(receipt, dict):
        failures.append("adapter did not return verification_receipt object")
    if not isinstance(response.get("report_markdown"), str) or not response["report_markdown"].strip():
        failures.append("adapter did not return report_markdown")
    if isinstance(receipt, dict) and receipt.get("verification_state") != "VERIFIABLE":
        failures.append("adapter returned a non-VERIFIABLE receipt as success")
    if isinstance(document, dict) and isinstance(receipt, dict):
        if document.get("report_id") != receipt.get("report_id"):
            failures.append("report document and receipt report_id differ")
        boundary = document.get("boundary")
        if not isinstance(boundary, dict) or boundary.get("completeness_state") != "COMPLETE_WITHIN_BOUNDARY":
            failures.append("fixture report did not preserve complete evidence boundary")
    if any(key in response for key in ("evidence_snapshot", "boundary_manifest", "report_document_path")):
        failures.append("adapter leaked repository/runtime output paths into public response")

    # Invalid registry state must fail before report execution.
    with tempfile.TemporaryDirectory(prefix="pe-http-validator-") as tmp:
        bad_registry_path = Path(tmp) / "registry.json"
        bad_registry = copy.deepcopy(registry)
        bad_registry["entries"][0]["state"] = "UNKNOWN"
        bad_registry_path.write_text(json.dumps(bad_registry), encoding="utf-8")
        expect_adapter_error(
            adapter,
            "INVALID_REGISTRY",
            lambda: adapter.generate_response(canonical_request, bad_registry_path),
            failures,
        )

    if failures:
        for failure in failures:
            print(f"FAIL {failure}")
        return 1

    print("PASS Physical Economics HTTP registry schema")
    print("PASS exact admitted snapshot selection")
    print("PASS ambiguous and unmatched snapshot fail-closed behavior")
    print("PASS historical-vintage release guard")
    print("PASS transport preserves evidence attributes and source receipts")
    print("PASS governed report transaction returns VERIFIABLE Site-compatible response")
    print("PASS public response omits runtime paths")
    print("PASS invalid registry fails before execution")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
