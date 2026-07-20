#!/usr/bin/env python3
"""Validate deterministic review routing and non-self-promotion boundaries."""
from __future__ import annotations
import json
from pathlib import Path
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[1]
def load(path): return json.loads(path.read_text(encoding="utf-8"))
def validate_items(schema_name, doc_path, key):
    schema=load(ROOT/"schemas"/schema_name); doc=load(ROOT/doc_path); validator=Draft202012Validator(schema)
    ids=set()
    for item in doc.get(key,[]):
        errors=list(validator.iter_errors(item))
        if errors: raise SystemExit(f"{doc_path}: {errors[0].message}")
        ident=item.get("assignment_id") or item.get("receipt_id")
        if ident in ids: raise SystemExit(f"duplicate identifier: {ident}")
        ids.add(ident)
    return doc.get(key,[])
def main():
    assignments=validate_items("review-assignment.schema.json",Path("review_assignments/generated.json"),"assignments")
    receipts=validate_items("promotion-candidate-receipt.schema.json",Path("promotion_candidates/generated.json"),"receipts")
    assignment_ids={x["assignment_id"] for x in assignments}
    for a in assignments:
        auth=a["automation_authority"]
        if auth["may_approve"] or auth["may_reject"] or auth["may_promote"]: raise SystemExit("automation authority escalation")
        if a["risk_level"]=="critical" and a["quorum"]<2: raise SystemExit("critical review requires quorum >= 2")
    for r in receipts:
        if r["decision_state"]!="awaiting-review" or r["promotion_state"]!="not-authorized": raise SystemExit("generated receipt cannot contain a decision or promotion")
        if r["automation_authority"]["may_record_decision"] or r["automation_authority"]["may_promote"]: raise SystemExit("promotion authority escalation")
        ref=r["review_assignment_ref"].split("#")[-1]
        if ref not in assignment_ids: raise SystemExit(f"missing review assignment: {ref}")
    print(f"Validated {len(assignments)} assignments and {len(receipts)} promotion candidates.")
if __name__=="__main__": main()
