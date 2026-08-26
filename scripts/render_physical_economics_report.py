#!/usr/bin/env python3
"""Build and render a deterministic Physical Economics public report document."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
DOCUMENT_SCHEMA = ROOT / "schemas" / "physical-economics-report-document.schema.json"
RENDERER_VERSION = "physical-economics-markdown-renderer.v0.1"


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def build_document(
    report_id: str,
    request: dict[str, Any],
    snapshot: dict[str, Any],
    boundary: dict[str, Any],
    findings: list[dict[str, Any]] | None = None,
    prospective_gates: list[dict[str, Any]] | None = None,
    prior_report_delta: dict[str, Any] | None = None,
) -> dict[str, Any]:
    findings = findings or []
    prospective_gates = prospective_gates or []

    coverage_matrix = []
    uncertainty_surface = []
    opaque_elements: list[str] = []
    for item in boundary["attribute_boundaries"]:
        coverage_matrix.append(
            {
                "attribute_id": item["attribute_id"],
                "required": item["required_for_claim_class"],
                "earliest_admissible_date": item["earliest_admissible_date"],
                "latest_observed_date": item["latest_observed_date"],
                "latest_complete_date": item["latest_complete_date"],
                "current_period_state": item["current_period_state"],
                "methodology_regime_id": item["methodology_regime_id"],
                "comparability": item["comparability_with_prior_regime"],
                "provenance_posture": item["provenance_posture"],
                "missingness_posture": item["missingness_posture"],
            }
        )
        if item.get("uncertainty") is not None:
            uncertainty = item["uncertainty"]
            aggregate_state = None
            if isinstance(uncertainty, dict):
                if uncertainty.get("dependence_posture") == "UNKNOWN_DEPENDENCE":
                    aggregate_state = "UNRESOLVED_UNKNOWN_DEPENDENCE"
                elif uncertainty.get("propagation_authorized"):
                    aggregate_state = "PROPAGATION_ELIGIBLE_SUBJECT_TO_OPERATION"
            uncertainty_surface.append(
                {
                    "attribute_id": item["attribute_id"],
                    "uncertainty_posture": uncertainty,
                    "aggregate_propagation_state": aggregate_state,
                }
            )
        for opaque in item.get("opaque_elements", []):
            if opaque not in opaque_elements:
                opaque_elements.append(opaque)

    receipt = boundary["receipts"]
    return {
        "report_id": report_id,
        "generated_as_of_time": request["requested_as_of_time"],
        "question": request["question"],
        "claim_classes": request["claim_classes"],
        "scope": request["scope"],
        "boundary": {
            "completeness_state": boundary["completeness_state"],
            "statement": boundary["boundary_statement"],
            "earliest_common_comparable_date": boundary["report_boundaries"]["earliest_common_comparable_date"],
            "latest_common_complete_date": boundary["report_boundaries"]["latest_common_complete_date"],
        },
        "coverage_matrix": coverage_matrix,
        "uncertainty_surface": uncertainty_surface,
        "findings": findings,
        "opaque_elements": opaque_elements,
        "prospective_evidence_gates": prospective_gates,
        "receipts": {
            "report_request_hash": receipt["report_request_hash"],
            "evidence_snapshot_hash": receipt["evidence_snapshot_hash"],
            "boundary_manifest_hash": receipt["boundary_manifest_hash"],
            "pertinence_matrix_version": receipt["pertinence_matrix_version"],
            "contract_version": receipt["contract_version"],
            "source_receipt_ids": receipt.get("source_receipt_set", []),
        },
        "renderer_version": RENDERER_VERSION,
        "prior_report_delta": prior_report_delta,
    }


def cell(value: Any) -> str:
    if value is None:
        return "—"
    return str(value).replace("|", "\\|").replace("\n", " ")


def render_markdown(document: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append(f"# Physical Economics Report — {document['report_id']}")
    lines.append("")
    lines.append(f"**Question:** {document['question']}")
    lines.append(f"**Generated as of:** {document['generated_as_of_time']}")
    lines.append(f"**Claim classes:** {', '.join(document['claim_classes'])}")
    lines.append("")
    lines.append("## Report Boundary")
    lines.append("")
    lines.append(f"**Completeness:** {document['boundary']['completeness_state']}")
    lines.append("")
    lines.append(document["boundary"]["statement"])
    lines.append("")
    lines.append("This boundary is derived from the required evidence attributes. Longer series may appear as context but do not expand the admissible conclusion window.")
    lines.append("")

    lines.append("## Scope")
    lines.append("")
    for key in sorted(document["scope"]):
        lines.append(f"- **{key}:** {cell(document['scope'][key])}")
    lines.append("")

    lines.append("## Data Coverage Matrix")
    lines.append("")
    lines.append("| Attribute | Required | Earliest admissible | Latest observed | Latest complete | Current state | Methodology | Comparability | Provenance | Missingness |")
    lines.append("|---|---:|---|---|---|---|---|---|---|---|")
    for row in document["coverage_matrix"]:
        lines.append(
            "| " + " | ".join(
                [
                    cell(row["attribute_id"]),
                    "yes" if row["required"] else "no",
                    cell(row["earliest_admissible_date"]),
                    cell(row["latest_observed_date"]),
                    cell(row["latest_complete_date"]),
                    cell(row["current_period_state"]),
                    cell(row["methodology_regime_id"]),
                    cell(row["comparability"]),
                    cell(row["provenance_posture"]),
                    cell(row["missingness_posture"]),
                ]
            ) + " |"
        )
    lines.append("")

    lines.append("## Uncertainty and Quality")
    lines.append("")
    if document["uncertainty_surface"]:
        for item in document["uncertainty_surface"]:
            lines.append(f"- **{item['attribute_id']}:** `{json.dumps(item['uncertainty_posture'], sort_keys=True)}`")
            if item.get("aggregate_propagation_state"):
                lines.append(f"  - Aggregate propagation: {item['aggregate_propagation_state']}")
    else:
        lines.append("No source-native uncertainty object is attached to the attributes in this report snapshot.")
    lines.append("")

    lines.append("## Findings")
    lines.append("")
    if document["findings"]:
        for finding in document["findings"]:
            lines.append(f"### {finding['finding_id']} — {finding['finding_class']}")
            lines.append("")
            lines.append(finding["statement"])
            lines.append("")
            lines.append(f"Evidence posture: **{finding['evidence_posture']}**")
            if finding.get("boundary_note"):
                lines.append(f"Boundary note: {finding['boundary_note']}")
            if finding.get("uncertainty_note"):
                lines.append(f"Uncertainty note: {finding['uncertainty_note']}")
            lines.append("")
    else:
        lines.append("No substantive finding objects were supplied to the deterministic renderer. Boundary, coverage, opacity, and receipts remain reportable without inventing conclusions.")
        lines.append("")

    lines.append("## Unresolved / Opaque Elements")
    lines.append("")
    if document["opaque_elements"]:
        for item in document["opaque_elements"]:
            lines.append(f"- {item}")
    else:
        lines.append("No required opaque elements are recorded in the current boundary manifest.")
    lines.append("")

    lines.append("## Prospective Evidence Gates")
    lines.append("")
    if document["prospective_evidence_gates"]:
        for gate in document["prospective_evidence_gates"]:
            date_value = f" — {gate['expected_or_known_date']}" if gate.get("expected_or_known_date") else ""
            lines.append(f"- **{gate['gate_id']}**: {gate['attribute_or_source']} — {gate['state']}{date_value}")
            if gate.get("notes"):
                lines.append(f"  - {gate['notes']}")
    else:
        lines.append("No prospective evidence gates were supplied for this report.")
    lines.append("")

    if document.get("prior_report_delta"):
        lines.append("## Change Since Prior Report")
        lines.append("")
        lines.append(document["prior_report_delta"].get("plain_language_summary", "A machine-readable report delta is attached."))
        lines.append("")

    lines.append("## Reproduction Receipts")
    lines.append("")
    for key, value in document["receipts"].items():
        if isinstance(value, list):
            lines.append(f"- **{key}:** {', '.join(value) if value else '—'}")
        else:
            lines.append(f"- **{key}:** `{value}`")
    lines.append(f"- **renderer_version:** `{document['renderer_version']}`")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("request", type=Path)
    parser.add_argument("snapshot", type=Path)
    parser.add_argument("boundary", type=Path)
    parser.add_argument("--report-id", required=True)
    parser.add_argument("--findings", type=Path)
    parser.add_argument("--prospective-gates", type=Path)
    parser.add_argument("--prior-delta", type=Path)
    parser.add_argument("--document-output", type=Path)
    parser.add_argument("--markdown-output", type=Path)
    args = parser.parse_args()

    findings = load(args.findings) if args.findings else []
    gates = load(args.prospective_gates) if args.prospective_gates else []
    delta = load(args.prior_delta) if args.prior_delta else None
    document = build_document(
        args.report_id,
        load(args.request),
        load(args.snapshot),
        load(args.boundary),
        findings,
        gates,
        delta,
    )
    schema = load(DOCUMENT_SCHEMA)
    errors = list(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(document))
    if errors:
        for error in errors:
            print(f"FAIL report document: {error.message}", file=sys.stderr)
        return 1

    document_text = json.dumps(document, indent=2, sort_keys=True) + "\n"
    markdown = render_markdown(document)
    if args.document_output:
        args.document_output.parent.mkdir(parents=True, exist_ok=True)
        args.document_output.write_text(document_text, encoding="utf-8")
    if args.markdown_output:
        args.markdown_output.parent.mkdir(parents=True, exist_ok=True)
        args.markdown_output.write_text(markdown, encoding="utf-8")
    if not args.document_output and not args.markdown_output:
        print(markdown)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
