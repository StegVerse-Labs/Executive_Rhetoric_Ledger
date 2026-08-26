import importlib.util, json, pathlib, tempfile
spec=importlib.util.spec_from_file_location("lane","scripts/run_crypto_system_shock_research_lane.py")
lane=importlib.util.module_from_spec(spec); spec.loader.exec_module(lane)

def test_summary_and_digest_deterministic():
    rows=[
      {"ts":1,"open":100.0,"high":102.0,"low":99.0,"close":101.0,"volume":10.0},
      {"ts":2,"open":101.0,"high":103.0,"low":98.0,"close":99.0,"volume":12.0},
    ]
    s=lane.summarize(rows)
    assert s["high"]==103.0 and s["low"]==98.0 and s["volume"]==22.0
    assert lane.digest(rows)==lane.digest(json.loads(json.dumps(rows)))

def test_rolling_cross_asset_candidate():
    base=1000
    def rec(pair,ret):
        return {"status":"OK","pair":pair,"rows":[
          {"ts":base,"open":100.0,"high":100.0,"low":100.0,"close":100.0,"volume":1.0},
          {"ts":base+300,"open":100.0,"high":110.0,"low":90.0,"close":100.0*(1+ret/100),"volume":1.0}
        ]}
    records=[rec("BTC-USD",-3),rec("ETH-USD",-4),rec("XRP-USD",-7),rec("SOL-USD",-1)]
    thresholds={"btc_5m_abs_return_pct":2,"eth_5m_abs_return_pct":3,"xrp_5m_abs_return_pct":5,"cross_asset_min_count":3}
    f=lane.rolling_flags(records,thresholds)
    assert f["cross_asset_shock_candidate"] is True
    assert {x["asset"] for x in f["triggered_assets"]}=={"BTC","ETH","XRP"}

def test_non_authority_config():
    c=json.loads(pathlib.Path("config/crypto-system-shock-research-lane.v1.json").read_text())
    assert c["research_authority"]=="ERL"
    assert c["execution_authority"]=="NONE"
    assert c["may_authorize_order"] is False
