#!/usr/bin/env python3
"""Validate machine-readable assessment Political Influence Trees.

This validator reuses the repository's existing Political Influence Tree and
Source Posture schemas. It intentionally does not introduce a parallel
assessment schema.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
ASSESSMENT_DIR = ROOT / "assessments" / "machine"
REVIEW_DIR = ROOT / "assessments" / "reviews"
CONTROL_DIR = ROOT / "assessments" / "controls"
TREE_SCHEMA_PATH = ROOT / "schemas" / "political-influence-tree.schema.json"
SOURCE_SCHEMA_PATH = ROOT / "schemas" / "source-posture.schema.json"


def load_json(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Unable to load {path.relative_to(ROOT)}: {exc}") from exc


def format_errors(path: Path, errors: list) -> list[str]:
    lines: list[str] = []
    for error in errors:
        location = ".".join(str(part) for part in error.path) or "<root>"
        lines.append(f"{path.relative_to(ROOT)}:{location}: {error.message}")
    return lines


def find_topic_reference(directory: Path, topic_id: str) -> bool:
    if not directory.exists():
        return False
    for candidate in directory.glob("*.md"):
        try:
            if topic_id in candidate.read_text(encoding="utf-8"):
                return True
        except OSError:
            continue
    return False


def main() -> int:
    tree_schema = load_json(TREE_SCHEMA_PATH)
    source_schema = load_json(SOURCE_SCHEMA_PATH)
    tree_validator = Draft202012Validator(tree_schema)
    source_validator = Draft202012Validator(source_schema)

    files = sorted(ASSESSMENT_DIR.glob("*.json"))
    if not files:
        print(f"FAIL: no assessment trees found in {ASSESSMENT_DIR.relative_to(ROOT)}", file=sys.stderr)
        return 1

    failures: list[str] = []

    for path in files:
        try:
            document = load_json(path)
        except ValueError as exc:
            failures.append(str(exc))
            continue

        tree_errors = sorted(
            tree_validator.iter_errors(document), key=lambda error: list(error.path)
        )
        failures.extend(format_errors(path, tree_errors))

        if not isinstance(document, dict):
            continue

        topic_id = str(document.get("topic_id", "")).strip()
        related_annotation = str(document.get("related_annotation", "")).strip()
        if related_annotation:
            annotation_path = ROOT / related_annotation
            if not annotation_path.is_file():
                failures.append(
                    f"{path.relative_to(ROOT)}:related_annotation: linked file does not exist: {related_annotation}"
                )

        receipts = document.get("receipts", {})
        sources = receipts.get("sources", []) if isinstance(receipts, dict) else []
        if not sources:
            failures.append(f"{path.relative_to(ROOT)}:receipts.sources: at least one source receipt is required")
        else:
            for index, source in enumerate(sources):
                source_errors = sorted(
                    source_validator.iter_errors(source), key=lambda error: list(error.path)
                )
                for error in source_errors:
                    location = ".".join(str(part) for part in error.path) or "<root>"
                    failures.append(
                        f"{path.relative_to(ROOT)}:receipts.sources.{index}.{location}: {error.message}"
                    )

        classification = document.get("ledger_classification", {})
        control = document.get("control_comparison", {})
        if isinstance(control, dict) and control.get("required") is True:
            status = str(control.get("status", "")).strip()
            if not status:
                failures.append(f"{path.relative_to(ROOT)}:control_comparison.status: required control comparison must have a status")
            if topic_id and not find_topic_reference(CONTROL_DIR, topic_id):
                failures.append(
                    f"{path.relative_to(ROOT)}:control_comparison: required control file referencing {topic_id} not found"
                )

        entry_status = str(document.get("entry_status", "")).strip()
        if entry_status in {"review", "published"} and topic_id:
            if not find_topic_reference(REVIEW_DIR, topic_id):
                failures.append(
                    f"{path.relative_to(ROOT)}:entry_status: {entry_status} entry requires a review file referencing {topic_id}"
                )

        if isinstance(classification, dict):
            admissibility = str(classification.get("admissibility_status", ""))
            confidence = str(classification.get("confidence", ""))
            if "justified" in admissibility and confidence not in {"high", "medium"}:
                failures.append(
                    f"{path.relative_to(ROOT)}:ledger_classification: justification classification requires medium or high confidence"
                )

        print(f"CHECKED {path.relative_to(ROOT)}")

    if failures:
        print("Assessment tree validation failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    print(f"Validated {len(files)} assessment tree(s), linked annotations, reviews, controls, and embedded source receipts.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
