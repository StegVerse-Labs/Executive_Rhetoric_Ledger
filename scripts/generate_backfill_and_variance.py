#!/usr/bin/env python3
"""Generate deterministic historical-backfill tasks and contradiction/correction candidates."""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def load(p: Path): return json.loads(p.read_text(encoding="utf-8"))
def hid(prefix: str, *parts: str) -> str:
    return prefix + hashlib.sha256("|".join(parts).encode()).hexdigest()[:20].upper()

def main() -> None:
    ap=argparse.ArgumentParser(); ap.add_argument("--generated-at", required=True); args=ap.parse_args()
    graph_path=ROOT/"adjacency_graphs/generated.json"
    graph=load(graph_path) if graph_path.exists() else {"nodes":[],"edges":[]}
    tasks=[]
    linked={e["source"] for e in graph.get("edges",[])}|{e["target"] for e in graph.get("edges",[])}
    for node in sorted(graph.get("nodes",[]), key=lambda n:n["node_id"]):
        if node["node_type"] in {"candidate","topic"} and node["node_id"] not in linked:
            tasks.append({"task_id":hid("BACKFILL-",node["node_id"],"graph-gap"),"priority":"high","reason":"graph-gap","query":f"Find historical records, controls, corrections, and outcomes related to {node['label']}","source_classes":["primary-legal-record","official-government","court-record","legislative-oversight","historical-archive"],"related_node_ids":[node["node_id"]],"status":"planned","review_required":True})
    for node in sorted(graph.get("nodes",[]), key=lambda n:n["node_id"]):
        if node["node_type"]=="topic":
            tasks.append({"task_id":hid("BACKFILL-",node["node_id"],"missing-control"),"priority":"medium","reason":"missing-control","query":f"Find historical oversight, judicial, statutory, and policy controls for {node['label']}","source_classes":["primary-legal-record","court-record","legislative-oversight","historical-archive"],"related_node_ids":[node["node_id"]],"status":"planned","review_required":True})
    tasks={t["task_id"]:t for t in tasks}
    queue={"queue_id":hid("QUEUE-",args.generated_at,*sorted(tasks)),"generated_at":args.generated_at,"status":"planned","tasks":[tasks[k] for k in sorted(tasks)],"authority_boundary":{"automation_may_queue":True,"automation_may_close_evidentiary_gap":False}}
    out=ROOT/"backfill_queues/generated.json"; out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(queue,indent=2,sort_keys=True)+"\n")

    candidates=[]
    paths=sorted((ROOT/"discovery_candidates").glob("**/CAND-*.json"))
    records=[]
    for p in paths:
        c=load(p); payload=c.get("normalized_payload") or {}; text=json.dumps(payload,sort_keys=True); observed=c.get("captured_at") or c.get("generated_at") or args.generated_at
        records.append((c["candidate_id"],observed,c.get("source_class","unknown"),hashlib.sha256(text.encode()).hexdigest(),str(payload.get("title") or payload.get("fixture_id") or "").lower()))
    for i,a in enumerate(records):
        for b in records[i+1:]:
            if not a[4] or a[4]!=b[4] or a[3]==b[3]: continue
            earlier,later=sorted([a,b],key=lambda r:(r[1],r[0]))
            candidates.append({"candidate_id":hid("VAR-",earlier[0],later[0]),"generated_at":args.generated_at,"posture":"unresolved-variance","earlier_record":{"record_id":earlier[0],"observed_at":earlier[1],"source_posture":earlier[2],"statement_hash":earlier[3]},"later_record":{"record_id":later[0],"observed_at":later[1],"source_posture":later[2],"statement_hash":later[3]},"comparison_basis":["same-topic"],"temporal_order":"earlier-before-later","status":"review-required","authority_boundary":{"automation_may_flag_variance":True,"automation_may_declare_falsehood":False,"automation_may_resolve_contradiction":False}})
    vout=ROOT/"variance_candidates/generated.json"; vout.parent.mkdir(parents=True,exist_ok=True); vout.write_text(json.dumps({"generated_at":args.generated_at,"candidates":sorted(candidates,key=lambda x:x["candidate_id"])},indent=2,sort_keys=True)+"\n")
    print(out.relative_to(ROOT)); print(vout.relative_to(ROOT))
if __name__=="__main__": main()
