#!/usr/bin/env python3
"""Retrieve declared producer manifests and exports with deterministic health/retry state.

Discovery identifies candidates. Retrieval may fetch, hash, stage, quarantine, acknowledge,
and schedule retries. It may not promote, publish, or deprecate a producer.
"""
from __future__ import annotations

import base64
import hashlib
import json
import os
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DISCOVERED = ROOT / "producer_adapters/discovered.json"
HEALTH = ROOT / "producer_intake/producer-health.json"
INCOMING = ROOT / "producer_intake/incoming"
FAILURES = ROOT / "producer_intake/retrieval-failures"


def now() -> datetime:
    value = os.environ.get("RECONCILIATION_TIME")
    return datetime.fromisoformat(value.replace("Z", "+00:00")) if value else datetime.now(timezone.utc)


def gh_json(repo: str, path: str) -> tuple[bytes, str]:
    encoded = subprocess.check_output(
        ["gh", "api", f"repos/{repo}/contents/{path}"], text=True
    )
    payload = json.loads(encoded)
    content = base64.b64decode(payload["content"])
    return content, payload.get("sha", "")


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    generated = now()
    document = json.loads(DISCOVERED.read_text(encoding="utf-8")) if DISCOVERED.exists() else {"producers": []}
    health_rows = []
    for row in document.get("producers", []):
        repo = row["repository"]
        declaration = row["declaration"]
        manifest_path = declaration["exports"]["manifest_path"]
        retry = declaration["lifecycle"]["retry_policy"]
        attempts = 0
        last_error = None
        retrieved = 0
        quarantined = 0
        producer_commit = None
        manifest_hash = None
        status = "healthy"
        next_retry = None
        try:
            manifest_bytes, _ = gh_json(repo, manifest_path)
            manifest_hash = hashlib.sha256(manifest_bytes).hexdigest()
            manifest = json.loads(manifest_bytes)
            if manifest.get("producer_repository") != repo:
                raise ValueError("manifest producer identity mismatch")
            producer_commit = manifest.get("producer_commit")
            for item in manifest.get("records", []):
                record_path = item["path"]
                raw, _ = gh_json(repo, record_path)
                digest = hashlib.sha256(raw).hexdigest()
                if digest != item.get("sha256"):
                    quarantined += 1
                    write_json(FAILURES / repo.replace("/", "__") / f"{digest}.json", {
                        "repository": repo,
                        "path": record_path,
                        "reason": "sha256-mismatch",
                        "expected": item.get("sha256"),
                        "actual": digest,
                        "authority": {"may_promote": False, "may_deprecate": False}
                    })
                    continue
                destination = INCOMING / repo.replace("/", "__") / f"{digest}.json"
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(raw)
                retrieved += 1
            status = "healthy" if quarantined == 0 else "quarantined"
        except Exception as exc:
            attempts = 1
            last_error = str(exc)[:500]
            backoff = retry.get("backoff_seconds", [3600])
            next_retry = (generated + timedelta(seconds=backoff[0])).isoformat().replace("+00:00", "Z")
            status = "retry-scheduled" if retry.get("max_attempts", 1) > 1 else "unreachable"
        health_rows.append({
            "repository": repo,
            "manifest_path": manifest_path,
            "status": status,
            "attempts": attempts,
            "next_retry_at": next_retry,
            "last_error": last_error,
            "retrieved_records": retrieved,
            "quarantined_records": quarantined,
            "producer_commit": producer_commit,
            "manifest_sha256": manifest_hash
        })
    write_json(HEALTH, {
        "generated_at": generated.isoformat().replace("+00:00", "Z"),
        "producers": sorted(health_rows, key=lambda item: item["repository"]),
        "authority": {"may_retrieve": True, "may_retry": True, "may_acknowledge": True, "may_promote": False, "may_deprecate": False}
    })
    print(f"Reconciled {len(health_rows)} discovered producers")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
