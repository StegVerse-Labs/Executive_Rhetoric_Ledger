#!/usr/bin/env python3
"""Validate Delaney Hall individualized force-event packets and their cross-record links."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "force-event-packet.schema.json"
EVENT_DIR = ROOT / "assessments" / "events"
ASSESSMENT_DIR = ROOT / "assessments" / "machine"
INTAKE_DIR = ROOT / "assessments" / "intake"
ASSESSMENT_INDEX = ROOT / "assessments" / "README.md"


def load(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    validator = Draft202012Validator(load(SCHEMA))
    assessments: dict[str, set[str]] = {}
    for path in ASSESSMENT_DIR.glob("*.json"):
        doc = load(path)
        if isinstance(doc, dict):
            topic = str(doc.get("topic_id", ""))
            receipts = doc.get("receipts", {})
            sources = receipts.get("sources", []) if isinstance(receipts, dict) else []
            assessments[topic] = {
                str(source.get("source_id", ""))
                for source in sources
                if isinstance(source, dict)
            }

    intake_ids: set[str] = set()
    for path in INTAKE_DIR.glob("*.json"):
        doc = load(path)
        if isinstance(doc, dict):
            for item in doc.get("items", []):
                if isinstance(item, dict):
                    intake_ids.add(str(item.get("intake_id", "")))

    try:
        index_text = ASSESSMENT_INDEX.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"FAIL: unable to read {ASSESSMENT_INDEX.relative_to(ROOT)}: {exc}", file=sys.stderr)
        return 1

    files = sorted(EVENT_DIR.glob("DH-FORCE-*.json"))
    if not files:
        print("FAIL: no Delaney Hall force-event packets found", file=sys.stderr)
        return 1

    failures: list[str] = []
    seen_ids: set[str] = set()
    for path in files:
        doc = load(path)
        errors = sorted(validator.iter_errors(doc), key=lambda error: list(error.path))
        for error in errors:
            location = ".".join(str(part) for part in error.path) or "<root>"
            failures.append(f"{path.relative_to(ROOT)}:{location}: {error.message}")
        if not isinstance(doc, dict):
            continue

        event_id = str(doc.get("event_id", ""))
        if event_id in seen_ids:
            failures.append(f"{path.relative_to(ROOT)}: duplicate event_id {event_id}")
        seen_ids.add(event_id)

        if not path.name.startswith(f"{event_id}-"):
            failures.append(
                f"{path.relative_to(ROOT)}: filename must begin with event_id {event_id}-"
            )

        relative_link = f"events/{path.name}"
        if event_id not in index_text:
            failures.append(
                f"{path.relative_to(ROOT)}: event_id {event_id} is missing from assessments/README.md"
            )
        if relative_link not in index_text:
            failures.append(
                f"{path.relative_to(ROOT)}: link {relative_link} is missing from assessments/README.md"
            )

        topic_id = str(doc.get("topic_id", ""))
        if topic_id not in assessments:
            failures.append(f"{path.relative_to(ROOT)}: unknown topic_id {topic_id}")
            continue

        for receipt_id in doc.get("source_receipt_ids", []):
            if receipt_id not in assessments[topic_id]:
                failures.append(
                    f"{path.relative_to(ROOT)}: source_receipt_id {receipt_id} is not present in assessment {topic_id}"
                )

        for intake_id in doc.get("intake_ids", []):
            if intake_id not in intake_ids:
                failures.append(f"{path.relative_to(ROOT)}: unknown intake_id {intake_id}")

        classification = doc.get("classification", {})
        status = str(doc.get("event_status", ""))
        if status == "accepted-with-limitations" and isinstance(classification, dict):
            if "not-established" in {
                classification.get("necessity"),
                classification.get("proportionality"),
                classification.get("lawfulness"),
            }:
                failures.append(
                    f"{path.relative_to(ROOT)}: accepted-with-limitations cannot retain not-established classification fields"
                )

        print(f"CHECKED {path.relative_to(ROOT)}")

    if failures:
        print("Force-event packet validation failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    print(
        f"Validated {len(files)} Delaney Hall individualized force-event packet(s), filenames, and assessment-index links."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
