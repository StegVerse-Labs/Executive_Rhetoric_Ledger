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
9. Rolling-origin out-of-sample calibration: `scripts/calibrate_longitudinal_analogue_oos.py`.
10. Deterministic validators/tests and hosted workflow: `.github/workflows/validate-longitudinal-market-research.yml`.

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

Run `32900895887` observed current dynamic coverage at `0.15625`, below the legacy state-local `0.25`; the preference packet therefore retained confidence `0.0625` and `INSUFFICIENT_EVIDENCE` rather than inheriting an optimistic static coverage assumption.

## Analogue method — BASELINE V1 COMPLETE

`weighted_normalized_l1_with_missingness_penalty.v1` operates only on retained numeric features, penalizes missing dimensions instead of silently imputing them, exposes matched/materially-different/missing dimensions, uses deterministic corpus-local scales and optional explicit weights, preserves digests and sorts deterministically. This is a reproducible baseline, not an economically optimal weighting claim.

## Rolling out-of-sample calibration — BASELINE INSTALLED / OBSERVED

`scripts/calibrate_longitudinal_analogue_oos.py` performs rolling-origin evaluation with no future-state leakage. Each evaluation state may use only prior states as its analogue corpus. The analogue-derived candidate is compared against a simple `positive_1d_momentum_else_FOREGO.v1` baseline using the next retained state as the realized outcome.

Run `32900895887` completed SUCCESS with 20 deterministic tests and retained an OOS calibration receipt. The current nine-state corpus yields only five valid OOS evaluation points versus the configured minimum of 20, so the correct state is `NOT_CALIBRATED`. `strategy_influence_authorized=false`, `execution_authority=NONE`, and `may_authorize_order=false` remain enforced. This is a corpus-size limitation, not a validator failure.

Artifact `9583005919` retained nine longitudinal evidence files with digest `sha256:8e1bc430cf0768b315a419637bb5775264386e4eec8e9f45268cae985064dba4`.

## Trade-preference interface — BASELINE V1 COMPLETE

ERL emits research-only comparisons against alternatives including `FOREGO`, retaining candidate/side, state digest, analogue similarity evidence, outcome distributions, favorable evidence, disconfirming evidence, source coverage/staleness, confidence and one of `PREFER`, `NEUTRAL`, `DEFER`, `FOREGO`, or `INSUFFICIENT_EVIDENCE`.

The builder fails closed when source coverage or analogue sample size is insufficient and cannot authorize capital or execution.

## Observed validation evidence

- Run `32893379964`: first retained full pipeline, artifact `9580268876`, digest `sha256:f5bb9ff4f7318b0f838e71fdb210e48cbec2b2e0d851fec78474d873024bf08b`.
- Run `32893544680`: measured state coverage pipeline, artifact `9580330248`, digest `sha256:48e313bf0c718a0d61de6d59d396b388dd0266d9b5178098d72fb7fccd935a58`.
- Run `32893864586`: system-shock event ingestion, artifact `9580447450`, digest `sha256:ae18bef654deb35396b1bd28700d1f5d934d09a4dec01f3e32213b7fe3bfed56`.
- Run `32894115550`: generalized event-normalization validation, artifact `9580539457`, digest `sha256:d0446ec738eb3292b4c27b462dec9ed614231df13ca50f2821d40a2e691fffd8`.
- Run `32896713367`: dynamic source-health/freshness and preference binding, artifact `9581481513`, digest `sha256:d0a12966e5a42a4e462c09b30e982e4fc6c8ead0661611a05b6bbdcedb5cba97`.
- Run `32900895887`: rolling OOS calibration + current dynamic health, artifact `9583005919`, digest `sha256:8e1bc430cf0768b315a419637bb5775264386e4eec8e9f45268cae985064dba4`.

The observed XRP comparison remains `INSUFFICIENT_EVIDENCE`; the corpus still contains only nine daily states and at most eight historical analogues, while major source families remain missing or stale. This is the intended fail-closed result.

## Crypto-bot integration boundary — RETAINED CROSS-REPOSITORY REPLAY OBSERVED

Downstream issue: `StegVerse-Labs/crypto-bot#15`.

Crypto-bot has a baseline consumer in `erl_evidence.py`, a retained-artifact replay adapter in `scripts/replay_erl_longitudinal_artifact.py`, and a research-only candidate-selection layer in `candidate_selection.py`.

Crypto-bot run `32900562867` downloaded exact ERL artifact `9581481513`, verified its ZIP digest, bound the packet to the retained state-vector digest, replayed it at its historical time and at a later admissibility time, and retained artifact `9582878281`, digest `sha256:e53ecc0f16f7d4cc2c0859f9d1aa37800e4f391c573550db69f67731be163988`.

Observed results were intentionally fail-closed:

- historical-time result: `ERL_INSUFFICIENT_EVIDENCE` because analogue sample size was below the configured minimum;
- later-time result: `ERL_EVIDENCE_STALE`;
- strategy influence: false;
- execution authority: none.

Crypto-bot CI run `32900675537` also completed SUCCESS after installing `candidate_selection.py` and tests. Rejected/stale/insufficient ERL evidence cannot alter the base research ranking; accepted ERL evidence can alter only the research ranking, never strategy/capital/execution authority; `FOREGO` is a first-class candidate.

This satisfies the first retained ERL -> crypto-bot replay requirement. It does not satisfy evidence of improved candidate selection because the admitted corpus remains too small and narrow to accept the ERL preference packet.

## Remaining feature/data gaps

- expand historical market ingestion beyond nine daily states and below daily resolution;
- derivatives: funding, basis, open interest, liquidations, options IV/skew;
- order-book spread/depth/imbalance/depth withdrawal;
- stablecoin supply and exchange/cross-chain flows;
- ETF/fund flows;
- broader on-chain exchange inflows, large transfers, bridge/network activity;
- macro rates/yields, DXY, equities/volatility, gold/oil/financial conditions;
- systematic event normalization and source-age decay across additional ERL event records;
- grow rolling OOS evaluation count to at least 20 retained evaluation points and then beyond that for meaningful calibration;
- compare candidate selection with and without accepted ERL evidence over out-of-sample periods;
- only after positive retained calibration evidence consider authorizing ERL research influence on the live candidate-selection path.

## Current build sequence

Completed: architecture, issue #77, scoped handoff, core schemas, deterministic validator, analogue engine, forward-outcome labeler, trade-preference builder, daily-panel indexer, system-shock adapter, generic event-normalization baseline, source registry, dynamic source-health receipt, observed retained fail-closed ERL pipeline, baseline crypto-bot consumer, exact retained cross-repository replay, candidate research-ranking layer, and baseline rolling OOS calibration infrastructure.

Next: expand historical/cross-family data, increase OOS evaluation depth, measure with-vs-without ERL candidate selection out of sample, and only then determine whether research evidence may influence strategy candidate selection. Strategy influence and execution authority remain unclaimed.

## Completion state

- architecture/goal definition: COMPLETE
- core schemas/validators: BASELINE V1 COMPLETE / HOSTED PASS
- daily-panel indexer: COMPLETE / HOSTED PASS
- market-event adapters: BASELINE V1 COMPLETE / HOSTED PASS
- source registry: COMPLETE V1
- dynamic source-health/freshness: BASELINE V1 COMPLETE / HOSTED PASS
- analogue/outcome/preference engine: BASELINE V1 COMPLETE / HOSTED PASS
- retained real-data ERL pipeline: COMPLETE / FAIL-CLOSED AS DESIGNED
- retained ERL -> crypto-bot replay: COMPLETE / HOSTED PASS / FAIL-CLOSED AS DESIGNED
- crypto-bot research-only candidate ranking: BASELINE V1 COMPLETE / HOSTED PASS
- rolling OOS calibration infrastructure: BASELINE V1 COMPLETE / HOSTED PASS
- current OOS calibration state: NOT_CALIBRATED (5 observations vs minimum 20)
- broad longitudinal corpus: PARTIAL
- derivatives/liquidity/flow/macro/on-chain breadth: PENDING/PARTIAL
- demonstrated out-of-sample improvement: PENDING
- strategy influence authorization: NOT CLAIMED
- execution authority: NONE

## Archive note

This handoff is sufficient to continue the bounded research lane without reconstructing the conversation. The lane remains active until data breadth and meaningful out-of-sample calibration/improvement evidence are complete; no strategy or execution activation is authorized.


## Automated crypto system-shock research lane — INSTALLED / RUNTIME PROOF PENDING

Canonical owner remains Issue #77; this is not a duplicate workstream.

Installed surfaces:
- `config/crypto-system-shock-research-lane.v1.json`
- `task-state/ERL-CRYPTO-SHOCK-001.json`
- `scripts/run_crypto_system_shock_research_lane.py`
- `tests/test_crypto_system_shock_research_lane.py`
- `.github/workflows/research-crypto-system-shock.yml`
- linked forensic records: `research-data/2026-08-22_crypto_system_shock_transaction_reconstruction.v1.json` and `research-data/2026-08-22_crypto_system_shock_venue_dispersion.v1.json`

Current implementation state:
- repo-native automation is INSTALLED on an hourly schedule at minute 17 plus manual dispatch;
- the workflow uses read-only repository permissions, checkout with `persist-credentials:false`, and clears `GITHUB_TOKEN` / `GH_TOKEN` for the collector process;
- public-source acquisition requires no provider or wallet credentials;
- configured spot venues are Coinbase, Kraken, Bitstamp, OKX, and Binance across BTC, ETH, XRP, XLM, SOL and ATOM where the venue exposes the pair;
- each run attempts the historical Aug. 22 05:05-05:20 UTC forensic window and a rolling three-hour watch;
- source failures are retained as missing evidence rather than imputed;
- the collector emits research receipts and venue-window artifacts only; it has `research_authority=ERL`, `execution_authority=NONE`, `may_authorize_order=false`, and `causal_finding_authorized=false`;
- rolling watch logic may flag a cross-asset shock candidate but cannot promote cause, manipulation, whale attribution, motive or trading authority.

Automation purpose:
1. keep the Aug. 22 venue-dispersion reconstruction reproducible from public exchange APIs where historical access remains available;
2. collect recurring multi-venue spot evidence for future synchronized market shocks;
3. preserve source-by-source success/failure and normalized price/volume evidence;
4. provide machine-readable candidates for later derivatives, open-interest, liquidation and order-book enrichment;
5. support longitudinal analogue/OOS research without bypassing the fail-closed trade-preference boundary.

Current limitation:
- workflow/runtime execution evidence for this newly installed scheduled lane has not yet been observed in the canonical handoff;
- the current collector is spot-first. Derivatives liquidation/open-interest and order-book depth acquisition remain open evidence-family tasks;
- GitHub Actions is the current scheduling substrate for this lane, not a claim that GitHub is a permanent sovereign runtime dependency.

Task state:
- ERL-CRYPTO-SHOCK-001-A public venue spot refresh — ACTIVE / IMPLEMENTED
- ERL-CRYPTO-SHOCK-001-B Aug. 22 first-break reconstruction — ACTIVE
- ERL-CRYPTO-SHOCK-001-C derivatives liquidation/open-interest — REVIEW_REQUIRED
- ERL-CRYPTO-SHOCK-001-D order-book depth — REVIEW_REQUIRED
- ERL-CRYPTO-SHOCK-001-E external-event control timeline — ACTIVE
- ERL-CRYPTO-SHOCK-001-F independent review before causal promotion — BLOCKED on evidence completion

No user action is required for the automated public-research lane.
