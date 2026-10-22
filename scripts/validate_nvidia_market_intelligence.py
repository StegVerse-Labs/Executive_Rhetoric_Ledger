#!/usr/bin/env python3
"""Deterministic validation of ERL #236 market intelligence inputs; stdlib only."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "research-data/nvidia-market-intelligence"

def load(name):
    with (BASE / name).open(encoding="utf-8") as stream:
        return json.load(stream)

def validate():
    evidence = load("evidence-matrix.json")
    opportunities = load("opportunity-register.json")
    assert evidence["schema"] == "erl.market-evidence/v1"
    assert opportunities["schema"] == "erl.market-opportunity/v1"
    assert opportunities["outreach_enabled"] is False
    assert opportunities["ranking_state"].startswith("UNRANKED_")
    ids = set()
    for item in evidence["observations"]:
        assert item["id"] not in ids
        ids.add(item["id"])
        assert item["date"] and item["source"].startswith("https://")
        assert item["class"] and item["claim"] and item["confidence"]
        assert isinstance(item["unknowns"], list)
    ids.clear()
    for item in opportunities["opportunities"]:
        assert item["id"] not in ids
        ids.add(item["id"])
        assert item["buyer"] and item["mechanism"] and item["timing"]
        assert item["commercial_validation"] == "UNKNOWN"
        assert item["score"] is None
        assert item["triggers"] and item["disconfirmers"]
    assert len(evidence["observations"]) >= 3
    assert len(opportunities["opportunities"]) >= 3
    return len(evidence["observations"]), len(opportunities["opportunities"])

if __name__ == "__main__":
    e, o = validate()
    print(f"PASS: {e} evidence records, {o} opportunities; outreach disabled")
