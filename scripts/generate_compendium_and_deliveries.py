#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, html, json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
DESTINATIONS = [
    ("StegVerse-Labs/Site", "data/executive-rhetoric-ledger/compendium.json"),
    ("GCAT-BCAT-Engine/Publisher", "inputs/executive-rhetoric-ledger/compendium.json"),
    ("StegVerse-Labs/admissibility-wiki", "data/executive-rhetoric-ledger/compendium.json"),
    ("StegVerse-Labs/stegguardian-wiki", "data/executive-rhetoric-ledger/compendium.json"),
]
def sha(data: bytes) -> str: return hashlib.sha256(data).hexdigest()
def title_of(text: str, fallback: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "): return line[2:].strip()
    return fallback

def main() -> None:
    p=argparse.ArgumentParser(); p.add_argument("--generated-at", required=True); a=p.parse_args()
    entries=[]
    for path in sorted((ROOT/"ledger_receipts/reviewed").glob("*.md")):
        data=path.read_bytes(); text=data.decode("utf-8")
        entries.append({"entry_id":sha(str(path.relative_to(ROOT)).encode())[:20].upper(),"title":title_of(text,path.stem),"receipt_path":str(path.relative_to(ROOT)),"receipt_sha256":sha(data),"review_status":"reviewed","search_text":" ".join(text.split())[:12000]})
    pub={"publication_id":"COMPENDIUM-"+sha("|".join(e["receipt_sha256"] for e in entries).encode())[:20].upper(),"generated_at":a.generated_at,"publication_status":"reviewed-only-compendium","entries":entries,"authority":{"reviewed_only":True,"may_include_candidates":False,"may_promote":False}}
    out=ROOT/"publication"; out.mkdir(exist_ok=True)
    json_bytes=(json.dumps(pub,indent=2,sort_keys=True)+"\n").encode(); (out/"compendium.json").write_bytes(json_bytes)
    rows="".join(f"<article><h2>{html.escape(e['title'])}</h2><p><code>{html.escape(e['receipt_path'])}</code></p></article>" for e in entries)
    (out/"index.html").write_text("<!doctype html><html><head><meta charset='utf-8'><title>Executive Rhetoric Ledger</title></head><body><h1>Reviewed Receipt Compendium</h1>"+rows+"</body></html>\n",encoding="utf-8")
    delivery={"delivery_id":"DELIVERY-"+sha(json_bytes)[:20].upper(),"generated_at":a.generated_at,"source_publication":{"path":"publication/compendium.json","sha256":sha(json_bytes)},"destinations":[{"repository":r,"target_path":t,"delivery_status":"prepared","acknowledgment_required":True,"acknowledgment":None} for r,t in DESTINATIONS],"authority":{"may_prepare":True,"may_claim_delivery":False,"may_claim_acknowledgment":False}}
    d=ROOT/"delivery_manifests"; d.mkdir(exist_ok=True); (d/"generated.json").write_text(json.dumps(delivery,indent=2,sort_keys=True)+"\n",encoding="utf-8")
if __name__=="__main__": main()
