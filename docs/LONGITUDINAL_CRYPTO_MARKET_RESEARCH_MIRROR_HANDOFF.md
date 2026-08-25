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

## Core object model

1. `market_observation` — timestamped source-grounded raw/derived observation.
2. `market_state_vector` — normalized point-in-time cross-domain condition vector.
3. `historical_analogue` — reproducible similarity link from current state to prior state(s), with both matched and materially different dimensions.
4. `forward_outcome` — realized post-state results at fixed horizons.
5. `trade_preference_evidence` — comparison of candidate trades or `TRADE` vs `FOREGO`, retaining favorable and disconfirming evidence separately.
6. `source_coverage` — source freshness, completeness, missingness and quality metadata.

## Initial feature families

### Crypto market structure
- spot returns and acceleration
- volume and volume expansion
- breadth, dispersion and cross-asset synchronization
- pair-relative strength and leadership
- spread/depth/liquidity when available

### Derivatives
- funding
- futures basis
- open interest
- liquidation direction/intensity
- options IV/skew/term structure when available

### Capital/flow
- spot ETF/fund flows
- stablecoin supply and exchange flows
- large exchange inflow/outflow observations
- on-chain large transfers, bridge/network flows and active-address/settlement activity when meaningful

### Cross-market/macro
- Treasury yields/rates
- dollar index
- equity indices and volatility
- gold and major commodities
- oil/energy conditions
- broad liquidity/financial-conditions measures

### Events
- regulation/policy/legal actions
- central-bank/Treasury announcements
- geopolitical/energy/shipping events
- protocol upgrades/outages/exploits
- token unlocks/governance/treasury actions
- institutional adoption or de-adoption events
- timestamped news with source quality and age/decay

## Longitudinal comparison

Current conditions are not compared to history by a single regime label. Analogue search must preserve a multi-dimensional vector and expose:

- dimensions used
- weights/version
- similarity score
- unavailable dimensions
- materially different dimensions
- event-context match/mismatch
- sample count
- horizon-specific realized outcomes
- uncertainty and result sensitivity

No best historical analogue may be presented without also preserving the largest material differences.

## Trade-preference interface

For each candidate opportunity, ERL may emit a bounded comparison against alternatives, including `FOREGO`.

Required output concepts:

- candidate instrument/pair and side
- current market-state vector digest
- analogue IDs and similarity distribution
- forward-return distribution by horizon
- drawdown/adverse-excursion distribution where available
- persistence/mean-reversion tendency
- relative performance vs competing assets
- source coverage/staleness
- favorable evidence
- disconfirming evidence
- uncertainty/confidence
- research-only recommendation class such as `PREFER`, `NEUTRAL`, `DEFER`, `FOREGO`, or `INSUFFICIENT_EVIDENCE`

The class is evidence preference only. It cannot authorize capital or execution.

## Existing ERL material to reuse

The current repository already contains reusable crypto/event research, including:

- `research-data/2026-08-13_2026-08-21_crypto_market_panel.coingecko.utc.json`
- `research-data/2026-08-22_crypto_system_shock_transaction_reconstruction.v1.json`
- `research-data/2026-08-20_2026-08-21_rlusd_institutional_credit_transition.v1.json`
- `research-data/2026-08-21_wlf_usd1_positive_adoption_matrix.json`
- `$TRUMP` event/custody/liquidity-pathway research

These are inputs to the generalized layer, not the entire market model.

## Crypto-bot integration boundary

`StegVerse-Labs/crypto-bot` may consume a versioned ERL evidence packet only after validating schema, freshness and non-authority fields.

The bot should use the packet as one component in candidate ranking and trade-vs-forego logic. It must preserve independent strategy/risk/TV/TVC authority and must remain fail-closed when ERL evidence is missing, stale, malformed or contradictory.

## Build sequence

1. Install schemas for state vectors and trade-preference evidence.
2. Install deterministic validators.
3. Index existing ERL crypto research-data into provenance-aware source families.
4. Build a first longitudinal panel with aligned UTC time.
5. Implement analogue-distance/retrieval logic with explicit missingness.
6. Build forward-outcome labeling at fixed horizons.
7. Implement trade-vs-trade and trade-vs-forego evidence comparison.
8. Produce first retained ERL evidence packet.
9. Add crypto-bot consumer validation and evidence-only ranking hook.
10. Run historical replay and out-of-sample validation before allowing any strategy influence.

## Completion state

- architecture/goal definition: COMPLETE
- canonical issue: COMPLETE (`#77`)
- scoped handoff: COMPLETE
- schemas: PENDING
- validators: PENDING
- longitudinal panel ingestion: PENDING
- analogue engine: PENDING
- forward-outcome labeling: PENDING
- trade-preference evidence builder: PENDING
- crypto-bot consumer: PENDING
- retained replay/out-of-sample evidence: PENDING
- strategy influence authorization: NOT CLAIMED

## Archive note

This handoff preserves the architecture and implementation sequence. Do not represent the research layer as activated until schemas, validators, retained longitudinal evidence, analogue/outcome reconstruction and crypto-bot consumption are observed in validation.