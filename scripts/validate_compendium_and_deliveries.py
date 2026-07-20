#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json
from pathlib import Path
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[1]
def load(p): return json.loads((ROOT/p).read_text())
def validate(schema_path, doc_path):
    errors=list(Draft202012Validator(load(schema_path)).iter_errors(load(doc_path)))
    if errors: raise SystemExit(f"{doc_path} failed schema validation: {errors[0].message}")
def main():
    validate("schemas/publication-index.schema.json","publication/compendium.json")
    validate("schemas/cross-repository-delivery.schema.json","delivery_manifests/generated.json")
    pub=load("publication/compendium.json"); delivery=load("delivery_manifests/generated.json")
    reviewed={str(p.relative_to(ROOT)) for p in (ROOT/"ledger_receipts/reviewed").glob("*.md")}
    published={e["receipt_path"] for e in pub["entries"]}
    if published != reviewed: raise SystemExit("Compendium must include all and only reviewed receipts")
    forbidden=("discovery_candidates/","variance_candidates/","promotion_candidates/","review_assignments/")
    if any(any(e["receipt_path"].startswith(x) for x in forbidden) for e in pub["entries"]): raise SystemExit("Candidate material leaked into publication")
    data=(ROOT/"publication/compendium.json").read_bytes()
    if delivery["source_publication"]["sha256"] != hashlib.sha256(data).hexdigest(): raise SystemExit("Delivery hash mismatch")
    if any(d["delivery_status"]!="prepared" or d["acknowledgment"] is not None for d in delivery["destinations"]): raise SystemExit("Automation may only prepare unacknowledged deliveries")
    print("Validated reviewed-only compendium and delivery authority boundaries")
if __name__=="__main__": main()
