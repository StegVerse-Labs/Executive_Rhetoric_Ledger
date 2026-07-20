#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[1]

def load(p): return json.loads(p.read_text(encoding="utf-8"))
def validate(schema_path, document, label):
    errors=sorted(Draft202012Validator(load(schema_path)).iter_errors(document),key=lambda e:list(e.path))
    if errors:
        for e in errors: print(f"{label} {'.'.join(map(str,e.path)) or '<root>'}: {e.message}")
        raise SystemExit(1)

def main():
    queue_path=ROOT/"backfill_queues/generated.json"; variance_path=ROOT/"variance_candidates/generated.json"
    if not queue_path.exists() or not variance_path.exists(): raise SystemExit("Generate backfill and variance outputs first")
    queue=load(queue_path); validate(ROOT/"schemas/historical-backfill-queue.schema.json",queue,"queue")
    ids=[]
    for task in queue["tasks"]:
        ids.append(task["task_id"])
        if not task["review_required"]: raise SystemExit("Backfill task bypasses review")
    if len(ids)!=len(set(ids)): raise SystemExit("Duplicate backfill task IDs")
    wrapper=load(variance_path)
    for candidate in wrapper.get("candidates",[]):
        validate(ROOT/"schemas/contradiction-candidate.schema.json",candidate,"variance")
        if candidate["earlier_record"]["observed_at"]>candidate["later_record"]["observed_at"]: raise SystemExit("Temporal order reversed")
        boundary=candidate["authority_boundary"]
        if boundary["automation_may_declare_falsehood"] or boundary["automation_may_resolve_contradiction"]: raise SystemExit("Automation exceeds variance authority")
    print(f"Validated {len(queue['tasks'])} backfill tasks and {len(wrapper.get('candidates',[]))} variance candidates")
if __name__=="__main__": main()
