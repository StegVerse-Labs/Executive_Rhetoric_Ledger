import copy

import pytest

from scripts.validate_canonical_provenance_reference import (
    ProvenanceReferenceError,
    validate_reference,
)


def record():
    return {
        "schema": "stegverse.erl.canonical-provenance-reference.v1",
        "candidate_id": "ERL-2026-09-03-ORLI-SHULL-AI-GOVERNANCE-COLLAPSE-001",
        "canonical_lineage_schema": "stegos.object_provenance_lineage.v1",
        "canonical_lineage_id": "svlineage:sha256:" + "a" * 64,
        "candidate_object_id": "svobj:sha256:" + "b" * 64,
        "source_root_object_ids": ["svobj:sha256:" + "c" * 64],
        "derivation_edge_ids": ["svedge:sha256:" + "d" * 64],
        "transition_receipt_refs": ["intr-receipt:erl-candidate-001"],
        "master_records_custody_receipt_ref": None,
        "authority_effect": "NONE",
    }


def test_accepts_reference_only_record():
    validate_reference(record())


def test_rejects_missing_source_root():
    value = record()
    value["source_root_object_ids"] = []
    with pytest.raises(ProvenanceReferenceError, match="source_root_object_ids"):
        validate_reference(value)


def test_rejects_noncanonical_object_identity():
    value = record()
    value["candidate_object_id"] = "candidate-local-id"
    with pytest.raises(ProvenanceReferenceError, match="canonical object id"):
        validate_reference(value)


def test_rejects_authority_expansion():
    value = record()
    value["authority_effect"] = "PUBLICATION"
    with pytest.raises(ProvenanceReferenceError, match="cannot grant authority"):
        validate_reference(value)


def test_rejects_manufactured_canonical_graph_fields():
    value = copy.deepcopy(record())
    value["objects"] = []
    with pytest.raises(ProvenanceReferenceError, match="must not reproduce or manufacture"):
        validate_reference(value)


def test_rejects_duplicate_receipt_refs():
    value = record()
    value["transition_receipt_refs"] = ["receipt:1", "receipt:1"]
    with pytest.raises(ProvenanceReferenceError, match="must be unique"):
        validate_reference(value)
