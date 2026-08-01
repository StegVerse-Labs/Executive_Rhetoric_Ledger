#!/usr/bin/env python3
"""Validate machine-readable primary-record intake queues."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "primary-record-intake.schema.json"
INTAKE_DIR = ROOT / "assessments" / "intake"
ASSESSMENT_DIRS = [ROOT / "assessments" / "machine", ROOT / "assessments" / "pit"]
SOURCE_PACKET_DIRS = [ROOT / "assessments" / "source-posture", ROOT / "assessments" / "receipts"]
STANDALONE_RECEIPT_DIRS = [ROOT / "assessments" / "evidence" / "receipts"]
ASSESSMENT_ROOT = ROOT / "assessments"


def load_json(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Unable to load {path.relative_to(ROOT)}: {exc}") from exc


def collect_source_ids(value: object) -> set[str]:
    """Collect explicitly named source receipt identifiers from nested packets."""
    found: set[str] = set()
    if isinstance(value, dict):
        source_id = str(value.get("source_id", "")).strip()
        if source_id:
            found.add(source_id)
        for child in value.values():
            found.update(collect_source_ids(child))
    elif isinstance(value, list):
        for child in value:
            found.update(collect_source_ids(child))
    return found


def index_aliases() -> dict[str, str]:
    """Map task record identifiers to their canonical PIT topic identifiers."""
    aliases: dict[str, str] = {}
    for path in sorted(ASSESSMENT_ROOT.glob("*INDEX.md")):
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        topic_match = re.search(r'^topic_id:\s*["\']?([^"\'\n]+)', text, re.MULTILINE)
        record_match = re.search(r'^record_id:\s*["\']?([^"\'\n]+)', text, re.MULTILINE)
        if topic_match and record_match:
            topic_id = topic_match.group(1).strip()
            record_id = record_match.group(1).strip()
            aliases[record_id] = topic_id
    return aliases


def standalone_receipt_index() -> tuple[set[str], list[str]]:
    source_ids: set[str] = set()
    failures: list[str] = []
    for directory in STANDALONE_RECEIPT_DIRS:
        if not directory.exists():
            continue
        for path in sorted(directory.glob("*.json")):
            try:
                document = load_json(path)
            except ValueError as exc:
                failures.append(str(exc))
                continue
            if not isinstance(document, dict):
                failures.append(f"{path.relative_to(ROOT)}: receipt must be a JSON object")
                continue
            source_id = str(document.get("source_id", "")).strip()
            if not source_id:
                failures.append(f"{path.relative_to(ROOT)}: missing source_id")
                continue
            source_ids.add(source_id)
    return source_ids, failures


def assessment_index() -> tuple[set[str], dict[str, set[str]], dict[str, str], list[str]]:
    topic_ids: set[str] = set()
    receipt_ids_by_topic: dict[str, set[str]] = {}
    aliases = index_aliases()
    failures: list[str] = []

    for directory in ASSESSMENT_DIRS:
        if not directory.exists():
            continue
        for path in sorted(directory.glob("*.json")):
            try:
                document = load_json(path)
            except ValueError as exc:
                failures.append(str(exc))
                continue
            if not isinstance(document, dict):
                continue
            topic_id = str(document.get("topic_id") or document.get("assessment_id") or "").strip()
            if not topic_id:
                print(f"SKIPPED {path.relative_to(ROOT)} (no governed assessment identifier)")
                continue
            topic_ids.add(topic_id)
            receipt_ids_by_topic.setdefault(topic_id, set()).update(collect_source_ids(document))

    for directory in SOURCE_PACKET_DIRS:
        if not directory.exists():
            continue
        for path in sorted(directory.glob("*.json")):
            try:
                document = load_json(path)
            except ValueError as exc:
                failures.append(str(exc))
                continue
            if not isinstance(document, dict):
                continue
            topic_id = str(document.get("topic_id") or document.get("assessment_id") or "").strip()
            if topic_id:
                receipt_ids_by_topic.setdefault(topic_id, set()).update(collect_source_ids(document))

    for alias, topic_id in aliases.items():
        if topic_id in topic_ids:
            topic_ids.add(alias)
            receipt_ids_by_topic[alias] = set(receipt_ids_by_topic.get(topic_id, set()))

    return topic_ids, receipt_ids_by_topic, aliases, failures


def main() -> int:
    schema = load_json(SCHEMA_PATH)
    validator = Draft202012Validator(schema)
    files = sorted(INTAKE_DIR.glob("*.json"))
    if not files:
        print("FAIL: no machine-readable intake queues found", file=sys.stderr)
        return 1

    topic_ids, receipt_ids_by_topic, aliases, failures = assessment_index()
    standalone_receipts, standalone_failures = standalone_receipt_index()
    failures.extend(standalone_failures)

    for path in files:
        try:
            document = load_json(path)
        except ValueError as exc:
            failures.append(str(exc))
            continue

        errors = sorted(validator.iter_errors(document), key=lambda error: list(error.path))
        for error in errors:
            location = ".".join(str(part) for part in error.path) or "<root>"
            failures.append(f"{path.relative_to(ROOT)}:{location}: {error.message}")

        if not isinstance(document, dict):
            continue

        topic_id = str(document.get("topic_id", "")).strip()
        canonical_topic = aliases.get(topic_id, topic_id)
        if topic_id not in topic_ids and canonical_topic not in topic_ids:
            failures.append(f"{path.relative_to(ROOT)}:topic_id: no machine-readable assessment exists for {topic_id}")
        known_receipts = receipt_ids_by_topic.get(topic_id, set()) | receipt_ids_by_topic.get(canonical_topic, set()) | standalone_receipts

        items = document.get("items", [])
        ids = [item.get("intake_id") for item in items if isinstance(item, dict)]
        duplicates = sorted({item_id for item_id in ids if ids.count(item_id) > 1})
        for duplicate in duplicates:
            failures.append(f"{path.relative_to(ROOT)}: duplicate intake_id {duplicate}")

        unresolved_states = {"requested", "located", "received-unverified", "conflicting-records", "restricted-or-sealed", "unavailable"}
        unresolved = [item for item in items if isinstance(item, dict) and item.get("state") in unresolved_states]
        if document.get("queue_status") == "complete" and unresolved:
            failures.append(f"{path.relative_to(ROOT)}: queue_status complete is invalid while {len(unresolved)} item(s) remain unresolved")

        for item in items:
            if not isinstance(item, dict):
                continue
            intake_id = item.get("intake_id")
            state = item.get("state")
            receipts = item.get("source_receipt_ids", [])
            if state in {"verified-primary", "verified-secondary"} and not receipts:
                failures.append(f"{path.relative_to(ROOT)}:{intake_id}: verified state requires at least one source_receipt_id")
            for receipt_id in receipts:
                if receipt_id not in known_receipts:
                    failures.append(f"{path.relative_to(ROOT)}:{intake_id}: source_receipt_id {receipt_id} is not present in assessment {topic_id}, its governed source packets, or the standalone receipt registry")

        print(f"CHECKED {path.relative_to(ROOT)}")

    if failures:
        print("Primary-record intake validation failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    print(f"Validated {len(files)} primary-record intake queue(s), governed assessment/source-packet receipts, {len(aliases)} task alias(es), and {len(standalone_receipts)} standalone receipt id(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
