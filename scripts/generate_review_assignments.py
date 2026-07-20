#!/usr/bin/env python3
"""Generate deterministic review assignments and promotion candidates without deciding them."""
from __future__ import annotations
import hashlib, json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def load(path: Path): return json.loads(path.read_text(encoding="utf-8"))
def hid(prefix: str, value: str) -> str: return prefix + hashlib.sha256(value.encode()).hexdigest()[:20].upper()

def route(subject_type: str, payload: dict) -> tuple[str, str, list[str], int]:
    text = json.dumps(payload, sort_keys=True).lower()
    if subject_type == "variance": return "contradiction-review", "critical", ["evidence-reviewer", "legal-reviewer"], 2
    if any(term in text for term in ("civil-right", "constitutional", "use of force", "fatal")):
        return "civil-rights-high-risk", "critical", ["evidence-reviewer", "civil-rights-reviewer", "legal-reviewer"], 2
    if subject_type == "backfill": return "historical-control", "medium", ["historical-control-reviewer"], 1
    return "standard-ledger", "medium", ["evidence-reviewer"], 1

def collect():
    roots = [("candidate", "discovery_candidates/**/*.json"), ("variance", "contradiction_candidates/**/*.json"), ("backfill", "historical_backfill/**/*.json")]
    for stype, pattern in roots:
        for path in sorted(ROOT.glob(pattern)):
            data = load(path)
            sid = data.get("candidate_id") or data.get("variance_id") or data.get("task_id") or data.get("queue_id") or str(path.relative_to(ROOT))
            yield stype, sid, path, data

def main():
    assignments=[]; promotions=[]
    for stype, sid, path, data in collect():
        queue, risk, authorities, quorum = route(stype, data)
        aid = hid("REVIEW-", f"{stype}|{sid}|{queue}")
        refs = [str(path.relative_to(ROOT))]
        assignments.append({"assignment_id":aid,"subject_id":sid,"subject_type":stype,"queue":queue,"risk_level":risk,"required_authority":authorities,"quorum":quorum,"packet_refs":refs,"status":"review-required","decision_receipt_refs":[],"automation_authority":{"may_route":True,"may_approve":False,"may_reject":False,"may_promote":False}})
        proposed = "contradiction_record" if stype=="variance" else ("hold" if stype=="backfill" else "rhetoric_record")
        promotions.append({"receipt_id":hid("PROMO-", aid),"subject_id":sid,"proposed_class":proposed,"review_assignment_ref":f"review_assignments/generated.json#{aid}","evidence_refs":refs,"decision_state":"awaiting-review","decision_receipt_refs":[],"promotion_state":"not-authorized","automation_authority":{"may_prepare":True,"may_record_decision":False,"may_promote":False}})
    out1=ROOT/"review_assignments/generated.json"; out1.parent.mkdir(parents=True,exist_ok=True); out1.write_text(json.dumps({"assignments":assignments},indent=2,sort_keys=True)+"\n")
    out2=ROOT/"promotion_candidates/generated.json"; out2.parent.mkdir(parents=True,exist_ok=True); out2.write_text(json.dumps({"receipts":promotions},indent=2,sort_keys=True)+"\n")
    print(out1.relative_to(ROOT)); print(out2.relative_to(ROOT))
if __name__ == "__main__": main()
