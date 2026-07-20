#!/usr/bin/env python3
"""Verify destination-owned acknowledgment receipts without self-acknowledgment."""
from __future__ import annotations

import argparse
import hashlib
import json
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def fetch_json(url: str) -> dict | None:
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError):
        return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--generated-at")
    parser.add_argument("--output", default="propagation/verification.json")
    args = parser.parse_args()

    config = load_json(ROOT / "config/destination-adapters.json")
    source_bytes = (ROOT / config["source_path"]).read_bytes()
    source_hash = hashlib.sha256(source_bytes).hexdigest()
    generated_at = args.generated_at or datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

    statuses = []
    for destination in config["destinations"]:
        repository = destination["repository"]
        ack_path = destination["acknowledgment_path"]
        url = f"https://raw.githubusercontent.com/{repository}/main/{ack_path}"
        receipt = fetch_json(url)
        status = "pending"
        commit = None
        reason = "destination acknowledgment not found"
        if receipt:
            authority = receipt.get("authority", {})
            source = receipt.get("source_publication", {})
            validation = receipt.get("validation", {})
            valid = (
                receipt.get("destination_repository") == repository
                and receipt.get("status") == "acknowledged"
                and source.get("repository") == config["source_repository"]
                and source.get("path") == config["source_path"]
                and source.get("sha256") == source_hash
                and receipt.get("target_path") == destination["target_path"]
                and validation.get("content_hash_matches") is True
                and validation.get("destination_checks_passed") is True
                and authority.get("owned_by_destination") is True
                and authority.get("source_may_self_acknowledge") is False
            )
            if valid:
                status = "acknowledged"
                commit = receipt.get("destination_commit")
                reason = None
            else:
                status = "failed"
                reason = "destination receipt exists but failed binding or authority checks"
        statuses.append({
            "repository": repository,
            "status": status,
            "acknowledgment_path": ack_path if receipt else None,
            "destination_commit": commit,
            "reason": reason,
        })

    complete = all(item["status"] in {"acknowledged", "deprecated"} for item in statuses)
    document = {
        "manifest_id": f"PROP-{source_hash[:20].upper()}",
        "generated_at": generated_at,
        "source_sha256": source_hash,
        "required_destinations": [item["repository"] for item in config["destinations"]],
        "destination_status": statuses,
        "complete": complete,
        "authority": {"may_verify": True, "may_fabricate_acknowledgment": False, "may_close_issue": False},
    }
    output = ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(output.relative_to(ROOT))


if __name__ == "__main__":
    main()
