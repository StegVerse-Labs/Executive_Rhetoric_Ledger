#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


def canonical_digest(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def pct_change(previous: float, current: float) -> float | None:
    if previous <= 0:
        return None
    return round((current / previous - 1.0) * 100.0, 8)


def build_states(panel: dict[str, Any], source_ref: str) -> dict[str, Any]:
    dates = panel["dates"]
    close = panel["close_usd"]
    instruments = sorted(close)
    expected = len(dates)
    for instrument in instruments:
        if len(close[instrument]) != expected:
            raise ValueError(f"length mismatch for {instrument}: {len(close[instrument])} != {expected}")

    states: list[dict[str, Any]] = []
    for index, date in enumerate(dates):
        prices = {f"{instrument}-USD": float(close[instrument][index]) for instrument in instruments}
        features: dict[str, Any] = {}
        if index > 0:
            returns = {
                instrument: pct_change(float(close[instrument][index - 1]), float(close[instrument][index]))
                for instrument in instruments
            }
            usable = [value for value in returns.values() if isinstance(value, (int, float))]
            positive = [value for value in usable if value > 0]
            features["cross_asset_breadth_positive_1d"] = round(len(positive) / len(usable), 8) if usable else None
            for instrument, value in returns.items():
                features[f"{instrument.lower()}_return_1d_pct"] = value
            if "XRP" in close and "XLM" in close and float(close["XLM"][index]) > 0:
                features["xrp_xlm_ratio"] = round(float(close["XRP"][index]) / float(close["XLM"][index]), 8)
                previous_ratio = float(close["XRP"][index - 1]) / float(close["XLM"][index - 1])
                current_ratio = float(close["XRP"][index]) / float(close["XLM"][index])
                features["xrp_xlm_ratio_change_1d_pct"] = pct_change(previous_ratio, current_ratio)
        else:
            for instrument in instruments:
                features[f"{instrument.lower()}_return_1d_pct"] = None
            features["cross_asset_breadth_positive_1d"] = None
            if "XRP" in close and "XLM" in close and float(close["XLM"][index]) > 0:
                features["xrp_xlm_ratio"] = round(float(close["XRP"][index]) / float(close["XLM"][index]), 8)
                features["xrp_xlm_ratio_change_1d_pct"] = None

        state = {
            "schema": "stegverse.erl.market_state_vector.v1",
            "state_id": f"coingecko-daily-{date}",
            "as_of_utc": f"{date}T23:59:59Z",
            "feature_version": "erl.crypto_daily_panel.v1",
            "universe": [f"{instrument}-USD" for instrument in instruments],
            "features": features,
            "source_coverage": {
                "coverage_score": 1.0,
                "missing_families": [
                    "derivatives",
                    "order_book_liquidity",
                    "stablecoin_flows",
                    "etf_fund_flows",
                    "on_chain_flows",
                    "macro_cross_market",
                    "event_context",
                ],
                "stale_families": [],
                "source_refs": [source_ref],
            },
            "research_authority": "ERL",
            "execution_authority": "NONE",
            "may_authorize_order": False,
        }
        state["vector_digest"] = canonical_digest(state)
        states.append({**state, "prices": prices})

    return {
        "schema": "stegverse.erl.longitudinal_market_panel.v1",
        "source_schema": panel.get("schema"),
        "source_ref": source_ref,
        "time_basis": panel.get("source", {}).get("time_basis"),
        "field": panel.get("source", {}).get("field"),
        "states": states,
        "research_authority": "ERL",
        "execution_authority": "NONE",
        "may_authorize_order": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Index an existing ERL crypto panel into longitudinal market-state rows.")
    parser.add_argument("panel")
    parser.add_argument("--source-ref")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    path = Path(args.panel)
    panel = json.loads(path.read_text())
    source_ref = args.source_ref or str(path)
    result = build_states(panel, source_ref)
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": "PASS", "states": len(result["states"]), "execution_authority": "NONE"}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
