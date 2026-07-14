#!/usr/bin/env python3
"""Validate incident evidence streams for reconstructability and Merkle consistency."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

try:
    import jsonschema
except ImportError as exc:
    raise SystemExit("jsonschema is required") from exc

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "incident-evidence-stream.schema.json"
STREAM_DIR = ROOT / "incident-evidence-streams"


def canonical_hash(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def merkle_root(leaves: list[str]) -> str:
    if not leaves:
        raise ValueError("cannot calculate Merkle root without leaves")
    level = leaves[:]
    while len(level) > 1:
        if len(level) % 2:
            level.append(level[-1])
        level = [
            hashlib.sha256(bytes.fromhex(level[i]) + bytes.fromhex(level[i + 1])).hexdigest()
            for i in range(0, len(level), 2)
        ]
    return level[0]


def validate_semantics(record: dict[str, Any], path: Path) -> list[str]:
    errors: list[str] = []
    events = record["events"]

    sequences = [event["sequence"] for event in events]
    if sequences != list(range(len(events))):
        errors.append("event sequences must be contiguous and begin at zero")

    hashes = [event["payload_hash"] for event in events]
    known = set(hashes)
    for event in events:
        for parent in event["parent_hashes"]:
            if parent not in known:
                errors.append(f"{event['event_id']}: unknown parent hash {parent}")

    root = merkle_root(hashes)
    merkle = record["merkle"]
    if merkle["root_status"] == "computed" and merkle["root_hash"] != root:
        errors.append(f"Merkle root mismatch: declared {merkle['root_hash']} calculated {root}")

    acknowledgments = record["replication"]["acknowledgments"]
    verified = [a for a in acknowledgments if a["custody_status"] in {"stored", "verified"}]
    if len(verified) < record["replication"]["required_replicas"]:
        errors.append("insufficient stored or verified replica acknowledgments")
    if merkle["root_status"] == "computed":
        for ack in verified:
            if ack["root_hash"] != root:
                errors.append(f"replica {ack['replica_id']} acknowledges a different root")

    reconstruction = record["reconstruction"]
    dimensions = reconstruction["dimension_status"]
    calculated_complete = all(value == "complete" for value in dimensions.values())
    if reconstruction["complete"] != calculated_complete:
        errors.append("reconstruction.complete does not match dimension statuses")
    if not calculated_complete and not reconstruction["missing_data_receipts"]:
        errors.append("incomplete reconstruction requires at least one missing-data receipt")
    if calculated_complete and reconstruction["missing_data_receipts"]:
        errors.append("complete reconstruction cannot retain unresolved missing-data receipts")

    for event in events:
        if event["event_type"] == "gap" and reconstruction["complete"]:
            errors.append("a stream containing an unresolved gap event cannot be complete")

    return [f"{path}: {error}" for error in errors]


def main() -> int:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker())
    paths = sorted(STREAM_DIR.rglob("*.json")) if STREAM_DIR.exists() else []
    if not paths:
        print("No incident evidence streams found.")
        return 0

    failures: list[str] = []
    for path in paths:
        record = json.loads(path.read_text(encoding="utf-8"))
        for error in validator.iter_errors(record):
            failures.append(f"{path}: schema error at {'/'.join(map(str, error.path))}: {error.message}")
        if not failures:
            failures.extend(validate_semantics(record, path))

    if failures:
        print("\n".join(failures), file=sys.stderr)
        return 1

    print(f"Validated {len(paths)} incident evidence stream(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
