#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
DICT_PATH = ROOT / "economic-trajectories/measurement-dictionary.v1.json"
CA_PATH = ROOT / "economic-trajectories/canada/trajectory.v1.json"
US_PATH = ROOT / "economic-trajectories/united-states/trajectory.v1.json"
OVERLAY_PATH = ROOT / "economic-trajectories/comparison/overlay.v1.json"
GAP_PATHS = [
    ROOT / "economic-trajectories/canada/gap-matrix.v1.json",
    ROOT / "economic-trajectories/united-states/gap-matrix.v1.json",
]
SCHEMAS = {
    "dictionary": ROOT / "schemas/economic-measurement-dictionary.schema.json",
    "national": ROOT / "schemas/national-economic-trajectory.schema.json",
    "overlay": ROOT / "schemas/economic-comparison-overlay.schema.json",
}


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def schema_errors(schema: dict[str, Any], document: dict[str, Any]) -> list[str]:
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    return [
        f"{'/'.join(str(part) for part in error.absolute_path) or '<root>'}: {error.message}"
        for error in sorted(validator.iter_errors(document), key=lambda item: list(item.absolute_path))
    ]


def validate_dictionary(document: dict[str, Any], schema: dict[str, Any]) -> list[str]:
    errors = schema_errors(schema, document)
    ids = [item.get("indicator_id") for item in document.get("indicators", [])]
    if len(ids) != len(set(ids)):
        errors.append("indicator_id values must be unique")
    return errors


def validate_national(
    document: dict[str, Any],
    schema: dict[str, Any],
    indicator_ids: set[str],
) -> list[str]:
    errors = schema_errors(schema, document)
    expected = {"ERL-ECON-CA": "Canada", "ERL-ECON-US": "United States"}
    if expected.get(document.get("lane_id")) != document.get("jurisdiction"):
        errors.append("lane_id and jurisdiction do not match")

    observations = document.get("observations", [])
    observation_ids = [item.get("observation_id") for item in observations]
    if len(observation_ids) != len(set(observation_ids)):
        errors.append("observation_id values must be unique")
    for item in observations:
        if item.get("indicator_id") not in indicator_ids:
            errors.append(f"{item.get('observation_id')}: unknown indicator_id")
        if item.get("effect_status") != "NOT_INFERRED_FROM_OBSERVATION":
            errors.append(f"{item.get('observation_id')}: observation inferred an effect")

    source_ids = {
        source.get("source_id")
        for observation in observations
        for source in observation.get("sources", [])
    }
    finding_ids: list[str] = []
    for finding in document.get("findings", []):
        finding_id = finding.get("finding_id")
        finding_ids.append(finding_id)
        unknown_observations = set(finding.get("observation_ids", [])) - set(observation_ids)
        if unknown_observations:
            errors.append(f"{finding_id}: unknown observations {sorted(unknown_observations)}")
        mechanism_sources = set(finding.get("mechanism", {}).get("evidence_source_ids", []))
        effect_sources = {
            source_id
            for effect in finding.get("effects", [])
            for source_id in effect.get("evidence_source_ids", [])
        }
        unknown_sources = (mechanism_sources | effect_sources) - source_ids
        if unknown_sources:
            errors.append(f"{finding_id}: unknown source IDs {sorted(unknown_sources)}")
        review = finding.get("review", {})
        if finding.get("status") == "reviewed":
            if not review.get("reviewer") or not review.get("reviewed_at"):
                errors.append(f"{finding_id}: reviewed finding lacks reviewer or reviewed_at")
            if not review.get("independent") or not review.get("reproducible"):
                errors.append(f"{finding_id}: reviewed finding lacks independent reproducible review")
    if len(finding_ids) != len(set(finding_ids)):
        errors.append("finding_id values must be unique")
    return errors


def reviewed_findings(document: dict[str, Any]) -> set[str]:
    return {
        finding["finding_id"]
        for finding in document.get("findings", [])
        if finding.get("status") == "reviewed"
        and finding.get("review", {}).get("independent") is True
        and finding.get("review", {}).get("reproducible") is True
        and finding.get("review", {}).get("reviewer")
        and finding.get("review", {}).get("reviewed_at")
    }


def validate_overlay(
    document: dict[str, Any],
    schema: dict[str, Any],
    canada: dict[str, Any],
    united_states: dict[str, Any],
) -> list[str]:
    errors = schema_errors(schema, document)
    ca_reviewed = reviewed_findings(canada)
    us_reviewed = reviewed_findings(united_states)
    comparison_ids: list[str] = []
    for comparison in document.get("comparisons", []):
        comparison_id = comparison.get("comparison_id")
        comparison_ids.append(comparison_id)
        if comparison.get("canada_finding_id") not in ca_reviewed:
            errors.append(f"{comparison_id}: Canada endpoint is not a reviewed national finding")
        if comparison.get("us_finding_id") not in us_reviewed:
            errors.append(f"{comparison_id}: U.S. endpoint is not a reviewed national finding")
        review = comparison.get("review", {})
        if comparison.get("status") == "reviewed":
            if not review.get("reviewer") or not review.get("reviewed_at"):
                errors.append(f"{comparison_id}: reviewed comparison lacks reviewer or reviewed_at")
            if not review.get("independent") or not review.get("reproducible"):
                errors.append(f"{comparison_id}: reviewed comparison lacks independent reproducible review")
    if len(comparison_ids) != len(set(comparison_ids)):
        errors.append("comparison_id values must be unique")
    return errors


def validate_gap_matrix(document: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required = {
        "gap_id",
        "claim_family",
        "supporting_evidence",
        "confidence",
        "contradictions",
        "missing_evidence",
        "next_targeted_query",
        "status",
    }
    for index, row in enumerate(document.get("rows", [])):
        missing = required - set(row)
        if missing:
            errors.append(f"row {index}: missing {sorted(missing)}")
        if not row.get("missing_evidence") and row.get("status") not in {"resolved", "superseded"}:
            errors.append(f"row {index}: open gap lacks missing_evidence")
        confidence = row.get("confidence")
        if not isinstance(confidence, (int, float)) or not 0 <= confidence <= 1:
            errors.append(f"row {index}: confidence must be within [0, 1]")
    if not document.get("rows"):
        errors.append("gap matrix must contain at least one row")
    return errors


def reviewed_finding(lane: str, observation: dict[str, Any]) -> dict[str, Any]:
    source_id = observation["sources"][0]["source_id"]
    return {
        "finding_id": f"{lane}-FIND-SELFTEST",
        "status": "reviewed",
        "observation_ids": [observation["observation_id"]],
        "mechanism": {
            "summary": "Deterministic validation-only mechanism.",
            "evidence_source_ids": [source_id],
            "alternatives": ["Deterministic validation-only alternative."],
        },
        "effects": [{
            "population": "validation fixture",
            "direction": "unresolved",
            "evidence_source_ids": [source_id],
        }],
        "controls": ["validation fixture control"],
        "contrary_evidence": ["validation fixture contrary evidence"],
        "confidence": 0.5,
        "review": {
            "reviewer": "independent-validation-fixture",
            "reviewed_at": "2026-08-25T00:00:00Z",
            "independent": True,
            "reproducible": True,
        },
    }


def run_self_tests(
    national_schema: dict[str, Any],
    overlay_schema: dict[str, Any],
    indicator_ids: set[str],
    canada: dict[str, Any],
    united_states: dict[str, Any],
    overlay: dict[str, Any],
) -> list[str]:
    failures: list[str] = []

    invalid_effect = copy.deepcopy(canada)
    invalid_effect["observations"][0]["effect_status"] = "INFERRED"
    if not validate_national(invalid_effect, national_schema, indicator_ids):
        failures.append("negative test accepted observation-level effect inference")

    ca_reviewed = copy.deepcopy(canada)
    us_reviewed = copy.deepcopy(united_states)
    ca_finding = reviewed_finding("ERL-ECON-CA", ca_reviewed["observations"][0])
    us_finding = reviewed_finding("ERL-ECON-US", us_reviewed["observations"][0])
    ca_reviewed["findings"].append(ca_finding)
    us_reviewed["findings"].append(us_finding)

    valid_overlay = copy.deepcopy(overlay)
    valid_overlay["comparisons"] = [{
        "comparison_id": "ERL-ECON-COMP-SELFTEST",
        "status": "reviewed",
        "canada_finding_id": ca_finding["finding_id"],
        "us_finding_id": us_finding["finding_id"],
        "aligned_dimensions": ["validation dimension"],
        "definition_reconciliation": ["validation reconciliation"],
        "mechanism_relation": "unresolved",
        "lag_analysis": {
            "status": "not-assessed",
            "lead_jurisdiction": "unresolved",
            "lag_years": None,
            "baseline_sensitivity": "validation fixture",
        },
        "controls": ["validation fixture control"],
        "gaps": ["validation fixture gap"],
        "confidence": 0.5,
        "review": {
            "reviewer": "independent-validation-fixture",
            "reviewed_at": "2026-08-25T00:00:00Z",
            "independent": True,
            "reproducible": True,
        },
    }]
    if validate_national(ca_reviewed, national_schema, indicator_ids):
        failures.append("positive Canada reviewed-finding fixture failed")
    if validate_national(us_reviewed, national_schema, indicator_ids):
        failures.append("positive U.S. reviewed-finding fixture failed")
    if validate_overlay(valid_overlay, overlay_schema, ca_reviewed, us_reviewed):
        failures.append("positive reviewed comparison fixture failed")

    missing_endpoint = copy.deepcopy(valid_overlay)
    missing_endpoint["comparisons"][0]["canada_finding_id"] = "ERL-ECON-CA-FIND-MISSING"
    if not validate_overlay(missing_endpoint, overlay_schema, ca_reviewed, us_reviewed):
        failures.append("negative test accepted nonexistent national finding")

    unreviewed_ca = copy.deepcopy(ca_reviewed)
    unreviewed_ca["findings"][0]["status"] = "candidate"
    unreviewed_ca["findings"][0]["review"] = {
        "reviewer": None,
        "reviewed_at": None,
        "independent": False,
        "reproducible": False,
    }
    if not validate_overlay(valid_overlay, overlay_schema, unreviewed_ca, us_reviewed):
        failures.append("negative test accepted unreviewed national finding")

    raw_endpoint = copy.deepcopy(valid_overlay)
    raw_endpoint["comparisons"][0]["canada_finding_id"] = canada["observations"][0]["observation_id"]
    if not validate_overlay(raw_endpoint, overlay_schema, ca_reviewed, us_reviewed):
        failures.append("negative test accepted raw observation as comparison endpoint")

    return failures


def main() -> int:
    schemas = {name: load(path) for name, path in SCHEMAS.items()}
    for name, schema in schemas.items():
        Draft202012Validator.check_schema(schema)

    dictionary = load(DICT_PATH)
    canada = load(CA_PATH)
    united_states = load(US_PATH)
    overlay = load(OVERLAY_PATH)
    indicator_ids = {item["indicator_id"] for item in dictionary.get("indicators", [])}

    errors: list[str] = []
    errors.extend(f"dictionary: {error}" for error in validate_dictionary(dictionary, schemas["dictionary"]))
    errors.extend(f"Canada: {error}" for error in validate_national(canada, schemas["national"], indicator_ids))
    errors.extend(f"United States: {error}" for error in validate_national(united_states, schemas["national"], indicator_ids))
    errors.extend(f"overlay: {error}" for error in validate_overlay(overlay, schemas["overlay"], canada, united_states))
    for path in GAP_PATHS:
        errors.extend(f"{path.relative_to(ROOT)}: {error}" for error in validate_gap_matrix(load(path)))
    errors.extend(f"self-test: {error}" for error in run_self_tests(
        schemas["national"], schemas["overlay"], indicator_ids, canada, united_states, overlay
    ))

    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1

    print(json.dumps({
        "status": "PASS",
        "canada_observations": len(canada["observations"]),
        "canada_findings": len(canada["findings"]),
        "us_observations": len(united_states["observations"]),
        "us_findings": len(united_states["findings"]),
        "comparison_hypotheses": len(overlay["hypotheses"]),
        "comparisons": len(overlay["comparisons"]),
        "negative_tests": 4,
        "publication_authorized": False,
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
