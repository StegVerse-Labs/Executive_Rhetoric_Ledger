#!/usr/bin/env python3
"""Validate ERL references to canonical StegOS object-provenance lineage.

This validator is projection-only. It never mints provenance objects, edges,
lineage IDs, transition receipts, or Master Records custody receipts.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any, Mapping

SCHEMA = "stegverse.erl.canonical-provenance-reference.v1"
CANONICAL_LINEAGE_SCHEMA = "stegos.object_provenance_lineage.v1"
OBJ = re.compile(r"^svobj:sha256:[0-9a-f]{64}$")
EDGE = re.compile(r"^svedge:sha256:[0-9a-f]{64}$")
LINEAGE = re.compile(r"^svlineage:sha256:[0-9a-f]{64}$")


class ProvenanceReferenceError(ValueError):
    pass


def _nonempty_unique_strings(value: Any, field: str) -> list[str]:
    if not isinstance(value, list) or not value:
        raise ProvenanceReferenceError(f"{field} must be a non-empty array")
    if any(not isinstance(item, str) or not item for item in value):
        raise ProvenanceReferenceError(f"{field} must contain non-empty strings")
    if len(value) != len(set(value)):
        raise ProvenanceReferenceError(f"{field} must be unique")
    return value


def validate_reference(record: Mapping[str, Any]) -> None:
    if record.get("schema") != SCHEMA:
        raise ProvenanceReferenceError("unsupported ERL provenance reference schema")
    if record.get("canonical_lineage_schema") != CANONICAL_LINEAGE_SCHEMA:
        raise ProvenanceReferenceError("canonical lineage schema mismatch")
    if record.get("authority_effect") != "NONE":
        raise ProvenanceReferenceError("provenance references cannot grant authority")
    candidate_id = record.get("candidate_id")
    if not isinstance(candidate_id, str) or not candidate_id:
        raise ProvenanceReferenceError("candidate_id is required")
    if not isinstance(record.get("canonical_lineage_id"), str) or not LINEAGE.fullmatch(record["canonical_lineage_id"]):
        raise ProvenanceReferenceError("canonical_lineage_id must be a canonical lineage id")
    if not isinstance(record.get("candidate_object_id"), str) or not OBJ.fullmatch(record["candidate_object_id"]):
        raise ProvenanceReferenceError("candidate_object_id must be a canonical object id")

    roots = _nonempty_unique_strings(record.get("source_root_object_ids"), "source_root_object_ids")
    if any(not OBJ.fullmatch(item) for item in roots):
        raise ProvenanceReferenceError("source_root_object_ids must contain canonical object ids")
    edges = _nonempty_unique_strings(record.get("derivation_edge_ids"), "derivation_edge_ids")
    if any(not EDGE.fullmatch(item) for item in edges):
        raise ProvenanceReferenceError("derivation_edge_ids must contain canonical edge ids")
    _nonempty_unique_strings(record.get("transition_receipt_refs"), "transition_receipt_refs")

    custody = record.get("master_records_custody_receipt_ref")
    if custody is not None and (not isinstance(custody, str) or not custody):
        raise ProvenanceReferenceError("master_records_custody_receipt_ref must be null or non-empty")

    forbidden = {
        "objects",
        "edges",
        "root_object_ids",
        "workspace_projection",
        "master_records_projection",
        "provider_object_id",
        "content_sha256",
    }
    overlap = sorted(forbidden.intersection(record))
    if overlap:
        raise ProvenanceReferenceError(
            "ERL reference must not reproduce or manufacture canonical provenance fields: " + ", ".join(overlap)
        )


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: validate_canonical_provenance_reference.py FILE [FILE ...]", file=sys.stderr)
        return 2
    for raw_path in argv[1:]:
        path = Path(raw_path)
        record = json.loads(path.read_text(encoding="utf-8"))
        validate_reference(record)
        print(f"PASS {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
