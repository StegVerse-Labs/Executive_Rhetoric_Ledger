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


def normalize_shock(payload: dict[str, Any], source_ref: str) -> dict[str, Any]:
    center = payload["event_center"]
    screenshots = payload.get("contemporaneous_screenshot_observations", {})
    instruments = sorted({key.split("_")[0] for key in screenshots})
    amplitude = payload.get("derived_amplitude_ratios_from_displayed_changes", {})
    public = payload.get("current_public_evidence", {})

    facts = {
        "event_center_utc": center["derived_utc_center"],
        "search_window_start_utc": center["primary_search_window_utc"][0],
        "search_window_end_utc": center["primary_search_window_utc"][1],
        "synchronized_cliff_observed": True,
        "xrp_vs_btc_display_change_amplitude_ratio": amplitude.get("XRP_vs_BTC"),
        "xrp_vs_eth_display_change_amplitude_ratio": amplitude.get("XRP_vs_ETH_0038"),
        "xrp_vs_atom_display_change_amplitude_ratio": amplitude.get("XRP_vs_ATOM"),
        "outage_check_result": public.get("exchange_or_network_outage_check", {}).get("result"),
        "discrete_news_trigger_check_result": public.get("discrete_news_trigger_check", {}).get("result"),
        "tick_data_access_result": public.get("public_tick_data_access", {}).get("result"),
        "finding_authorized": bool(payload.get("finding_authorized", False)),
    }
    uncertainties = [
        center.get("note", ""),
        amplitude.get("interpretation_limit", ""),
        public.get("exchange_or_network_outage_check", {}).get("qualification", ""),
        public.get("discrete_news_trigger_check", {}).get("qualification", ""),
        public.get("public_tick_data_access", {}).get("note", ""),
        payload.get("current_disposition", ""),
    ]
    uncertainties = [item for item in uncertainties if item]

    observation = {
        "schema": "stegverse.erl.market_observation.v1",
        "observation_id": "crypto-system-shock-2026-08-22T05:11:20Z",
        "observed_at_utc": center["derived_utc_center"],
        "family": "event_context",
        "observation_type": "synchronized_crypto_system_shock_candidate",
        "status": "UNRESOLVED",
        "instruments": instruments,
        "facts": facts,
        "hypotheses": payload.get("causal_hypotheses_to_discriminate", []),
        "uncertainties": uncertainties,
        "source_refs": [source_ref],
        "source_quality": 0.65,
        "research_authority": "ERL",
        "execution_authority": "NONE",
        "may_authorize_order": False,
    }
    observation["observation_digest"] = canonical_digest(observation)
    return observation


def main() -> int:
    parser = argparse.ArgumentParser(description="Normalize ERL crypto system-shock reconstruction into longitudinal event context.")
    parser.add_argument("source")
    parser.add_argument("--source-ref")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    source_path = Path(args.source)
    payload = json.loads(source_path.read_text())
    observation = normalize_shock(payload, args.source_ref or str(source_path))
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(observation, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": "PASS", "observation_id": observation["observation_id"], "execution_authority": "NONE"}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
