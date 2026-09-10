#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

EDGE_POSTURE = {
    "DECLARED_BY_PROVIDER": ("DOWNSTREAM", "DECLARED", "ELIGIBLE"),
    "OBSERVED_TRANSFER": ("DOWNSTREAM", "OBSERVED", "ELIGIBLE"),
    "REGULATORY_OR_COURT_RECORD": ("DOWNSTREAM", "REGULATORY", "ELIGIBLE"),
    "CREDIBLE_THIRD_PARTY_REPORT": ("WATCH", "CREDIBLE_REPORT", "WATCH_ONLY"),
    "INFERRED_UNVERIFIED": ("WATCH", "INFERRED_UNVERIFIED", "BLOCKED_UNVERIFIED"),
    "UNKNOWN": ("WATCH", "UNKNOWN", "BLOCKED_UNVERIFIED"),
}

PROPAGATION_ELIGIBLE_TYPES = {"data_broker", "downstream_recipient", "index_or_cache", "model_or_retrieval_surface"}
PRIORITY_RANK = {"PRIMARY": 0, "DOWNSTREAM": 1, "WATCH": 2, "EXCLUDED": 3}


def load(path):
    return json.loads(Path(path).read_text())


def target_key(target):
    return (target["org_ref"], target["source"])


def build(skap, propagation, generated_at):
    if skap["subject_ref"] != propagation["subject_ref"]:
        raise ValueError("SKAP and propagation graphs must refer to the same subject")

    targets = []

    # A user-authorized SKAP account is direct evidence that the account provider
    # holds at least account-associated data for the subject. It is therefore a
    # primary reclamation/access/export candidate without inferring downstream flow.
    for account in skap["accounts"]:
        targets.append({
            "target_id": f"target:account-provider:{account['provider_org_ref']}",
            "org_ref": account["provider_org_ref"],
            "source": "SKAP_ACCOUNT_PROVIDER",
            "priority": "PRIMARY",
            "evidence_state": "DIRECT",
            "action_state": "ELIGIBLE",
            "data_classes": ["account"],
            "skap_account_refs": [account["skap_account_ref"]],
            "reason_refs": [f"skap-account:{account['skap_account_ref']}"],
        })

    for edge in skap["disclosure_edges"]:
        priority, evidence_state, action_state = EDGE_POSTURE[edge["evidence_state"]]
        # Explicit source graph priority can only make posture more conservative.
        if edge.get("reclamation_priority") == "WATCH":
            priority = "WATCH"
            if action_state == "ELIGIBLE":
                action_state = "WATCH_ONLY"
        elif edge.get("reclamation_priority") == "EXCLUDED_LEGAL":
            priority = "EXCLUDED"
            action_state = "EXCLUDED_LEGAL"
        targets.append({
            "target_id": f"target:disclosure:{edge['edge_id']}",
            "org_ref": edge["to_org_ref"],
            "source": "SKAP_DISCLOSURE_EDGE",
            "priority": priority,
            "evidence_state": evidence_state,
            "action_state": action_state,
            "data_classes": sorted(edge["data_classes"]),
            "skap_account_refs": sorted(edge.get("skap_account_refs", [])),
            "reason_refs": sorted(edge.get("evidence_refs", []) or [f"disclosure-edge:{edge['edge_id']}"]),
        })

    for node in propagation["nodes"]:
        if node["node_type"] not in PROPAGATION_ELIGIBLE_TYPES:
            continue
        state = node.get("current_state", "UNVERIFIABLE")
        if state in {"OBSERVED", "REAPPEARED"}:
            action_state = "ELIGIBLE"
            evidence_state = "OBSERVED"
            priority = "DOWNSTREAM"
        elif state in {"REMOVAL_REQUESTED", "RESTRICTED", "PROVIDER_ASSERTED_DELETED", "INDEPENDENTLY_VERIFIED_DELETED"}:
            action_state = "COMPLETE" if state == "INDEPENDENTLY_VERIFIED_DELETED" else "WATCH_ONLY"
            evidence_state = "OBSERVED"
            priority = "WATCH"
        else:
            action_state = "WATCH_ONLY"
            evidence_state = "UNKNOWN"
            priority = "WATCH"
        targets.append({
            "target_id": f"target:propagation:{node['node_id']}",
            "org_ref": node["identity"],
            "source": "OBSERVED_PROPAGATION_NODE",
            "priority": priority,
            "evidence_state": evidence_state,
            "action_state": action_state,
            "data_classes": [],
            "skap_account_refs": [],
            "reason_refs": [f"propagation-node:{node['node_id']}"],
        })

    # Preserve distinct evidence lanes; deduplicate only exact source/org collisions.
    deduped = {}
    for target in targets:
        deduped[target_key(target)] = target

    return {
        "schema": "stegverse.reclamation-target-set/v1",
        "target_set_id": f"{skap['graph_id']}:targets",
        "subject_ref": skap["subject_ref"],
        "generated_at": generated_at,
        "targets": sorted(
            deduped.values(),
            key=lambda t: (PRIORITY_RANK[t["priority"]], t["org_ref"], t["source"]),
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--skap-graph", required=True)
    parser.add_argument("--propagation-graph", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--generated-at")
    args = parser.parse_args()

    generated_at = args.generated_at or datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    result = build(load(args.skap_graph), load(args.propagation_graph), generated_at)
    Path(args.output).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
