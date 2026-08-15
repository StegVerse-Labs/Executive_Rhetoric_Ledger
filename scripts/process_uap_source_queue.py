#!/usr/bin/env python3
"""Validate or acquire public UAP research sources without credentials.

This worker is deliberately narrow: public HTTPS GET only, no Authorization/Cookie
headers, no GitHub token use, deterministic class/path validation, SHA-256 receipts,
and no analytical or promotion authority.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_QUEUE = ROOT / "config" / "uap-media-source-queue.json"
CLASS_CONFIG = ROOT / "config" / "uap-evidence-classes.json"
FORBIDDEN_ENV = ("GITHUB_TOKEN", "GH_TOKEN")
FORBIDDEN_REQUEST_HEADERS = {"authorization", "cookie", "proxy-authorization"}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def expected_prefixes() -> dict[str, str]:
    cfg = load_json(CLASS_CONFIG)
    root = cfg["root"].rstrip("/")
    return {k: f"{root}/{v.strip('/')}" for k, v in cfg["evidence_classes"].items()}


def validate_queue(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if data.get("credential_requirement") != "NONE":
        errors.append("credential_requirement must be NONE")
    if data.get("github_token_runtime_authority") != "NONE":
        errors.append("github_token_runtime_authority must be NONE")
    if data.get("network_policy") != "PUBLIC_HTTPS_ONLY_NO_AUTH":
        errors.append("network_policy must be PUBLIC_HTTPS_ONLY_NO_AUTH")
    items = data.get("items")
    if not isinstance(items, list) or not items:
        return errors + ["items must be a non-empty array"]
    prefixes = expected_prefixes()
    seen: set[str] = set()
    for idx, item in enumerate(items):
        pfx = f"items[{idx}]"
        if not isinstance(item, dict):
            errors.append(f"{pfx} must be an object")
            continue
        source_id = item.get("source_id")
        if not isinstance(source_id, str) or not source_id:
            errors.append(f"{pfx}.source_id missing")
        elif source_id in seen:
            errors.append(f"duplicate source_id: {source_id}")
        else:
            seen.add(source_id)
        cls = item.get("evidence_class")
        if cls not in prefixes:
            errors.append(f"{pfx}.evidence_class unknown: {cls!r}")
        url = item.get("url")
        try:
            parsed = urllib.parse.urlparse(url)
        except Exception:
            parsed = None
        if not parsed or parsed.scheme != "https" or not parsed.hostname:
            errors.append(f"{pfx}.url must be public HTTPS")
        allowed_hosts = item.get("allowed_hosts")
        if not isinstance(allowed_hosts, list) or not allowed_hosts or not all(isinstance(v, str) and v for v in allowed_hosts):
            errors.append(f"{pfx}.allowed_hosts must be a non-empty string array")
        elif parsed and parsed.hostname not in allowed_hosts:
            errors.append(f"{pfx}.url host is not allowlisted")
        destination = item.get("destination")
        if isinstance(cls, str) and cls in prefixes:
            prefix = prefixes[cls] + "/"
            if not isinstance(destination, str) or not destination.startswith(prefix):
                errors.append(f"{pfx}.destination must remain under {prefix}")
        if item.get("state") not in {"READY", "COMPLETE", "BLOCKED", "RETRY", "REVIEW_REQUIRED", "FAILED", "SUPERSEDED"}:
            errors.append(f"{pfx}.state is not governed")
    return errors


def safe_request(url: str, allowed_hosts: list[str], timeout: float) -> tuple[bytes, str, str | None]:
    req = urllib.request.Request(url, headers={"User-Agent": "StegVerse-ERL-UAP-Research/1.0", "Accept": "*/*"})
    for key in req.headers:
        if key.lower() in FORBIDDEN_REQUEST_HEADERS:
            raise RuntimeError(f"forbidden request header: {key}")
    with urllib.request.urlopen(req, timeout=timeout) as response:
        final_url = response.geturl()
        host = urllib.parse.urlparse(final_url).hostname
        if host not in allowed_hosts:
            raise RuntimeError(f"redirect escaped allowlisted hosts: {host}")
        payload = response.read()
        content_type = response.headers.get("Content-Type")
        return payload, final_url, content_type


def acquire_item(item: dict[str, Any], output_root: Path, timeout: float) -> dict[str, Any]:
    destination = output_root / item["destination"]
    destination.parent.mkdir(parents=True, exist_ok=True)
    payload, final_url, content_type = safe_request(item["url"], item["allowed_hosts"], timeout)
    digest = hashlib.sha256(payload).hexdigest()
    destination.write_bytes(payload)
    receipt_path = destination.with_name(destination.name + ".receipt.json")
    receipt = {
        "evidence_class": item["evidence_class"],
        "source_id": item["source_id"],
        "source_url": item["url"],
        "final_url": final_url,
        "retrieved_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "sha256": digest,
        "byte_length": len(payload),
        "content_type": content_type,
        "native_object": destination.relative_to(output_root).as_posix(),
        "authority": {
            "credential_authority": "TV/TVC",
            "credential_used": False,
            "github_token_used": False,
            "promotion_authority": False,
            "factual_finding_authority": False
        }
    }
    receipt_path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {"source_id": item["source_id"], "status": "COMPLETE", "sha256": digest, "receipt": receipt_path.relative_to(output_root).as_posix()}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--queue", default=str(DEFAULT_QUEUE))
    parser.add_argument("--output-root", default=str(ROOT))
    parser.add_argument("--fetch", action="store_true", help="Acquire READY public sources after validating the queue")
    parser.add_argument("--source-id", action="append", default=[], help="Limit fetch to one or more source IDs")
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument("--receipt", default=None, help="Write execution receipt JSON")
    args = parser.parse_args()

    queue = load_json(Path(args.queue))
    errors = validate_queue(queue)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    inherited = {name: bool(os.environ.get(name)) for name in FORBIDDEN_ENV}
    for name in FORBIDDEN_ENV:
        os.environ.pop(name, None)

    results: list[dict[str, Any]] = []
    if args.fetch:
        selected = set(args.source_id)
        for item in queue["items"]:
            if item["state"] != "READY":
                continue
            if selected and item["source_id"] not in selected:
                continue
            try:
                results.append(acquire_item(item, Path(args.output_root).resolve(), args.timeout))
            except (OSError, urllib.error.URLError, RuntimeError) as exc:
                results.append({"source_id": item["source_id"], "status": "RETRY", "error": str(exc)})
    receipt = {
        "derived_class": "receipt",
        "goal_id": queue.get("goal_id"),
        "execution_status": "PASS" if args.fetch and results and all(r.get("status") == "COMPLETE" for r in results) else ("VALIDATED_ONLY" if not args.fetch else "RETRY"),
        "queue_valid": True,
        "fetch_requested": args.fetch,
        "credential_authority": "TV/TVC",
        "credential_requirement": "NONE",
        "github_token_used": False,
        "inherited_token_presence_removed_before_network": inherited,
        "results": results
    }
    if args.receipt:
        path = Path(args.receipt)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0 if receipt["execution_status"] in {"PASS", "VALIDATED_ONLY"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
