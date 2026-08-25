# Longitudinal Crypto Market Research Mirror Handoff

## Authority

Scoped continuity source for ERL longitudinal market research and downstream trade-preference evidence. Repository-wide ERL authority remains `ERL_MIRROR_HANDOFF.md`. Canonical coordination issue: `#77`.

## Goal

Build a longitudinal, provenance-preserving research layer that continuously curates market, macro, policy, liquidity, derivatives, on-chain, flow and event evidence; normalizes those observations into reproducible market-state vectors; finds historical analogue states; measures their realized forward outcomes; and emits bounded trade-preference evidence that downstream consumers may use when comparing one candidate trade against another or against `FOREGO`.

## Non-authority boundary

ERL is research/evidence authority only. Historical resemblance is not deterministic forecast, correlation is not causation, stronger evidence is not guaranteed outcome, and trade preference is not order authorization. Every downstream packet preserves `research_authority=ERL`, `execution_authority=NONE`, and `may_authorize_order=false`.

## Implemented core object model

1. `market_observation`: `schemas/market-observation.schema.json`.
2. `market_state_vector`: `schemas/market-state-vector.schema.json`.
3. Deterministic historical analogue retrieval: `scripts/find_historical_market_analogues.py`.
4. Realized forward outcomes: `scripts/label_market_forward_outcomes.py`.
5. `trade_preference_evidence`: `schemas/trade-preference-evidence.schema.json` and `scripts/build_trade_preference_evidence.py`.
6. Source-family registry: `research-data/longitudinal-market-source-registry.v1.json`.
7. Source-health policy: `research-data/longitudinal-market-source-health-policy.v1.json`.
8. Deterministic source-health receipts: `scripts/build_longitudinal_source_health.py`.
9. Deterministic validators/tests and hosted workflow: `.github/workflows/validate-longitudinal-market-research.yml`.

## Current source adapters

### Daily crypto panel — INSTALLED / OBSERVED

`scripts/index_existing_crypto_market_panel.py` converts `research-data/2026-08-13_2026-08-21_crypto_market_panel.coingecko.utc.json` into nine UTC-aligned states. Derived features remain intentionally narrow: per-asset 1-day returns, positive breadth, XRP/XLM ratio and ratio change. State-local source coverage remains `0.25` because these vectors are built from one daily spot/relative-price family.

### Crypto system-shock event — INSTALLED / OBSERVED

`scripts/index_crypto_system_shock_event.py` normalizes `research-data/2026-08-22_crypto_system_shock_transaction_reconstruction.v1.json` into `stegverse.erl.market_observation.v1` while preserving the event center near `2026-08-22T05:11:20Z`, synchronized-cliff observation, amplitude ratios, source limitations, six competing hypotheses and unresolved state. The adapter does not promote spot-led, derivatives-led, whale attribution, or XRP-specific amplification into fact.

### Generic event normalization — BASELINE INSTALLED

`scripts/normalize_existing_market_events.py` and deterministic tests provide a generalized boundary for normalizing additional admitted ERL event objects without granting execution authority or inventing findings.

### Source-family registry and dynamic health — INSTALLED / OBSERVED

The registry independently tracks spot, event, derivatives, order-book liquidity, stablecoin flows, ETF/fund flows, on-chain flows and macro cross-market families. A source valid in one family never implies coverage of another.

`research-data/longitudinal-market-source-health-policy.v1.json` defines family-specific freshness limits. `scripts/build_longitudinal_source_health.py` produces a deterministic receipt at an explicit `as_of_utc`, extracts only source observation/as-of timestamps rather than arbitrary dates in prose or future windows, and marks each family `FRESH`, `STALE`, `UNKNOWN_FRESHNESS`, or `MISSING`.

Run `32896713367` completed SUCCESS through all 33 steps and retained artifact `9581481513`, digest `sha256:d0a12966e5a42a4e462c09b30e982e4fc6c8ead0661611a05b6bbdcedb5cba97`. This run built the source-health receipt, fed its measured coverage into the XRP preference packet, retained the packet fail-closed, and uploaded the resulting evidence bundle.

The important behavioral change is that preference confidence is no longer driven by a static optimistic coverage placeholder. Source freshness/missingness is now an executable input to the preference evidence path.

## Analogue method — BASELINE V1 COMPLETE

`weighted_normalized_l1_with_missingness_penalty.v1` operates only on retained numeric features, penalizes missing dimensions instead of silently imputing them, exposes matched/materially-different/missing dimensions, uses deterministic corpus-local scales and optional explicit weights, preserves digests and sorts deterministically. This is a reproducible baseline, not an economically optimal weighting claim.

## Trade-preference interface — BASELINE V1 COMPLETE

ERL emits research-only comparisons against alternatives including `FOREGO`, retaining candidate/side, state digest, analogue similarity evidence, outcome distributions, favorable evidence, disconfirming evidence, source coverage/staleness, confidence and one of `PREFER`, `NEUTRAL`, `DEFER`, `FOREGO`, or `INSUFFICIENT_EVIDENCE`.

The builder fails closed when source coverage or analogue sample size is insufficient and cannot authorize capital or execution.

## Observed validation evidence

- Run `32893379964`: first retained full pipeline, artifact `9580268876`, digest `sha256:f5bb9ff4f7318b0f838e71fdb210e48cbec2b2e0d851fec78474d873024bf08b`.
- Run `32893544680`: measured state coverage pipeline, artifact `9580330248`, digest `sha256:48e313bf0c718a0d61de6d59d396b388dd0266d9b5178098d72fb7fccd935a58`.
- Run `32893864586`: system-shock event ingestion, artifact `9580447450`, digest `sha256:ae18bef654deb35396b1bd28700d1f5d934d09a4dec01f3e32213b7fe3bfed56`.
- Run `32894115550`: generalized event-normalization validation, artifact `9580539457`, digest `sha256:d0446ec738eb3292b4c27b462dec9ed614231df13ca50f2821d40a2e691fffd8`.
- Run `32896713367`: dynamic source-health/freshness and preference binding, artifact `9581481513`, digest `sha256:d0a12966e5a42a4e462c09b30e982e4fc6c8ead0661611a05b6bbdcedb5cba97`.

The observed XRP comparison remains `INSUFFICIENT_EVIDENCE`; the corpus still contains only nine daily states and at most eight historical analogues, while major source families remain missing or stale. This is the intended fail-closed result.

## Crypto-bot integration boundary

Downstream issue: `StegVerse-Labs/crypto-bot#15`.

Crypto-bot now has a baseline consumer in `erl_evidence.py` with hosted passing tests. It validates ERL authority fields, freshness, source coverage, state-vector digest binding, analogue sample size, favorable/disconfirming evidence and preserves `FOREGO`. CI run `32896880997` completed SUCCESS. Scoped downstream handoff: `StegVerse-Labs/crypto-bot/docs/ERL_LONGITUDINAL_EVIDENCE_CONSUMER_MIRROR_HANDOFF.md`.

This is not yet the full retained ERL -> crypto-bot replay. The consumer currently has deterministic/synthetic packet tests; the next integration step is binding an actual retained ERL artifact and measuring historical candidate-selection behavior with and without ERL influence.

## Remaining feature/data gaps

- expand historical market ingestion beyond nine daily states and below daily resolution;
- derivatives: funding, basis, open interest, liquidations, options IV/skew;
- order-book spread/depth/imbalance/depth withdrawal;
- stablecoin supply and exchange/cross-chain flows;
- ETF/fund flows;
- broader on-chain exchange inflows, large transfers, bridge/network activity;
- macro rates/yields, DXY, equities/volatility, gold/oil/financial conditions;
- systematic event normalization and source-age decay across additional ERL event records;
- out-of-sample analogue/preference calibration;
- actual retained ERL -> crypto-bot replay and candidate-ranking integration.

## Current build sequence

Completed: architecture, issue #77, scoped handoff, core schemas, deterministic validator, analogue engine, forward-outcome labeler, trade-preference builder, daily-panel indexer, system-shock adapter, generic event-normalization baseline, source registry, dynamic source-health receipt, observed retained fail-closed pipeline, and baseline crypto-bot consumer validation.

Next: expand historical and cross-family data, replay actual retained ERL artifacts through crypto-bot, calibrate out of sample, then determine whether research evidence may influence candidate ranking. Strategy influence and execution authority remain unclaimed.

## Completion state

- architecture/goal definition: COMPLETE
- core schemas/validators: BASELINE V1 COMPLETE / HOSTED PASS
- daily-panel indexer: COMPLETE / HOSTED PASS
- market-event adapters: BASELINE V1 COMPLETE / HOSTED PASS
- source registry: COMPLETE V1
- dynamic source-health/freshness: BASELINE V1 COMPLETE / HOSTED PASS
- analogue/outcome/preference engine: BASELINE V1 COMPLETE / HOSTED PASS
- retained real-data ERL pipeline: COMPLETE / FAIL-CLOSED AS DESIGNED
- crypto-bot consumer boundary: BASELINE V1 COMPLETE / HOSTED PASS
- broad longitudinal corpus: PARTIAL
- derivatives/liquidity/flow/macro/on-chain breadth: PENDING/PARTIAL
- actual ERL -> crypto-bot retained replay: PENDING
- out-of-sample calibration: PENDING
- strategy influence authorization: NOT CLAIMED
- execution authority: NONE

## Archive note

This handoff is sufficient to continue the bounded research lane without reconstructing the conversation. The lane remains active until data breadth, retained ERL -> crypto-bot replay and out-of-sample calibration are complete; no strategy or execution activation is authorized.
