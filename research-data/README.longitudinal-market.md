# ERL Longitudinal Market Research Data

This directory contains source-grounded research inputs that may be indexed into the longitudinal market research layer governed by `docs/LONGITUDINAL_CRYPTO_MARKET_RESEARCH_MIRROR_HANDOFF.md` and Issue #77.

## Governing rules

- Preserve source provenance and original timestamp semantics.
- Do not infer coverage of one source family from another.
- Missing and stale source families remain explicit.
- Event hypotheses remain hypotheses until their source-specific release conditions are satisfied.
- Forward outcomes are labels applied after a historical state; they must never leak into the state vector used to retrieve that historical analogue.
- Current-state similarity is evidence, not a deterministic forecast.
- Trade preference is a bounded research result, not capital or execution authority.

All normalized downstream objects must preserve `research_authority=ERL`, `execution_authority=NONE`, and `may_authorize_order=false`.

## Current admitted source families

See `longitudinal-market-source-registry.v1.json` for the machine-readable source-family state. Current coverage is intentionally incomplete. Daily spot/relative-price evidence and a first governed event-context adapter are installed; derivatives, order-book liquidity, broad macro, ETF/fund flows and stablecoin-flow families still require admitted sources and adapters.
