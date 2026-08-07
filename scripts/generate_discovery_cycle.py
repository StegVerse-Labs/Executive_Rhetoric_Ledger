#!/usr/bin/env python3
"""Generate a governed discovery-cycle manifest from recurring-search configuration."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "config" / "recurring-searches.example.json"
DEFAULT_OUTPUT_DIR = ROOT / "discovery_cycles" / "generated"


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SystemExit(f"Missing input file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}") from exc


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def build_cycle(config: dict, started_at: str) -> dict:
    enabled_searches = [item for item in config["searches"] if item.get("enabled", True)]
    if not enabled_searches:
        raise SystemExit("Configuration contains no enabled searches.")

    cycle_suffix = started_at.replace("-", "").replace(":", "").replace("T", "-").replace("Z", "")
    queries = [
        {
            "query_id": item["search_id"],
            "query_text": item["query_template"],
            "discovery_class": item["discovery_class"],
            "status": "planned",
            "dpoi_search_parameters": item["dpoi_search_parameters"],
        }
        for item in enabled_searches
    ]

    return {
        "cycle_id": f"{config['config_id']}--{cycle_suffix}",
        "cycle_status": "planned",
        "started_at": started_at,
        "scope": config["scope"],
        "discovery_classes": sorted({item["discovery_class"] for item in enabled_searches}),
        "source_classes": config["source_classes"],
        "queries": queries,
        "candidate_outputs": {
            "new_topics": [],
            "source_receipts": [],
            "adjacency_links": [],
            "control_candidates": [],
            "contradictions": [],
            "outcome_updates": [],
            "dpoi_evidence_candidates": [],
        },
        "review_boundary": config["review_boundary"],
        "notes": "Generated from recurring-search configuration. DPOI directional parameters can identify evidence candidates that may strengthen, weaken, or disambiguate a data point of interest, but automation may not change DPOI state or treat a zero-result search as disproof.",
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--started-at", help="RFC3339 timestamp; defaults to current UTC time")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    config = load_json(args.config.resolve())
    started_at = args.started_at or utc_timestamp()
    cycle = build_cycle(config, started_at)

    output = args.output
    if output is None:
        DEFAULT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        output = DEFAULT_OUTPUT_DIR / f"{cycle['cycle_id']}.json"
    else:
        output = output.resolve()
        output.parent.mkdir(parents=True, exist_ok=True)

    output.write_text(json.dumps(cycle, indent=2) + "\n", encoding="utf-8")
    print(f"Generated {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
