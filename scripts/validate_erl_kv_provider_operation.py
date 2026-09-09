#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence/kv-provider-operations"
PROVIDER_PATH = EVIDENCE / "2026-09-09-google-drive-nsa-distillation.provider-operation-receipt.json"
NATIVE_PATH = EVIDENCE / "2026-09-09-google-drive-nsa-distillation.native-write-receipt.json"
MANIFEST_PATH = EVIDENCE / "2026-09-09-google-drive-nsa-distillation.manifest.json"
SCHEMA_PATH = ROOT / "schemas/erl-kv-provider-operation-receipt.schema.json"


def canonical_json(document: dict) -> bytes:
    return (json.dumps(document, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    provider = json.loads(PROVIDER_PATH.read_text(encoding="utf-8"))
    native = json.loads(NATIVE_PATH.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    errors = list(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(provider))
    if errors:
        raise SystemExit("\n".join(error.message for error in errors))

    artifact_id = provider["artifact_id"]
    if native["artifact_id"] != artifact_id or manifest["artifact_id"] != artifact_id:
        raise SystemExit("artifact identity mismatch across provider, native, and manifest evidence")
    if native["manifest_sha256"] != provider["manifest"]["sha256"]:
        raise SystemExit("native receipt and provider receipt disagree on manifest hash")
    if sha256(canonical_json(manifest)) != provider["manifest"]["sha256"]:
        raise SystemExit("canonical manifest bytes do not match provider receipt")
    if sha256(NATIVE_PATH.read_bytes()) != provider["native_writer_receipt"]["sha256"]:
        raise SystemExit("native writer receipt bytes do not match provider receipt")

    provider_objects = {item["filename"]: item for item in provider["objects"]}
    native_objects = {item["filename"]: item for item in native["objects"]}
    manifest_objects = {item["filename"]: item for item in manifest["objects"]}
    if set(provider_objects) != set(native_objects) or set(provider_objects) != set(manifest_objects):
        raise SystemExit("object membership mismatch across evidence chain")
    for filename, item in provider_objects.items():
        for candidate in (native_objects[filename], manifest_objects[filename]):
            if candidate["sha256"] != item["sha256"] or candidate["size_bytes"] != item["size_bytes"]:
                raise SystemExit(f"object hash/size mismatch: {filename}")
        if not item["readback_verified"]:
            raise SystemExit(f"provider readback not verified: {filename}")

    provider_ids = [
        provider["provider_folder"]["id"],
        provider["native_writer_receipt"]["provider_file_id"],
        provider["manifest"]["provider_file_id"],
        *[item["provider_file_id"] for item in provider["objects"]],
    ]
    if len(provider_ids) != len(set(provider_ids)):
        raise SystemExit("provider resource identifiers must be unique")
    if not all((
        provider["provider_write_execution_proven"],
        provider["native_writer_execution_proven"],
        provider["byte_for_byte_provider_readback_verified"],
        provider["provider_operation_receipt_retained"],
        provider["manifest"]["readback_verified"],
        provider["native_writer_receipt"]["readback_verified"],
    )):
        raise SystemExit("provider operation proof is incomplete")
    if provider["credential_material_present"]:
        raise SystemExit("credential material contaminated provider receipt")
    print("Live ERL KV provider operation receipt validated.")


if __name__ == "__main__":
    main()
