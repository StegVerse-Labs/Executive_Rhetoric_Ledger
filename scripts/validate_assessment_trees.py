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
ASSESSMENT_INDEX_PATH = ROOT / "assessments" / "README.md"
REVIEW_DIR = ROOT / "assessments" / "reviews"
CONTROL_DIR = ROOT / "assessments" / "controls"
STANDALONE_RECEIPT_DIR = ROOT / "assessments" / "evidence" / "receipts"
TREE_SCHEMA_PATH = ROOT / "schemas" / "political-influence-tree.schema.json"
SOURCE_SCHEMA_PATH = ROOT / "schemas" / "source-posture.schema.json"


def load_json(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Unable to load {path.relative_to(ROOT)}: {exc}") from exc


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ValueError(f"Unable to read {path.relative_to(ROOT)}: {exc}") from exc


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


def standalone_receipt_index() -> tuple[set[str], list[str]]:
    source_ids: set[str] = set()
    failures: list[str] = []
    if not STANDALONE_RECEIPT_DIR.exists():
        return source_ids, failures

    for path in sorted(STANDALONE_RECEIPT_DIR.glob("*.json")):
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
        if source_id in source_ids:
            failures.append(f"{path.relative_to(ROOT)}: duplicate standalone source_id {source_id}")
        source_ids.add(source_id)
    return source_ids, failures


def main() -> int:
    tree_schema = load_json(TREE_SCHEMA_PATH)
    source_schema = load_json(SOURCE_SCHEMA_PATH)
    tree_validator = Draft202012Validator(tree_schema)
    source_validator = Draft202012Validator(source_schema)

    try:
        assessment_index = read_text(ASSESSMENT_INDEX_PATH)
    except ValueError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1

    files = sorted(ASSESSMENT_DIR.glob("*.json"))
    if not files:
        print(f"FAIL: no assessment trees found in {ASSESSMENT_DIR.relative_to(ROOT)}", file=sys.stderr)
        return 1

    standalone_ids, failures = standalone_receipt_index()

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

        if topic_id and topic_id not in assessment_index:
            failures.append(
                f"{path.relative_to(ROOT)}:topic_id: {topic_id} is not visible in assessments/README.md"
            )

        if path.name not in assessment_index:
            failures.append(
                f"{path.relative_to(ROOT)}: machine assessment file is not linked from assessments/README.md"
            )

        if related_annotation:
            annotation_path = ROOT / related_annotation
            if not annotation_path.is_file():
                failures.append(
                    f"{path.relative_to(ROOT)}:related_annotation: linked file does not exist: {related_annotation}"
                )
            elif annotation_path.name not in assessment_index:
                failures.append(
                    f"{path.relative_to(ROOT)}:related_annotation: {annotation_path.name} is not linked from assessments/README.md"
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

        if isinstance(receipts, dict):
            references = receipts.get("source_receipt_refs", [])
            if references is not None and not isinstance(references, list):
                failures.append(
                    f"{path.relative_to(ROOT)}:receipts.source_receipt_refs: must be an array"
                )
                references = []
            normalized_refs = [str(ref).strip() for ref in references if str(ref).strip()]
            duplicates = sorted({ref for ref in normalized_refs if normalized_refs.count(ref) > 1})
            for duplicate in duplicates:
                failures.append(
                    f"{path.relative_to(ROOT)}:receipts.source_receipt_refs: duplicate reference {duplicate}"
                )
            embedded_ids = {
                str(source.get("source_id", "")).strip()
                for source in sources
                if isinstance(source, dict) and str(source.get("source_id", "")).strip()
            }
            for reference in normalized_refs:
                if reference in embedded_ids:
                    failures.append(
                        f"{path.relative_to(ROOT)}:receipts.source_receipt_refs: {reference} is already embedded"
                    )
                elif reference not in standalone_ids:
                    failures.append(
                        f"{path.relative_to(ROOT)}:receipts.source_receipt_refs: standalone receipt {reference} not found"
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

    print(
        f"Validated {len(files)} assessment tree(s), index visibility, linked annotations, reviews, controls, embedded receipts, and standalone receipt references."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
