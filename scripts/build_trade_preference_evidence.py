#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import statistics
from pathlib import Path
from typing import Any


def _distribution(values: list[float]) -> dict[str, Any]:
    if not values:
        return {
            "observations": 0,
            "median_return_pct": None,
            "mean_return_pct": None,
            "positive_outcome_rate": None,
            "median_adverse_excursion_pct": None,
        }
    return {
        "observations": len(values),
        "median_return_pct": round(statistics.median(values), 8),
        "mean_return_pct": round(statistics.fmean(values), 8),
        "positive_outcome_rate": round(sum(value > 0 for value in values) / len(values), 8),
        "median_adverse_excursion_pct": None,
    }


def build_trade_preference_evidence(
    *,
    analogue_set: dict[str, Any],
    outcome_panel: dict[str, Any],
    candidate_instrument: str,
    candidate_side: str,
    comparison_instruments: list[str],
    horizon: str,
    source_coverage: dict[str, Any],
    minimum_observations: int = 10,
) -> dict[str, Any]:
    if analogue_set.get("execution_authority") != "NONE" or analogue_set.get("may_authorize_order") is not False:
        raise ValueError("analogue set must be non-authoritative")

    analogue_ids = [row["analogue_id"] for row in analogue_set.get("historical_analogues", [])]
    analogue_meta = {row["analogue_id"]: row for row in analogue_set.get("historical_analogues", [])}
    outcome_by_state = {row["state_id"]: row for row in outcome_panel.get("records", [])}
    instruments = list(dict.fromkeys([candidate_instrument, *comparison_instruments]))
    values_by_instrument: dict[str, list[float]] = {instrument: [] for instrument in instruments}

    for state_id in analogue_ids:
        record = outcome_by_state.get(state_id)
        if not record:
            continue
        horizon_record = record.get("horizons", {}).get(horizon, {})
        if horizon_record.get("status") != "OBSERVED":
            continue
        returns = horizon_record.get("returns_pct", {})
        for instrument in instruments:
            value = returns.get(instrument)
            if isinstance(value, (int, float)):
                adjusted = float(value) if candidate_side == "BUY" or instrument != candidate_instrument else -float(value)
                values_by_instrument[instrument].append(adjusted)

    distributions = {instrument: _distribution(values) for instrument, values in values_by_instrument.items()}
    candidate_distribution = distributions[candidate_instrument]
    observed_count = candidate_distribution["observations"]
    candidate_median = candidate_distribution["median_return_pct"]
    candidate_positive = candidate_distribution["positive_outcome_rate"]

    comparison_medians = [
        distribution["median_return_pct"]
        for instrument, distribution in distributions.items()
        if instrument != candidate_instrument and distribution["median_return_pct"] is not None
    ]
    best_comparison = max(comparison_medians) if comparison_medians else 0.0

    favorable: list[str] = []
    disconfirming: list[str] = []
    if observed_count >= minimum_observations:
        favorable.append(f"analogue_sample_sufficient:{observed_count}>={minimum_observations}")
    else:
        disconfirming.append(f"analogue_sample_insufficient:{observed_count}<{minimum_observations}")
    if candidate_median is not None and candidate_median > 0:
        favorable.append(f"candidate_median_positive:{candidate_median}")
    else:
        disconfirming.append(f"candidate_median_nonpositive:{candidate_median}")
    if candidate_positive is not None and candidate_positive >= 0.55:
        favorable.append(f"candidate_positive_rate_supportive:{candidate_positive}")
    elif candidate_positive is not None:
        disconfirming.append(f"candidate_positive_rate_weak:{candidate_positive}")
    if candidate_median is not None and candidate_median > best_comparison:
        favorable.append(f"candidate_median_exceeds_comparison:{candidate_median}>{best_comparison}")
    else:
        disconfirming.append(f"candidate_not_better_than_comparison:{candidate_median}<={best_comparison}")

    coverage_score = float(source_coverage.get("coverage_score", 0.0))
    if coverage_score < 0.5:
        disconfirming.append(f"source_coverage_low:{coverage_score}")

    if observed_count < minimum_observations or coverage_score < 0.5:
        preference = "INSUFFICIENT_EVIDENCE"
    elif candidate_median is not None and candidate_median > 0 and candidate_positive is not None and candidate_positive >= 0.55 and candidate_median > best_comparison:
        preference = "PREFER"
    elif candidate_median is not None and candidate_median <= 0:
        preference = "FOREGO"
    else:
        preference = "DEFER"

    confidence = min(1.0, coverage_score * min(1.0, observed_count / max(minimum_observations * 2, 1)))
    historical_analogues = [
        {
            "analogue_id": state_id,
            "similarity_score": analogue_meta[state_id]["similarity_score"],
            "matched_dimensions": analogue_meta[state_id].get("matched_dimensions", []),
            "material_differences": analogue_meta[state_id].get("material_differences", []),
        }
        for state_id in analogue_ids
        if state_id in analogue_meta
    ]

    return {
        "schema": "stegverse.erl.trade_preference_evidence.v1",
        "evidence_id": f"{analogue_set['current_state_id']}:{candidate_instrument}:{candidate_side}:{horizon}",
        "as_of_utc": analogue_set.get("as_of_utc", "1970-01-01T00:00:00Z"),
        "candidate": {"instrument": candidate_instrument, "side": candidate_side},
        "comparison_set": [
            {"instrument": instrument, "side": "BUY"} for instrument in comparison_instruments
        ] + [{"instrument": "CASH", "side": "FOREGO"}],
        "current_state_vector_digest": analogue_set["current_state_vector_digest"],
        "historical_analogues": historical_analogues,
        "outcomes": {horizon: candidate_distribution},
        "comparison_outcomes": {horizon: distributions},
        "favorable_evidence": favorable,
        "disconfirming_evidence": disconfirming,
        "source_coverage": source_coverage,
        "confidence": round(confidence, 8),
        "preference": preference,
        "research_authority": "ERL",
        "execution_authority": "NONE",
        "may_authorize_order": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build ERL trade-preference evidence from historical analogues and realized outcomes.")
    parser.add_argument("analogue_set")
    parser.add_argument("outcome_panel")
    parser.add_argument("--candidate", required=True)
    parser.add_argument("--side", choices=["BUY", "SELL"], default="BUY")
    parser.add_argument("--compare", default="")
    parser.add_argument("--horizon", default="step_1")
    parser.add_argument("--coverage-score", type=float, default=1.0)
    parser.add_argument("--minimum-observations", type=int, default=10)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    analogue_set = json.loads(Path(args.analogue_set).read_text())
    outcome_panel = json.loads(Path(args.outcome_panel).read_text())
    source_coverage = {"coverage_score": args.coverage_score, "missing_families": [], "stale_families": []}
    result = build_trade_preference_evidence(
        analogue_set=analogue_set,
        outcome_panel=outcome_panel,
        candidate_instrument=args.candidate,
        candidate_side=args.side,
        comparison_instruments=[value for value in args.compare.split(",") if value],
        horizon=args.horizon,
        source_coverage=source_coverage,
        minimum_observations=args.minimum_observations,
    )
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": "PASS", "preference": result["preference"], "confidence": result["confidence"], "execution_authority": "NONE"}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
