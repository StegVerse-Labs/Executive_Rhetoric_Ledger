#!/usr/bin/env python3
"""Validate the governed Iran-Jordan-FirstNet research assessment.

This validator checks structure and promotion boundaries. It does not validate
external facts or replace independent review.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ASSESSMENT = ROOT / "assessments/pit/PIT-MODERN-2026-IRAN-JORDAN-FIRSTNET.assessment.json"
CHRONOLOGY = ROOT / "assessments/chronology/2026-07-28-30-iran-jordan-firstnet.normalized.json"
CONTRADICTIONS = ROOT / "assessments/contradictions/2026-07-iran-jordan-firstnet.matrix.md"

ALLOWED_PRECISION = {"exact", "minute", "hour", "approximate", "unknown"}
REQUIRED_PROHIBITED_COLLAPSES = {
    "five_intercepted_equals_five_launched",
    "prepared_target_architecture_equals_preauthorized_execution",
    "simultaneous_network_degradation_equals_common_cause",
    "firstnet_degradation_equals_iranian_compromise",
    "jordanian_interception_equals_voluntary_political_alignment",
    "rapid_rhetoric_equals_prior_orchestration",
}
REQUIRED_PROMOTION_REQUIREMENTS = {
    "primary_source_capture_and_hashes",
    "normalized_timestamp_receipt",
    "claim_level_contradiction_matrix",
    "independent_review_receipt",
    "machine_validation_pass",
}


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise ValueError(f"missing required file: {path.relative_to(ROOT)}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON in {path.relative_to(ROOT)}: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"top-level JSON must be an object: {path.relative_to(ROOT)}")
    return data


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def validate_assessment(data: dict[str, Any], errors: list[str]) -> None:
    require(data.get("assessment_id") == "PIT-MODERN-2026-IRAN-JORDAN-FIRSTNET", "incorrect assessment_id", errors)
    require(data.get("status") == "research_candidate", "status must remain research_candidate", errors)
    require(data.get("final_finding") is False, "final_finding must be false", errors)

    observations = data.get("observations")
    require(isinstance(observations, list) and len(observations) >= 6, "at least six observations are required", errors)
    if isinstance(observations, list):
        ids = [item.get("id") for item in observations if isinstance(item, dict)]
        require(len(ids) == len(set(ids)), "observation IDs must be unique", errors)
        for item in observations:
            if not isinstance(item, dict):
                errors.append("each observation must be an object")
                continue
            require(bool(item.get("claim")), f"{item.get('id', 'unknown observation')} missing claim", errors)
            require(bool(item.get("posture")), f"{item.get('id', 'unknown observation')} missing posture", errors)

    hypotheses = data.get("hypotheses")
    require(isinstance(hypotheses, list) and len(hypotheses) >= 6, "six competing hypotheses are required", errors)
    if isinstance(hypotheses, list):
        hypothesis_ids = {item.get("id") for item in hypotheses if isinstance(item, dict)}
        require({"H1", "H2", "H3", "H4", "H5", "H6"}.issubset(hypothesis_ids), "H1-H6 must all be present", errors)

    prohibited = set(data.get("prohibited_collapses", []))
    missing_prohibited = REQUIRED_PROHIBITED_COLLAPSES - prohibited
    require(not missing_prohibited, f"missing prohibited collapses: {sorted(missing_prohibited)}", errors)

    promotion = set(data.get("promotion_requirements", []))
    missing_promotion = REQUIRED_PROMOTION_REQUIREMENTS - promotion
    require(not missing_promotion, f"missing promotion requirements: {sorted(missing_promotion)}", errors)

    determination = data.get("current_determination")
    require(isinstance(determination, dict), "current_determination must be an object", errors)
    if isinstance(determination, dict):
        inadmissible = str(determination.get("inadmissible_statement", "")).lower()
        require("orchestrated" in inadmissible and "firstnet" in inadmissible, "inadmissible statement must preserve both orchestration and FirstNet boundaries", errors)
        require(determination.get("review_state") == "open", "review_state must remain open", errors)


def validate_chronology(data: dict[str, Any], errors: list[str]) -> None:
    require(data.get("status") == "incomplete", "chronology status must remain incomplete until primary captures exist", errors)
    policy = data.get("normalization_policy")
    require(isinstance(policy, dict), "normalization_policy must be an object", errors)
    if isinstance(policy, dict):
        require(policy.get("canonical_timezone") == "UTC", "canonical timezone must be UTC", errors)
        require(policy.get("retain_source_timezone") is True, "source timezone retention must be enabled", errors)

    events = data.get("events")
    require(isinstance(events, list) and len(events) >= 8, "at least eight chronology events are required", errors)
    if not isinstance(events, list):
        return

    ids: list[str] = []
    for event in events:
        if not isinstance(event, dict):
            errors.append("each chronology event must be an object")
            continue
        event_id = str(event.get("id", ""))
        ids.append(event_id)
        require(event.get("precision") in ALLOWED_PRECISION, f"{event_id} has invalid precision", errors)
        require(bool(event.get("posture")), f"{event_id} missing posture", errors)
        if event.get("event_time_utc") is not None:
            require(event.get("precision") != "unknown", f"{event_id} cannot have a timestamp with unknown precision", errors)
            require(bool(event.get("source_local_time")), f"{event_id} normalized timestamp requires retained source_local_time", errors)
            require(bool(event.get("source_timezone")), f"{event_id} normalized timestamp requires retained source_timezone", errors)
    require(len(ids) == len(set(ids)), "chronology event IDs must be unique", errors)


def main() -> int:
    errors: list[str] = []
    try:
        assessment = load_json(ASSESSMENT)
        chronology = load_json(CHRONOLOGY)
    except ValueError as exc:
        print(f"FAIL: {exc}")
        return 1

    require(CONTRADICTIONS.exists(), "missing contradiction matrix", errors)
    validate_assessment(assessment, errors)
    validate_chronology(chronology, errors)

    if errors:
        print("FAIL: governed assessment validation failed")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS: governed assessment structure and promotion boundaries validated")
    print("NOTE: external facts, source custody, and independent review remain unresolved")
    return 0


if __name__ == "__main__":
    sys.exit(main())
