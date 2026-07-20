#!/usr/bin/env python3
"""Capture configured sources, retain immutable raw bytes, and emit review-required candidates."""

from __future__ import annotations

import argparse
import hashlib
import json
import mimetypes
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_source(adapter: dict) -> tuple[bytes, str]:
    endpoint = adapter["endpoint"]
    if adapter["adapter_type"] == "local-json":
        path = ROOT / endpoint
        return path.read_bytes(), "application/json"
    request = urllib.request.Request(endpoint, headers=adapter.get("request_headers", {}))
    with urllib.request.urlopen(request, timeout=adapter.get("timeout_seconds", 30)) as response:
        return response.read(), response.headers.get_content_type()


def stable_candidate(payload: bytes, adapter: dict, source_uri: str) -> dict:
    digest = hashlib.sha256(payload).hexdigest()
    parsed = None
    try:
        parsed = json.loads(payload.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        pass
    return {
        "candidate_id": f"CAND-{digest[:20].upper()}",
        "source_uri": source_uri,
        "source_class": adapter["source_class"],
        "content_sha256": digest,
        "candidate_status": "candidate-review-required",
        "claimed_use": "discovery-candidate",
        "automation_authority": {
            "captured": True,
            "proposed": True,
            "promoted": False
        },
        "normalized_payload": parsed,
        "review_notes": "Capture proves retained source content and provenance only; it does not establish truth or final ledger classification."
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config/source-adapters.json")
    parser.add_argument("--captured-at", default=None)
    args = parser.parse_args()

    captured_at = args.captured_at or now_utc()
    day = captured_at[:10]
    config = load_json(ROOT / args.config)
    receipts_dir = ROOT / "archive" / "receipts" / day
    candidates_dir = ROOT / "discovery_candidates" / day
    receipts_dir.mkdir(parents=True, exist_ok=True)
    candidates_dir.mkdir(parents=True, exist_ok=True)

    index: list[dict] = []
    for adapter in config["adapters"]:
        if not adapter["enabled"]:
            continue
        payload, content_type = read_source(adapter)
        digest = hashlib.sha256(payload).hexdigest()
        extension = mimetypes.guess_extension(content_type) or ".bin"
        raw_dir = ROOT / adapter["capture_policy"]["archive_directory"] / day
        raw_dir.mkdir(parents=True, exist_ok=True)
        raw_path = raw_dir / f"{digest}{extension}"
        duplicate = raw_path.exists()
        if not duplicate:
            raw_path.write_bytes(payload)

        candidate = stable_candidate(payload, adapter, adapter["endpoint"])
        candidate_path = candidates_dir / f"{candidate['candidate_id']}.json"
        candidate_path.write_text(json.dumps(candidate, indent=2, sort_keys=True) + "\n", encoding="utf-8")

        receipt = {
            "capture_id": f"CAP-{digest[:20].upper()}",
            "adapter_id": adapter["adapter_id"],
            "captured_at": captured_at,
            "source_uri": adapter["endpoint"],
            "source_class": adapter["source_class"],
            "content_type": content_type,
            "content_sha256": digest,
            "byte_length": len(payload),
            "raw_archive_path": str(raw_path.relative_to(ROOT)),
            "candidate_path": str(candidate_path.relative_to(ROOT)),
            "capture_status": "duplicate" if duplicate else "captured",
            "review_status": "candidate-review-required"
        }
        if duplicate:
            receipt["duplicate_of"] = str(raw_path.relative_to(ROOT))
        receipt_path = receipts_dir / f"{receipt['capture_id']}.json"
        receipt_path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        index.append(receipt)

    (receipts_dir / "index.json").write_text(json.dumps(index, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Captured {len(index)} configured source(s) at {captured_at}.")


if __name__ == "__main__":
    main()
