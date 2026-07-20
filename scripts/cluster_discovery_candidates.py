#!/usr/bin/env python3
"""Group discovery candidates deterministically without merging or promoting records."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOKEN = re.compile(r"[a-z0-9]{3,}")


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def tokens(candidate: dict) -> set[str]:
    payload = candidate.get("normalized_payload")
    text = json.dumps(payload, sort_keys=True) if payload is not None else candidate.get("source_uri", "")
    return set(TOKEN.findall(text.lower()))


def jaccard(left: set[str], right: set[str]) -> float:
    union = left | right
    return 1.0 if not union else len(left & right) / len(union)


def cluster_id(members: list[dict]) -> str:
    basis = "|".join(sorted(member["candidate_id"] for member in members))
    return "CLUSTER-" + hashlib.sha256(basis.encode()).hexdigest()[:20].upper()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-root", default="discovery_candidates")
    parser.add_argument("--output", default="incident_clusters/generated.json")
    parser.add_argument("--threshold", type=float, default=0.72)
    args = parser.parse_args()

    candidates = [load(path) for path in sorted((ROOT / args.candidate_root).glob("**/CAND-*.json"))]
    by_hash: dict[str, list[dict]] = defaultdict(list)
    for candidate in candidates:
        by_hash[candidate["content_sha256"]].append(candidate)

    clusters: list[dict] = []
    assigned: set[str] = set()
    for digest, members in sorted(by_hash.items()):
        if len(members) > 1:
            assigned.update(member["candidate_id"] for member in members)
            clusters.append({
                "cluster_id": cluster_id(members),
                "cluster_status": "candidate-cluster",
                "member_candidate_ids": sorted(member["candidate_id"] for member in members),
                "member_hashes": [digest],
                "cluster_key": digest,
                "similarity_method": "exact-content-hash",
                "minimum_similarity": 1.0,
                "review_status": "cluster-review-required",
                "automation_authority": {"may_group": True, "may_merge_records": False, "may_promote": False}
            })

    unassigned = [item for item in candidates if item["candidate_id"] not in assigned]
    while unassigned:
        seed = unassigned.pop(0)
        seed_tokens = tokens(seed)
        group = [seed]
        remaining = []
        scores = []
        for candidate in unassigned:
            score = jaccard(seed_tokens, tokens(candidate))
            if score >= args.threshold:
                group.append(candidate)
                scores.append(score)
            else:
                remaining.append(candidate)
        unassigned = remaining
        clusters.append({
            "cluster_id": cluster_id(group),
            "cluster_status": "candidate-cluster",
            "member_candidate_ids": sorted(item["candidate_id"] for item in group),
            "member_hashes": sorted({item["content_sha256"] for item in group}),
            "cluster_key": hashlib.sha256("|".join(sorted(seed_tokens)).encode()).hexdigest(),
            "similarity_method": "normalized-token-jaccard",
            "minimum_similarity": min(scores) if scores else 1.0,
            "review_status": "cluster-review-required",
            "automation_authority": {"may_group": True, "may_merge_records": False, "may_promote": False}
        })

    output = ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps({"threshold": args.threshold, "clusters": clusters}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(output.relative_to(ROOT))


if __name__ == "__main__":
    main()
