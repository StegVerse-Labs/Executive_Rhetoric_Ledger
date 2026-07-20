#!/usr/bin/env python3
"""Validate generated candidate clusters and authority boundaries."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    output = ROOT / "incident_clusters/generated.json"
    subprocess.run(["python", "scripts/cluster_discovery_candidates.py", "--output", str(output.relative_to(ROOT))], cwd=ROOT, check=True)
    document = load(output)
    schema = load(ROOT / "schemas/incident-cluster.schema.json")
    validator = Draft202012Validator(schema)
    seen: set[str] = set()
    for cluster in document["clusters"]:
        errors = list(validator.iter_errors(cluster))
        if errors:
            raise SystemExit("Incident cluster schema validation failed: " + "; ".join(error.message for error in errors))
        overlap = seen.intersection(cluster["member_candidate_ids"])
        if overlap:
            raise SystemExit(f"Candidate assigned to multiple clusters: {sorted(overlap)}")
        seen.update(cluster["member_candidate_ids"])
        if cluster["automation_authority"]["may_merge_records"]:
            raise SystemExit("Automation may group but not merge records.")
        if cluster["automation_authority"]["may_promote"]:
            raise SystemExit("Automation may not promote clusters.")
    print(f"Validated {len(document['clusters'])} deterministic candidate cluster(s).")


if __name__ == "__main__":
    main()
