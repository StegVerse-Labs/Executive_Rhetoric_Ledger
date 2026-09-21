#!/usr/bin/env python3
"""Acquire ACS 1-year B25140 from the official credential-free table-based Summary File."""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

GOAL = "ERL-HOUSEHOLD-ECONOMIC-CONDITIONS-SITE-001"
FIELDS = {
    "total": ("B25140_E001", "B25140_M001"),
    "owned_with_mortgage_total": ("B25140_E002", "B25140_M002"),
    "owned_with_mortgage_over_30": ("B25140_E003", "B25140_M003"),
    "owned_with_mortgage_over_50": ("B25140_E004", "B25140_M004"),
    "owned_without_mortgage_total": ("B25140_E006", "B25140_M006"),
    "owned_without_mortgage_over_30": ("B25140_E007", "B25140_M007"),
    "owned_without_mortgage_over_50": ("B25140_E008", "B25140_M008"),
    "rented_total": ("B25140_E010", "B25140_M010"),
    "rented_over_30": ("B25140_E011", "B25140_M011"),
    "rented_over_50": ("B25140_E012", "B25140_M012"),
}


def fetch(year: int) -> tuple[str, bytes]:
    url = f"https://www2.census.gov/programs-surveys/acs/summary_file/{year}/table-based-SF/data/1YRData/acsdt1y{year}-b25140.dat"
    req = urllib.request.Request(url, headers={"User-Agent": "StegVerse-ERL/1.0", "Accept": "text/plain"})
    with urllib.request.urlopen(req, timeout=30) as response:
        raw = response.read()
    if not raw.startswith(b"GEO_ID|"):
        raise RuntimeError(f"unexpected Census Summary File prefix={raw[:80]!r}")
    return url, raw


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--year", type=int, default=2024)
    ap.add_argument("--output-dir", type=Path, required=True)
    args = ap.parse_args()
    if args.year == 2020:
        raise SystemExit("2020 ACS 1-year experimental release is excluded from standard comparison")

    url, raw = fetch(args.year)
    reader = csv.DictReader(io.StringIO(raw.decode("utf-8-sig")), delimiter="|")
    national = next((row for row in reader if row.get("GEO_ID") == "0100000US"), None)
    if national is None:
        raise SystemExit("Census B25140 Summary File missing national GEO_ID 0100000US")

    observations = []
    direct_values = {}
    for measure, (estimate_field, moe_field) in FIELDS.items():
        if estimate_field not in national or moe_field not in national:
            raise SystemExit(f"Census Summary File missing {estimate_field}/{moe_field}")
        value = float(national[estimate_field])
        direct_values[measure] = value
        observations.append({
            "period": str(args.year),
            "value": value,
            "margin_of_error": float(national[moe_field]),
            "measure": measure,
            "source_variable": estimate_field,
            "source_moe_variable": moe_field,
            "evidence_class": "DIRECT_OBSERVATION",
        })

    derived = {
        "owned_with_mortgage_over_30_share_pct": ("owned_with_mortgage_over_30", "owned_with_mortgage_total"),
        "owned_with_mortgage_over_50_share_pct": ("owned_with_mortgage_over_50", "owned_with_mortgage_total"),
        "owned_without_mortgage_over_30_share_pct": ("owned_without_mortgage_over_30", "owned_without_mortgage_total"),
        "owned_without_mortgage_over_50_share_pct": ("owned_without_mortgage_over_50", "owned_without_mortgage_total"),
        "rented_over_30_share_pct": ("rented_over_30", "rented_total"),
        "rented_over_50_share_pct": ("rented_over_50", "rented_total"),
    }
    for measure, (numerator_name, denominator_name) in derived.items():
        numerator = direct_values[numerator_name]
        denominator = direct_values[denominator_name]
        if denominator <= 0:
            continue
        observations.append({
            "period": str(args.year),
            "value": (numerator / denominator) * 100.0,
            "measure": measure,
            "unit": "percent",
            "numerator_measure": numerator_name,
            "denominator_measure": denominator_name,
            "evidence_class": "DERIVED_FROM_DIRECT_OBSERVATIONS",
            "finding_authority": False,
        })

    acquired_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    body = {
        "schema": "stegverse.erl.household-economic-source-candidate/v1",
        "goal_task_id": GOAL,
        "inventory_series_id": "CENSUS_ACS_HOUSING_COST_BURDEN",
        "provider": "CENSUS_ACS_TABLE_BASED_SUMMARY_FILE",
        "source_url": url,
        "acquired_at": acquired_at,
        "source_vintage": f"{args.year} ACS 1-year Table-Based Summary File",
        "raw_sha256": hashlib.sha256(raw).hexdigest(),
        "raw_size_bytes": len(raw),
        "status": "NORMALIZED_SOURCE_OBSERVATIONS",
        "required_cost_scope": "HOUSING_COST_BURDEN_ONLY",
        "standard_acs1_comparability_floor": 2005,
        "observations": observations,
        "finding_authority": False,
        "public_activation_authorized": False,
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "census_acs_housing_cost_burden.raw").write_bytes(raw)
    (args.output_dir / "census_acs_housing_cost_burden.candidate.json").write_text(json.dumps(body, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
    print(f"CENSUS_ACS_HOUSING_COST_BURDEN=NORMALIZED_SOURCE_OBSERVATIONS observations={len(observations)} derived=6 required_cost_scope=HOUSING_COST_BURDEN_ONLY raw_sha256={body['raw_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
