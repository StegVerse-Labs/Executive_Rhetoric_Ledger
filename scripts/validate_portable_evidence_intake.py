#!/usr/bin/env python3
"""Validate FREE-DOM portable evidence packets without granting standing."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PACKETS = ROOT / "intake" / "portable-evidence"


def canonical_hash(obj: dict[str, Any], hash_field: str) -> str:
    payload = {key: value for key, value in obj.items() if key != hash_field}
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def calculate_merkle_root(receipt_hash: str, siblings: list[dict[str, str]]) -> str:
    current = bytes.fromhex(receipt_hash.split(":", 1)[1])
    for sibling in siblings:
        sibling_bytes = bytes.fromhex(sibling["hash"].split(":", 1)[1])
        current = hashlib.sha256(
            sibling_bytes + current if sibling["position"] == "left" else current + sibling_bytes
        ).digest()
    return "sha256:" + current.hex()


def validate_packet(packet: dict[str, Any], path: Path) -> None:
    required = [
        "packet_version", "packet_id", "producer_repository", "destination_repository",
        "received_at", "manifest", "receipt", "merkle_batch", "inclusion_proof", "intake_decision",
    ]
    missing = [field for field in required if field not in packet]
    if missing:
        raise ValueError(f"{path}: missing {', '.join(missing)}")
    if packet["packet_version"] != "stegverse.portable-evidence-intake.v1":
        raise ValueError(f"{path}: unsupported packet_version")
    if packet["producer_repository"] != "StegVerse-Labs/FREE-DOM":
        raise ValueError(f"{path}: unapproved producer")
    if packet["destination_repository"] != "StegVerse-Labs/Executive_Rhetoric_Ledger":
        raise ValueError(f"{path}: wrong destination")

    manifest = packet["manifest"]
    receipt = packet["receipt"]
    batch = packet["merkle_batch"]
    proof = packet["inclusion_proof"]
    decision = packet["intake_decision"]

    if manifest.get("producer_node_id") != "StegVerse-Labs/FREE-DOM":
        raise ValueError(f"{path}: manifest producer mismatch")
    if manifest.get("manifest_hash") != canonical_hash(manifest, "manifest_hash"):
        raise ValueError(f"{path}: manifest hash mismatch")
    if receipt.get("receipt_hash") != canonical_hash(receipt, "receipt_hash"):
        raise ValueError(f"{path}: receipt hash mismatch")
    if receipt.get("evidence_id") != manifest.get("evidence_id"):
        raise ValueError(f"{path}: receipt evidence mismatch")
    if receipt.get("manifest_hash") != manifest.get("manifest_hash"):
        raise ValueError(f"{path}: receipt manifest binding mismatch")
    if receipt.get("authority_class") != "observe" or receipt.get("evidence_effect") != "discovery-only":
        raise ValueError(f"{path}: producer exceeded discovery authority")
    if batch.get("batch_hash") != canonical_hash(batch, "batch_hash"):
        raise ValueError(f"{path}: batch hash mismatch")
    if proof.get("proof_hash") != canonical_hash(proof, "proof_hash"):
        raise ValueError(f"{path}: proof hash mismatch")
    if proof.get("receipt_hash") != receipt.get("receipt_hash"):
        raise ValueError(f"{path}: proof receipt mismatch")
    if proof.get("batch_hash") != batch.get("batch_hash"):
        raise ValueError(f"{path}: proof batch mismatch")
    if proof.get("merkle_root") != batch.get("merkle_root"):
        raise ValueError(f"{path}: proof root mismatch")
    if calculate_merkle_root(receipt["receipt_hash"], proof.get("siblings", [])) != batch.get("merkle_root"):
        raise ValueError(f"{path}: invalid Merkle inclusion proof")
    if receipt["receipt_hash"] not in batch.get("leaf_receipt_hashes", []):
        raise ValueError(f"{path}: receipt absent from batch")

    if decision.get("authority_effect") != "none":
        raise ValueError(f"{path}: intake may not grant authority")
    if decision.get("standing_effect") != "none-until-ledger-review":
        raise ValueError(f"{path}: intake may not grant standing")


def main() -> int:
    paths = sorted(PACKETS.glob("*.json")) if PACKETS.exists() else []
    if not paths:
        print("ALLOW portable_evidence_intake_valid packets=0")
        return 0
    try:
        ids: set[str] = set()
        for path in paths:
            packet = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(packet, dict):
                raise ValueError(f"{path}: root must be object")
            packet_id = packet.get("packet_id")
            if not packet_id or packet_id in ids:
                raise ValueError(f"{path}: missing or duplicate packet_id")
            ids.add(packet_id)
            validate_packet(packet, path)
    except (ValueError, json.JSONDecodeError, KeyError) as exc:
        print(f"DENY portable_evidence_intake_invalid: {exc}", file=sys.stderr)
        return 1
    print(f"ALLOW portable_evidence_intake_valid packets={len(paths)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
