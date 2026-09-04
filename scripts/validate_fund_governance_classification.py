#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "assessments" / "fund-governance"
EXPECTED_SCHEMA = "stegverse.erl.fund_governance_classification.v1"

LEGAL = {
    "NOT_ASSESSED", "INSUFFICIENT_EVIDENCE", "NO_VIOLATION_SUPPORTED",
    "POTENTIAL_VIOLATION", "VIOLATION_SUPPORTED"
}
REPRESENTATION = {
    "NOT_ASSESSED", "REPRESENTATION_NOT_RECONSTRUCTED", "ALIGNED",
    "PARTIAL_DIVERGENCE", "MATERIAL_DIVERGENCE_SUPPORTED"
}
GOVERNANCE = {
    "NOT_ASSESSED", "INSUFFICIENT_EVIDENCE", "NO_GOVERNANCE_CONCERN_SUPPORTED",
    "GOVERNANCE_RISK", "GOVERNANCE_MISUSE_SUPPORTED"
}
STRATEGY = {
    "NOT_ASSESSED", "STRATEGY_NOT_RECONSTRUCTED", "NORMAL_DEPLOYMENT",
    "DELAYED_OR_SELECTIVE_DEPLOYMENT", "STRATEGIC_NONDEPLOYMENT_SUPPORTED"
}
EARLY_LIFECYCLES = {"RESEARCH_CANDIDATE", "RESEARCH_ACTIVE_NOT_ASSESSABLE"}
REQUIRED_VECTOR = {
    "LEGALITY", "DONOR_REPRESENTATION", "BENEFICIAL_RECIPIENT",
    "ORGANIZATIONAL_PURPOSE", "DEPLOYMENT_TIMING", "CONTROL_CONCENTRATION",
    "DISCLOSURE_ACCURACY"
}


def fail(path: Path, message: str) -> None:
    raise SystemExit(f"FAIL_CLOSED: {path.relative_to(ROOT)}: {message}")


def require(condition: bool, path: Path, message: str) -> None:
    if not condition:
        fail(path, message)


def validate(path: Path) -> None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(path, f"invalid JSON: {exc}")

    require(data.get("schema") == EXPECTED_SCHEMA, path, "unexpected schema")
    require(isinstance(data.get("record_id"), str) and data["record_id"], path, "record_id required")

    axes = data.get("axes")
    require(isinstance(axes, dict), path, "axes object required")
    require(axes.get("legal_misuse") in LEGAL, path, "invalid legal_misuse state")
    require(axes.get("represented_purpose_divergence") in REPRESENTATION, path, "invalid represented_purpose_divergence state")
    require(axes.get("governance_ethical_misuse") in GOVERNANCE, path, "invalid governance_ethical_misuse state")
    require(axes.get("strategic_nondeployment") in STRATEGY, path, "invalid strategic_nondeployment state")

    vector = data.get("state_vector")
    require(isinstance(vector, dict), path, "state_vector object required")
    require(set(vector) == REQUIRED_VECTOR, path, "state_vector must contain exactly the seven required dimensions")
    for key, value in vector.items():
        require(isinstance(value, str) and value, path, f"state_vector.{key} must be non-empty string")

    finding = data.get("finding_authorized")
    publication = data.get("publication_authorized")
    require(isinstance(finding, bool), path, "finding_authorized must be boolean")
    require(isinstance(publication, bool), path, "publication_authorized must be boolean")

    if data.get("lifecycle") in EARLY_LIFECYCLES:
        require(finding is False, path, "early lifecycle cannot authorize finding")
        require(publication is False, path, "early lifecycle cannot authorize publication")

    strongest = {
        axes.get("legal_misuse") == "VIOLATION_SUPPORTED",
        axes.get("represented_purpose_divergence") == "MATERIAL_DIVERGENCE_SUPPORTED",
        axes.get("governance_ethical_misuse") == "GOVERNANCE_MISUSE_SUPPORTED",
    }
    if any(strongest):
        require(data.get("lifecycle") in {"ASSESSABLE", "REVIEWED", "TERMINAL"}, path,
                "strong adverse state forbidden before assessable lifecycle")
        require(bool(data.get("evidence_refs")), path, "strong adverse state requires evidence_refs")
        require(bool(data.get("alternative_explanations")), path, "strong adverse state requires alternative explanations")


def main() -> int:
    require(TARGET.exists(), TARGET, "assessment directory missing")
    files = sorted(TARGET.glob("*.classification.json"))
    require(bool(files), TARGET, "no classification files found")
    for path in files:
        validate(path)
    print(f"PASS: validated {len(files)} ERL fund-governance classification file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
