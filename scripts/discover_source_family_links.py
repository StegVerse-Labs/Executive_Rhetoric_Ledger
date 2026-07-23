#!/usr/bin/env python3
"""Discover allowlisted, relevance-filtered links and emit existing source adapters.

Discovery creates capture candidates only. It never promotes or classifies records.
Each enabled source family is isolated so one unavailable index cannot suppress the
remaining sweep. The command fails only when every enabled family fails.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import urllib.error
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse, urlunparse

ROOT = Path(__file__).resolve().parents[1]


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[tuple[str, str]] = []
        self._href: str | None = None
        self._text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() != "a":
            return
        values = dict(attrs)
        self._href = values.get("href")
        self._text = []

    def handle_data(self, data: str) -> None:
        if self._href is not None:
            self._text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "a" and self._href is not None:
            self.links.append((self._href, " ".join(self._text).strip()))
            self._href = None
            self._text = []


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def fetch_index(family: dict) -> bytes:
    if family["index_type"] == "local-html-index":
        return (ROOT / family["index_url"]).read_bytes()
    request = urllib.request.Request(family["index_url"], headers=family.get("request_headers", {}))
    with urllib.request.urlopen(request, timeout=45) as response:
        return response.read()


def canonical_url(base: str, href: str) -> str | None:
    absolute = urljoin(base, href)
    parsed = urlparse(absolute)
    if parsed.scheme not in {"http", "https"}:
        return None
    return urlunparse((parsed.scheme, parsed.netloc.lower(), parsed.path, "", parsed.query, ""))


def relevant(text: str, terms: list[str]) -> bool:
    lower = text.lower()
    return any(term.lower() in lower for term in terms)


def allowed(url: str, family: dict) -> bool:
    parsed = urlparse(url)
    return parsed.hostname in set(family["allowed_hosts"]) and any(
        parsed.path.startswith(prefix) for prefix in family["allowed_path_prefixes"]
    )


def adapter_for(family: dict, url: str) -> dict:
    digest = hashlib.sha256(url.encode()).hexdigest()[:16].upper()
    return {
        "adapter_id": f"DISCOVERED_{family['family_id']}_{digest}",
        "enabled": True,
        "adapter_type": "html-document",
        "source_class": family["source_class"],
        "endpoint": url,
        "request_headers": family.get("request_headers", {}),
        "timeout_seconds": 45,
        "capture_policy": {
            "retain_raw": True,
            "hash_algorithm": "sha256",
            "deduplicate": True,
            "archive_directory": "archive/captures",
        },
        "review_boundary": {
            "automation_may_capture": True,
            "automation_may_propose": True,
            "automation_may_promote": False,
        },
    }


def error_text(exc: Exception) -> str:
    if isinstance(exc, urllib.error.HTTPError):
        return f"HTTP {exc.code}: {exc.reason}"
    if isinstance(exc, urllib.error.URLError):
        return f"URL error: {exc.reason}"
    return f"{type(exc).__name__}: {exc}"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config/source-families.json")
    parser.add_argument("--base-config", default="config/source-adapters.json")
    parser.add_argument("--output", default="config/source-adapters.runtime.json")
    parser.add_argument("--receipt", default="discovery_cycles/source-family-discovery.latest.json")
    parser.add_argument("--discovered-at", required=True)
    args = parser.parse_args()

    config = load_json(ROOT / args.config)
    base = load_json(ROOT / args.base_config)
    discovered: list[dict] = []
    family_results: list[dict] = []
    enabled_count = 0
    successful_count = 0

    for family in config["families"]:
        if not family["enabled"]:
            continue
        enabled_count += 1
        try:
            payload = fetch_index(family)
            parser_ = LinkParser()
            parser_.feed(payload.decode("utf-8", errors="replace"))
            accepted: list[str] = []
            seen: set[str] = set()
            link_base = family.get("link_base_url", family["index_url"])
            for href, anchor_text in parser_.links:
                url = canonical_url(link_base, href)
                if not url or url in seen or not allowed(url, family):
                    continue
                if not relevant(f"{anchor_text} {url}", family["relevance_terms"]):
                    continue
                seen.add(url)
                accepted.append(url)
                if len(accepted) >= family["max_links"]:
                    break
            discovered.extend(adapter_for(family, url) for url in accepted)
            successful_count += 1
            family_results.append({
                "family_id": family["family_id"],
                "index_url": family["index_url"],
                "fetch_status": "PASS",
                "index_sha256": hashlib.sha256(payload).hexdigest(),
                "discovered_count": len(accepted),
                "candidate_urls": accepted,
                "error": None,
                "promotion_authority": False,
            })
        except (OSError, UnicodeError, urllib.error.URLError) as exc:
            family_results.append({
                "family_id": family["family_id"],
                "index_url": family["index_url"],
                "fetch_status": "FAILED",
                "index_sha256": None,
                "discovered_count": 0,
                "candidate_urls": [],
                "error": error_text(exc),
                "promotion_authority": False,
            })

    existing = {item["endpoint"] for item in base["adapters"]}
    unique = [item for item in discovered if item["endpoint"] not in existing]
    runtime = {"adapters": base["adapters"] + unique}
    output = ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(runtime, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    failed_count = enabled_count - successful_count
    receipt = {
        "schema": "stegverse.executive_rhetoric_ledger.source_family_discovery.v2",
        "discovered_at": args.discovered_at,
        "execution_status": "PASS" if successful_count > 0 else "FAILED",
        "enabled_family_count": enabled_count,
        "successful_family_count": successful_count,
        "failed_family_count": failed_count,
        "families": family_results,
        "runtime_adapter_count": len(runtime["adapters"]),
        "new_adapter_count": len(unique),
        "authority": {
            "may_discover": True,
            "may_capture": True,
            "may_promote": False,
            "human_review_required": True,
        },
    }
    receipt_path = ROOT / args.receipt
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    receipt_path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(str(output.relative_to(ROOT)))

    if enabled_count == 0:
        raise SystemExit("No enabled source families")
    if successful_count == 0:
        raise SystemExit("Every enabled source family failed; see discovery receipt")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
