#!/usr/bin/env python3
"""Validate producer acknowledgment objects and their succession links."""

from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    from jsonschema import Draft202012Validator
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "Missing dependency: jsonschema. Install with `python -m pip install jsonschema`."
    ) from exc

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "producer-acknowledgment.schema.json"
DEFAULT_DIR = ROOT / "producer_acknowledgments" / "example"


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in {path}: {exc}") from exc


def target_files(args: list[str]) -> list[Path]:
    if args:
        return [Path(arg).resolve() for arg in args]
    if not DEFAULT_DIR.exists():
        return []
    return sorted(DEFAULT_DIR.glob("*.json"))


def main(argv: list[str]) -> int:
    files = target_files(argv)
    if not files:
        print("No producer acknowledgment JSON files found.", file=sys.stderr)
        return 1

    schema = load_json(SCHEMA_PATH)
    validator = Draft202012Validator(schema)
    records: dict[str, tuple[dict, Path]] = {}
    failures: list[str] = []

    for path in files:
        try:
            record = load_json(path)
        except ValueError as exc:
            failures.append(str(exc))
            continue

        errors = sorted(validator.iter_errors(record), key=lambda error: list(error.path))
        if errors:
            error = errors[0]
            location = ".".join(str(part) for part in error.path) or "<root>"
            failures.append(f"{path}: schema failure at {location}: {error.message}")
            continue

        ack_id = record["acknowledgment_id"]
        if ack_id in records:
            failures.append(f"{path}: duplicate acknowledgment_id {ack_id}")
            continue
        records[ack_id] = (record, path)

    for ack_id, (record, path) in records.items():
        prior_id = record.get("supersedes_acknowledgment_id")
        if not prior_id:
            continue
        prior = records.get(prior_id)
        if prior is None:
            failures.append(f"{path}: supersedes unknown acknowledgment {prior_id}")
            continue
        prior_record = prior[0]
        if prior_record["ingestion_id"] != record["ingestion_id"]:
            failures.append(f"{path}: succession crosses ingestion_id boundary")
        if prior_record["producer_repo"] != record["producer_repo"]:
            failures.append(f"{path}: succession crosses producer_repo boundary")
        if prior_id == ack_id:
            failures.append(f"{path}: acknowledgment cannot supersede itself")

    current_by_ingestion: dict[str, list[str]] = {}
    superseded_ids = {
        record["supersedes_acknowledgment_id"]
        for record, _ in records.values()
        if record.get("supersedes_acknowledgment_id")
    }
    for ack_id, (record, _) in records.items():
        if ack_id not in superseded_ids:
            current_by_ingestion.setdefault(record["ingestion_id"], []).append(ack_id)

    for ingestion_id, current_ids in current_by_ingestion.items():
        if len(current_ids) != 1:
            failures.append(
                f"ingestion_id {ingestion_id} has {len(current_ids)} current acknowledgments: {current_ids}"
            )

    if failures:
        print("\n".join(f"FAIL {failure}" for failure in failures), file=sys.stderr)
        return 1

    for _, path in records.values():
        print(f"PASS {path}")
    print(f"Validated {len(records)} producer acknowledgment file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
