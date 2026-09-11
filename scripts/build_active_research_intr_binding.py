#!/usr/bin/env python3
"""Build a reusable, non-authorizing Universal InTr runtime binding for ERL active research.

This builder prepares the exact acquisition envelope, canonical Universal InTr
transport intent, and event-ephemeral materialization request for the authentic
runtime owner. It deliberately does not fabricate hop receipts or claim that
transport occurred.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

from scripts.consume_active_research_acquisition import digest, find_item

BINDING_SCHEMA = "stegverse.erl.active-research-intr-binding/v1"
INTENT_SCHEMA = "stegverse.universal-intr-transport/v1"
MATERIALIZATION_SCHEMA = "stegverse.universal-intr-materialization-request/v1"
INTR_PATH = ["EXTERNAL_SYSTEM", "STEGOS_ECOSYSTEM", "DEVICE_SYSTEM", "KV"]
SOURCE_SUBSYSTEM = "ERL:ActiveResearchExternalSource"
DESTINATION_SUBSYSTEM = "KnowledgeVault:ERL"
DOWNSTREAM_OWNER_REF = "StegVerse-Labs/Executive_Rhetoric_Ledger:active-research-kv-consumer"


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")


def sha256_uri_bytes(value: bytes) -> str:
    return "sha256:" + hashlib.sha256(value).hexdigest()


def build_acquisition_envelope(*, dispatch: Mapping[str, Any], group_id: str, source_id: str) -> dict[str, Any]:
    item = find_item(dispatch, group_id, source_id)
    return {
        "schema": "stegverse.erl.active-research-acquisition-envelope/v1",
        "group_id": group_id,
        "source_id": source_id,
        "source_url": str(item["url"]),
        "required_storage_lane": "02_Research/ERL",
        "finding_authorized": False,
        "publication_authorized": False,
    }


def build_transport_intent(*, envelope: Mapping[str, Any]) -> dict[str, Any]:
    payload_hash = digest(dict(envelope))
    operation_id = "ERL-ACTIVE-RESEARCH-" + hashlib.sha256(canonical_bytes({
        "group_id": envelope["group_id"],
        "source_id": envelope["source_id"],
        "payload_hash": payload_hash,
    })).hexdigest()[:24]
    basis = {
        "operation_id": operation_id,
        "payload_hash": payload_hash,
        "source_boundary": "EXTERNAL_SYSTEM",
        "source_subsystem": SOURCE_SUBSYSTEM,
        "destination_boundary": "KV",
        "destination_subsystem": DESTINATION_SUBSYSTEM,
        "boundary_path": INTR_PATH,
    }
    return {
        "schema": INTENT_SCHEMA,
        "protocol": "InTr",
        "operation_id": operation_id,
        "packet_id": "INTR-" + hashlib.sha256(canonical_bytes(basis)).hexdigest()[:24],
        "payload_hash": payload_hash,
        "prior_transport_receipt_hash": None,
        "source": {"boundary": "EXTERNAL_SYSTEM", "subsystem": SOURCE_SUBSYSTEM},
        "destination": {"boundary": "KV", "subsystem": DESTINATION_SUBSYSTEM},
        "boundary_path": list(INTR_PATH),
        "interlock_required": True,
        "transport_semantics": {
            "event_triggered": True,
            "always_on_receiver_required": False,
            "second_user_device_required": False,
            "receiver_unavailable_disposition": "DURABLE_QUEUE_OR_EVENT_EPHEMERAL_MATERIALIZATION",
            "exact_packet_transport_retry_allowed": True,
            "blind_consequence_retry_allowed": False,
        },
        "authority": {
            "authority_transfer": False,
            "transport_grants_execution_authority": False,
            "credential_authority": "TV/TVC",
        },
        "receipt_chain": {
            "required": True,
            "receipt_schema": "stegverse.intr.hop_receipt/v1",
            "payload_plaintext_in_receipts": False,
            "prior_hash_required_after_first_hop": True,
        },
    }


def build_materialization_request(*, intent: Mapping[str, Any], payload_ref: str) -> dict[str, Any]:
    if not payload_ref.strip():
        raise ValueError("payload_ref is required")
    intent_hash = digest(dict(intent))
    identity_basis = {
        "transport_intent_hash": intent_hash,
        "operation_id": intent["operation_id"],
        "packet_id": intent["packet_id"],
        "payload_hash": intent["payload_hash"],
        "destination": intent["destination"],
    }
    body = {
        "schema": MATERIALIZATION_SCHEMA,
        "materialization_id": "INTR-MAT-" + hashlib.sha256(canonical_bytes(identity_basis)).hexdigest()[:24],
        "state": "QUEUED_FOR_EVENT_EPHEMERAL_MATERIALIZATION",
        "transport_schema": INTENT_SCHEMA,
        "transport_protocol": "InTr",
        "transport_intent_hash": intent_hash,
        "operation_id": intent["operation_id"],
        "packet_id": intent["packet_id"],
        "payload_hash": intent["payload_hash"],
        "payload_ref": payload_ref.strip(),
        "destination": dict(intent["destination"]),
        "boundary_path": list(intent["boundary_path"]),
        "downstream_owner_ref": DOWNSTREAM_OWNER_REF,
        "event_triggered": True,
        "always_on_receiver_required": False,
        "second_user_device_required": False,
        "receiver_unavailable_disposition": "DURABLE_QUEUE_OR_EVENT_EPHEMERAL_MATERIALIZATION",
        "exact_packet_transport_retry_allowed": True,
        "blind_consequence_retry_allowed": False,
        "interlock_required": True,
        "request_grants_execution_authority": False,
        "claim_or_fence_minted": False,
        "transport_grants_execution_authority": False,
        "credential_authority": "TV/TVC",
        "github_token_runtime_authority": "NONE",
        "authority_transfer": False,
        "authority_effect": "NONE_REQUEST_ONLY",
    }
    return {**body, "request_hash": digest(body)}


def build_binding(*, dispatch: Mapping[str, Any], group_id: str, source_id: str, payload_ref: str) -> dict[str, Any]:
    envelope = build_acquisition_envelope(dispatch=dispatch, group_id=group_id, source_id=source_id)
    intent = build_transport_intent(envelope=envelope)
    request = build_materialization_request(intent=intent, payload_ref=payload_ref)
    body = {
        "schema": BINDING_SCHEMA,
        "group_id": group_id,
        "source_id": source_id,
        "acquisition_envelope": envelope,
        "acquisition_envelope_sha256": digest(envelope),
        "transport_intent": intent,
        "materialization_request": request,
        "expected_runtime_receipt_schema": "stegverse.intr.hop_receipt/v1",
        "expected_runtime_receipt_count": 3,
        "expected_boundary_path": list(INTR_PATH),
        "runtime_receipts_present": False,
        "transport_execution_claimed": False,
        "finding_authorized": False,
        "publication_authorized": False,
        "authority_effect": "NONE_REQUEST_ONLY",
    }
    return {**body, "binding_hash": digest(body)}


def persist_binding(path: Path, binding: Mapping[str, Any]) -> Path:
    path = path.expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    rendered = json.dumps(dict(binding), indent=2, sort_keys=True) + "\n"
    if path.exists():
        existing = path.read_text(encoding="utf-8")
        if existing == rendered:
            return path
        raise ValueError("binding output already exists with different bytes")
    path.write_text(rendered, encoding="utf-8")
    if path.read_text(encoding="utf-8") != rendered:
        raise ValueError("binding persistence readback mismatch")
    return path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dispatch", type=Path, required=True)
    parser.add_argument("--group-id", required=True)
    parser.add_argument("--source-id", required=True)
    parser.add_argument("--payload-ref", required=True,
                        help="Stable reference to the exact canonical acquisition-envelope bytes presented to the runtime")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    binding = build_binding(
        dispatch=json.loads(args.dispatch.read_text(encoding="utf-8")),
        group_id=args.group_id,
        source_id=args.source_id,
        payload_ref=args.payload_ref,
    )
    if args.output:
        persist_binding(args.output, binding)
    print(json.dumps(binding, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
