#!/usr/bin/env python3
"""Run a keyless RSS evidence-gap monitor for the Ruben Ray Martinez case."""
from __future__ import annotations

import argparse
import hashlib
import json
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def stable_id(title: str, link: str) -> str:
    digest = hashlib.sha256(f"{title}\n{link}".encode()).hexdigest()[:16]
    return f"RRM-DISCOVERY-{digest.upper()}"


def parse_rss(xml_text: str, query: str) -> list[dict[str, str]]:
    root = ET.fromstring(xml_text)
    items: list[dict[str, str]] = []
    for item in root.findall(".//item"):
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        published = (item.findtext("pubDate") or "").strip()
        source = (item.findtext("source") or "").strip()
        if not title or not link:
            continue
        items.append({
            "candidate_id": stable_id(title, link),
            "title": title,
            "url": link,
            "publication_date": published,
            "source_name": source,
            "matched_query": query,
            "review_status": "candidate-generated",
            "evidence_effect": "none-until-reviewed",
        })
    return items


def fetch_query(query: str) -> str:
    encoded = urllib.parse.quote_plus(query)
    url = f"https://news.google.com/rss/search?q={encoded}&hl=en-US&gl=US&ceid=US:en"
    request = urllib.request.Request(url, headers={"User-Agent": "StegVerse-ERL-Evidence-Monitor/1.0"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8", errors="replace")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config/ruben-ray-martinez-evidence-monitor.json")
    parser.add_argument("--output", default="discovery_candidates/ruben-ray-martinez/latest.json")
    parser.add_argument("--fixture")
    parser.add_argument("--generated-at")
    args = parser.parse_args()

    config = json.loads((ROOT / args.config).read_text())
    generated_at = args.generated_at or datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    candidates: dict[str, dict[str, str]] = {}
    errors: list[dict[str, str]] = []

    fixture_text = Path(args.fixture).read_text() if args.fixture else None
    for query in config["queries"]:
        try:
            xml_text = fixture_text if fixture_text is not None else fetch_query(query)
            for item in parse_rss(xml_text, query):
                candidates[item["candidate_id"]] = item
        except Exception as exc:  # network failures become machine-readable health state
            errors.append({"query": query, "error": type(exc).__name__, "message": str(exc)[:300]})

    output = {
        "monitor_id": config["monitor_id"],
        "case_id": config["case_id"],
        "generated_at": generated_at,
        "status": "healthy" if not errors else ("degraded" if candidates else "retry-pending"),
        "candidate_count": len(candidates),
        "candidates": sorted(candidates.values(), key=lambda item: (item["publication_date"], item["candidate_id"]), reverse=True),
        "errors": errors,
        "evidence_gaps": config["evidence_gaps"],
        "authority": config["review_boundary"],
    }
    path = ROOT / args.output
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps({"status": output["status"], "candidate_count": output["candidate_count"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
