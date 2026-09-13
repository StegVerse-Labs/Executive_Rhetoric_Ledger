#!/usr/bin/env python3
"""Bind an ERL active-research acquisition envelope to existing provider proof.

This verifier is evidence-only. It never contacts the provider, writes provider
content, replays an operation, or grants transport/credential/execution authority.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

PROOF_SCHEMA = "stegverse.erl.active-research-provider-proof-projection/v1"
ENVELOPE_SCHEMA = "stegverse.erl.active-research-acquisition-envelope/v1"


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")


def sha_uri(value: Any) -> str:
    raw = value if isinstance(value, (bytes, bytearray)) else canonical(value)
    return "sha256:" + hashlib.sha256(bytes(raw)).hexdigest()


def require(ok: bool, reason: str) -> None:
    if not ok:
        raise ValueError(reason)


def verify(envelope: Mapping[str, Any], proof: Mapping[str, Any]) -> dict[str, Any]:
    require(envelope.get("schema") == ENVELOPE_SCHEMA, "envelope_schema_invalid")
    require(proof.get("schema") == PROOF_SCHEMA, "provider_proof_schema_invalid")
    require(proof.get("state") == "EXISTING_PROVIDER_WRITE_READBACK_OBSERVED", "provider_proof_state_invalid")
    require(proof.get("projection_only") is True and proof.get("projection_creates_new_provider_evidence") is False, "provider_proof_projection_semantics_invalid")
    require(proof.get("provider_operation_reexecution_authorized") is False, "provider_reexecution_must_remain_forbidden")
    require(proof.get("write_observed") is True and proof.get("independent_raw_readback_observed") is True and proof.get("exact_byte_readback_verified") is True, "provider_readback_predicates_missing")
    require(proof.get("universal_intr_traversal_proven_by_this_record") is False, "provider_proof_must_not_claim_intr")
    require(proof.get("authority_effect") == "NONE_EVIDENCE_PROJECTION_ONLY", "provider_proof_authority_invalid")
    require(proof.get("proof_class") == "PROVIDER_WRITE_PLUS_EXACT_BYTE_READBACK", "provider_proof_class_invalid")
    require(proof.get("source_id") == envelope.get("source_id"), "source_id_binding_mismatch")
    require(proof.get("source_url") == envelope.get("source_url"), "source_url_binding_mismatch")
    require(proof.get("required_storage_lane") == envelope.get("required_storage_lane"), "storage_lane_binding_mismatch")
    exact_sha = proof.get("exact_sha256")
    require(isinstance(exact_sha, str) and len(exact_sha) == 64 and all(ch in "0123456789abcdef" for ch in exact_sha), "provider_exact_sha256_invalid")
    size = proof.get("exact_size_bytes")
    require(isinstance(size, int) and size > 0, "provider_exact_size_invalid")
    provider_ref = proof.get("provider_file_ref")
    require(isinstance(provider_ref, str) and provider_ref.startswith("google-drive:file:"), "provider_file_ref_invalid")
    return {
        "schema": "stegverse.erl.active-research-provider-proof-binding/v1",
        "state": "SOURCE_IDENTITY_BOUND_TO_EXISTING_PROVIDER_PROOF",
        "source_id": envelope["source_id"],
        "source_url": envelope["source_url"],
        "acquisition_envelope_hash": sha_uri(envelope),
        "provider_file_ref": provider_ref,
        "provider_filename": proof["provider_filename"],
        "provider_exact_size_bytes": size,
        "provider_exact_sha256": exact_sha,
        "provider_proof_hash": sha_uri(proof),
        "provider_operation_reexecution_authorized": False,
        "provider_operation_attempted": False,
        "universal_intr_traversal_proven_by_provider_proof": False,
        "authority_effect": "NONE_EVIDENCE_BINDING_ONLY"
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--envelope", type=Path, required=True)
    parser.add_argument("--provider-proof", type=Path, required=True)
    args = parser.parse_args()
    envelope = json.loads(args.envelope.read_text(encoding="utf-8"))
    proof = json.loads(args.provider_proof.read_text(encoding="utf-8"))
    print(json.dumps(verify(envelope, proof), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
