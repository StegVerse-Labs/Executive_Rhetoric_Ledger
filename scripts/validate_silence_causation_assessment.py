#!/usr/bin/env python3
"""Validate ERL silence-causation assessments and governance invariants."""

from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    import jsonschema
except ImportError as exc:  # pragma: no cover
    raise SystemExit("jsonschema is required: pip install jsonschema") from exc

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "silence-causation-assessment.schema.json"
ASSESSMENTS = ROOT / "assessments" / "silence-causation"


def bounded_total(score: dict[str, int]) -> int:
    return (
        score["evidence_support"]
        + score["pattern_fit"]
        + score["document_conflict_fit"]
        + score["authority_network_fit"]
        - score["alternative_explanation_penalty"]
        - score["missing_evidence_penalty"]
    )


def validate_governance(data: dict) -> list[str]:
    errors: list[str] = []
    complete = data["source_posture"]["complete_primary_record"]
    questions = data["questions"]

    if not complete and data["classification"] not in {"not_assessable", "plausible_but_unranked"}:
        errors.append("Incomplete primary record cannot support ranked or preferred hypotheses.")

    if data["classification"] == "single_hypothesis_materially_preferred":
        if data["review"]["contradiction_review"] != "complete":
            errors.append("Preferred hypothesis requires complete contradiction review.")
        if data["review"]["independent_review"] != "complete":
            errors.append("Preferred hypothesis requires complete independent review.")
        if not questions:
            errors.append("Preferred hypothesis requires an atomic question ledger.")

    for hypothesis in data["hypotheses"]:
        expected = bounded_total(hypothesis["score"])
        actual = hypothesis["score"]["bounded_total"]
        if expected != actual:
            errors.append(f"{hypothesis['hypothesis_id']}: bounded_total {actual} != computed {expected}")
        if hypothesis["class"] == "political_pressure_or_coercion" and not hypothesis["supporting_evidence"]:
            if actual > 0:
                errors.append(f"{hypothesis['hypothesis_id']}: unsupported coercion hypothesis cannot score above zero")

    for participant in data["participants"]:
        for edge in participant["edges"]:
            if edge["evidence_status"] in {"hypothesized", "unknown"} and edge.get("source_ids"):
                errors.append(f"{participant['participant_id']}: unknown/hypothesized edge must not cite sources as proof")

    return errors


def main() -> int:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    files = sorted(ASSESSMENTS.glob("*.json"))
    if not files:
        print("No silence-causation assessments found.", file=sys.stderr)
        return 1

    failures = 0
    for path in files:
        data = json.loads(path.read_text(encoding="utf-8"))
        try:
            jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker()).validate(data)
        except jsonschema.ValidationError as exc:
            failures += 1
            print(f"FAIL {path}: schema: {exc.message}")
            continue
        governance_errors = validate_governance(data)
        if governance_errors:
            failures += 1
            for error in governance_errors:
                print(f"FAIL {path}: governance: {error}")
        else:
            print(f"PASS {path}")

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
