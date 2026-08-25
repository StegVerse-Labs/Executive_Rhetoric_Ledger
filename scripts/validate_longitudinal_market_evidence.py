#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

SCHEMA_BY_KIND = {
    "state": "schemas/market-state-vector.schema.json",
    "preference": "schemas/trade-preference-evidence.schema.json",
}


def load_json(path: str | Path) -> Any:
    return json.loads(Path(path).read_text())


def validate_document(document: dict[str, Any], schema: dict[str, Any]) -> list[str]:
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(document), key=lambda err: list(err.absolute_path))
    messages = [f"schema:{'/'.join(map(str, err.absolute_path)) or '<root>'}:{err.message}" for err in errors]

    if document.get("research_authority") != "ERL":
        messages.append("authority:research_authority_must_equal_ERL")
    if document.get("execution_authority") != "NONE":
        messages.append("authority:execution_authority_must_equal_NONE")
    if document.get("may_authorize_order") is not False:
        messages.append("authority:may_authorize_order_must_be_false")

    if document.get("schema") == "stegverse.erl.trade_preference_evidence.v1":
        coverage = document.get("source_coverage", {})
        confidence = document.get("confidence")
        analogue_count = len(document.get("historical_analogues", []))
        if coverage.get("coverage_score", 0) < 0.5 and document.get("preference") == "PREFER":
            messages.append("evidence:prefer_forbidden_when_source_coverage_below_0_5")
        if analogue_count == 0 and document.get("preference") not in {"INSUFFICIENT_EVIDENCE", "DEFER", "FOREGO"}:
            messages.append("evidence:nonempty_analogue_set_required_for_positive_preference")
        if isinstance(confidence, (int, float)) and confidence < 0.5 and document.get("preference") == "PREFER":
            messages.append("evidence:prefer_forbidden_when_confidence_below_0_5")

    return messages


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate ERL longitudinal market evidence documents.")
    parser.add_argument("kind", choices=sorted(SCHEMA_BY_KIND))
    parser.add_argument("document")
    parser.add_argument("--repo-root", default=".")
    args = parser.parse_args()

    root = Path(args.repo_root)
    schema = load_json(root / SCHEMA_BY_KIND[args.kind])
    document = load_json(args.document)
    errors = validate_document(document, schema)
    result = {
        "status": "PASS" if not errors else "FAIL",
        "kind": args.kind,
        "document": str(args.document),
        "errors": errors,
        "execution_authority": "NONE",
    }
    print(json.dumps(result, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
