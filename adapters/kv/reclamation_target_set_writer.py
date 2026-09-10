#!/usr/bin/env python3
"""Persist deterministic reclamation target sets into an authorized KnowledgeVault."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from pathlib import Path
from typing import Any, Mapping

TARGET_SCHEMA = "stegverse.reclamation-target-set/v1"
WRITE_RECEIPT_SCHEMA = "stegverse.reclamation.kv-write-receipt/v1"
READBACK_RECEIPT_SCHEMA = "stegverse.reclamation.kv-readback-receipt/v1"
PROOF_CLASS = "NATIVE_KV_WRITER_EXACT_READBACK"
KV_LANE = Path("02_Research") / "Data_Reclamation" / "Subjects"
HEX64 = re.compile(r"^[0-9a-f]{64}$")


class ReclamationKVError(ValueError):
    pass


def _canonical_json(document: Mapping[str, Any]) -> bytes:
    return (json.dumps(document, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _key(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:24]


def _validate_target_set(document: Mapping[str, Any]) -> None:
    if document.get("schema") != TARGET_SCHEMA:
        raise ReclamationKVError(f"schema must equal {TARGET_SCHEMA}")
    for field in ("target_set_id", "subject_ref", "generated_at"):
        if not isinstance(document.get(field), str) or not document[field]:
            raise ReclamationKVError(f"{field} is required")
    if not isinstance(document.get("targets"), list):
        raise ReclamationKVError("targets must be an array")


def _destination(kv_root: Path, subject_ref: str, target_set_id: str) -> Path:
    root = kv_root.expanduser().resolve()
    if not root.is_dir():
        raise ReclamationKVError("kv_root must be an existing mounted directory")
    dest = (root / KV_LANE / _key(subject_ref) / _key(target_set_id) / "target-set.json").resolve()
    try:
        dest.relative_to(root)
    except ValueError as exc:
        raise ReclamationKVError("resolved destination escaped kv_root") from exc
    return dest


def _exclusive_write(path: Path, data: bytes) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.is_symlink() or not path.is_file():
            raise ReclamationKVError("destination is not a regular file")
        if path.read_bytes() != data:
            raise ReclamationKVError("conflicting target set already exists")
        return "NOOP"
    try:
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except FileExistsError:
        if path.read_bytes() != data:
            raise ReclamationKVError("concurrent conflicting write")
        return "NOOP"
    with os.fdopen(fd, "wb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    if path.read_bytes() != data:
        raise ReclamationKVError("post-write readback mismatch")
    return "WRITTEN"


def write_target_set(*, kv_root: Path, target_set: Mapping[str, Any], kv_instance_id: str) -> dict[str, Any]:
    _validate_target_set(target_set)
    if not isinstance(kv_instance_id, str) or not kv_instance_id:
        raise ReclamationKVError("kv_instance_id is required")
    data = _canonical_json(target_set)
    subject_ref = str(target_set["subject_ref"])
    target_set_id = str(target_set["target_set_id"])
    path = _destination(kv_root, subject_ref, target_set_id)
    result = _exclusive_write(path, data)
    root = kv_root.expanduser().resolve()
    return {
        "schema": WRITE_RECEIPT_SCHEMA,
        "target_set_id": target_set_id,
        "subject_ref": subject_ref,
        "subject_key": _key(subject_ref),
        "target_set_key": _key(target_set_id),
        "kv_instance_id": kv_instance_id,
        "relative_path": path.relative_to(root).as_posix(),
        "sha256": _sha256(data),
        "size_bytes": len(data),
        "result": result,
        "proof_class": PROOF_CLASS,
        "readback_verified": True,
        "provider_deletion_success": False,
        "credential_material_present": False,
    }


def readback_target_set(*, kv_root: Path, write_receipt: Mapping[str, Any]) -> dict[str, Any]:
    if write_receipt.get("schema") != WRITE_RECEIPT_SCHEMA:
        raise ReclamationKVError("unsupported write receipt schema")
    subject_ref = write_receipt.get("subject_ref")
    target_set_id = write_receipt.get("target_set_id")
    if not isinstance(subject_ref, str) or not isinstance(target_set_id, str):
        raise ReclamationKVError("receipt subject/target identity missing")
    if write_receipt.get("subject_key") != _key(subject_ref) or write_receipt.get("target_set_key") != _key(target_set_id):
        raise ReclamationKVError("receipt identity binding mismatch")
    digest = write_receipt.get("sha256")
    if not isinstance(digest, str) or not HEX64.fullmatch(digest):
        raise ReclamationKVError("receipt sha256 invalid")
    expected = _destination(kv_root, subject_ref, target_set_id)
    root = kv_root.expanduser().resolve()
    if write_receipt.get("relative_path") != expected.relative_to(root).as_posix():
        raise ReclamationKVError("receipt path binding mismatch")
    if expected.is_symlink() or not expected.is_file():
        raise ReclamationKVError("target set is not readable as a regular file")
    data = expected.read_bytes()
    if len(data) != write_receipt.get("size_bytes") or _sha256(data) != digest:
        raise ReclamationKVError("exact-byte readback mismatch")
    document = json.loads(data.decode("utf-8"))
    _validate_target_set(document)
    if document.get("subject_ref") != subject_ref or document.get("target_set_id") != target_set_id:
        raise ReclamationKVError("stored target identity mismatch")
    return {
        "schema": READBACK_RECEIPT_SCHEMA,
        "target_set_id": target_set_id,
        "subject_ref": subject_ref,
        "kv_instance_id": write_receipt.get("kv_instance_id"),
        "relative_path": write_receipt.get("relative_path"),
        "sha256": digest,
        "size_bytes": len(data),
        "exact_byte_match": True,
        "proof_class": PROOF_CLASS,
        "provider_deletion_success": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--kv-root", type=Path, required=True)
    parser.add_argument("--target-set", type=Path, required=True)
    parser.add_argument("--kv-instance-id", required=True)
    parser.add_argument("--write-receipt", type=Path, required=True)
    parser.add_argument("--readback-receipt", type=Path, required=True)
    args = parser.parse_args()
    target_set = json.loads(args.target_set.read_text(encoding="utf-8"))
    write_receipt = write_target_set(kv_root=args.kv_root, target_set=target_set, kv_instance_id=args.kv_instance_id)
    readback_receipt = readback_target_set(kv_root=args.kv_root, write_receipt=write_receipt)
    for path, receipt in ((args.write_receipt, write_receipt), (args.readback_receipt, readback_receipt)):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"write_receipt": write_receipt, "readback_receipt": readback_receipt}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
