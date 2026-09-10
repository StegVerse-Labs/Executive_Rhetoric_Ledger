#!/usr/bin/env python3
"""Bidirectionally reconcile a non-secret SKAP account projection against evidence mappings."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _reachable_from_provider(graph: dict[str, Any], provider: str) -> tuple[set[str], set[str]]:
    downstream: set[str] = set()
    refs: set[str] = set()
    frontier = [provider]
    visited = {provider}
    while frontier:
        current = frontier.pop(0)
        for edge in graph["disclosure_edges"]:
            if edge["from_org_ref"] != current:
                continue
            downstream.add(edge["to_org_ref"])
            refs.update(edge.get("evidence_refs", []))
            if edge["to_org_ref"] not in visited:
                visited.add(edge["to_org_ref"])
                frontier.append(edge["to_org_ref"])
    return downstream, refs


def reconcile(
    skap_inventory: dict[str, Any],
    disclosure_graph: dict[str, Any],
    propagation_graph: dict[str, Any],
    generated_at: str,
) -> dict[str, Any]:
    subjects = {
        skap_inventory["subject_ref"],
        disclosure_graph["subject_ref"],
        propagation_graph["subject_ref"],
    }
    if len(subjects) != 1:
        raise ValueError("cross-subject SKAP/evidence reconciliation is prohibited")
    if skap_inventory.get("contains_secret_material") is not False:
        raise ValueError("SKAP reconciliation input must be a non-secret account projection")

    mapped_orgs = {org["org_ref"] for org in disclosure_graph["organizations"]}
    known_providers = {a["provider_org_ref"] for a in skap_inventory["accounts"]}
    accounts = []
    downstream_from_known: set[str] = set()

    for account in sorted(skap_inventory["accounts"], key=lambda a: a["skap_account_ref"]):
        provider = account["provider_org_ref"]
        downstream, refs = _reachable_from_provider(disclosure_graph, provider)
        downstream_from_known.update(downstream)
        accounts.append({
            "skap_account_ref": account["skap_account_ref"],
            "provider_org_ref": provider,
            "classification": "KNOWN_AND_MAPPED" if provider in mapped_orgs else "KNOWN_BUT_UNMAPPED",
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
        "subject_ref": skap_inventory["subject_ref"],
        "generated_at": generated_at,
        "accounts": accounts,
        "evidence_only_origins": [
            {
                "org_ref": org,
                "classification": "EVIDENCE_WITHOUT_KNOWN_ACCOUNT_ORIGIN",
                "evidence_refs": sorted(refs),
            }
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
    p.add_argument("--skap-inventory", type=Path, required=True)
    p.add_argument("--disclosure-graph", type=Path, required=True)
    p.add_argument("--propagation-graph", type=Path, required=True)
    p.add_argument("--generated-at", required=True)
    args = p.parse_args()
    result = reconcile(
        json.loads(args.skap_inventory.read_text()),
        json.loads(args.disclosure_graph.read_text()),
        json.loads(args.propagation_graph.read_text()),
        args.generated_at,
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
