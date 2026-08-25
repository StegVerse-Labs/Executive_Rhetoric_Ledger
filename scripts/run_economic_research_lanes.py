#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = ROOT / "economic-trajectories/research-lanes.v1.json"
DEFAULT_GAPS = {
    "ERL-ECON-CA": ROOT / "economic-trajectories/canada/gap-matrix.v1.json",
    "ERL-ECON-US": ROOT / "economic-trajectories/united-states/gap-matrix.v1.json",
}
MAX_BYTES = 2_000_000
USER_AGENT = "StegVerse-ERL-economic-research/1.0 (+https://github.com/StegVerse-Labs/Executive_Rhetoric_Ledger)"


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def parse_time(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def iso(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def validate_registry(registry: dict[str, Any], indicator_ids: set[str], gaps: dict[str, set[str]]) -> list[str]:
    errors: list[str] = []
    expected = {
        "ERL-ECON-CA": ("Canada", "national-source-monitor", "weekly"),
        "ERL-ECON-US": ("United States", "national-source-monitor", "weekly"),
        "ERL-ECON-CA-US-OVERLAY": ("Canada-United States comparison", "reviewed-findings-only", "manual-only"),
    }
    lanes = registry.get("lanes", [])
    ids = [lane.get("lane_id") for lane in lanes]
    if set(ids) != set(expected) or len(ids) != len(set(ids)):
        errors.append("registry must contain each independent national lane and the overlay exactly once")
    source_ids: list[str] = []
    for lane in lanes:
        lane_id = lane.get("lane_id")
        if lane_id not in expected:
            continue
        jurisdiction, mode, cadence = expected[lane_id]
        if (lane.get("jurisdiction"), lane.get("mode"), lane.get("cadence")) != (jurisdiction, mode, cadence):
            errors.append(f"{lane_id}: jurisdiction, mode, or cadence violates lane contract")
        sources = lane.get("sources", [])
        if lane_id == "ERL-ECON-CA-US-OVERLAY" and sources:
            errors.append("comparison overlay may not acquire external sources")
        if lane_id != "ERL-ECON-CA-US-OVERLAY" and not sources:
            errors.append(f"{lane_id}: automated national lane has no sources")
        for source in sources:
            source_id = source.get("source_id")
            source_ids.append(source_id)
            if source.get("jurisdiction") != jurisdiction:
                errors.append(f"{source_id}: source jurisdiction crosses national lane")
            if source.get("evidence_use") != "DISCOVERY_ONLY_UNTIL_REVIEW":
                errors.append(f"{source_id}: source attempts automatic evidentiary promotion")
            unknown_indicators = set(source.get("indicator_ids", [])) - indicator_ids
            if unknown_indicators:
                errors.append(f"{source_id}: unknown indicators {sorted(unknown_indicators)}")
            unknown_gaps = set(source.get("gap_ids", [])) - gaps.get(lane_id, set())
            if unknown_gaps:
                errors.append(f"{source_id}: unknown or cross-lane gaps {sorted(unknown_gaps)}")
    if len(source_ids) != len(set(source_ids)):
        errors.append("source_id values must be unique")
    authority = registry.get("authority", {})
    if any(authority.get(key) is not False for key in ("may_create_findings", "may_compare", "may_publish")):
        errors.append("automation authority must deny findings, comparison, and publication")
    return errors


def default_fetch(source: dict[str, Any]) -> dict[str, Any]:
    request = urllib.request.Request(
        source["url"],
        method="GET",
        headers={"User-Agent": USER_AGENT, "Accept": ", ".join(source["expected_media_types"])},
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            body = response.read(MAX_BYTES + 1)
            if len(body) > MAX_BYTES:
                raise ValueError(f"response exceeded {MAX_BYTES} bytes")
            return {
                "ok": True,
                "http_status": response.status,
                "final_url": response.geturl(),
                "content_type": response.headers.get("Content-Type", "").split(";", 1)[0].strip().lower(),
                "etag": response.headers.get("ETag"),
                "last_modified": response.headers.get("Last-Modified"),
                "sha256": hashlib.sha256(body).hexdigest(),
                "bytes": len(body),
            }
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ValueError) as error:
        return {"ok": False, "error_type": type(error).__name__, "error": str(error)[:500]}


def previous_sources(previous: dict[str, Any] | None) -> dict[str, dict[str, Any]]:
    if not previous:
        return {}
    return {row["source_id"]: row for row in previous.get("sources", [])}


def capture(
    registry: dict[str, Any],
    gaps: dict[str, dict[str, Any]],
    captured_at: datetime,
    previous: dict[str, Any] | None = None,
    fetcher: Callable[[dict[str, Any]], dict[str, Any]] = default_fetch,
) -> tuple[dict[str, Any], dict[str, Any]]:
    prior = previous_sources(previous)
    receipts: list[dict[str, Any]] = []
    tasks: list[dict[str, Any]] = []
    for lane in registry["lanes"]:
        if lane["mode"] != "national-source-monitor":
            continue
        gap_rows = {row["gap_id"]: row for row in gaps[lane["lane_id"]]["rows"]}
        for source in lane["sources"]:
            result = fetcher(source)
            old = prior.get(source["source_id"])
            media_ok = result.get("content_type") in source["expected_media_types"] if result.get("ok") else False
            content_changed_at = iso(captured_at)
            if old and old.get("content_changed_at"):
                content_changed_at = old["content_changed_at"]
            if not result.get("ok"):
                state = "UNAVAILABLE"
            elif not media_ok:
                state = "UNEXPECTED_MEDIA_TYPE"
            elif old is None:
                state = "BASELINE_CAPTURED"
            elif old.get("sha256") != result.get("sha256"):
                state = "CHANGED"
                content_changed_at = iso(captured_at)
            else:
                age_days = (captured_at - parse_time(content_changed_at)).total_seconds() / 86400
                state = "STALE" if age_days > source["stale_after_days"] else "UNCHANGED"
            receipt = {
                "source_id": source["source_id"],
                "lane_id": lane["lane_id"],
                "jurisdiction": source["jurisdiction"],
                "url": source["url"],
                "captured_at": iso(captured_at),
                "content_changed_at": content_changed_at,
                "state": state,
                "http_status": result.get("http_status"),
                "final_url": result.get("final_url"),
                "content_type": result.get("content_type"),
                "etag": result.get("etag"),
                "last_modified": result.get("last_modified"),
                "sha256": result.get("sha256"),
                "bytes": result.get("bytes"),
                "error_type": result.get("error_type"),
                "error": result.get("error"),
                "gap_ids": source["gap_ids"],
                "evidence_use": "DISCOVERY_ONLY_UNTIL_REVIEW",
                "finding_authorized": False,
                "comparison_authorized": False,
                "publication_authorized": False,
            }
            receipts.append(receipt)
            if state in {"BASELINE_CAPTURED", "CHANGED", "STALE", "UNAVAILABLE", "UNEXPECTED_MEDIA_TYPE"}:
                for gap_id in source["gap_ids"]:
                    task_id = hashlib.sha256(f"{lane['lane_id']}|{source['source_id']}|{gap_id}|{state}".encode()).hexdigest()[:16]
                    tasks.append({
                        "task_id": f"ERL-ECON-TASK-{task_id.upper()}",
                        "lane_id": lane["lane_id"],
                        "source_id": source["source_id"],
                        "gap_id": gap_id,
                        "trigger": state,
                        "next_targeted_query": gap_rows[gap_id]["next_targeted_query"],
                        "status": "REVIEW_REQUIRED",
                        "may_create_finding": False,
                    })
    receipts.sort(key=lambda row: row["source_id"])
    tasks.sort(key=lambda row: row["task_id"])
    run_id = hashlib.sha256((iso(captured_at) + "|" + "|".join(row["source_id"] for row in receipts)).encode()).hexdigest()[:16]
    run = {
        "schema_version": "stegverse.erl.economic-research-run.v1",
        "run_id": f"ERL-ECON-RUN-{run_id.upper()}",
        "captured_at": iso(captured_at),
        "registry_id": registry["registry_id"],
        "receipts": receipts,
        "review_tasks": tasks,
        "summary": {
            "sources": len(receipts),
            "changed": sum(row["state"] == "CHANGED" for row in receipts),
            "baseline_captured": sum(row["state"] == "BASELINE_CAPTURED" for row in receipts),
            "stale": sum(row["state"] == "STALE" for row in receipts),
            "unavailable": sum(row["state"] in {"UNAVAILABLE", "UNEXPECTED_MEDIA_TYPE"} for row in receipts),
            "review_tasks": len(tasks),
            "findings_created": 0,
            "comparisons_created": 0,
        },
        "authority": {"finding_authorized": False, "comparison_authorized": False, "publication_authorized": False},
    }
    state = {
        "schema_version": "stegverse.erl.economic-source-state.v1",
        "updated_at": iso(captured_at),
        "sources": [{key: row[key] for key in ("source_id", "lane_id", "sha256", "etag", "last_modified", "captured_at", "content_changed_at", "state")} for row in receipts],
        "authority": {"finding_authorized": False, "comparison_authorized": False, "publication_authorized": False},
    }
    return run, state


def main() -> int:
    parser = argparse.ArgumentParser(description="Capture official economic source changes into review-only national lanes.")
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument("--previous", type=Path)
    parser.add_argument("--captured-at", required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--state-out", type=Path, required=True)
    args = parser.parse_args()

    registry = load(args.registry)
    dictionary = load(ROOT / "economic-trajectories/measurement-dictionary.v1.json")
    gaps = {lane: load(path) for lane, path in DEFAULT_GAPS.items()}
    errors = validate_registry(
        registry,
        {row["indicator_id"] for row in dictionary["indicators"]},
        {lane: {row["gap_id"] for row in matrix["rows"]} for lane, matrix in gaps.items()},
    )
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    previous = load(args.previous) if args.previous and args.previous.exists() else None
    run, state = capture(registry, gaps, parse_time(args.captured_at), previous)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.state_out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(run, indent=2, sort_keys=True) + "\n")
    args.state_out.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n")
    print(json.dumps(run["summary"], sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
