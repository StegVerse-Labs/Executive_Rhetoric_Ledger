#!/usr/bin/env python3
"""Conservative source-conflict handling for Physical Economics evidence snapshots."""

from __future__ import annotations

from typing import Any


def resolve_conflict(conflict: dict[str, Any], source_receipts: list[dict[str, Any]]) -> dict[str, Any]:
    """Return a bounded conflict posture without guessing between source values.

    Automatic resolution is permitted only for an explicit official correction or
    replacement chain. Scope/vintage differences may be acknowledged only when
    already declared by the conflict record; otherwise the conflict remains open.
    """
    receipts = {item["source_receipt_id"]: item for item in source_receipts}
    ids = conflict.get("source_receipt_ids", [])
    missing = [item for item in ids if item not in receipts]
    if missing:
        return {
            "conflict_id": conflict.get("conflict_id", "UNKNOWN"),
            "status": "UNRESOLVED",
            "resolution_basis": f"referenced receipts missing: {', '.join(missing)}",
        }

    explicit_status = conflict.get("status", "UNRESOLVED")
    if explicit_status in {"RESOLVED_BY_SCOPE_DIFFERENCE", "RESOLVED_BY_VINTAGE", "REJECTED_SOURCE"}:
        return {
            "conflict_id": conflict["conflict_id"],
            "status": explicit_status,
            "resolution_basis": conflict.get("resolution_basis"),
        }

    candidates = [receipts[item] for item in ids]
    corrected = [item for item in candidates if item.get("revision_status") == "CORRECTED"]
    replaced = [item for item in candidates if item.get("revision_status") == "REPLACED"]

    for correction in corrected:
        superseded = correction.get("supersedes_source_receipt_id")
        if superseded and superseded in ids:
            return {
                "conflict_id": conflict["conflict_id"],
                "status": "RESOLVED_BY_OFFICIAL_CORRECTION",
                "resolution_basis": f"receipt {correction['source_receipt_id']} explicitly corrects {superseded}",
                "controlling_source_receipt_id": correction["source_receipt_id"],
            }

    for replacement in replaced:
        superseded = replacement.get("supersedes_source_receipt_id")
        if superseded and superseded in ids:
            return {
                "conflict_id": conflict["conflict_id"],
                "status": "RESOLVED_BY_OFFICIAL_CORRECTION",
                "resolution_basis": f"receipt {replacement['source_receipt_id']} explicitly replaces {superseded}",
                "controlling_source_receipt_id": replacement["source_receipt_id"],
            }

    return {
        "conflict_id": conflict["conflict_id"],
        "status": "UNRESOLVED",
        "resolution_basis": "no explicit correction/replacement chain or declared scope/vintage resolution; no reconciliation by guess",
    }


def unresolved_conflicts(snapshot: dict[str, Any]) -> list[dict[str, Any]]:
    results = [resolve_conflict(item, snapshot["source_receipts"]) for item in snapshot.get("conflicts", [])]
    return [item for item in results if item["status"] == "UNRESOLVED"]
