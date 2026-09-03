#!/usr/bin/env python3
import json
import sys

DEFAULT_COUNTS = [1000, 100000, 1000000]

def scenarios(exact_per_request=None, lower_per_request=None, upper_per_request=None, counts=None):
    counts = counts or DEFAULT_COUNTS
    if exact_per_request is not None:
        if exact_per_request < 0:
            raise ValueError("exact_per_request must be nonnegative")
        return [
            {
                "equivalent_requests": n,
                "state": "EXACT",
                "known_total_cost_usd": round(exact_per_request * n, 12),
                "lower_bound_usd": None,
                "upper_bound_usd": None,
            }
            for n in counts
        ]

    if lower_per_request is not None or upper_per_request is not None:
        if lower_per_request is None or upper_per_request is None:
            raise ValueError("both lower_per_request and upper_per_request are required")
        if lower_per_request < 0 or upper_per_request < 0 or upper_per_request < lower_per_request:
            raise ValueError("invalid per-request bounds")
        return [
            {
                "equivalent_requests": n,
                "state": "BOUNDED",
                "known_total_cost_usd": None,
                "lower_bound_usd": round(lower_per_request * n, 12),
                "upper_bound_usd": round(upper_per_request * n, 12),
            }
            for n in counts
        ]

    return [
        {
            "equivalent_requests": n,
            "state": "UNBOUNDED_UNKNOWN",
            "known_total_cost_usd": None,
            "lower_bound_usd": None,
            "upper_bound_usd": None,
        }
        for n in counts
    ]

def main():
    payload = json.load(sys.stdin)
    result = scenarios(
        exact_per_request=payload.get("exact_per_request_usd"),
        lower_per_request=payload.get("lower_per_request_usd"),
        upper_per_request=payload.get("upper_per_request_usd"),
        counts=payload.get("equivalent_request_counts"),
    )
    print(json.dumps({"scale_scenarios": result}, separators=(",", ":")))

if __name__ == "__main__":
    main()
