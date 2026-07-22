#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RELATED_REPOSITORIES = ROOT / "integration" / "related-repositories.json"

GENERAL_DESTINATIONS = [
    ("StegVerse-Labs/Site", "data/executive-rhetoric-ledger/compendium.json"),
    ("GCAT-BCAT-Engine/Publisher", "inputs/executive-rhetoric-ledger/compendium.json"),
    ("StegVerse-Labs/admissibility-wiki", "data/executive-rhetoric-ledger/compendium.json"),
    ("StegVerse-Labs/stegguardian-wiki", "data/executive-rhetoric-ledger/compendium.json"),
]


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def title_of(text: str, fallback: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def slug(repository: str) -> str:
    return repository.split("/", 1)[-1].lower().replace("_", "-")


def reviewed_entries() -> list[dict]:
    entries: list[dict] = []
    for path in sorted((ROOT / "ledger_receipts" / "reviewed").glob("*.md")):
        data = path.read_bytes()
        text = data.decode("utf-8")
        entries.append(
            {
                "entry_id": sha(str(path.relative_to(ROOT)).encode())[:20].upper(),
                "title": title_of(text, path.stem),
                "receipt_path": str(path.relative_to(ROOT)),
                "receipt_sha256": sha(data),
                "review_status": "reviewed",
                "search_text": " ".join(text.split())[:12000],
                "_source_text": text,
            }
        )
    return entries


def person_specific_repositories() -> list[dict]:
    network = json.loads(RELATED_REPOSITORIES.read_text(encoding="utf-8"))
    result = []
    for item in network.get("repositories", []):
        roles = set(item.get("roles", []))
        if roles.intersection({"person-or-network-specific-record", "public-figure-record"}):
            result.append(item)
    return result


def explicitly_related(entry: dict, repository: str) -> bool:
    text = entry["_source_text"]
    repo_short = repository.split("/", 1)[-1]
    patterns = (
        rf'producer_repo:\s*["\']?{re.escape(repository)}["\']?',
        rf'producer_repo:\s*["\']?{re.escape(repo_short)}["\']?',
        rf'person_specific_repository:\s*["\']?{re.escape(repository)}["\']?',
        rf'person_specific_repository:\s*["\']?{re.escape(repo_short)}["\']?',
        rf'target_repository:\s*["\']?{re.escape(repository)}["\']?',
    )
    return any(re.search(pattern, text, re.IGNORECASE) for pattern in patterns)


def public_entry(entry: dict) -> dict:
    return {key: value for key, value in entry.items() if not key.startswith("_")}


def write_person_specific_projections(entries: list[dict], generated_at: str) -> list[dict]:
    output_dir = ROOT / "person_specific_projections"
    output_dir.mkdir(exist_ok=True)
    destinations: list[dict] = []

    for related in person_specific_repositories():
        repository = related["repository"]
        matched = [public_entry(entry) for entry in entries if explicitly_related(entry, repository)]
        if not matched:
            continue

        projection = {
            "schema": "stegverse.executive_rhetoric_ledger.person_specific_projection.v1",
            "projection_id": "PERSON-PROJECTION-" + sha(
                (repository + "|" + "|".join(item["receipt_sha256"] for item in matched)).encode()
            )[:20].upper(),
            "generated_at": generated_at,
            "source_repository": "StegVerse-Labs/Executive_Rhetoric_Ledger",
            "destination_repository": repository,
            "projection_status": "reviewed-ledger-projection",
            "entries": matched,
            "evidence_boundary": related["evidence_boundary"],
            "authority": {
                "reviewed_only": True,
                "may_include_candidates": False,
                "may_change_native_source_records": False,
                "may_change_destination_verification_labels": False,
                "may_establish_culpability": False,
                "may_claim_delivery": False,
                "may_claim_acknowledgment": False,
            },
        }
        material = json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()
        projection["projection_sha256"] = sha(material)
        output_path = output_dir / f"{slug(repository)}.json"
        output_path.write_text(json.dumps(projection, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        destinations.append(
            {
                "repository": repository,
                "target_path": "data/receipts/ledger_reviewed_projections/latest.json",
                "source_path": str(output_path.relative_to(ROOT)),
                "source_sha256": sha(output_path.read_bytes()),
                "delivery_status": "prepared",
                "acknowledgment_required": True,
                "acknowledgment": None,
                "delivery_scope": "explicitly-related-reviewed-records-only",
            }
        )
    return destinations


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--generated-at", required=True)
    args = parser.parse_args()

    entries = reviewed_entries()
    public_entries = [public_entry(entry) for entry in entries]
    publication = {
        "publication_id": "COMPENDIUM-" + sha(
            "|".join(entry["receipt_sha256"] for entry in public_entries).encode()
        )[:20].upper(),
        "generated_at": args.generated_at,
        "publication_status": "reviewed-only-compendium",
        "entries": public_entries,
        "authority": {
            "reviewed_only": True,
            "may_include_candidates": False,
            "may_promote": False,
        },
    }

    publication_dir = ROOT / "publication"
    publication_dir.mkdir(exist_ok=True)
    json_bytes = (json.dumps(publication, indent=2, sort_keys=True) + "\n").encode()
    (publication_dir / "compendium.json").write_bytes(json_bytes)
    rows = "".join(
        f"<article><h2>{html.escape(entry['title'])}</h2><p><code>{html.escape(entry['receipt_path'])}</code></p></article>"
        for entry in public_entries
    )
    (publication_dir / "index.html").write_text(
        "<!doctype html><html><head><meta charset='utf-8'><title>Executive Rhetoric Ledger</title></head>"
        "<body><h1>Reviewed Receipt Compendium</h1>" + rows + "</body></html>\n",
        encoding="utf-8",
    )

    destinations = [
        {
            "repository": repository,
            "target_path": target_path,
            "delivery_status": "prepared",
            "acknowledgment_required": True,
            "acknowledgment": None,
            "delivery_scope": "reviewed-compendium",
        }
        for repository, target_path in GENERAL_DESTINATIONS
    ]
    destinations.extend(write_person_specific_projections(entries, args.generated_at))

    delivery = {
        "delivery_id": "DELIVERY-" + sha(json_bytes)[:20].upper(),
        "generated_at": args.generated_at,
        "source_publication": {
            "path": "publication/compendium.json",
            "sha256": sha(json_bytes),
        },
        "destinations": destinations,
        "authority": {
            "may_prepare": True,
            "may_claim_delivery": False,
            "may_claim_acknowledgment": False,
        },
    }
    delivery_dir = ROOT / "delivery_manifests"
    delivery_dir.mkdir(exist_ok=True)
    (delivery_dir / "generated.json").write_text(
        json.dumps(delivery, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
