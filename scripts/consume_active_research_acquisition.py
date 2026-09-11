#!/usr/bin/env python3
"""Consume one admitted ERL active-research acquisition into MyKV.

This consumer is intentionally transport-neutral: source acquisition happens before this
step, but durable completion is impossible unless a canonical InTr hop receipt binds the
exact acquisition envelope and the existing ERL KV writer completes exact-byte readback.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import mimetypes
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping
from urllib.parse import urlparse

from adapters.kv.erl_kv_writer import write_bundle

INTR_SCHEMA = "stegverse.intr.hop_receipt/v1"
RESULT_SCHEMA = "stegverse.erl.active-research-acquisition-result/v1"


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")


def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_bytes(value)).hexdigest()


def verify_intr_receipt(receipt: Mapping[str, Any], *, payload_hash: str) -> None:
    required = {
        "schema", "receipt_id", "packet_id", "hop_index", "direction", "from_role", "to_role",
        "operation_hash", "payload_hash", "prior_receipt_hash", "boundary_identity_ref",
        "boundary_verification", "transition_state", "secret_plaintext_present", "authority_transfer",
        "recorded_at", "receipt_hash",
    }
    if set(receipt) != required:
        raise ValueError("InTr hop receipt canonical field mismatch")
    if receipt.get("schema") != INTR_SCHEMA:
        raise ValueError("unexpected InTr hop receipt schema")
    if receipt.get("direction") != "FORWARD" or not isinstance(receipt.get("hop_index"), int):
        raise ValueError("InTr receipt must describe a forward hop")
    if receipt.get("boundary_verification") != "VERIFIED" or receipt.get("transition_state") != "RECEIVED":
        raise ValueError("InTr receipt must prove verified receipt at the consumer boundary")
    if receipt.get("payload_hash") != payload_hash:
        raise ValueError("InTr receipt does not bind the exact acquisition envelope")
    if receipt.get("secret_plaintext_present") is not False or receipt.get("authority_transfer") is not False:
        raise ValueError("InTr acquisition receipt may contain neither secret plaintext nor authority transfer")
    body = dict(receipt)
    claimed = body.pop("receipt_hash")
    if claimed != digest(body):
        raise ValueError("InTr receipt hash mismatch")


def find_item(dispatch: Mapping[str, Any], group_id: str, source_id: str) -> Mapping[str, Any]:
    for lane in dispatch.get("lanes", []):
        if lane.get("group_id") != group_id:
            continue
        if lane.get("dispatch_state") != "ELIGIBLE_FOR_AUTOMATED_ACQUISITION":
            raise ValueError("requested research lane is not eligible for automated acquisition")
        if lane.get("finding_authorized") is not False or lane.get("publication_authorized") is not False:
            raise ValueError("dispatcher illegally elevated finding/publication authority")
        for queue in lane.get("queues", []):
            for item in queue.get("executable_items", []):
                if item.get("source_id") == source_id:
                    if item.get("persistence_required") is not True:
                        raise ValueError("dispatch item does not require MyKV persistence")
                    if item.get("required_storage_lane") != "02_Research/ERL":
                        raise ValueError("dispatch item targets the wrong MyKV lane")
                    return item
    raise ValueError("dispatch item not found")


def consume(*, dispatch: Mapping[str, Any], group_id: str, source_id: str, intr_receipt: Mapping[str, Any],
            payload: Path, kv_root: Path, kv_instance_id: str, captured_at: str | None = None) -> dict[str, Any]:
    if dispatch.get("mykv_coordination", {}).get("github_storage_satisfies_persistence") is not False:
        raise ValueError("dispatch must explicitly reject GitHub storage as MyKV persistence")
    if dispatch.get("mykv_coordination", {}).get("exact_byte_readback_required") is not True:
        raise ValueError("dispatch must require exact-byte MyKV readback")

    item = find_item(dispatch, group_id, source_id)
    url = str(item.get("url", ""))
    parsed = urlparse(url)
    if parsed.scheme != "https":
        raise ValueError("active research acquisition consumer requires HTTPS source identity")
    allowed_hosts = set(item.get("allowed_hosts", []))
    if parsed.hostname not in allowed_hosts:
        raise ValueError("source host is not admitted by the dispatch item")

    acquisition_envelope = {
        "schema": "stegverse.erl.active-research-acquisition-envelope/v1",
        "group_id": group_id,
        "source_id": source_id,
        "source_url": url,
        "required_storage_lane": "02_Research/ERL",
        "finding_authorized": False,
        "publication_authorized": False,
    }
    envelope_hash = digest(acquisition_envelope)
    verify_intr_receipt(intr_receipt, payload_hash=envelope_hash)

    data = payload.read_bytes()
    raw_sha = hashlib.sha256(data).hexdigest()
    timestamp = captured_at or datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    artifact_id = f"ERL-ACTIVE-{source_id}"
    filename = payload.name
    manifest = {
        "schema": "stegverse.erl.kv-artifact/v1",
        "artifact_id": artifact_id,
        "artifact_class": "SOURCE_CAPTURE",
        "captured_at": timestamp,
        "source": {"title": source_id, "publisher": parsed.hostname or "unknown", "primary_url": url},
        "storage": {"lane": "02_Research/ERL", "kv_instance_id": kv_instance_id, "credential_material_present": False},
        "objects": [{
            "filename": filename,
            "sha256": raw_sha,
            "size_bytes": len(data),
            "media_type": mimetypes.guess_type(filename)[0] or "application/octet-stream",
            "role": "acquired-source",
        }],
    }
    kv_receipt = write_bundle(kv_root=kv_root, manifest=manifest, payloads={filename: payload})
    if kv_receipt.get("readback_verified") is not True:
        raise ValueError("MyKV exact-byte readback was not verified")

    return {
        "schema": RESULT_SCHEMA,
        "group_id": group_id,
        "source_id": source_id,
        "state": "KV_STORED_AND_READBACK_VERIFIED" if kv_receipt["result"] == "WRITTEN" else "KV_ALREADY_PRESENT_AND_HASH_MATCHED",
        "acquisition_envelope_sha256": envelope_hash,
        "intr_receipt_hash": intr_receipt["receipt_hash"],
        "artifact_id": artifact_id,
        "source_sha256": raw_sha,
        "kv_write_receipt": kv_receipt,
        "finding_authorized": False,
        "publication_authorized": False,
    }


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--dispatch", type=Path, required=True)
    p.add_argument("--group-id", required=True)
    p.add_argument("--source-id", required=True)
    p.add_argument("--intr-receipt", type=Path, required=True)
    p.add_argument("--payload", type=Path, required=True)
    p.add_argument("--kv-root", type=Path, required=True)
    p.add_argument("--kv-instance-id", required=True)
    p.add_argument("--captured-at")
    p.add_argument("--result", type=Path)
    args = p.parse_args()
    result = consume(
        dispatch=json.loads(args.dispatch.read_text()), group_id=args.group_id, source_id=args.source_id,
        intr_receipt=json.loads(args.intr_receipt.read_text()), payload=args.payload, kv_root=args.kv_root,
        kv_instance_id=args.kv_instance_id, captured_at=args.captured_at,
    )
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.result:
        args.result.write_text(rendered)
    print(rendered, end="")


if __name__ == "__main__":
    main()
