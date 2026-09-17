#!/usr/bin/env python3
"""Acquire official household-economic source observations without creating findings.

The output is candidate source evidence only. It never sets public activation true and
never converts an aggregate observation into a household-welfare conclusion.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import os
import re
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BINDINGS_PATH = ROOT / "research-data/household-economic-conditions/official-series-bindings.v1.json"
GOAL = "ERL-HOUSEHOLD-ECONOMIC-CONDITIONS-SITE-001"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def fetch_bytes(url: str, *, method: str = "GET", body: bytes | None = None, headers: dict[str, str] | None = None) -> bytes:
    req = urllib.request.Request(url, data=body, method=method, headers=headers or {"User-Agent": "StegVerse-ERL/1.0"})
    with urllib.request.urlopen(req, timeout=45) as response:
        return response.read()


def load_bindings() -> dict[str, Any]:
    body = json.loads(BINDINGS_PATH.read_text(encoding="utf-8"))
    assert body["goal_task_id"] == GOAL
    assert body["public_activation_authorized"] is False
    return body


def make_candidate(binding: dict[str, Any], raw: bytes, observations: list[dict[str, Any]], acquired_at: str, status: str = "NORMALIZED_SOURCE_OBSERVATIONS") -> dict[str, Any]:
    return {
        "schema": "stegverse.erl.household-economic-source-candidate/v1",
        "goal_task_id": GOAL,
        "inventory_series_id": binding["inventory_series_id"],
        "provider": binding["provider"],
        "acquired_at": acquired_at,
        "source_vintage": acquired_at,
        "raw_sha256": sha256_bytes(raw),
        "raw_size_bytes": len(raw),
        "status": status,
        "observations": observations,
        "finding_authority": False,
        "public_activation_authorized": False,
    }


def normalize_bls(binding: dict[str, Any], payload: dict[str, Any]) -> list[dict[str, Any]]:
    series = payload.get("Results", {}).get("series", [])
    expected = binding["official_series_id"]
    selected = next((item for item in series if item.get("seriesID") == expected), None)
    if selected is None:
        raise ValueError(f"BLS response missing {expected}")
    result = []
    for row in selected.get("data", []):
        period = row.get("period", "")
        if not re.fullmatch(r"M(0[1-9]|1[0-2])", period):
            continue
        raw_value = row.get("value")
        if raw_value in (None, "", "-", "."):
            continue
        try:
            value = float(str(raw_value).replace(",", ""))
        except ValueError as exc:
            raise ValueError(f"BLS {expected} invalid numeric value for {row.get('year')}-{period}: {raw_value!r}") from exc
        result.append({"period": f"{row['year']}-{period[1:]}", "value": value, "evidence_class": "DIRECT_OBSERVATION"})
    if not result:
        raise ValueError(f"BLS response contained no numeric monthly observations for {expected}")
    return sorted(result, key=lambda row: row["period"])


def acquire_bls(binding: dict[str, Any], start_year: int, end_year: int, acquired_at: str) -> tuple[bytes, list[dict[str, Any]]]:
    query = {"seriesid": [binding["official_series_id"]], "startyear": str(start_year), "endyear": str(end_year)}
    raw = fetch_bytes(binding["endpoint"], method="POST", body=json.dumps(query).encode("utf-8"), headers={"Content-Type": "application/json", "User-Agent": "StegVerse-ERL/1.0"})
    return raw, normalize_bls(binding, json.loads(raw))


def normalize_fred_csv(binding: dict[str, Any], raw: bytes) -> list[dict[str, Any]]:
    text = raw.decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(text))
    value_column = binding["normalization"]["value_column"]
    date_column = binding["normalization"]["date_column"]
    rows = []
    for row in reader:
        value = row.get(value_column)
        if value in (None, "", "."):
            continue
        rows.append({"period": row[date_column], "value": float(value), "evidence_class": "DIRECT_OBSERVATION"})
    return rows


def acquire_fred(binding: dict[str, Any], acquired_at: str) -> tuple[bytes, list[dict[str, Any]]]:
    raw = fetch_bytes(binding["endpoint"])
    return raw, normalize_fred_csv(binding, raw)


def normalize_bea(binding: dict[str, Any], payload: dict[str, Any]) -> list[dict[str, Any]]:
    results = payload.get("BEAAPI", {}).get("Results", {})
    data = results.get("Data", [])
    target_line = str(binding["line_number"])
    rows = []
    for row in data:
        if str(row.get("LineNumber", "")) != target_line:
            continue
        period = row.get("TimePeriod")
        value = row.get("DataValue")
        if not period or value in (None, ""):
            continue
        rows.append({"period": period, "value": float(str(value).replace(",", "")), "evidence_class": "DIRECT_OBSERVATION"})
    if not rows:
        raise ValueError(f"BEA response contained no line {target_line} observations")
    return sorted(rows, key=lambda row: row["period"])


def acquire_bea(binding: dict[str, Any], years: str, acquired_at: str) -> tuple[bytes, list[dict[str, Any]]]:
    key = os.environ.get("BEA_API_KEY")
    if not key:
        raise RuntimeError("BEA_API_KEY is absent; BEA acquisition remains fail-closed")
    params = {
        "UserID": key,
        "method": "GetData",
        "datasetname": binding["dataset"],
        "TableName": binding["table_name"],
        "Frequency": binding["frequency"],
        "Year": years,
        "ResultFormat": "JSON",
    }
    raw = fetch_bytes(binding["endpoint"] + "?" + urllib.parse.urlencode(params))
    return raw, normalize_bea(binding, json.loads(raw))


def normalize_census(binding: dict[str, Any], payload: list[list[str]], year: int) -> list[dict[str, Any]]:
    if year in binding.get("excluded_standard_comparison_years", []):
        raise ValueError(f"ACS {year} is excluded from standard comparison")
    if len(payload) < 2:
        raise ValueError("Census response has no data rows")
    header, values = payload[0], payload[1]
    row = dict(zip(header, values))
    variables = binding["variables"]
    return [{
        "period": str(year),
        "value": float(row[variable]),
        "measure": name,
        "source_variable": variable,
        "evidence_class": "DIRECT_OBSERVATION",
    } for name, variable in variables.items()]


def acquire_census(binding: dict[str, Any], year: int, acquired_at: str) -> tuple[bytes, list[dict[str, Any]]]:
    variables = list(binding["variables"].values())
    endpoint = binding["endpoint_template"].format(year=year)
    params = {"get": "NAME," + ",".join(variables), "for": binding["geography"]}
    raw = fetch_bytes(endpoint + "?" + urllib.parse.urlencode(params, safe=",:*"))
    return raw, normalize_census(binding, json.loads(raw), year)


def acquire_nyfed_workbook(binding: dict[str, Any], acquired_at: str) -> tuple[bytes, list[dict[str, Any]]]:
    raw = fetch_bytes(binding["current_workbook"])
    # The raw official workbook is retained and hashed now; deterministic cell-level
    # normalization is intentionally withheld until the exact worksheet/column map is
    # separately bound and validated. Missing parser evidence must not become zeros.
    return raw, []


def write_capture(output_dir: Path, binding: dict[str, Any], raw: bytes, candidate: dict[str, Any]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    stem = binding["inventory_series_id"].lower()
    (output_dir / f"{stem}.raw").write_bytes(raw)
    (output_dir / f"{stem}.candidate.json").write_bytes(canonical_bytes(candidate))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", choices=["bls", "bea", "fred", "census", "nyfed", "all"], default="all")
    parser.add_argument("--start-year", type=int, default=2000)
    parser.add_argument("--end-year", type=int, default=datetime.now(timezone.utc).year)
    parser.add_argument("--bea-years", default="X")
    parser.add_argument("--census-year", type=int, default=2024)
    parser.add_argument("--output-dir", type=Path, default=Path("build/household-economic-source-candidates"))
    parser.add_argument("--acquired-at", default=None, help="Explicit timestamp for reproducible fixture/test runs")
    parser.add_argument("--validate-bindings-only", action="store_true")
    args = parser.parse_args()

    document = load_bindings()
    if args.validate_bindings_only:
        print(f"HOUSEHOLD_ECONOMIC_SOURCE_BINDINGS=PASS count={len(document['bindings'])}")
        print("PUBLIC_ACTIVATION_AUTHORIZED=false")
        return 0

    acquired_at = args.acquired_at or utc_now()
    failures = []
    for binding in document["bindings"]:
        provider = binding["provider"]
        family = "bls" if provider == "BLS_PUBLIC_DATA_API" else "bea" if provider == "BEA_DATA_API" else "fred" if provider == "FRED_BOARD_OF_GOVERNORS_SOURCE" else "census" if provider == "CENSUS_DATA_API" else "nyfed"
        if args.source not in ("all", family):
            continue
        try:
            if family == "bls":
                raw, observations = acquire_bls(binding, args.start_year, args.end_year, acquired_at)
                status = "NORMALIZED_SOURCE_OBSERVATIONS"
            elif family == "bea":
                raw, observations = acquire_bea(binding, args.bea_years, acquired_at)
                status = "NORMALIZED_SOURCE_OBSERVATIONS"
            elif family == "fred":
                raw, observations = acquire_fred(binding, acquired_at)
                status = "NORMALIZED_SOURCE_OBSERVATIONS"
            elif family == "census":
                raw, observations = acquire_census(binding, args.census_year, acquired_at)
                status = "NORMALIZED_SOURCE_OBSERVATIONS"
            else:
                raw, observations = acquire_nyfed_workbook(binding, acquired_at)
                status = "RAW_CAPTURED_NORMALIZATION_PENDING"
            candidate = make_candidate(binding, raw, observations, acquired_at, status=status)
            write_capture(args.output_dir, binding, raw, candidate)
            print(f"{binding['inventory_series_id']}={status} observations={len(observations)}")
        except Exception as exc:  # fail each source independently, never fabricate data
            failures.append({"series": binding["inventory_series_id"], "error": str(exc)})
            print(f"{binding['inventory_series_id']}=FAIL_CLOSED error={exc}")

    (args.output_dir / "acquisition-summary.json").parent.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "acquisition-summary.json").write_bytes(canonical_bytes({
        "schema": "stegverse.erl.household-economic-acquisition-summary/v1",
        "goal_task_id": GOAL,
        "acquired_at": acquired_at,
        "failures": failures,
        "public_activation_authorized": False,
    }))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
