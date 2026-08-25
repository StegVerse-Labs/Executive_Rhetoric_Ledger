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

Every downstream packet must preserve:

- `research_authority=ERL`
- `execution_authority=NONE`
- `may_authorize_order=false`

## Implemented core object model

1. `market_state_vector` — normalized point-in-time cross-domain condition vector: `schemas/market-state-vector.schema.json`.
2. `historical_analogue` set — deterministic similarity link from current state to prior states: `scripts/find_historical_market_analogues.py`.
3. `forward_outcome` panel — realized post-state results at fixed horizons: `scripts/label_market_forward_outcomes.py`.
4. `trade_preference_evidence` — comparison of candidate trades or trade vs `FOREGO`, retaining favorable and disconfirming evidence separately: `schemas/trade-preference-evidence.schema.json` + `scripts/build_trade_preference_evidence.py`.
5. `source_coverage` — source freshness/completeness/missingness is mandatory inside state and preference evidence.
6. Deterministic validation: `scripts/validate_longitudinal_market_evidence.py`.

A generalized raw `market_observation` source-family schema remains to be installed as ingestion breadth expands.

## Current source adapters

### Canonical ERL daily crypto panel — INSTALLED / OBSERVED

`scripts/index_existing_crypto_market_panel.py` converts `research-data/2026-08-13_2026-08-21_crypto_market_panel.coingecko.utc.json` into nine UTC-aligned longitudinal state rows without changing source provenance.

Current derived features are deliberately narrow:

- per-asset 1-day returns;
- cross-asset positive breadth;
- XRP/XLM relative-price ratio;
- XRP/XLM ratio change;
- retained spot prices for later forward-outcome labeling.

The legacy panel is assigned `source_coverage.coverage_score=0.25`, because it covers only a daily spot/relative-price family. It explicitly marks derivatives, order-book liquidity, stablecoin flows, ETF/fund flows, on-chain flows, macro cross-market context, and event context as missing. This prevents a valid source from being misrepresented as comprehensive market evidence.

### Crypto system-shock event object — NEXT ACTIVE INGESTION TARGET

Existing ERL record `research-data/2026-08-22_crypto_system_shock_transaction_reconstruction.v1.json` preserves a synchronized BTC/ETH/ATOM/XRP shock candidate centered near `2026-08-22T05:11:20Z`, multiple competing causal hypotheses, explicit evidence gaps, and required transaction-level discrimination. It is the first event-context object to be normalized into the longitudinal layer.

## Analogue method — BASELINE V1 COMPLETE

`weighted_normalized_l1_with_missingness_penalty.v1`:

- operates only on retained numeric state features;
- penalizes missing dimensions rather than silently imputing them;
- exposes matched dimensions, material differences, and missing dimensions;
- uses deterministic corpus-local scales and optional explicit weights;
- preserves current-state and analogue-set digests;
- sorts deterministically.

This is a reproducible baseline distance function, not a claim that the current weighting is economically optimal. Later calibration must compare alternative similarity methods out of sample.

## Trade-preference interface — BASELINE V1 COMPLETE

For each candidate opportunity, ERL can now emit a bounded comparison against alternatives, including `FOREGO`.

Current output includes:

- candidate instrument/pair and side;
- current market-state vector digest;
- analogue IDs and similarity evidence;
- candidate and comparison forward-return distributions;
- favorable evidence;
- disconfirming evidence;
- source coverage/staleness;
- confidence;
- research-only classification: `PREFER`, `NEUTRAL`, `DEFER`, `FOREGO`, or `INSUFFICIENT_EVIDENCE`.

The baseline builder fails closed when source coverage or analogue sample size is insufficient. The class is evidence preference only and cannot authorize capital or execution.

## Observed validation evidence

Dedicated workflow: `.github/workflows/validate-longitudinal-market-research.yml`.

### First retained full pipeline

Run `32893379964` completed SUCCESS and exercised:

`existing ERL source -> longitudinal state rows -> historical analogue retrieval -> forward-outcome labels -> XRP-vs-BTC/ETH/SOL/FOREGO preference packet -> schema/non-authority validation -> retained artifact`.

Artifact `9580268876` was retained with digest `sha256:f5bb9ff4f7318b0f838e71fdb210e48cbec2b2e0d851fec78474d873024bf08b`.

That first run used an interim manually supplied coverage score while the coverage model was being hardened.

### Current measured-coverage pipeline

Commit `635485b8d06f5617663e5a9911e3b15383d70d36` binds the observed preference packet to the indexed state's measured coverage instead of an optimistic placeholder.

Run `32893544680` completed SUCCESS across all 27 job steps:

- compile PASS;
- deterministic tests PASS;
- canonical ERL panel indexing PASS;
- current/history split PASS;
- historical analogue retrieval PASS;
- forward-outcome labeling PASS;
- XRP-vs-BTC/ETH/SOL/FOREGO packet build PASS;
- state and preference validation PASS;
- retained artifact upload PASS.

Artifact `9580330248` is retained with digest `sha256:48e313bf0c718a0d61de6d59d396b388dd0266d9b5178098d72fb7fccd935a58`.

The observed packet correctly remains `INSUFFICIENT_EVIDENCE`: the legacy corpus contains only nine daily states, at most eight historical analogues, versus a minimum sample requirement of ten, and the source-family coverage is only `0.25`. This is a successful fail-closed result, not a failed research pipeline.

## Initial feature families still to ingest

### Crypto market structure
- higher-frequency spot returns and acceleration;
- volume and volume expansion;
- broader breadth, dispersion and cross-asset synchronization;
- pair-relative strength and leadership;
- spread/depth/liquidity.

### Derivatives
- funding;
- futures basis;
- open interest;
- liquidation direction/intensity;
- options IV/skew/term structure where available.

### Capital/flow
- spot ETF/fund flows;
- stablecoin supply and exchange flows;
- large exchange inflow/outflow observations;
- on-chain large transfers, bridge/network flows and activity measures when meaningful.

### Cross-market/macro
- Treasury yields/rates;
- dollar index;
- equity indices and volatility;
- gold and major commodities;
- oil/energy conditions;
- broad liquidity/financial-conditions measures.

### Events
- regulation/policy/legal actions;
- central-bank/Treasury announcements;
- geopolitical/energy/shipping events;
- protocol upgrades/outages/exploits;
- token unlocks/governance/treasury actions;
- institutional adoption/de-adoption events;
- timestamped news with source quality and age/decay.

## Longitudinal comparison requirements

Current conditions must never be represented by a single regime label alone. Analogue search must preserve:

- dimensions used;
- weights/version;
- similarity score;
- unavailable dimensions;
- materially different dimensions;
- event-context match/mismatch;
- sample count;
- horizon-specific realized outcomes;
- uncertainty/result sensitivity.

No best historical analogue may be presented without preserving its largest material differences.

## Crypto-bot integration boundary

Downstream issue: `StegVerse-Labs/crypto-bot#15`.

`StegVerse-Labs/crypto-bot` may eventually consume a versioned ERL evidence packet only after validating schema, freshness, digest and non-authority fields. It must remain fail-closed for missing, stale, malformed, contradictory, or authority-bearing ERL evidence.

No crypto-bot consumer source is claimed complete yet. ERL corpus breadth and out-of-sample evidence should improve before research preference is permitted to influence live candidate ranking.

## Current build sequence

Completed:

1. Architecture/goal definition.
2. Canonical issue `#77`.
3. Scoped handoff.
4. State-vector and trade-preference schemas.
5. Deterministic validator.
6. Baseline historical analogue engine.
7. Forward-outcome labeler.
8. Baseline trade-vs-trade / trade-vs-FOREGO evidence builder.
9. Existing ERL daily crypto panel indexer.
10. Observed retained end-to-end fail-closed pipeline.

Next:

11. Normalize existing system-shock/event evidence into event context.
12. Expand historical market ingestion beyond nine daily states and below daily resolution.
13. Add source-family adapters for derivatives/liquidity/flows/macro/on-chain/event evidence.
14. Add source-health/freshness calculations rather than static family coverage alone.
15. Calibrate analogue weighting/similarity and preference rules out of sample.
16. Add crypto-bot #15 consumer validation and evidence-only ranking hook.
17. Demonstrate retained ERL->crypto-bot historical replay before any strategy influence.

## Completion state

- architecture/goal definition: COMPLETE
- canonical issue: COMPLETE (`#77`)
- scoped handoff: COMPLETE
- schemas: BASELINE V1 COMPLETE
- validators: BASELINE V1 COMPLETE / HOSTED PASS
- canonical daily-panel indexer: COMPLETE / HOSTED PASS
- analogue engine: BASELINE V1 COMPLETE / HOSTED PASS
- forward-outcome labeling: BASELINE V1 COMPLETE / HOSTED PASS
- trade-preference evidence builder: BASELINE V1 COMPLETE / HOSTED PASS
- first retained real-data ERL pipeline: COMPLETE / FAIL-CLOSED AS DESIGNED
- broad longitudinal panel ingestion: PARTIAL
- event-context ingestion: ACTIVE
- derivatives/liquidity/flow/macro/on-chain ingestion: PENDING
- crypto-bot consumer: PENDING
- out-of-sample calibration: PENDING
- strategy influence authorization: NOT CLAIMED
- execution authority: NONE

## Archive note

This handoff is sufficient to continue the bounded market-research lane without reconstructing this conversation. The lane remains active: data breadth, event/context enrichment, out-of-sample calibration and crypto-bot consumption are not complete, and no strategy or execution activation is authorized.