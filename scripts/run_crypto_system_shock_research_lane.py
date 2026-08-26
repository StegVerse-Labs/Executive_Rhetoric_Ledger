#!/usr/bin/env python3
"""Credential-free ERL public-market research lane.

Fetches public spot candles from multiple venues, preserves source failure as evidence,
normalizes historical/rolling windows, and emits research-only receipts.
It cannot authorize orders or promote causal findings.
"""
from __future__ import annotations
import argparse, datetime as dt, hashlib, json, math, pathlib, time, urllib.parse, urllib.request
from typing import Any

UA = "StegVerse-ERL-PublicResearch/1.0"
TIMEOUT = 20

def utc_epoch(s: str) -> int:
    return int(dt.datetime.fromisoformat(s.replace("Z","+00:00")).timestamp())

def now_utc() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)

def fetch_json(url: str) -> Any:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return json.loads(r.read().decode("utf-8"))

def candle(ts, o, h, l, c, v):
    return {"ts": int(ts), "open": float(o), "high": float(h), "low": float(l), "close": float(c), "volume": float(v)}

def get_coinbase(pair: str, start: int, end: int):
    qs=urllib.parse.urlencode({"granularity":60,"start":dt.datetime.fromtimestamp(start,dt.timezone.utc).isoformat(),"end":dt.datetime.fromtimestamp(end,dt.timezone.utc).isoformat()})
    data=fetch_json(f"https://api.exchange.coinbase.com/products/{pair}/candles?{qs}")
    return sorted([candle(x[0],x[3],x[2],x[1],x[4],x[5]) for x in data],key=lambda x:x["ts"])

def get_kraken(pair: str, start: int, end: int):
    data=fetch_json(f"https://api.kraken.com/0/public/OHLC?pair={urllib.parse.quote(pair)}&interval=1&since={start}")
    if data.get("error"): raise RuntimeError(str(data["error"]))
    key=next(k for k in data["result"] if k!="last")
    rows=[candle(x[0],x[1],x[2],x[3],x[4],x[6]) for x in data["result"][key] if start <= int(x[0]) <= end]
    return sorted(rows,key=lambda x:x["ts"])

def get_bitstamp(pair: str, start: int, end: int):
    qs=urllib.parse.urlencode({"step":60,"limit":1000,"start":start,"end":end})
    data=fetch_json(f"https://www.bitstamp.net/api/v2/ohlc/{pair}/?{qs}")
    rows=data["data"]["ohlc"]
    return sorted([candle(x["timestamp"],x["open"],x["high"],x["low"],x["close"],x["volume"]) for x in rows],key=lambda x:x["ts"])

def get_okx(pair: str, start: int, end: int):
    # OKX timestamps are milliseconds. history-candles accepts a bounded request;
    # filter locally because pagination semantics can vary across API revisions.
    qs=urllib.parse.urlencode({"instId":pair,"bar":"1m","after":end*1000,"before":start*1000,"limit":300})
    data=fetch_json(f"https://www.okx.com/api/v5/market/history-candles?{qs}")
    if str(data.get("code","0"))!="0": raise RuntimeError(str(data))
    rows=[]
    for x in data.get("data",[]):
        ts=int(x[0])//1000
        if start <= ts <= end:
            rows.append(candle(ts,x[1],x[2],x[3],x[4],x[5]))
    return sorted(rows,key=lambda x:x["ts"])

def get_binance(pair: str, start: int, end: int):
    qs=urllib.parse.urlencode({"symbol":pair,"interval":"1m","startTime":start*1000,"endTime":end*1000,"limit":1000})
    data=fetch_json(f"https://api.binance.com/api/v3/klines?{qs}")
    return sorted([candle(int(x[0])//1000,x[1],x[2],x[3],x[4],x[5]) for x in data],key=lambda x:x["ts"])

FETCHERS={"coinbase":get_coinbase,"kraken":get_kraken,"bitstamp":get_bitstamp,"okx":get_okx,"binance":get_binance}

def digest(obj: Any) -> str:
    b=json.dumps(obj,sort_keys=True,separators=(",",":")).encode()
    return "sha256:"+hashlib.sha256(b).hexdigest()

def summarize(rows):
    if not rows: return {"count":0}
    high=max(x["high"] for x in rows); low=min(x["low"] for x in rows)
    first=rows[0]["open"]; last=rows[-1]["close"]; vol=sum(x["volume"] for x in rows)
    return {"count":len(rows),"high":high,"low":low,"open":first,"close":last,"return_pct":((last/first)-1)*100 if first else None,"high_to_low_pct":((low/high)-1)*100 if high else None,"volume":vol}

def collect(config, start, end, rolling=False):
    out=[]
    for src in config["venue_sources"]:
        venue=src["id"]; fetcher=FETCHERS.get(venue)
        for pair in src["pairs"]:
            record={"venue":venue,"pair":pair,"start_utc":dt.datetime.fromtimestamp(start,dt.timezone.utc).isoformat().replace("+00:00","Z"),"end_utc":dt.datetime.fromtimestamp(end,dt.timezone.utc).isoformat().replace("+00:00","Z")}
            try:
                rows=fetcher(pair,start,end)
                record.update({"status":"OK" if rows else "NO_ROWS","rows":rows,"summary":summarize(rows)})
                record["digest"]=digest(rows)
            except Exception as e:
                record.update({"status":"SOURCE_ERROR","error_type":type(e).__name__,"error":str(e)[:500],"rows":[],"summary":{"count":0}})
            out.append(record)
    return out

def asset_name(pair):
    for a in ("BTC","XBT","ETH","XRP","XLM","SOL","ATOM"):
        if pair.startswith(a): return "BTC" if a=="XBT" else a
    return pair

def rolling_flags(records, thresholds):
    by_asset={}
    for r in records:
        if r["status"]!="OK" or not r["rows"]: continue
        rows=r["rows"]
        cutoff=rows[-1]["ts"]-5*60
        recent=[x for x in rows if x["ts"]>=cutoff]
        if len(recent)<2: continue
        start=recent[0]["open"]; end=recent[-1]["close"]
        ret=((end/start)-1)*100 if start else 0
        by_asset.setdefault(asset_name(r["pair"]),[]).append(ret)
    med={}
    for a,vals in by_asset.items():
        vals=sorted(vals); med[a]=vals[len(vals)//2]
    triggered=[]
    for a,r in med.items():
        t=thresholds.get(a.lower()+"_5m_abs_return_pct")
        if t is None:
            t=thresholds.get("xrp_5m_abs_return_pct",5.0)
        if abs(r)>=float(t): triggered.append({"asset":a,"median_venue_5m_return_pct":r,"threshold_pct":t})
    return {"asset_median_5m_returns_pct":med,"triggered_assets":triggered,"cross_asset_shock_candidate":len(triggered)>=int(thresholds["cross_asset_min_count"])}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--config",default="config/crypto-system-shock-research-lane.v1.json")
    ap.add_argument("--out-dir",default="reports/crypto-system-shock")
    ap.add_argument("--as-of")
    args=ap.parse_args()
    config=json.load(open(args.config))
    outdir=pathlib.Path(args.out_dir); outdir.mkdir(parents=True,exist_ok=True)
    asof=dt.datetime.fromisoformat(args.as_of.replace("Z","+00:00")) if args.as_of else now_utc()
    hist=config["scopes"]["historical_forensic_windows"][0]
    hs,he=utc_epoch(hist["start_utc"]),utc_epoch(hist["end_utc"])
    historical=collect(config,hs,he)
    (outdir/"2026-08-22-venue-window.json").write_text(json.dumps({"lane_id":config["lane_id"],"window":hist,"source_results":historical,"research_authority":"ERL","execution_authority":"NONE","may_authorize_order":False},indent=2,sort_keys=True)+"\n")
    lookback=int(config["scopes"]["rolling_watch"]["lookback_minutes"])
    re=int(asof.timestamp()); rs=re-lookback*60
    rolling=collect(config,rs,re,rolling=True)
    flags=rolling_flags(rolling,config["scopes"]["rolling_watch"]["shock_thresholds"])
    receipt={
      "schema":"stegverse.erl.crypto_system_shock_research_receipt.v1",
      "lane_id":config["lane_id"],
      "as_of_utc":asof.astimezone(dt.timezone.utc).isoformat().replace("+00:00","Z"),
      "historical_window_digest":digest(historical),
      "historical_source_status":[{"venue":r["venue"],"pair":r["pair"],"status":r["status"],"count":r["summary"]["count"]} for r in historical],
      "rolling_source_status":[{"venue":r["venue"],"pair":r["pair"],"status":r["status"],"count":r["summary"]["count"]} for r in rolling],
      "rolling_watch":flags,
      "source_failures_are_missing_evidence":True,
      "causal_finding_authorized":False,
      "research_authority":"ERL",
      "execution_authority":"NONE",
      "may_authorize_order":False
    }
    (outdir/"latest-research-receipt.json").write_text(json.dumps(receipt,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"status":"PASS","lane_id":config["lane_id"],"historical_ok":sum(r["status"]=="OK" for r in historical),"historical_total":len(historical),"rolling_ok":sum(r["status"]=="OK" for r in rolling),"rolling_total":len(rolling),"shock_candidate":flags["cross_asset_shock_candidate"],"execution_authority":"NONE"},sort_keys=True))

if __name__=="__main__":
    main()
