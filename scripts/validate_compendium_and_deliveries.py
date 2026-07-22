#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]


def load(path):
    return json.loads((ROOT / path).read_text())


def validate(schema_path, doc_path):
    errors = list(Draft202012Validator(load(schema_path)).iter_errors(load(doc_path)))
    if errors:
        raise SystemExit(f"{doc_path} failed schema validation: {errors[0].message}")


def validate_person_projection(destination: dict) -> None:
    source_path = ROOT / destination["source_path"]
    if not source_path.exists():
        raise SystemExit(f"Person-specific projection missing: {destination['source_path']}")
    raw = source_path.read_bytes()
    if destination["source_sha256"] != hashlib.sha256(raw).hexdigest():
        raise SystemExit("Person-specific projection delivery hash mismatch")
    projection = json.loads(raw)
    if projection.get("destination_repository") != destination["repository"]:
        raise SystemExit("Person-specific projection destination mismatch")
    if projection.get("projection_status") != "reviewed-ledger-projection":
        raise SystemExit("Person-specific projection status is not reviewed")
    authority = projection.get("authority") or {}
    if authority.get("reviewed_only") is not True:
        raise SystemExit("Person-specific projection is not reviewed-only")
    for key in (
        "may_include_candidates",
        "may_change_native_source_records",
        "may_change_destination_verification_labels",
        "may_establish_culpability",
        "may_claim_delivery",
        "may_claim_acknowledgment",
    ):
        if authority.get(key) is not False:
            raise SystemExit(f"Person-specific projection authority violation: {key}")
    for entry in projection.get("entries", []):
        if entry.get("review_status") != "reviewed":
            raise SystemExit("Non-reviewed entry leaked into person-specific projection")
        if not str(entry.get("receipt_path", "")).startswith("ledger_receipts/reviewed/"):
            raise SystemExit("Person-specific projection entry is outside reviewed receipts")


def main():
    validate("schemas/publication-index.schema.json", "publication/compendium.json")
    validate("schemas/cross-repository-delivery.schema.json", "delivery_manifests/generated.json")
    publication = load("publication/compendium.json")
    delivery = load("delivery_manifests/generated.json")
    reviewed = {
        str(path.relative_to(ROOT)) for path in (ROOT / "ledger_receipts" / "reviewed").glob("*.md")
    }
    published = {entry["receipt_path"] for entry in publication["entries"]}
    if published != reviewed:
        raise SystemExit("Compendium must include all and only reviewed receipts")
    forbidden = (
        "discovery_candidates/",
        "variance_candidates/",
        "promotion_candidates/",
        "review_assignments/",
    )
    if any(
        any(entry["receipt_path"].startswith(prefix) for prefix in forbidden)
        for entry in publication["entries"]
    ):
        raise SystemExit("Candidate material leaked into publication")
    data = (ROOT / "publication" / "compendium.json").read_bytes()
    if delivery["source_publication"]["sha256"] != hashlib.sha256(data).hexdigest():
        raise SystemExit("Delivery hash mismatch")
    if any(
        item["delivery_status"] != "prepared" or item["acknowledgment"] is not None
        for item in delivery["destinations"]
    ):
        raise SystemExit("Automation may only prepare unacknowledged deliveries")
    for destination in delivery["destinations"]:
        if destination["delivery_scope"] == "explicitly-related-reviewed-records-only":
            validate_person_projection(destination)
    print("Validated reviewed-only compendium, person-specific projections, and delivery authority boundaries")


if __name__ == "__main__":
    main()
