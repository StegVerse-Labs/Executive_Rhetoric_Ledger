#!/usr/bin/env python3
"""Process staged producer exports into hash-bound intake results.

Mechanical receipt acknowledgment is allowed. Final classification, promotion, and
publication remain review-bound.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

REQUIRED = {
    "producer_repo", "producer_commit", "producer_path", "ingestion_id",
    "review_status", "source_receipts"
}


def canonical_bytes(document: dict) -> bytes:
    return (json.dumps(document, sort_keys=True, separators=(",", ":")) + "\n").encode()


def iso_now(value: str | None) -> str:
    return value or datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="producer_intake/incoming")
    parser.add_argument("--output", default="producer_intake/results")
    parser.add_argument("--quarantine", default="producer_intake/quarantine")
    parser.add_argument("--generated-at")
    args = parser.parse_args()

    incoming = Path(args.input)
    output = Path(args.output)
    quarantine = Path(args.quarantine)
    output.mkdir(parents=True, exist_ok=True)
    quarantine.mkdir(parents=True, exist_ok=True)
    generated_at = iso_now(args.generated_at)

    seen: dict[str, str] = {}
    processed = 0
    for path in sorted(incoming.glob("**/*.json")):
        reason = None
        try:
            document = json.loads(path.read_text(encoding="utf-8"))
            missing = sorted(REQUIRED - set(document))
            if missing:
                reason = "missing-required-fields:" + ",".join(missing)
            elif document["review_status"] not in {"pending", "candidate", "review-required"}:
                reason = "invalid-review-status"
            elif not isinstance(document["source_receipts"], list) or not document["source_receipts"]:
                reason = "missing-source-receipts"
        except Exception as exc:
            document = {}
            reason = f"invalid-json:{type(exc).__name__}"

        raw = path.read_bytes()
        digest = hashlib.sha256(raw).hexdigest()
        repository = document.get("producer_repo", "unresolved/unresolved")
        commit = document.get("producer_commit", "unresolved")
        ingestion_id = document.get("ingestion_id", digest[:20])

        if reason:
            status = "quarantined"
            qpath = quarantine / f"{digest}.json"
            qpath.write_bytes(raw)
        elif digest in seen:
            status = "duplicate"
            reason = f"duplicate-of:{seen[digest]}"
        else:
            seen[digest] = ingestion_id
            status = "review-required"

        chronology = {
            "created_at": document.get("record_created_at") or document.get("ingestion_date"),
            "updated_at": document.get("record_updated_at") or document.get("ingestion_date"),
            "supersedes": document.get("supersedes"),
            "corrects": document.get("corrects"),
        }
        result = {
            "intake_id": "ERL-INTAKE-" + hashlib.sha256(f"{repository}|{commit}|{digest}".encode()).hexdigest()[:24].upper(),
            "generated_at": generated_at,
            "producer_repository": repository,
            "producer_commit": commit,
            "export_path": str(path),
            "export_sha256": digest,
            "status": status,
            "chronology": chronology,
            "reason": reason,
            "retry": None,
            "authority": {
                "may_acknowledge_receipt": True,
                "may_classify_final": False,
                "may_promote": False,
                "requires_review": True,
            },
        }
        (output / f"{result['intake_id']}.json").write_bytes(canonical_bytes(result))
        processed += 1

    index = {
        "generated_at": generated_at,
        "processed": processed,
        "results": sorted(str(p) for p in output.glob("ERL-INTAKE-*.json")),
        "authority": {"may_route": True, "may_promote": False, "may_publish": False},
    }
    (output / "index.json").write_bytes(canonical_bytes(index))
    print(f"Processed producer exports: {processed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
