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


class TableRows(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_row = False
        self.in_cell = False
        self.cell = []
        self.row = []
        self.rows = []

    def handle_starttag(self, tag, attrs):
        if tag == "tr":
            self.in_row = True
            self.row = []
        elif self.in_row and tag in ("td", "th"):
            self.in_cell = True
            self.cell = []

    def handle_data(self, data):
        if self.in_cell:
            self.cell.append(data)

    def handle_endtag(self, tag):
        if self.in_row and tag in ("td", "th") and self.in_cell:
            self.row.append(" ".join("".join(self.cell).split()))
            self.in_cell = False
        elif tag == "tr" and self.in_row:
            if self.row:
                self.rows.append(self.row)
            self.in_row = False


def fetch() -> bytes:
    req = urllib.request.Request(URL, headers={"User-Agent": "StegVerse-ERL/1.0"})
    with urllib.request.urlopen(req, timeout=30) as response:
        return response.read()


def observations(raw: bytes, index: int) -> list[dict]:
    parser = TableRows()
    parser.feed(raw.decode("utf-8", errors="replace"))
    out = []
    for row in parser.rows:
        if len(row) < 4 or not re.fullmatch(r"\d{4}:\d", row[0]):
            continue
        year, quarter = row[0].split(":")
        out.append({
            "period": f"{year}-Q{quarter}",
            "value": float(row[index + 1].replace(",", "")),
            "evidence_class": "DIRECT_OBSERVATION",
        })
    if not out:
        raise SystemExit("Federal Reserve Board DSR table produced no observations")
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
