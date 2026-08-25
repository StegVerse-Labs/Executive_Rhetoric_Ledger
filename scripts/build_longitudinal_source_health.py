#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ISO_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def canonical_digest(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def parse_timestamp(value: str) -> datetime | None:
    if ISO_RE.match(value):
        return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)
    if DATE_RE.match(value):
        return datetime.fromisoformat(value + "T23:59:59+00:00")
    return None


def source_latest_timestamp(path: Path) -> datetime | None:
    """Return the source's own observation/as-of timestamp, never arbitrary dates in prose or future windows."""
    try:
        data = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError):
        return None

    schema = str(data.get("schema", "")) if isinstance(data, dict) else ""
    if schema == "stegverse.erl.crypto_market_panel.coingecko.utc.v1" or "crypto_market_panel" in schema:
        dates = data.get("dates", [])
        if dates:
            return parse_timestamp(str(dates[-1]))

    if schema == "stegverse.erl.crypto_system_shock_transaction_reconstruction.v1":
        center = data.get("event_center", {}).get("derived_utc_center")
        return parse_timestamp(str(center)) if center else None

    if isinstance(data, dict):
        for key in (
            "as_of_utc",
            "observed_at_utc",
            "observed_at",
            "captured_at_utc",
            "captured_at",
            "captured_on",
            "date",
        ):
            value = data.get(key)
            if isinstance(value, str):
                parsed = parse_timestamp(value)
                if parsed is not None:
                    return parsed
    return None


def build_health(registry: dict[str, Any], policy: dict[str, Any], root: Path, as_of: datetime) -> dict[str, Any]:
    thresholds = policy["freshness_hours"]
    scoring = policy["scoring"]
    families: list[dict[str, Any]] = []
    total_score = 0.0

    for family in registry["families"]:
        family_name = family["family"]
        admitted = family.get("admitted_sources", [])
        threshold = float(thresholds[family_name])
        latest: datetime | None = None
        resolved_sources: list[dict[str, Any]] = []

        for source in admitted:
            source_path = root / source
            source_latest = source_latest_timestamp(source_path)
            resolved_sources.append({
                "source_ref": source,
                "latest_observation_utc": source_latest.isoformat().replace("+00:00", "Z") if source_latest else None,
            })
            if source_latest is not None and (latest is None or source_latest > latest):
                latest = source_latest

        if not admitted:
            state = "MISSING"
            age_hours = None
        elif latest is None:
            state = "UNKNOWN_FRESHNESS"
            age_hours = None
        else:
            age_hours = max(0.0, (as_of - latest).total_seconds() / 3600.0)
            state = "FRESH" if age_hours <= threshold else "STALE"

        contribution = float(scoring[state]) / len(registry["families"])
        total_score += contribution
        families.append({
            "family": family_name,
            "registry_state": family["state"],
            "health_state": state,
            "latest_observation_utc": latest.isoformat().replace("+00:00", "Z") if latest else None,
            "age_hours": round(age_hours, 3) if age_hours is not None else None,
            "freshness_threshold_hours": threshold,
            "coverage_contribution": round(contribution, 8),
            "sources": resolved_sources,
        })

    result = {
        "schema": "stegverse.erl.longitudinal_market_source_health_receipt.v1",
        "as_of_utc": as_of.isoformat().replace("+00:00", "Z"),
        "registry_id": registry["registry_id"],
        "policy_id": policy["policy_id"],
        "coverage_score": round(total_score, 8),
        "families": families,
        "research_authority": "ERL",
        "execution_authority": "NONE",
        "may_authorize_order": False,
    }
    result["receipt_digest"] = canonical_digest(result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a deterministic ERL longitudinal market source-health receipt.")
    parser.add_argument("registry")
    parser.add_argument("policy")
    parser.add_argument("--root", default=".")
    parser.add_argument("--as-of", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    registry = json.loads(Path(args.registry).read_text())
    policy = json.loads(Path(args.policy).read_text())
    as_of = parse_timestamp(args.as_of)
    if as_of is None:
        raise ValueError("--as-of must be ISO-8601 date-time")
    result = build_health(registry, policy, Path(args.root), as_of)
    output = Path(args.out)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": "PASS",
        "coverage_score": result["coverage_score"],
        "execution_authority": "NONE",
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
