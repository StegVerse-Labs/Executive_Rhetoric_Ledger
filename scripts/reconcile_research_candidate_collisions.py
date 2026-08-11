#!/usr/bin/env python3
"""Reconcile cross-repository research candidate identity without erasing provenance."""
from __future__ import annotations
import argparse,hashlib,json,pathlib
from urllib.parse import urlsplit,urlunsplit

def fail(message):raise SystemExit("FAIL: "+message)
def normalize_url(url):
    parsed=urlsplit(url);host=(parsed.hostname or "").lower();port=parsed.port
    netloc=host+(f":{port}" if port and not ((parsed.scheme=="http" and port==80) or (parsed.scheme=="https" and port==443)) else "")
    return urlunsplit((parsed.scheme.lower(),netloc,parsed.path or "/",parsed.query,""))
def read(paths):
    rows=[]
    for path in paths:
        for n,line in enumerate(pathlib.Path(path).read_text(encoding="utf-8").splitlines(),1):
            if not line.strip():continue
            try:rows.append(json.loads(line))
            except Exception as exc:fail(f"{path}:{n}: {exc}")
    return rows
def identity(candidate):
    digest=candidate.get("content_sha256")
    if digest:return "sha256:"+digest.lower()
    url=candidate.get("source_url")
    if not url:fail("candidate missing source_url")
    return "url:"+hashlib.sha256(normalize_url(url).encode()).hexdigest()
def main():
    parser=argparse.ArgumentParser();parser.add_argument("inputs",nargs="+");parser.add_argument("--output",required=True);args=parser.parse_args();rows=read(args.inputs);groups={}
    for candidate in rows:
        if candidate.get("evidence_role") not in {"lead-only","context-only"}:fail("authority posture violation")
        if candidate.get("evaluation_changed") is not False:fail("evaluation change violation")
        groups.setdefault(identity(candidate),[]).append(candidate)
    output=[]
    for ident,items in sorted(groups.items()):
        repositories=sorted({item.get("repository") for item in items})
        output.append({"identity":ident,"candidate_ids":[item.get("candidate_id") for item in items],"repositories":repositories,"candidate_count":len(items),"collision":len(items)>1,"provenance_preserved":True,"deduplication_effect":"identity-linked-not-deleted","authority_effect":"NONE"})
    pathlib.Path(args.output).write_text(json.dumps({"schema":"stegverse.erl.candidate_collision_registry.v1","groups":output},indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({"status":"PASS","candidates":len(rows),"identity_groups":len(output),"collisions":sum(1 for group in output if group["collision"]),"provenance_preserved":True},sort_keys=True))
    return 0
if __name__=="__main__":raise SystemExit(main())
