#!/usr/bin/env python3
"""Acquire current-method DSR series directly from the Federal Reserve Board release."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import urllib.request
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path

GOAL = "ERL-HOUSEHOLD-ECONOMIC-CONDITIONS-SITE-001"
URL = "https://www.federalreserve.gov/releases/DSR/"
SERIES = {
    "FRB_DSR_CURRENT_TOTAL": (0, "TDSP"),
    "FRB_DSR_CURRENT_MORTGAGE": (1, "MDSP"),
    "FRB_DSR_CURRENT_CONSUMER": (2, "CDSP"),
}


class VisibleText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts: list[str] = []
        self.suppressed = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self.suppressed += 1

    def handle_endtag(self, tag):
        if tag in ("script", "style") and self.suppressed:
            self.suppressed -= 1

    def handle_data(self, data):
        if not self.suppressed:
            text = " ".join(data.split())
            if text:
                self.parts.append(text)


def fetch() -> bytes:
    req = urllib.request.Request(URL, headers={"User-Agent": "StegVerse-ERL/1.0"})
    with urllib.request.urlopen(req, timeout=30) as response:
        return response.read()


def parsed_rows(raw: bytes) -> list[tuple[str, float, float, float]]:
    parser = VisibleText()
    parser.feed(raw.decode("utf-8", errors="replace"))
    text = " ".join(parser.parts)
    matches = re.findall(
        r"(?<!\d)(20\d{2}:[1-4])\s+([0-9]+(?:\.[0-9]+)?)\s+([0-9]+(?:\.[0-9]+)?)\s+([0-9]+(?:\.[0-9]+)?)(?![0-9.])",
        text,
    )
    rows = [(period, float(total), float(mortgage), float(consumer)) for period, total, mortgage, consumer in matches]
    rows = [row for row in rows if int(row[0][:4]) >= 2005]
    if not rows:
        # Retain a bounded diagnostic without fabricating observations.
        marker = "Household debt service payments as a percentage of disposable personal income"
        raise SystemExit(f"Federal Reserve Board DSR release produced no parseable observations; expected marker present={marker in text}")
    return rows


def observations(raw: bytes, index: int) -> list[dict]:
    out = []
    for period, total, mortgage, consumer in parsed_rows(raw):
        year, quarter = period.split(":")
        values = (total, mortgage, consumer)
        out.append({
            "period": f"{year}-Q{quarter}",
            "value": values[index],
            "evidence_class": "DIRECT_OBSERVATION",
        })
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-dir", type=Path, required=True)
    ap.add_argument("--acquired-at", default=None)
    args = ap.parse_args()
    acquired_at = args.acquired_at or datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    raw = fetch()
    raw_hash = hashlib.sha256(raw).hexdigest()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for series_id, (column, official_id) in SERIES.items():
        rows = observations(raw, column)
        body = {
            "schema": "stegverse.erl.household-economic-source-candidate/v1",
            "goal_task_id": GOAL,
            "inventory_series_id": series_id,
            "provider": "BOARD_OF_GOVERNORS_DSR_RELEASE",
            "official_series_id": official_id,
            "source_url": URL,
            "acquired_at": acquired_at,
            "source_vintage": "Federal Reserve Board DSR release 2026-06-22",
            "raw_sha256": raw_hash,
            "raw_size_bytes": len(raw),
            "status": "NORMALIZED_SOURCE_OBSERVATIONS",
            "observations": rows,
            "finding_authority": False,
            "public_activation_authorized": False,
        }
        stem = series_id.lower()
        (args.output_dir / f"{stem}.raw").write_bytes(raw)
        (args.output_dir / f"{stem}.candidate.json").write_text(json.dumps(body, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
        print(f"{series_id}=NORMALIZED_SOURCE_OBSERVATIONS observations={len(rows)} latest={rows[-1]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
