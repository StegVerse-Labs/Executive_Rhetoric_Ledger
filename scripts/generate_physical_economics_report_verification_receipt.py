#!/usr/bin/env python3
"""Generate a portable verification receipt for a rendered Physical Economics report."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "physical-economics-report-verification-receipt.schema.json"


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_bytes(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def generate(
    report_id: str,
    report_bytes: bytes,
    request: dict[str, Any],
    snapshot: dict[str, Any],
    boundary: dict[str, Any],
    renderer_version: str,
) -> dict[str, Any]:
    receipts = boundary["receipts"]
    notes: list[str] = []
    state = "VERIFIABLE"

    if boundary["evidence_snapshot_id"] != snapshot["evidence_snapshot_id"]:
        state = "FAIL_CLOSED_PROTOCOL_MISMATCH"
        notes.append("boundary manifest evidence_snapshot_id does not match supplied snapshot")
    if receipts.get("evidence_snapshot_hash") != snapshot.get("snapshot_hash"):
        state = "FAIL_CLOSED_HASH_MISMATCH"
        notes.append("boundary manifest evidence_snapshot_hash does not match supplied snapshot")
    if receipts.get("report_request_hash") is None:
        state = "FAIL_CLOSED_MISSING_RECEIPT"
        notes.append("boundary manifest lacks report request hash")
    if receipts.get("pertinence_matrix_version") is None or receipts.get("contract_version") is None:
        state = "FAIL_CLOSED_MISSING_RECEIPT"
        notes.append("boundary manifest lacks protocol version receipts")

    source_receipt_ids = [item["source_receipt_id"] for item in snapshot.get("source_receipts", [])]
    boundary_source_ids = receipts.get("source_receipt_set", [])
    if sorted(source_receipt_ids) != sorted(boundary_source_ids):
        state = "FAIL_CLOSED_MISSING_RECEIPT"
        notes.append("boundary source receipt set does not match evidence snapshot source receipts")

    result = {
        "verification_receipt_id": f"PE-VR-{hashlib.sha256((report_id + boundary['boundary_manifest_id']).encode('utf-8')).hexdigest()[:16]}",
        "report_id": report_id,
        "report_request_hash": receipts.get("report_request_hash", "MISSING"),
        "evidence_snapshot_id": snapshot["evidence_snapshot_id"],
        "evidence_snapshot_hash": snapshot.get("snapshot_hash", "MISSING"),
        "boundary_manifest_id": boundary["boundary_manifest_id"],
        "boundary_manifest_hash": receipts.get("boundary_manifest_hash", "MISSING"),
        "pertinence_matrix_version": receipts.get("pertinence_matrix_version", "MISSING"),
        "contract_version": receipts.get("contract_version", "MISSING"),
        "renderer_version": renderer_version,
        "report_content_hash": sha256_bytes(report_bytes),
        "source_receipt_ids": source_receipt_ids,
        "verification_state": state,
        "verification_notes": notes,
    }
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("report", type=Path)
    parser.add_argument("request", type=Path)
    parser.add_argument("snapshot", type=Path)
    parser.add_argument("boundary", type=Path)
    parser.add_argument("--report-id", required=True)
    parser.add_argument("--renderer-version", required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = generate(
        args.report_id,
        args.report.read_bytes(),
        load(args.request),
        load(args.snapshot),
        load(args.boundary),
        args.renderer_version,
    )
    schema = load(SCHEMA_PATH)
    errors = list(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(result))
    if errors:
        for error in errors:
            print(f"FAIL verification receipt schema: {error.message}", file=sys.stderr)
        return 1

    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded, encoding="utf-8")
    else:
        print(encoded, end="")
    return 0 if result["verification_state"] == "VERIFIABLE" else 1


if __name__ == "__main__":
    raise SystemExit(main())
