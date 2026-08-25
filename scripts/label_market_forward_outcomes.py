#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import statistics
from pathlib import Path
from typing import Any


def _return_pct(start: float, end: float) -> float | None:
    if start <= 0:
        return None
    return round((end / start - 1.0) * 100.0, 8)


def label_forward_outcomes(panel: list[dict[str, Any]], horizons: list[int]) -> dict[str, Any]:
    if sorted(horizons) != horizons or any(h <= 0 for h in horizons):
        raise ValueError("horizons must be sorted positive integer step counts")
    records: list[dict[str, Any]] = []
    for index, row in enumerate(panel):
        prices = row.get("prices", {})
        horizon_results: dict[str, Any] = {}
        for horizon in horizons:
            target_index = index + horizon
            key = f"step_{horizon}"
            if target_index >= len(panel):
                horizon_results[key] = {"status": "UNAVAILABLE", "returns_pct": {}}
                continue
            target_prices = panel[target_index].get("prices", {})
            returns: dict[str, float | None] = {}
            for instrument in sorted(prices):
                if instrument not in target_prices:
                    returns[instrument] = None
                else:
                    returns[instrument] = _return_pct(float(prices[instrument]), float(target_prices[instrument]))
            usable = [value for value in returns.values() if isinstance(value, (int, float))]
            horizon_results[key] = {
                "status": "OBSERVED" if usable else "UNAVAILABLE",
                "target_as_of_utc": panel[target_index]["as_of_utc"],
                "returns_pct": returns,
                "cross_asset_median_return_pct": round(statistics.median(usable), 8) if usable else None,
            }
        records.append({
            "state_id": row["state_id"],
            "as_of_utc": row["as_of_utc"],
            "horizons": horizon_results,
        })
    return {
        "schema": "stegverse.erl.forward_outcome_panel.v1",
        "step_unit": "panel_interval",
        "horizons": horizons,
        "records": records,
        "research_authority": "ERL",
        "execution_authority": "NONE",
        "may_authorize_order": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Label realized forward market outcomes for ERL states.")
    parser.add_argument("panel")
    parser.add_argument("--horizons", default="1,2,6,24")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    payload = json.loads(Path(args.panel).read_text())
    panel = payload["states"] if isinstance(payload, dict) else payload
    horizons = sorted({int(part) for part in args.horizons.split(",") if part.strip()})
    result = label_forward_outcomes(panel, horizons)
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": "PASS", "records": len(result["records"]), "execution_authority": "NONE"}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
