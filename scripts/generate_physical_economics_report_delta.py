#!/usr/bin/env python3
"""Generate machine-readable deltas between Physical Economics reports."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
DELTA_SCHEMA = ROOT / "schemas" / "physical-economics-report-delta.schema.json"


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def attr_map(snapshot: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {item["attribute_id"]: item for item in snapshot["attributes"]}


def receipt_map(snapshot: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {item["source_receipt_id"]: item for item in snapshot["source_receipts"]}


def add_change(
    changes: list[dict[str, Any]],
    change_class: str,
    scope: str,
    description: str,
    finding_impact: str,
    *,
    attribute_id: str | None = None,
    prior_value: Any = None,
    current_value: Any = None,
    source_receipt_ids: list[str] | None = None,
) -> None:
    changes.append(
        {
            "change_id": f"CHANGE-{len(changes) + 1:04d}",
            "change_class": change_class,
            "scope": scope,
            "attribute_id": attribute_id,
            "prior_value_or_state": prior_value,
            "current_value_or_state": current_value,
            "description": description,
            "finding_impact": finding_impact,
            "source_receipt_ids": source_receipt_ids or [],
        }
    )


def compare_attributes(prior: dict[str, Any], current: dict[str, Any], changes: list[dict[str, Any]]) -> None:
    prior_attrs = attr_map(prior)
    current_attrs = attr_map(current)
    for attribute_id in sorted(set(prior_attrs) | set(current_attrs)):
        before = prior_attrs.get(attribute_id)
        after = current_attrs.get(attribute_id)
        if before is None and after is not None:
            add_change(
                changes,
                "NEW_OBSERVATION",
                attribute_id,
                f"Attribute {attribute_id} entered the evidence snapshot.",
                "BOUNDARY_CHANGED",
                attribute_id=attribute_id,
                current_value=after,
                source_receipt_ids=after.get("source_receipt_ids", []),
            )
            continue
        if before is not None and after is None:
            add_change(
                changes,
                "SOURCE_WITHDRAWN_OR_REPLACED",
                attribute_id,
                f"Attribute {attribute_id} is no longer represented in the current evidence snapshot.",
                "CLAIM_NO_LONGER_GENERATABLE",
                attribute_id=attribute_id,
                prior_value=before,
                source_receipt_ids=before.get("source_receipt_ids", []),
            )
            continue
        assert before is not None and after is not None

        if before.get("latest_observed_date") != after.get("latest_observed_date"):
            add_change(
                changes,
                "NEW_OBSERVATION",
                attribute_id,
                f"Latest observed date changed for {attribute_id}.",
                "BOUNDARY_CHANGED",
                attribute_id=attribute_id,
                prior_value=before.get("latest_observed_date"),
                current_value=after.get("latest_observed_date"),
                source_receipt_ids=after.get("source_receipt_ids", []),
            )
        if before.get("latest_complete_date") != after.get("latest_complete_date"):
            add_change(
                changes,
                "PRIOR_PERIOD_COMPLETED",
                attribute_id,
                f"Latest complete date changed for {attribute_id}.",
                "BOUNDARY_CHANGED",
                attribute_id=attribute_id,
                prior_value=before.get("latest_complete_date"),
                current_value=after.get("latest_complete_date"),
                source_receipt_ids=after.get("source_receipt_ids", []),
            )
        if before.get("methodology_regime_id") != after.get("methodology_regime_id"):
            add_change(
                changes,
                "METHODOLOGY_CHANGE",
                attribute_id,
                f"Methodology regime changed for {attribute_id}.",
                "BOUNDARY_CHANGED",
                attribute_id=attribute_id,
                prior_value=before.get("methodology_regime_id"),
                current_value=after.get("methodology_regime_id"),
                source_receipt_ids=after.get("source_receipt_ids", []),
            )
        if before.get("revision_vintage") != after.get("revision_vintage"):
            add_change(
                changes,
                "ROUTINE_REVISION",
                attribute_id,
                f"Revision vintage changed for {attribute_id}.",
                "FINDING_REFINED",
                attribute_id=attribute_id,
                prior_value=before.get("revision_vintage"),
                current_value=after.get("revision_vintage"),
                source_receipt_ids=after.get("source_receipt_ids", []),
            )
        before_missing = before.get("missingness_posture")
        after_missing = after.get("missingness_posture")
        if before_missing in {"MISSING", "OPAQUE"} and after_missing in {"OBSERVED", "PARTIAL"}:
            add_change(
                changes,
                "OPAQUE_ATTRIBUTE_RESOLVED",
                attribute_id,
                f"Previously unresolved attribute {attribute_id} gained evidence.",
                "CONFIDENCE_CHANGED",
                attribute_id=attribute_id,
                prior_value=before_missing,
                current_value=after_missing,
                source_receipt_ids=after.get("source_receipt_ids", []),
            )
        if before.get("uncertainty") != after.get("uncertainty"):
            add_change(
                changes,
                "UNCERTAINTY_POSTURE_CHANGED",
                attribute_id,
                f"Uncertainty posture changed for {attribute_id}.",
                "CONFIDENCE_CHANGED",
                attribute_id=attribute_id,
                prior_value=before.get("uncertainty"),
                current_value=after.get("uncertainty"),
                source_receipt_ids=after.get("source_receipt_ids", []),
            )


def compare_receipts(prior: dict[str, Any], current: dict[str, Any], changes: list[dict[str, Any]]) -> None:
    prior_receipts = receipt_map(prior)
    current_receipts = receipt_map(current)
    for receipt_id, after in current_receipts.items():
        before = prior_receipts.get(receipt_id)
        if before is None:
            if after.get("revision_status") == "CORRECTED":
                change_class = "SOURCE_CORRECTION"
            elif after.get("revision_status") in {"WITHDRAWN", "REPLACED"}:
                change_class = "SOURCE_WITHDRAWN_OR_REPLACED"
            else:
                continue
            add_change(
                changes,
                change_class,
                receipt_id,
                f"Source receipt {receipt_id} entered with status {after.get('revision_status')}.",
                "FINDING_REFINED",
                current_value=after.get("revision_status"),
                source_receipt_ids=[receipt_id],
            )
        elif before.get("revision_status") != after.get("revision_status"):
            status = after.get("revision_status")
            if status == "CORRECTED":
                change_class = "SOURCE_CORRECTION"
            elif status in {"WITHDRAWN", "REPLACED"}:
                change_class = "SOURCE_WITHDRAWN_OR_REPLACED"
            else:
                change_class = "ROUTINE_REVISION"
            add_change(
                changes,
                change_class,
                receipt_id,
                f"Source receipt status changed for {receipt_id}.",
                "FINDING_REFINED",
                prior_value=before.get("revision_status"),
                current_value=status,
                source_receipt_ids=[receipt_id],
            )


def compare_conflicts(prior: dict[str, Any], current: dict[str, Any], changes: list[dict[str, Any]]) -> None:
    before = {item["conflict_id"]: item for item in prior.get("conflicts", [])}
    after = {item["conflict_id"]: item for item in current.get("conflicts", [])}
    for conflict_id in sorted(set(before) & set(after)):
        if before[conflict_id].get("status") == "UNRESOLVED" and after[conflict_id].get("status") != "UNRESOLVED":
            add_change(
                changes,
                "SOURCE_CONFLICT_RESOLVED",
                conflict_id,
                f"Source conflict {conflict_id} was resolved.",
                "CONFIDENCE_CHANGED",
                prior_value=before[conflict_id],
                current_value=after[conflict_id],
                source_receipt_ids=after[conflict_id].get("source_receipt_ids", []),
            )


def compare_manifests(prior: dict[str, Any], current: dict[str, Any], changes: list[dict[str, Any]]) -> None:
    prior_receipts = prior.get("receipts", {})
    current_receipts = current.get("receipts", {})
    if prior_receipts.get("pertinence_matrix_version") != current_receipts.get("pertinence_matrix_version"):
        add_change(
            changes,
            "REQUIRED_ATTRIBUTE_PROTOCOL_CHANGE",
            "pertinence_matrix",
            "Required-attribute protocol version changed.",
            "BOUNDARY_CHANGED",
            prior_value=prior_receipts.get("pertinence_matrix_version"),
            current_value=current_receipts.get("pertinence_matrix_version"),
        )
    if prior_receipts.get("contract_version") != current_receipts.get("contract_version") or prior_receipts.get("renderer_version") != current_receipts.get("renderer_version"):
        add_change(
            changes,
            "RENDERER_OR_CONTRACT_CHANGE",
            "report_runtime",
            "Report contract or renderer version changed.",
            "CONTEXT_ONLY",
            prior_value={"contract": prior_receipts.get("contract_version"), "renderer": prior_receipts.get("renderer_version")},
            current_value={"contract": current_receipts.get("contract_version"), "renderer": current_receipts.get("renderer_version")},
        )


def material_state(changes: list[dict[str, Any]]) -> str:
    impacts = {item["finding_impact"] for item in changes}
    classes = {item["change_class"] for item in changes}
    if not changes or impacts <= {"NONE", "CONTEXT_ONLY"}:
        return "NO_MATERIAL_CHANGE"
    if "REQUIRED_ATTRIBUTE_PROTOCOL_CHANGE" in classes or "RENDERER_OR_CONTRACT_CHANGE" in classes:
        return "MATERIAL_PROTOCOL_CHANGE"
    if impacts.intersection({"FINDING_REFINED", "FINDING_REVERSED", "CLAIM_NO_LONGER_GENERATABLE", "CONFIDENCE_CHANGED"}):
        return "MATERIAL_FINDING_CHANGE"
    return "MATERIAL_BOUNDARY_CHANGE"


def generate(
    prior_report_id: str,
    current_report_id: str,
    prior_snapshot: dict[str, Any],
    current_snapshot: dict[str, Any],
    prior_manifest: dict[str, Any],
    current_manifest: dict[str, Any],
) -> dict[str, Any]:
    changes: list[dict[str, Any]] = []
    compare_attributes(prior_snapshot, current_snapshot, changes)
    compare_receipts(prior_snapshot, current_snapshot, changes)
    compare_conflicts(prior_snapshot, current_snapshot, changes)
    compare_manifests(prior_manifest, current_manifest, changes)

    result = {
        "report_delta_id": f"PE-DELTA-{digest([prior_report_id, current_report_id, prior_snapshot['evidence_snapshot_id'], current_snapshot['evidence_snapshot_id']])[:16]}",
        "prior_report_id": prior_report_id,
        "current_report_id": current_report_id,
        "prior_snapshot_id": prior_snapshot["evidence_snapshot_id"],
        "current_snapshot_id": current_snapshot["evidence_snapshot_id"],
        "changes": changes,
        "material_change_state": material_state(changes),
        "plain_language_summary": (
            "No material report change was detected."
            if not changes
            else f"Detected {len(changes)} report-state change(s); see machine-readable change records for causes."
        ),
        "delta_hash": "PENDING",
    }
    hashable = dict(result)
    hashable["delta_hash"] = ""
    result["delta_hash"] = digest(hashable)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("prior_snapshot", type=Path)
    parser.add_argument("current_snapshot", type=Path)
    parser.add_argument("prior_manifest", type=Path)
    parser.add_argument("current_manifest", type=Path)
    parser.add_argument("--prior-report-id", required=True)
    parser.add_argument("--current-report-id", required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = generate(
        args.prior_report_id,
        args.current_report_id,
        load(args.prior_snapshot),
        load(args.current_snapshot),
        load(args.prior_manifest),
        load(args.current_manifest),
    )
    schema = load(DELTA_SCHEMA)
    failures = [error.message for error in Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(result)]
    if failures:
        for failure in failures:
            print(f"FAIL report delta: {failure}", file=sys.stderr)
        return 1

    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded, encoding="utf-8")
    else:
        print(encoded, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
