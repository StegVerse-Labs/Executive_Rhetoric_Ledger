#!/usr/bin/env python3
"""Aggregate bounded Issue #30 reviewer comments into a governed receipt.

The script never invents a disposition or finding. It emits a blocked state until
at least two distinct reviewers submit matching dispositions through ERL-REVIEW-V1
comment blocks.
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "federal-force-review-receipt.schema.json"
MARKER = "ERL-REVIEW-V1"
EVENTS = ["RRM-FORCE-001", "RRM-FORCE-002", "RRM-FORCE-003"]
ALLOWED_AUTHORITY = {"evidence-reviewer", "civil-rights-reviewer", "legal-reviewer", "medical-evidence-reviewer"}
ALLOWED_DISPOSITIONS = {"accepted-with-limitations", "needs-more-evidence", "disputed", "rejected-unsupported", "rejected-out-of-scope"}


def parse_block(body: str) -> dict[str, object] | None:
    if MARKER not in body:
        return None
    values: dict[str, str] = {}
    for line in body.splitlines():
        match = re.match(r"^([a-z-]+):\s*(.+?)\s*$", line.strip())
        if match:
            values[match.group(1)] = match.group(2)
    required = {"disposition", "authority", "finding", "evidence-limit"}
    if not required.issubset(values):
        return None
    if values["disposition"] not in ALLOWED_DISPOSITIONS or values["authority"] not in ALLOWED_AUTHORITY:
        return None
    return values


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--comments", required=True)
    parser.add_argument("--receipt", required=True)
    parser.add_argument("--state", required=True)
    args = parser.parse_args()

    comments = json.loads(Path(args.comments).read_text(encoding="utf-8"))
    parsed: list[dict[str, object]] = []
    for comment in comments:
        block = parse_block(str(comment.get("body", "")))
        if block is None:
            continue
        parsed.append({
            **block,
            "github_login": str(comment.get("user", {}).get("login", "")),
            "comment_id": int(comment["id"]),
            "comment_created_at": str(comment["created_at"]),
        })

    latest_by_login: dict[str, dict[str, object]] = {}
    for item in sorted(parsed, key=lambda x: (str(x["comment_created_at"]), int(x["comment_id"]))):
        latest_by_login[str(item["github_login"])] = item
    votes = list(latest_by_login.values())

    counts: dict[str, int] = {}
    for vote in votes:
        disposition = str(vote["disposition"])
        counts[disposition] = counts.get(disposition, 0) + 1
    agreed = sorted([key for key, count in counts.items() if count >= 2])

    state = {
        "case_id": "RRM-SPI-2025-03-15",
        "issue_number": 30,
        "status": "awaiting-governed-review",
        "valid_reviewer_comments": len(votes),
        "matching_quorum_dispositions": agreed,
        "receipt_created": False,
        "manual_mechanics_remaining": False,
        "human_authority_remaining": True,
    }

    if len(agreed) == 1:
        disposition = agreed[0]
        agreeing = [vote for vote in votes if vote["disposition"] == disposition]
        authorities = {str(vote["authority"]) for vote in agreeing}
        if len(authorities) >= 2:
            receipt = {
                "receipt_version": "1.0",
                "issue_number": 30,
                "case_id": "RRM-SPI-2025-03-15",
                "reviewed_event_ids": EVENTS,
                "disposition": disposition,
                "reviewers": [{
                    "github_login": vote["github_login"],
                    "authority": vote["authority"],
                    "comment_id": vote["comment_id"],
                    "comment_created_at": vote["comment_created_at"],
                } for vote in agreeing],
                "findings": [str(vote["finding"]) for vote in agreeing],
                "evidence_limits": [str(vote["evidence-limit"]) for vote in agreeing],
                "created_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
                "authority": {
                    "automation_aggregated_comments": True,
                    "automation_selected_disposition": False,
                    "automation_expanded_findings": False,
                    "publication_authorized": disposition == "accepted-with-limitations",
                },
            }
            errors = list(Draft202012Validator(json.loads(SCHEMA.read_text())).iter_errors(receipt))
            if errors:
                raise SystemExit("Generated receipt failed schema validation: " + "; ".join(error.message for error in errors))
            receipt_path = Path(args.receipt)
            receipt_path.parent.mkdir(parents=True, exist_ok=True)
            receipt_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
            state.update({"status": "governed-review-receipt-ready", "receipt_created": True, "human_authority_remaining": False, "disposition": disposition})

    state_path = Path(args.state)
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(state, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
