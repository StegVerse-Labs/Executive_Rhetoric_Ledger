#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from statistics import mean

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from find_historical_market_analogues import find_analogues


def pct_change(a: float, b: float) -> float | None:
    if a <= 0:
        return None
    return (b / a - 1.0) * 100.0


def predicted_returns(states: list[dict], analogue_rows: list[dict]) -> dict[str, float]:
    by_id = {row["state_id"]: idx for idx, row in enumerate(states)}
    weighted: dict[str, list[tuple[float, float]]] = {}
    for analogue in analogue_rows:
        idx = by_id.get(analogue["analogue_id"])
        if idx is None or idx + 1 >= len(states):
            continue
        current_prices = states[idx].get("prices", {})
        next_prices = states[idx + 1].get("prices", {})
        weight = max(float(analogue.get("similarity_score", 0.0)), 0.0)
        if weight <= 0:
            continue
        for instrument in sorted(set(current_prices) & set(next_prices)):
            realized = pct_change(float(current_prices[instrument]), float(next_prices[instrument]))
            if realized is not None and math.isfinite(realized):
                weighted.setdefault(instrument, []).append((weight, realized))
    output: dict[str, float] = {}
    for instrument, observations in weighted.items():
        total_weight = sum(weight for weight, _ in observations)
        if total_weight > 0:
            output[instrument] = sum(weight * value for weight, value in observations) / total_weight
    return output


def momentum_baseline(state: dict) -> str:
    candidates: list[tuple[float, str]] = []
    for key, value in state.get("features", {}).items():
        if not key.endswith("_return_1d_pct") or not isinstance(value, (int, float)):
            continue
        instrument = key[: -len("_return_1d_pct")].upper() + "-USD"
        candidates.append((float(value), instrument))
    if not candidates:
        return "FOREGO"
    score, instrument = max(candidates, key=lambda row: (row[0], row[1]))
    return instrument if score > 0 else "FOREGO"


def realized_selection_return(state: dict, next_state: dict, selection: str) -> float:
    if selection == "FOREGO":
        return 0.0
    current_price = state.get("prices", {}).get(selection)
    next_price = next_state.get("prices", {}).get(selection)
    if current_price is None or next_price is None:
        return 0.0
    return pct_change(float(current_price), float(next_price)) or 0.0


def build_calibration(panel: dict, *, min_history: int, top_k: int, min_evaluations: int) -> dict:
    states = panel["states"]
    evaluations: list[dict] = []
    for index in range(max(min_history, 1), max(len(states) - 1, 1)):
        current = states[index]
        history = states[:index]
        analogue_set = find_analogues(current, history, top_k=min(top_k, len(history)))
        predictions = predicted_returns(states[: index + 1], analogue_set["historical_analogues"])
        if predictions:
            best_instrument, best_prediction = max(predictions.items(), key=lambda row: (row[1], row[0]))
            analogue_selection = best_instrument if best_prediction > 0 else "FOREGO"
        else:
            best_prediction = 0.0
            analogue_selection = "FOREGO"
        baseline_selection = momentum_baseline(current)
        next_state = states[index + 1]
        analogue_realized = realized_selection_return(current, next_state, analogue_selection)
        baseline_realized = realized_selection_return(current, next_state, baseline_selection)
        evaluations.append({
            "state_id": current["state_id"],
            "as_of_utc": current["as_of_utc"],
            "history_states": len(history),
            "analogue_count": analogue_set["analogue_count"],
            "analogue_selection": analogue_selection,
            "predicted_return_pct": round(best_prediction, 8),
            "analogue_realized_return_pct": round(analogue_realized, 8),
            "baseline_selection": baseline_selection,
            "baseline_realized_return_pct": round(baseline_realized, 8),
        })

    analogue_returns = [row["analogue_realized_return_pct"] for row in evaluations]
    baseline_returns = [row["baseline_realized_return_pct"] for row in evaluations]
    analogue_mean = mean(analogue_returns) if analogue_returns else 0.0
    baseline_mean = mean(baseline_returns) if baseline_returns else 0.0
    analogue_positive = sum(value > 0 for value in analogue_returns) / len(analogue_returns) if analogue_returns else 0.0
    baseline_positive = sum(value > 0 for value in baseline_returns) / len(baseline_returns) if baseline_returns else 0.0
    enough = len(evaluations) >= min_evaluations
    improvement = analogue_mean > baseline_mean and analogue_positive >= baseline_positive

    return {
        "schema": "stegverse.erl.longitudinal_analogue_oos_calibration.v1",
        "method": "rolling_origin_no_future_state_leakage.v1",
        "baseline": "positive_1d_momentum_else_FOREGO.v1",
        "minimum_history_states": min_history,
        "top_k_analogues": top_k,
        "minimum_evaluations": min_evaluations,
        "evaluation_count": len(evaluations),
        "evaluations": evaluations,
        "summary": {
            "analogue_mean_return_pct": round(analogue_mean, 8),
            "baseline_mean_return_pct": round(baseline_mean, 8),
            "mean_return_uplift_pct": round(analogue_mean - baseline_mean, 8),
            "analogue_positive_rate": round(analogue_positive, 8),
            "baseline_positive_rate": round(baseline_positive, 8),
            "positive_rate_uplift": round(analogue_positive - baseline_positive, 8),
        },
        "calibration_state": "CALIBRATION_CANDIDATE" if enough and improvement else "NOT_CALIBRATED",
        "strategy_influence_authorized": False,
        "research_authority": "ERL",
        "execution_authority": "NONE",
        "may_authorize_order": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Rolling-origin out-of-sample calibration for ERL longitudinal analogue selection.")
    parser.add_argument("panel")
    parser.add_argument("--minimum-history", type=int, default=3)
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--minimum-evaluations", type=int, default=20)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    panel = json.loads(Path(args.panel).read_text())
    result = build_calibration(panel, min_history=args.minimum_history, top_k=args.top_k, min_evaluations=args.minimum_evaluations)
    output = Path(args.out)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": "PASS",
        "calibration_state": result["calibration_state"],
        "evaluation_count": result["evaluation_count"],
        "strategy_influence_authorized": False,
        "execution_authority": "NONE",
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
