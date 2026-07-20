#!/usr/bin/env python3
"""Generate candidate adjacency links without asserting identity or causation."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def edge_id(source: str, target: str, relationship: str) -> str:
    basis = f"{source}|{target}|{relationship}".encode()
    return "EDGE-" + hashlib.sha256(basis).hexdigest()[:20].upper()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-root", default="discovery_candidates")
    parser.add_argument("--cluster-file", default="incident_clusters/generated.json")
    parser.add_argument("--output", default="adjacency_graphs/generated.json")
    args = parser.parse_args()

    candidate_paths = sorted((ROOT / args.candidate_root).glob("**/CAND-*.json"))
    candidates = {load(path)["candidate_id"]: load(path) for path in candidate_paths}
    cluster_document = load(ROOT / args.cluster_file) if (ROOT / args.cluster_file).exists() else {"clusters": []}

    nodes = []
    edges = []
    for candidate_id, candidate in sorted(candidates.items()):
        payload = candidate.get("normalized_payload") or {}
        label = payload.get("title") or payload.get("fixture_id") or candidate_id
        nodes.append({"node_id": candidate_id, "node_type": "candidate", "label": str(label), "review_status": "candidate-review-required"})
        topic = payload.get("fixture_id") or payload.get("title")
        if topic:
            topic_id = "TOPIC-" + hashlib.sha256(str(topic).lower().encode()).hexdigest()[:20].upper()
            nodes.append({"node_id": topic_id, "node_type": "topic", "label": str(topic), "review_status": "candidate-review-required"})
            edges.append({
                "edge_id": edge_id(candidate_id, topic_id, "topical-overlap"),
                "source": candidate_id,
                "target": topic_id,
                "relationship_type": "topical-overlap",
                "evidence_basis": "normalized payload title or fixture identifier",
                "confidence": 0.8,
                "causation_asserted": False,
                "review_status": "edge-review-required"
            })

    for cluster in cluster_document.get("clusters", []):
        cluster_id = cluster["cluster_id"]
        nodes.append({"node_id": cluster_id, "node_type": "cluster", "label": cluster_id, "review_status": "candidate-review-required"})
        for candidate_id in cluster["member_candidate_ids"]:
            edges.append({
                "edge_id": edge_id(candidate_id, cluster_id, "member-of-cluster"),
                "source": candidate_id,
                "target": cluster_id,
                "relationship_type": "member-of-cluster",
                "evidence_basis": cluster["similarity_method"],
                "confidence": cluster["minimum_similarity"],
                "causation_asserted": False,
                "review_status": "edge-review-required"
            })

    unique_nodes = {node["node_id"]: node for node in nodes}
    generated_from = [args.cluster_file] + [str(path.relative_to(ROOT)) for path in candidate_paths]
    graph_basis = "|".join(sorted(unique_nodes)) + "|" + "|".join(sorted(edge["edge_id"] for edge in edges))
    document = {
        "graph_id": "GRAPH-" + hashlib.sha256(graph_basis.encode()).hexdigest()[:20].upper(),
        "graph_status": "candidate-graph",
        "generated_from": generated_from,
        "nodes": [unique_nodes[key] for key in sorted(unique_nodes)],
        "edges": sorted(edges, key=lambda edge: edge["edge_id"]),
        "review_status": "graph-review-required",
        "automation_authority": {"may_link": True, "may_assert_identity": False, "may_assert_causation": False, "may_publish": False}
    }
    output = ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(output.relative_to(ROOT))


if __name__ == "__main__":
    main()
