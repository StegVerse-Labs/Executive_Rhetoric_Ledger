#!/usr/bin/env python3
"""Validate generated adjacency graph determinism and governance boundaries."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    output = ROOT / "adjacency_graphs/generated.json"
    subprocess.run(["python", "scripts/generate_adjacency_graph.py", "--output", str(output.relative_to(ROOT))], cwd=ROOT, check=True)
    graph = load(output)
    schema = load(ROOT / "schemas/adjacency-graph.schema.json")
    errors = list(Draft202012Validator(schema).iter_errors(graph))
    if errors:
        raise SystemExit("Adjacency graph schema validation failed: " + "; ".join(error.message for error in errors))
    node_ids = {node["node_id"] for node in graph["nodes"]}
    if len(node_ids) != len(graph["nodes"]):
        raise SystemExit("Adjacency graph contains duplicate node IDs.")
    edge_ids = set()
    for edge in graph["edges"]:
        if edge["edge_id"] in edge_ids:
            raise SystemExit("Adjacency graph contains duplicate edge IDs.")
        edge_ids.add(edge["edge_id"])
        if edge["source"] not in node_ids or edge["target"] not in node_ids:
            raise SystemExit("Adjacency edge references a missing node.")
        if edge["causation_asserted"]:
            raise SystemExit("Automation may not assert causation.")
    authority = graph["automation_authority"]
    if authority["may_assert_identity"] or authority["may_assert_causation"] or authority["may_publish"]:
        raise SystemExit("Adjacency automation exceeded governed authority.")
    print(f"Validated graph {graph['graph_id']} with {len(graph['nodes'])} nodes and {len(graph['edges'])} edges.")


if __name__ == "__main__":
    main()
