#!/usr/bin/env python3
"""Validate the Fauci/HSGAC atomic-question reconstruction ledger."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "assessments" / "silence-causation" / "2026-07-29-fauci-hsgac-atomic-question-ledger.partial.json"
EXPECTED_SOURCE = "https://www.govinfo.gov/content/pkg/CHRG-119shrg64382/html/CHRG-119shrg64382.htm"
LINE_RANGE = re.compile(r"^[0-9]+(?:-[0-9]+)?$")
ALLOWED_RESPONSES = {
    "FIFTH_AMENDMENT_INVOCATION",
    "ANSWERED",
    "PARTIAL_ANSWER",
    "PROCEDURAL_RESPONSE",
    "NO_RESPONSE",
}


def fail(errors: list[str]) -> int:
    for error in errors:
        print(f"FAIL atomic-question-ledger: {error}", file=sys.stderr)
    return 1


def main() -> int:
    data = json.loads(LEDGER.read_text(encoding="utf-8"))
    errors: list[str] = []

    if data.get("source_url") != EXPECTED_SOURCE:
        errors.append("source_url must remain the official immutable GovInfo transcript pointer")
    if data.get("state") not in {"PARTIAL_NON_PROMOTIONAL", "COMPLETE_NON_PROMOTIONAL"}:
        errors.append("ledger state must remain non-promotional")

    records = data.get("records")
    if not isinstance(records, list) or not records:
        errors.append("records must be a non-empty list")
        return fail(errors)

    ids: list[int] = []
    seen: set[str] = set()
    by_id: dict[str, dict] = {}
    for record in records:
        aq = record.get("atomic_id")
        if not isinstance(aq, str) or not re.fullmatch(r"AQ-[0-9]{3}", aq):
            errors.append(f"invalid atomic_id: {aq!r}")
            continue
        if aq in seen:
            errors.append(f"duplicate atomic_id: {aq}")
        seen.add(aq)
        ids.append(int(aq.split("-")[1]))
        by_id[aq] = record

        for required in ("speaker", "turn_lines", "question_summary", "response_speaker", "response_state", "response_lines"):
            if not record.get(required):
                errors.append(f"{aq}: missing {required}")
        for key in ("turn_lines", "response_lines"):
            value = str(record.get(key, ""))
            if value and not LINE_RANGE.fullmatch(value):
                errors.append(f"{aq}: invalid {key} {value!r}")
        if record.get("response_state") not in ALLOWED_RESPONSES:
            errors.append(f"{aq}: invalid response_state {record.get('response_state')!r}")
        if record.get("response_state") == "FIFTH_AMENDMENT_INVOCATION":
            forbidden = {"admission", "guilt", "culpability", "motive_finding", "truth_finding"}
            present = forbidden.intersection(record)
            if present:
                errors.append(f"{aq}: Fifth invocation record contains prohibited inference fields {sorted(present)}")

    expected_ids = list(range(1, len(records) + 1))
    if sorted(ids) != expected_ids:
        errors.append(f"atomic IDs must be continuous AQ-001..AQ-{len(records):03d}")

    coverage = data.get("coverage", {})
    if coverage.get("atomics") != len(records):
        errors.append(f"coverage.atomics {coverage.get('atomics')} != record count {len(records)}")
    if coverage.get("proceeding_complete") is True and data.get("state") != "COMPLETE_NON_PROMOTIONAL":
        errors.append("proceeding_complete=true requires COMPLETE_NON_PROMOTIONAL state")

    controls = data.get("control_analysis", {})
    harmless = controls.get("harmless_baseline_ids", [])
    if len(harmless) < 3:
        errors.append("at least three harmless baseline questions are required")
    for aq in harmless:
        record = by_id.get(aq)
        if record is None:
            errors.append(f"harmless baseline id missing from ledger: {aq}")
        elif record.get("control_class") != "HARMLESS_BASELINE":
            errors.append(f"{aq}: harmless baseline must use HARMLESS_BASELINE control_class")
        elif record.get("response_state") != "FIFTH_AMENDMENT_INVOCATION":
            errors.append(f"{aq}: harmless baseline expected observed Fifth invocation")

    interpretation = str(controls.get("interpretation", "")).lower()
    if "cannot" not in interpretation or "standing alone" not in interpretation:
        errors.append("control interpretation must explicitly prevent standalone refusal inference")

    no_question_turns = data.get("senator_turns_without_witness_questions", [])
    speakers = [entry.get("speaker") for entry in no_question_turns if isinstance(entry, dict)]
    if len(speakers) != len(set(speakers)):
        errors.append("senator_turns_without_witness_questions contains duplicate speakers")

    boundary = str(data.get("promotion_boundary", "")).lower()
    for concept in ("motive", "culpability", "causation", "publication"):
        if concept not in boundary:
            errors.append(f"promotion_boundary must mention {concept}")

    if errors:
        return fail(errors)

    print(f"PASS atomic-question-ledger: {len(records)} atomics")
    print(f"PASS harmless-baseline: {len(harmless)} questions")
    print("PASS refusal semantics: invocation != admission")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
