#!/usr/bin/env python3
"""Validate ERL transition-calculus schemas, fixtures, and governance invariants."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "transition-record.schema.json"
OPAQUE_SCHEMA_PATH = ROOT / "schemas" / "opaque-transition-element.schema.json"
FIXTURES = ROOT / "tests" / "transition-calculus"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def governance_errors(data: dict) -> list[str]:
    errors: list[str] = []
    tid = data["transition_id"]
    continuity = data["continuity"]

    if data["canonical_status"] == "canonical":
        if continuity["posture"] != "ESTABLISHED":
            errors.append(f"{tid}: canonical transition requires ESTABLISHED continuity")
        if not continuity["evidence_ids"]:
            errors.append(f"{tid}: canonical continuity requires evidence")
    elif continuity["posture"] == "ESTABLISHED" and data["canonical_status"] == "candidate":
        errors.append(f"{tid}: candidate transition cannot silently carry ESTABLISHED continuity")

    receipt_ids = {item["evidence_id"] for item in data["evidence_receipts"]}
    referenced: set[str] = set(data["pre_state"]["evidence_ids"]) | set(data["post_state"]["evidence_ids"]) | set(continuity["evidence_ids"])
    for element in data["observed_elements"]:
        referenced.update(element["evidence_ids"])
    for opaque in data["opaque_elements"]:
        referenced.update(opaque["evidence_ids"])
        referenced.update(opaque.get("resolution_evidence_ids", []))
    for event in data["resolution_history"]:
        referenced.update(event["evidence_ids"])
    for relation in data["provenance_relations"]:
        referenced.update(relation["evidence_ids"])
        posture = relation["posture"]
        weight = relation["independent_confirmation_weight"]
        if posture in {"known_dependency", "common_upstream"} and weight != 0:
            errors.append(f"{tid}: {relation['relation_id']} dependent/common-upstream relation must have weight 0")
        if posture == "unknown_provenance" and weight > 0.5:
            errors.append(f"{tid}: {relation['relation_id']} unknown provenance weight exceeds 0.5")

    missing = sorted(referenced - receipt_ids)
    if missing:
        errors.append(f"{tid}: referenced evidence IDs missing receipts: {', '.join(missing)}")

    observed_ids = {item["element_id"] for item in data["observed_elements"]}
    opaque_ids = {item["opaque_id"] for item in data["opaque_elements"]}
    for opaque in data["opaque_elements"]:
        if opaque["resolution_state"] == "RESOLVED":
            resolved_id = opaque.get("resolved_element_id")
            if resolved_id not in observed_ids:
                errors.append(f"{tid}: resolved opaque {opaque['opaque_id']} points to absent element {resolved_id}")
            matches = [e for e in data["resolution_history"] if e["event_type"] == "RESOLVE_OPAQUE" and e.get("opaque_id") == opaque["opaque_id"] and e.get("resolved_element_id") == resolved_id]
            if not matches:
                errors.append(f"{tid}: resolved opaque {opaque['opaque_id']} lacks preserved RESOLVE_OPAQUE history")

    for event in data["resolution_history"]:
        if event.get("opaque_id") and event["opaque_id"] not in opaque_ids:
            errors.append(f"{tid}: resolution history references removed opaque slot {event['opaque_id']}")

    # Layer-O schema permits references to hypotheses, never embedded explanatory objects.
    if any(isinstance(item, dict) for item in data["hypothesis_refs"]):
        errors.append(f"{tid}: hypotheses must be external references, not embedded Layer-H content")

    return errors


def validate_transition(path: Path, schema: dict, opaque_schema: dict) -> list[str]:
    data = load(path)
    errors: list[str] = []
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    for exc in validator.iter_errors(data):
        errors.append(f"{path.name}: schema: {exc.message}")
    opaque_validator = Draft202012Validator(opaque_schema, format_checker=FormatChecker())
    for opaque in data.get("opaque_elements", []):
        for exc in opaque_validator.iter_errors(opaque):
            errors.append(f"{path.name}: opaque schema: {exc.message}")
    if not errors:
        errors.extend(governance_errors(data))
    return errors


def validate_composition(path: Path, schema: dict, opaque_schema: dict) -> list[str]:
    doc = load(path)
    errors: list[str] = []
    transitions = {item["transition_id"]: item for item in doc["transitions"]}
    for item in transitions.values():
        temp_errors = list(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(item))
        if temp_errors:
            errors.extend(f"{path.name}: {item['transition_id']}: {exc.message}" for exc in temp_errors)
        else:
            errors.extend(governance_errors(item))
    for assertion in doc["composition_assertions"]:
        left = transitions[assertion["left_transition_id"]]
        right = transitions[assertion["right_transition_id"]]
        composed = transitions[assertion["composed_transition_id"]]
        if left["post_state"]["state_id"] != right["pre_state"]["state_id"]:
            errors.append(f"{path.name}: component boundary mismatch")
        if composed["pre_state"]["state_id"] != left["pre_state"]["state_id"]:
            errors.append(f"{path.name}: composition failed pre-state conservation")
        if composed["post_state"]["state_id"] != right["post_state"]["state_id"]:
            errors.append(f"{path.name}: composition failed post-state conservation")
        component_evidence = {e["evidence_id"] for t in (left, right) for e in t["evidence_receipts"]}
        composed_evidence = {e["evidence_id"] for e in composed["evidence_receipts"]}
        if not component_evidence.issubset(composed_evidence):
            errors.append(f"{path.name}: composition lost component evidence lineage")
    return errors


def main() -> int:
    schema = load(SCHEMA_PATH)
    opaque_schema = load(OPAQUE_SCHEMA_PATH)
    failures: list[str] = []
    transition_files = sorted(FIXTURES.glob("*.transition.json"))
    composition_files = sorted(FIXTURES.glob("*.composition.json"))
    if not transition_files or not composition_files:
        print("Missing transition-calculus fixtures.", file=sys.stderr)
        return 1
    for path in transition_files:
        failures.extend(validate_transition(path, schema, opaque_schema))
    for path in composition_files:
        failures.extend(validate_composition(path, schema, opaque_schema))
    if failures:
        for error in failures:
            print(f"FAIL {error}")
        return 1
    for path in transition_files + composition_files:
        print(f"PASS {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
