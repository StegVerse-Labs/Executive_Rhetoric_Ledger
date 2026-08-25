# Longitudinal Crypto Market Research Mirror Handoff

## Authority

Scoped continuity source for ERL longitudinal market research and downstream trade-preference evidence. Repository-wide ERL authority remains `ERL_MIRROR_HANDOFF.md`. Canonical coordination issue: `#77`.

## Goal

Build a longitudinal, provenance-preserving research layer that continuously curates market, macro, policy, liquidity, derivatives, on-chain, flow and event evidence; normalizes those observations into reproducible market-state vectors; finds historical analogue states; measures their realized forward outcomes; and emits bounded trade-preference evidence that downstream consumers may use when comparing one candidate trade against another or against `FOREGO`.

## Non-authority boundary

ERL is research/evidence authority only.

- historical resemblance != deterministic forecast
- correlation != causation
- stronger evidence != guaranteed outcome
- trade preference != order authorization
- ERL evidence must not bypass strategy, risk, capital, or TV/TVC execution gates

Every downstream packet must preserve `research_authority=ERL`, `execution_authority=NONE`, and `may_authorize_order=false`.

## Implemented core object model

1. `market_observation` — source-grounded event/data-family observation: `schemas/market-observation.schema.json`.
2. `market_state_vector` — normalized point-in-time cross-domain condition vector: `schemas/market-state-vector.schema.json`.
3. `historical_analogue` set — deterministic similarity link from current state to prior states: `scripts/find_historical_market_analogues.py`.
4. `forward_outcome` panel — realized post-state results at fixed horizons: `scripts/label_market_forward_outcomes.py`.
5. `trade_preference_evidence` — comparison of candidate trades or trade vs `FOREGO`, retaining favorable and disconfirming evidence separately: `schemas/trade-preference-evidence.schema.json` + `scripts/build_trade_preference_evidence.py`.
6. `source_coverage` — source freshness/completeness/missingness is mandatory inside state and preference evidence.
7. Source-family registry: `research-data/longitudinal-market-source-registry.v1.json`.
8. Deterministic validation: `scripts/validate_longitudinal_market_evidence.py` plus dedicated tests/workflow.

## Current source adapters

### Canonical ERL daily crypto panel — INSTALLED / OBSERVED

`scripts/index_existing_crypto_market_panel.py` converts `research-data/2026-08-13_2026-08-21_crypto_market_panel.coingecko.utc.json` into nine UTC-aligned longitudinal state rows without changing source provenance.

Derived features are deliberately narrow: per-asset 1-day returns, cross-asset positive breadth, XRP/XLM relative-price ratio, XRP/XLM ratio change, and retained spot prices for later forward-outcome labeling.

The legacy panel is assigned `source_coverage.coverage_score=0.25`, because it covers only a daily spot/relative-price family. It explicitly marks derivatives, order-book liquidity, stablecoin flows, ETF/fund flows, on-chain flows, macro cross-market context, and event context as missing.

### Crypto system-shock event context — INSTALLED / OBSERVED

`scripts/index_crypto_system_shock_event.py` normalizes `research-data/2026-08-22_crypto_system_shock_transaction_reconstruction.v1.json` into `stegverse.erl.market_observation.v1` while preserving the event center near `2026-08-22T05:11:20Z`, synchronized-cliff observation, displayed XRP-vs-control amplitude ratios, source limitations, all six competing causal hypotheses, and unresolved status.

The adapter explicitly does not promote `spot_led`, `derivatives_led`, whale attribution, or an XRP-specific amplifier into facts. `finding_authorized=false` remains preserved.

Hosted run `32893864586` completed SUCCESS with 11 deterministic tests. Event normalization and schema validation passed, and the full existing daily-panel -> analogue -> outcome -> preference pipeline remained green. Artifact `9580447450` retained seven JSON evidence files with digest `sha256:ae18bef654deb35396b1bd28700d1f5d934d09a4dec01f3e32213b7fe3bfed56`.

### Source-family registry — INSTALLED

`research-data/longitudinal-market-source-registry.v1.json` now records admitted sources and missing source families independently. Current posture:

- spot market: PARTIAL;
- event context: PARTIAL;
- on-chain flows: PARTIAL_RESEARCH_ONLY;
- derivatives: MISSING;
- order-book liquidity: MISSING;
- stablecoin flows: MISSING;
- ETF/fund flows: MISSING;
- macro cross-market: MISSING.

A valid source in one family never implies coverage of another. Missing or stale families lower confidence; silent imputation is forbidden.

## Analogue method — BASELINE V1 COMPLETE

`weighted_normalized_l1_with_missingness_penalty.v1` operates only on retained numeric state features, penalizes missing dimensions instead of silently imputing them, exposes matched/materially-different/missing dimensions, uses deterministic corpus-local scales and optional explicit weights, preserves digests, and sorts deterministically.

This is a reproducible baseline distance function, not a claim that current weighting is economically optimal. Later calibration must compare alternative similarity methods out of sample.

## Trade-preference interface — BASELINE V1 COMPLETE

ERL can emit a bounded comparison against alternatives, including `FOREGO`, containing candidate instrument/side, current-state digest, analogue similarity evidence, candidate/comparison forward-return distributions, favorable evidence, disconfirming evidence, source coverage/staleness, confidence, and a research-only classification: `PREFER`, `NEUTRAL`, `DEFER`, `FOREGO`, or `INSUFFICIENT_EVIDENCE`.

The baseline builder fails closed when source coverage or analogue sample size is insufficient. This class cannot authorize capital or execution.

## Observed validation evidence

Dedicated workflow: `.github/workflows/validate-longitudinal-market-research.yml`.

Run `32893379964` first demonstrated the retained full pipeline. Artifact `9580268876`, digest `sha256:f5bb9ff4f7318b0f838e71fdb210e48cbec2b2e0d851fec78474d873024bf08b`.

Run `32893544680` replaced interim optimistic coverage with measured `0.25` source coverage and completed SUCCESS. Artifact `9580330248`, digest `sha256:48e313bf0c718a0d61de6d59d396b388dd0266d9b5178098d72fb7fccd935a58`.

Run `32893864586` added governed system-shock event observation ingestion and completed SUCCESS. Artifact `9580447450`, digest `sha256:ae18bef654deb35396b1bd28700d1f5d934d09a4dec01f3e32213b7fe3bfed56`.

The observed XRP comparison packet remains `INSUFFICIENT_EVIDENCE`, confidence `0.10`: the corpus contains only nine daily states, at most eight historical analogues versus the configured minimum of ten, and broad source coverage remains only `0.25`. This is the intended fail-closed result.

## Initial feature families still to ingest

### Crypto market structure
Higher-frequency spot returns/acceleration, volume/volume expansion, broader breadth/dispersion/synchronization, pair-relative strength/leadership, and spread/depth/liquidity.

### Derivatives
Funding, futures basis, open interest, liquidation direction/intensity, and options IV/skew/term structure where available.

### Capital/flow
Spot ETF/fund flows, stablecoin supply/exchange flows, large exchange inflow/outflow observations, and on-chain large transfers/bridge/network activity when meaningful.

### Cross-market/macro
Treasury yields/rates, DXY, equities/volatility, gold, commodities, oil/energy, and broad liquidity/financial-conditions measures.

### Events
Regulation/policy/legal actions, central-bank/Treasury announcements, geopolitical/energy/shipping events, protocol upgrades/outages/exploits, token unlocks/governance/treasury actions, institutional adoption/de-adoption events, and timestamped news with source quality and age/decay.

## Longitudinal comparison requirements

Current conditions must never be represented by a single regime label alone. Analogue search must preserve dimensions used, weights/version, similarity score, unavailable dimensions, materially different dimensions, event-context match/mismatch, sample count, horizon-specific realized outcomes, and uncertainty/result sensitivity. No best analogue may be presented without its largest material differences.

## Crypto-bot integration boundary

Downstream issue: `StegVerse-Labs/crypto-bot#15`.

crypto-bot may eventually consume a versioned ERL evidence packet only after validating schema, freshness, digest, source coverage and non-authority fields. It must remain fail-closed for missing, stale, malformed, contradictory, or authority-bearing ERL evidence.

No crypto-bot consumer source is claimed complete yet. ERL corpus breadth and out-of-sample evidence should improve before research preference is permitted to influence live candidate ranking.

## Current build sequence

Completed:

1. Architecture/goal definition and Issue `#77`.
2. Scoped handoff.
3. Market-observation, state-vector, and trade-preference schemas.
4. Deterministic validator.
5. Baseline historical analogue engine.
6. Forward-outcome labeler.
7. Baseline trade-vs-trade / trade-vs-FOREGO evidence builder.
8. Existing ERL daily crypto panel indexer.
9. Existing system-shock event observation adapter.
10. Source-family registry.
11. Observed retained end-to-end fail-closed pipeline.

Next:

12. Expand historical market ingestion beyond nine daily states and below daily resolution.
13. Normalize additional existing ERL event records into the event-context family.
14. Add source-family adapters for derivatives/liquidity/flows/macro/on-chain evidence.
15. Add dynamic source-health/freshness calculations.
16. Calibrate analogue weighting/similarity and preference rules out of sample.
17. Add crypto-bot #15 consumer validation and evidence-only ranking hook.
18. Demonstrate retained ERL -> crypto-bot historical replay before any strategy influence.

## Completion state

- architecture/goal definition: COMPLETE
- canonical issue: COMPLETE (`#77`)
- scoped handoff: COMPLETE
- core schemas: BASELINE V1 COMPLETE
- validators: BASELINE V1 COMPLETE / HOSTED PASS
- canonical daily-panel indexer: COMPLETE / HOSTED PASS
- market-observation/event adapter: BASELINE V1 COMPLETE / HOSTED PASS
- source-family registry: COMPLETE V1
- analogue engine: BASELINE V1 COMPLETE / HOSTED PASS
- forward-outcome labeling: BASELINE V1 COMPLETE / HOSTED PASS
- trade-preference evidence builder: BASELINE V1 COMPLETE / HOSTED PASS
- first retained real-data ERL pipeline: COMPLETE / FAIL-CLOSED AS DESIGNED
- broad longitudinal panel ingestion: PARTIAL
- event-context ingestion breadth: PARTIAL
- derivatives/liquidity/flow/macro/on-chain ingestion: PENDING/PARTIAL AS REGISTRY STATES
- crypto-bot consumer: PENDING
- out-of-sample calibration: PENDING
- strategy influence authorization: NOT CLAIMED
- execution authority: NONE

## Archive note

This handoff is sufficient to continue the bounded market-research lane without reconstructing this conversation. The lane remains active: data breadth, event/context enrichment, out-of-sample calibration and crypto-bot consumption are not complete, and no strategy or execution activation is authorized.