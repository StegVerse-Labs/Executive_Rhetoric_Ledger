#!/usr/bin/env python3
"""Fail-closed validator for ERL research source-candidate transport/intake.

Validates candidate packets without conferring evidentiary standing. Uses only
Python stdlib so every acquisition repository can reproduce the gate locally.
"""
from __future__ import annotations

import json
import pathlib
import re
import sys

SHA256 = re.compile(r"^[0-9a-fA-F]{64}$")
ALLOWED_VERIFICATION = {
    "UNVERIFIED", "PROVENANCE_CAPTURED", "HASH_CAPTURED", "CUSTODY_CAPTURED", "REVIEW_REQUIRED"
}
ALLOWED_ROLE = {"lead-only", "context-only"}


def fail(msg: str) -> None:
    raise SystemExit("FAIL: " + msg)


def validate(candidate: dict) -> None:
    required = [
        "schema", "candidate_id", "repository", "trajectory_ids", "acquisition_request_id",
        "source_url", "retrieved_at", "source_class", "verification_state", "evidence_role",
        "native_records_mutated", "evaluation_changed", "transport",
    ]
    missing = [key for key in required if key not in candidate]
    if missing:
        fail("missing fields: " + ", ".join(missing))
    if candidate["schema"] != "stegverse.erl.research_source_candidate.v1":
        fail("wrong schema")
    if not isinstance(candidate["trajectory_ids"], list) or not candidate["trajectory_ids"]:
        fail("trajectory_ids must be non-empty")
    if any(not isinstance(value, str) or not value for value in candidate["trajectory_ids"]):
        fail("trajectory_ids must contain non-empty strings")
    if len(set(candidate["trajectory_ids"])) != len(candidate["trajectory_ids"]):
        fail("duplicate trajectory_ids")
    if not isinstance(candidate["source_url"], str) or not candidate["source_url"].startswith(("http://", "https://")):
        fail("source_url must be http(s)")
    if candidate["verification_state"] not in ALLOWED_VERIFICATION:
        fail("invalid verification_state")
    if candidate["evidence_role"] not in ALLOWED_ROLE:
        fail("candidate posture exceeds lead/context")
    if candidate["native_records_mutated"] is not False:
        fail("native record mutation forbidden")
    if candidate["evaluation_changed"] is not False:
        fail("local evaluation change forbidden")
    digest = candidate.get("content_sha256")
    if digest is not None and (not isinstance(digest, str) or not SHA256.fullmatch(digest)):
        fail("invalid content_sha256")

    transport = candidate["transport"]
    if not isinstance(transport, dict):
        fail("transport must be object")
    if transport.get("source_repository") != candidate["repository"]:
        fail("source repository mismatch")
    if transport.get("destination_repository") != "StegVerse-Labs/Executive_Rhetoric_Ledger":
        fail("wrong destination")
    if transport.get("authority_effect") != "NONE":
        fail("transport cannot confer authority")
    if transport.get("credential_authority") != "TV/TVC":
        fail("credential authority must be TV/TVC")
    if transport.get("github_token_authority") != "NONE":
        fail("GitHub token authority must be NONE")


def main() -> int:
    if len(sys.argv) != 2:
        fail("usage: validate_research_candidate_intake.py <candidate.jsonl>")
    path = pathlib.Path(sys.argv[1])
    packets = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            candidate = json.loads(line)
        except Exception as exc:
            fail(f"invalid JSONL line {line_number}: {exc}")
        validate(candidate)
        packets.append(candidate)
    if not packets:
        fail("no candidate packets")
    candidate_ids = [candidate["candidate_id"] for candidate in packets]
    if len(set(candidate_ids)) != len(candidate_ids):
        fail("duplicate candidate_id in batch")
    print(json.dumps({
        "status": "PASS",
        "packets": len(packets),
        "authority_effect": "NONE",
        "credential_authority": "TV/TVC",
        "github_token_authority": "NONE",
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
