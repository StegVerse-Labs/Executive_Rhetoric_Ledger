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


def normalize_known_event(payload: dict[str, Any], source_ref: str) -> dict[str, Any]:
    schema = payload.get("schema", "")
    if schema == "stegverse.erl.crypto_system_shock_transaction_reconstruction.v1":
        from index_crypto_system_shock_event import normalize_shock
        return normalize_shock(payload, source_ref)

    # General event adapter deliberately extracts only fields that can be
    # represented without inventing causation or timestamps.
    candidate_times = [
        payload.get("observed_at_utc"),
        payload.get("announced_at_utc"),
        payload.get("timestamp_utc"),
        payload.get("event_time_utc"),
        payload.get("captured_at_utc"),
    ]
    observed_at = next((value for value in candidate_times if isinstance(value, str) and value), None)
    if observed_at is None:
        captured_on = payload.get("captured_on")
        if isinstance(captured_on, str) and len(captured_on) == 10:
            observed_at = captured_on + "T00:00:00Z"
        else:
            raise ValueError("no authoritative UTC-compatible event timestamp found")

    facts: dict[str, Any] = {}
    for key in ("status", "finding_authorized", "activation_state", "amendment_state", "network", "asset"):
        value = payload.get(key)
        if isinstance(value, (str, int, float, bool)) or value is None:
            if key in payload:
                facts[key] = value

    uncertainties: list[str] = []
    for key in ("qualification", "current_disposition", "interpretation_limit", "note"):
        value = payload.get(key)
        if isinstance(value, str) and value:
            uncertainties.append(value)

    observation = {
        "schema": "stegverse.erl.market_observation.v1",
        "observation_id": "event:" + hashlib.sha256(source_ref.encode()).hexdigest()[:20],
        "observed_at_utc": observed_at,
        "family": "event_context",
        "observation_type": schema or "erl_market_event",
        "status": "PARTIAL",
        "instruments": [],
        "facts": facts,
        "hypotheses": [],
        "uncertainties": uncertainties or ["Event normalized from an existing ERL object; detailed causal interpretation remains source-specific."],
        "source_refs": [source_ref],
        "source_quality": 0.5,
        "research_authority": "ERL",
        "execution_authority": "NONE",
        "may_authorize_order": False,
    }
    observation["observation_digest"] = canonical_digest(observation)
    return observation


def main() -> int:
    parser = argparse.ArgumentParser(description="Normalize known ERL market-event records into market observations.")
    parser.add_argument("source")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    source = Path(args.source)
    payload = json.loads(source.read_text())
    observation = normalize_known_event(payload, str(source))
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(observation, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status":"PASS","observation_id":observation["observation_id"],"execution_authority":"NONE"}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
