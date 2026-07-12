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


def canonical_value_hash(value: Any) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def canonical_hash(obj: dict[str, Any], hash_field: str) -> str:
    return canonical_value_hash({key: value for key, value in obj.items() if key != hash_field})


def calculate_merkle_root(receipt_hash: str, siblings: list[dict[str, str]]) -> str:
    current = bytes.fromhex(receipt_hash.split(":", 1)[1])
    for sibling in siblings:
        sibling_bytes = bytes.fromhex(sibling["hash"].split(":", 1)[1])
        position = sibling.get("position")
        if position == "left":
            current = hashlib.sha256(sibling_bytes + current).digest()
        elif position == "right":
            current = hashlib.sha256(current + sibling_bytes).digest()
        else:
            raise ValueError("proof sibling position must be left or right")
    return "sha256:" + current.hex()


def validate_packet(packet: dict[str, Any], path: Path) -> None:
    required = [
        "packet_version", "packet_id", "producer_repository", "destination_repository",
        "received_at", "artifact", "manifest", "receipt", "merkle_batch",
        "inclusion_proof", "intake_decision",
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

    artifact = packet["artifact"]
    manifest = packet["manifest"]
    receipt = packet["receipt"]
    batch = packet["merkle_batch"]
    proof = packet["inclusion_proof"]
    decision = packet["intake_decision"]

    if not all(isinstance(item, dict) for item in (artifact, manifest, receipt, batch, proof, decision)):
        raise ValueError(f"{path}: packet components must be objects")
    if manifest.get("producer_node_id") != "StegVerse-Labs/FREE-DOM":
        raise ValueError(f"{path}: manifest producer mismatch")
    if manifest.get("manifest_hash") != canonical_hash(manifest, "manifest_hash"):
        raise ValueError(f"{path}: manifest hash mismatch")
    if manifest.get("artifact", {}).get("content_hash") != canonical_value_hash(artifact):
        raise ValueError(f"{path}: artifact content hash mismatch")
    declared_size = manifest.get("artifact", {}).get("size_bytes")
    actual_size = len(json.dumps(artifact, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8"))
    if declared_size is not None and declared_size != actual_size:
        raise ValueError(f"{path}: artifact size mismatch")

    if receipt.get("receipt_hash") != canonical_hash(receipt, "receipt_hash"):
        raise ValueError(f"{path}: receipt hash mismatch")
    if receipt.get("evidence_id") != manifest.get("evidence_id"):
        raise ValueError(f"{path}: receipt evidence mismatch")
    if receipt.get("manifest_hash") != manifest.get("manifest_hash"):
        raise ValueError(f"{path}: receipt manifest binding mismatch")
    if receipt.get("authority_class") != "observe" or receipt.get("evidence_effect") != "discovery-only":
        raise ValueError(f"{path}: producer exceeded discovery authority")
    if receipt.get("transition_type") not in {"discovered", "captured"}:
        raise ValueError(f"{path}: unsupported producer transition")

    if receipt.get("transition_type") == "captured":
        subjects = manifest.get("subjects", [])
        if not subjects or not any(subject.get("subject_type") == "artifact" for subject in subjects if isinstance(subject, dict)):
            raise ValueError(f"{path}: captured run receipt must describe a run artifact")
        excluded = (receipt.get("standing") or {}).get("excluded_inferences", [])
        if not any("absence" in str(item).lower() for item in excluded):
            raise ValueError(f"{path}: run receipt must exclude absence inference")
        results = artifact.get("results")
        if not isinstance(results, dict) or "total_hits" not in results or "source_failures" not in results:
            raise ValueError(f"{path}: run artifact lacks bounded result fields")

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
    leaves = batch.get("leaf_receipt_hashes", [])
    if receipt["receipt_hash"] not in leaves:
        raise ValueError(f"{path}: receipt absent from batch")
    index = proof.get("leaf_index")
    if not isinstance(index, int) or index < 0 or index >= len(leaves) or leaves[index] != receipt["receipt_hash"]:
        raise ValueError(f"{path}: proof leaf index mismatch")

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
