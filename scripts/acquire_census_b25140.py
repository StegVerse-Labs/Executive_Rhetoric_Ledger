#!/usr/bin/env python3
"""Acquire ACS 1-year B25140 housing-cost burden observations without authority effect."""
from __future__ import annotations

import argparse
import hashlib
import json
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

GOAL = "ERL-HOUSEHOLD-ECONOMIC-CONDITIONS-SITE-001"
VARIABLES = {
    "total": "B25140_001E",
    "owned_with_mortgage_total": "B25140_002E",
    "owned_with_mortgage_over_30": "B25140_003E",
    "owned_with_mortgage_over_50": "B25140_004E",
    "owned_without_mortgage_total": "B25140_006E",
    "owned_without_mortgage_over_30": "B25140_007E",
    "owned_without_mortgage_over_50": "B25140_008E",
    "rented_total": "B25140_010E",
    "rented_over_30": "B25140_011E",
    "rented_over_50": "B25140_012E",
}


def fetch(year: int) -> tuple[str, bytes]:
    base = f"https://api.census.gov/data/{year}/acs/acs1"
    params = urllib.parse.urlencode({"get": "NAME," + ",".join(VARIABLES.values()), "for": "us:*"})
    url = base + "?" + params
    last = None
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "StegVerse-ERL/1.0", "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=20) as response:
                raw = response.read()
                if not raw.strip().startswith(b"["):
                    raise RuntimeError(f"unexpected Census response content-type={response.headers.get('Content-Type')} bytes={len(raw)} prefix={raw[:80]!r}")
                return url, raw
        except Exception as exc:
            last = exc
            if attempt < 2:
                time.sleep(2 ** attempt)
    raise RuntimeError(f"Census ACS acquisition failed after retries: {last}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--year", type=int, default=2024)
    ap.add_argument("--output-dir", type=Path, required=True)
    args = ap.parse_args()
    if args.year == 2020:
        raise SystemExit("2020 ACS 1-year experimental release is excluded from standard comparison")
    url, raw = fetch(args.year)
    payload = json.loads(raw)
    if len(payload) != 2:
        raise SystemExit(f"expected one national Census data row, got {len(payload)-1}")
    header, values = payload
    row = dict(zip(header, values))
    observations = []
    for measure, variable in VARIABLES.items():
        if variable not in row:
            raise SystemExit(f"Census response missing {variable}")
        observations.append({
            "period": str(args.year),
            "value": float(row[variable]),
            "measure": measure,
            "source_variable": variable,
            "evidence_class": "DIRECT_OBSERVATION",
        })
    acquired_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    body = {
        "schema": "stegverse.erl.household-economic-source-candidate/v1",
        "goal_task_id": GOAL,
        "inventory_series_id": "CENSUS_ACS_HOUSING_COST_BURDEN",
        "provider": "CENSUS_DATA_API",
        "source_url": url,
        "acquired_at": acquired_at,
        "source_vintage": f"{args.year} ACS 1-year",
        "raw_sha256": hashlib.sha256(raw).hexdigest(),
        "raw_size_bytes": len(raw),
        "status": "NORMALIZED_SOURCE_OBSERVATIONS",
        "observations": observations,
        "finding_authority": False,
        "public_activation_authorized": False,
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "census_acs_housing_cost_burden.raw").write_bytes(raw)
    (args.output_dir / "census_acs_housing_cost_burden.candidate.json").write_text(json.dumps(body, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
    print(f"CENSUS_ACS_HOUSING_COST_BURDEN=NORMALIZED_SOURCE_OBSERVATIONS observations={len(observations)} raw_sha256={body['raw_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
