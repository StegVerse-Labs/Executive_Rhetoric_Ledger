#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Any


def canonical_digest(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def numeric_features(state: dict[str, Any]) -> dict[str, float]:
    out: dict[str, float] = {}
    for key, value in state.get("features", {}).items():
        if isinstance(value, bool):
            continue
        if isinstance(value, (int, float)) and math.isfinite(float(value)):
            out[key] = float(value)
    return out


def feature_scales(states: list[dict[str, Any]], keys: set[str]) -> dict[str, float]:
    scales: dict[str, float] = {}
    feature_maps = [numeric_features(state) for state in states]
    for key in keys:
        values = [features[key] for features in feature_maps if key in features]
        if not values:
            scales[key] = 1.0
            continue
        lo, hi = min(values), max(values)
        absolute_reference = max(abs(value) for value in values)
        # Avoid making a tiny observed range define a 100% distance. The scale
        # must preserve both variation across the corpus and the magnitude of
        # the feature itself, while remaining deterministic and unit-local.
        scales[key] = max(hi - lo, absolute_reference, 1e-12)
    return scales


def compare_states(current: dict[str, Any], prior: dict[str, Any], scales: dict[str, float], weights: dict[str, float]) -> dict[str, Any]:
    current_features = numeric_features(current)
    prior_features = numeric_features(prior)
    all_keys = sorted(set(current_features) | set(prior_features))
    matched: list[str] = []
    missing: list[str] = []
    material_differences: list[str] = []
    weighted_distance = 0.0
    total_weight = 0.0

    for key in all_keys:
        weight = max(float(weights.get(key, 1.0)), 0.0)
        if weight == 0:
            continue
        total_weight += weight
        if key not in current_features or key not in prior_features:
            missing.append(key)
            weighted_distance += weight
            continue
        delta = abs(current_features[key] - prior_features[key]) / max(scales.get(key, 1.0), 1e-12)
        delta = min(delta, 1.0)
        weighted_distance += weight * delta
        if delta <= 0.20:
            matched.append(key)
        if delta >= 0.50:
            material_differences.append(key)

    normalized_distance = weighted_distance / total_weight if total_weight else 1.0
    similarity = round(max(0.0, 1.0 - normalized_distance), 8)
    return {
        "analogue_id": prior["state_id"],
        "as_of_utc": prior["as_of_utc"],
        "similarity_score": similarity,
        "matched_dimensions": matched,
        "material_differences": material_differences,
        "missing_dimensions": missing,
    }


def find_analogues(current: dict[str, Any], history: list[dict[str, Any]], *, top_k: int = 20, minimum_similarity: float = 0.0, weights: dict[str, float] | None = None) -> dict[str, Any]:
    weights = weights or {}
    current_numeric = numeric_features(current)
    keys = set(current_numeric)
    for state in history:
        keys.update(numeric_features(state))
    scales = feature_scales([current, *history], keys)
    candidates = [compare_states(current, state, scales, weights) for state in history if state.get("state_id") != current.get("state_id")]
    candidates = [candidate for candidate in candidates if candidate["similarity_score"] >= minimum_similarity]
    candidates.sort(key=lambda row: (-row["similarity_score"], row["as_of_utc"], row["analogue_id"]))
    selected = candidates[: max(0, top_k)]
    result = {
        "schema": "stegverse.erl.historical_analogue_set.v1",
        "current_state_id": current["state_id"],
        "current_state_vector_digest": current.get("vector_digest") or canonical_digest(current),
        "feature_version": current["feature_version"],
        "similarity_method": "weighted_normalized_l1_with_missingness_penalty.v1",
        "weights": {key: float(value) for key, value in sorted(weights.items())},
        "analogue_count": len(selected),
        "historical_analogues": selected,
        "research_authority": "ERL",
        "execution_authority": "NONE",
        "may_authorize_order": False,
    }
    result["analogue_set_digest"] = canonical_digest(result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Find reproducible ERL historical market analogues.")
    parser.add_argument("current_state")
    parser.add_argument("history")
    parser.add_argument("--weights")
    parser.add_argument("--top-k", type=int, default=20)
    parser.add_argument("--minimum-similarity", type=float, default=0.0)
    parser.add_argument("--out")
    args = parser.parse_args()

    current = json.loads(Path(args.current_state).read_text())
    history_payload = json.loads(Path(args.history).read_text())
    history = history_payload["states"] if isinstance(history_payload, dict) else history_payload
    weights = json.loads(Path(args.weights).read_text()) if args.weights else {}
    result = find_analogues(current, history, top_k=args.top_k, minimum_similarity=args.minimum_similarity, weights=weights)
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(encoded)
    print(json.dumps({"status": "PASS", "analogue_count": result["analogue_count"], "execution_authority": "NONE"}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
