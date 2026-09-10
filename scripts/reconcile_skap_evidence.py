#!/usr/bin/env python3
"""Bidirectionally reconcile SKAP-known accounts against evidence-backed organization mappings."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _reachable_from_provider(graph: dict[str, Any], provider: str) -> tuple[set[str], set[str]]:
    account_edges = [e for e in graph["disclosure_edges"] if e["from_org_ref"] == provider]
    downstream: set[str] = set()
    refs: set[str] = set()
    frontier = [provider]
    visited = {provider}
    while frontier:
        current = frontier.pop(0)
        for edge in graph["disclosure_edges"]:
            if edge["from_org_ref"] != current:
                continue
            # Every edge may be retained as evidence context, but inference never becomes observed transfer.
            downstream.add(edge["to_org_ref"])
            refs.update(edge.get("evidence_refs", []))
            if edge["to_org_ref"] not in visited:
                visited.add(edge["to_org_ref"])
                frontier.append(edge["to_org_ref"])
    return downstream, refs


def reconcile(skap_graph: dict[str, Any], propagation_graph: dict[str, Any], generated_at: str) -> dict[str, Any]:
    if skap_graph["subject_ref"] != propagation_graph["subject_ref"]:
        raise ValueError("cross-subject SKAP/evidence reconciliation is prohibited")

    known_providers = {a["provider_org_ref"] for a in skap_graph["accounts"]}
    accounts = []
    downstream_from_known: set[str] = set()
    for account in sorted(skap_graph["accounts"], key=lambda a: a["skap_account_ref"]):
        downstream, refs = _reachable_from_provider(skap_graph, account["provider_org_ref"])
        downstream_from_known.update(downstream)
        mapped = bool(downstream or refs)
        accounts.append({
            "skap_account_ref": account["skap_account_ref"],
            "provider_org_ref": account["provider_org_ref"],
            "classification": "KNOWN_AND_MAPPED" if mapped else "KNOWN_BUT_UNMAPPED",
            "downstream_org_refs": sorted(downstream),
            "evidence_refs": sorted(refs),
        })

    evidence_only: dict[str, set[str]] = {}
    node_by_id = {n["node_id"]: n for n in propagation_graph["nodes"]}
    for edge in propagation_graph["edges"]:
        if edge.get("verification_state") != "VERIFIED":
            continue
        to_node = node_by_id[edge["to"]]
        org_ref = to_node.get("identity")
        if not isinstance(org_ref, str) or not org_ref.startswith("org:"):
            continue
        if org_ref in known_providers or org_ref in downstream_from_known:
            continue
        evidence_only.setdefault(org_ref, set()).add(f"propagation-edge:{edge['edge_id']}")

    return {
        "schema": "stegverse.skap-evidence-reconciliation/v1",
        "subject_ref": skap_graph["subject_ref"],
        "generated_at": generated_at,
        "accounts": accounts,
        "evidence_only_origins": [
            {"org_ref": org, "classification": "EVIDENCE_WITHOUT_KNOWN_ACCOUNT_ORIGIN", "evidence_refs": sorted(refs)}
            for org, refs in sorted(evidence_only.items())
        ],
        "summary": {
            "known_accounts": len(accounts),
            "known_and_mapped": sum(a["classification"] == "KNOWN_AND_MAPPED" for a in accounts),
            "known_but_unmapped": sum(a["classification"] == "KNOWN_BUT_UNMAPPED" for a in accounts),
            "downstream_from_known_account": len(downstream_from_known),
            "evidence_without_known_account_origin": len(evidence_only),
        },
    }


def main() -> None:
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--skap-graph", type=Path, required=True)
    p.add_argument("--propagation-graph", type=Path, required=True)
    p.add_argument("--generated-at", required=True)
    args = p.parse_args()
    result = reconcile(json.loads(args.skap_graph.read_text()), json.loads(args.propagation_graph.read_text()), args.generated_at)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
