#!/usr/bin/env python3
"""Persist validated ERL artifact bundles into an already-mounted KnowledgeVault."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Mapping


SCHEMA = "stegverse.erl.kv-artifact/v1"
RECEIPT_SCHEMA = "stegverse.erl.kv-write-receipt/v1"
KV_LANE = Path("02_Research") / "ERL"
SAFE_COMPONENT = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
ARTIFACT_CLASSES = {
    "SOURCE_CAPTURE",
    "ERL_RESEARCH_ARTIFACT",
    "ASSESSMENT",
    "EVIDENCE_RECEIPT",
    "REVIEW_RECORD",
}


class ERLKVWriteError(ValueError):
    """Raised when an ERL bundle cannot be safely persisted."""


def _canonical_json(document: Mapping[str, Any]) -> bytes:
    return (
        json.dumps(document, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode("utf-8")


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _require_safe_component(value: Any, field: str) -> str:
    if not isinstance(value, str) or not SAFE_COMPONENT.fullmatch(value):
        raise ERLKVWriteError(f"{field} must be a safe path component")
    return value


def _require_rfc3339(value: Any, field: str) -> None:
    if not isinstance(value, str) or not value.endswith("Z"):
        raise ERLKVWriteError(f"{field} must be an RFC3339 UTC timestamp")
    try:
        datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError as exc:
        raise ERLKVWriteError(f"{field} must be an RFC3339 UTC timestamp") from exc


def validate_manifest(manifest: Mapping[str, Any]) -> None:
    if manifest.get("schema") != SCHEMA:
        raise ERLKVWriteError(f"schema must equal {SCHEMA}")

    _require_safe_component(manifest.get("artifact_id"), "artifact_id")
    if manifest.get("artifact_class") not in ARTIFACT_CLASSES:
        raise ERLKVWriteError("artifact_class is unsupported")
    _require_rfc3339(manifest.get("captured_at"), "captured_at")

    source = manifest.get("source")
    if not isinstance(source, dict):
        raise ERLKVWriteError("source must be an object")
    for field in ("title", "publisher", "primary_url"):
        if not isinstance(source.get(field), str) or not source[field].strip():
            raise ERLKVWriteError(f"source.{field} is required")
    if not source["primary_url"].startswith(("https://", "http://")):
        raise ERLKVWriteError("source.primary_url must be HTTP(S)")

    storage = manifest.get("storage")
    if not isinstance(storage, dict):
        raise ERLKVWriteError("storage must be an object")
    if storage.get("lane") != KV_LANE.as_posix():
        raise ERLKVWriteError(f"storage.lane must equal {KV_LANE.as_posix()}")
    _require_safe_component(storage.get("kv_instance_id"), "storage.kv_instance_id")
    if storage.get("credential_material_present") is not False:
        raise ERLKVWriteError("credential material must not be stored in ERL KV artifacts")

    objects = manifest.get("objects")
    if not isinstance(objects, list) or not objects:
        raise ERLKVWriteError("objects must be a non-empty array")
    names: set[str] = set()
    for index, item in enumerate(objects):
        if not isinstance(item, dict):
            raise ERLKVWriteError(f"objects[{index}] must be an object")
        filename = _require_safe_component(item.get("filename"), f"objects[{index}].filename")
        if filename == "manifest.json" or filename in names:
            raise ERLKVWriteError("object filenames must be unique and exclude manifest.json")
        names.add(filename)
        if not re.fullmatch(r"[0-9a-f]{64}", str(item.get("sha256", ""))):
            raise ERLKVWriteError(f"objects[{index}].sha256 must be lowercase SHA-256")
        if not isinstance(item.get("size_bytes"), int) or item["size_bytes"] < 0:
            raise ERLKVWriteError(f"objects[{index}].size_bytes must be non-negative")
        if not isinstance(item.get("media_type"), str) or not item["media_type"]:
            raise ERLKVWriteError(f"objects[{index}].media_type is required")
        if not isinstance(item.get("role"), str) or not item["role"]:
            raise ERLKVWriteError(f"objects[{index}].role is required")


def _preflight(destination: Path, data: bytes) -> str:
    if not destination.exists():
        return "WRITE"
    if destination.is_symlink() or not destination.is_file():
        raise ERLKVWriteError(f"destination is not a regular file: {destination}")
    if destination.read_bytes() != data:
        raise ERLKVWriteError(f"conflicting artifact already exists: {destination.name}")
    return "NOOP"


def _exclusive_write(destination: Path, data: bytes) -> None:
    try:
        descriptor = os.open(destination, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except FileExistsError:
        if destination.read_bytes() != data:
            raise ERLKVWriteError(f"concurrent conflicting write: {destination.name}")
        return
    with os.fdopen(descriptor, "wb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    if destination.read_bytes() != data:
        raise ERLKVWriteError(f"readback mismatch: {destination.name}")


def write_bundle(
    *,
    kv_root: Path,
    manifest: Mapping[str, Any],
    payloads: Mapping[str, Path],
) -> dict[str, Any]:
    """Write one create-only, idempotent ERL artifact bundle into KV."""

    validate_manifest(manifest)
    root = kv_root.expanduser().resolve()
    if not root.is_dir():
        raise ERLKVWriteError("kv_root must be an existing mounted directory")

    artifact_id = str(manifest["artifact_id"])
    destination = (root / KV_LANE / artifact_id).resolve()
    try:
        destination.relative_to(root)
    except ValueError as exc:
        raise ERLKVWriteError("resolved artifact destination escaped kv_root") from exc

    expected = {str(item["filename"]): item for item in manifest["objects"]}
    if set(payloads) != set(expected):
        raise ERLKVWriteError("payload filenames must exactly match manifest objects")

    payload_bytes: dict[str, bytes] = {}
    for filename, item in expected.items():
        source_path = Path(payloads[filename])
        if source_path.is_symlink() or not source_path.is_file():
            raise ERLKVWriteError(f"payload is not a regular file: {filename}")
        data = source_path.read_bytes()
        if len(data) != item["size_bytes"]:
            raise ERLKVWriteError(f"payload size mismatch: {filename}")
        if _sha256(data) != item["sha256"]:
            raise ERLKVWriteError(f"payload hash mismatch: {filename}")
        payload_bytes[filename] = data

    manifest_bytes = _canonical_json(manifest)
    if destination.exists():
        planned = {
            filename: _preflight(destination / filename, data)
            for filename, data in payload_bytes.items()
        }
        planned["manifest.json"] = _preflight(destination / "manifest.json", manifest_bytes)
    else:
        planned = {filename: "WRITE" for filename in payload_bytes}
        planned["manifest.json"] = "WRITE"

    destination.mkdir(parents=True, exist_ok=True)
    for filename, data in payload_bytes.items():
        if planned[filename] == "WRITE":
            _exclusive_write(destination / filename, data)
    if planned["manifest.json"] == "WRITE":
        _exclusive_write(destination / "manifest.json", manifest_bytes)

    result = "WRITTEN" if "WRITE" in planned.values() else "NOOP"
    return {
        "schema": RECEIPT_SCHEMA,
        "artifact_id": artifact_id,
        "result": result,
        "kv_instance_id": manifest["storage"]["kv_instance_id"],
        "lane": KV_LANE.as_posix(),
        "relative_artifact_path": (KV_LANE / artifact_id).as_posix(),
        "manifest_sha256": _sha256(manifest_bytes),
        "objects": [
            {
                "filename": filename,
                "sha256": expected[filename]["sha256"],
                "size_bytes": expected[filename]["size_bytes"],
                "write_result": planned[filename],
            }
            for filename in sorted(expected)
        ],
        "credential_material_present": False,
        "readback_verified": True,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--kv-root", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--payload-dir", type=Path, required=True)
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    payloads = {
        str(item["filename"]): args.payload_dir / str(item["filename"])
        for item in manifest.get("objects", [])
    }
    receipt = write_bundle(kv_root=args.kv_root, manifest=manifest, payloads=payloads)
    rendered = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    if args.receipt:
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
