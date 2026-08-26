# ERL Economic Distribution Mirror Handoff

## Authority

Bounded source of truth for the ERL economic distribution / household-value-capture lane.

- repository: `StegVerse-Labs/Executive_Rhetoric_Ledger`
- parent authority: `ERL_MIRROR_HANDOFF.md`
- scope: economic distribution, capital participation, producer surplus allocation, household value capture, household resilience, and mobility linkage
- collision boundary: this lane does not alter the Fauci/HSGAC silence-causation case, its claims, or its activation posture

## Goal

Build an evidence-backed, reproducible economic distribution capability that measures not only income and prices, but who captures newly created economic value and whether household economic capacity and upward mobility improve or deteriorate.

The lane must distinguish value flowing to labor compensation; employee ownership/equity participation; existing external capital owners; retirement and broad household asset ownership; consumers through lower prices or better quantity/quality; government through taxes and public revenue; creditors through financing costs; retained enterprise surplus; and unmet household need/foregone consumption.

## Core model

```text
Production / Productivity
  -> Producer Surplus / Margin Capacity
  -> Distribution of Created Value
  -> Household Economic Position
  -> Mobility / Opportunity
```

Interactive lanes include income, substitution, debt and financing costs, unmet need, consumer-price transmission, ownership concentration, tax incidence, producer margin, household required-cost burden, asset access, and mobility.

The model explicitly preserves:

```text
national economic resilience
!= household economic resilience
!= upward social mobility
```

## CPI / household resilience integration — 2026-08-26

The household lane now formalizes a boundary that emerged from the Canada/U.S. economic trajectory and CPI analysis: CPI is a useful price-change input but is not a complete measure of household economic condition.

Required analytical separation now includes:

- representative-basket price change;
- household required-cost burden;
- household discretionary/usable capacity;
- substitution and quality loss;
- debt and financing burden;
- unmet need and foregone consumption;
- savings capacity and wealth accumulation/depletion;
- asset access, including housing;
- intergenerational transfer dependence;
- mobility and opportunity transmission.

Observed expenditure must not be treated as proof of need satisfaction. Consumption that disappears because a household can no longer afford or access it remains an eligible unmet-need signal.

## Canada social-mobility / Horizons research seed — 2026-08-26

Installed research candidate:

- `research-candidates/2026-08-26-canada-household-mobility-cpi-trajectory.md`

Primary foresight seed:

- Policy Horizons Canada, *Future Lives: Social mobility in question* (2025-01-10)
- https://horizons.service.canada.ca/en/2025/01/10/future-lives-social-mobility/index.shtml

The source is admitted as a foresight/taxonomy source, not as proof that its future scenario will occur.

The key ERL integration is that Canada can improve sovereign resilience, including trade diversification, while household affordability or mobility deteriorates. Likewise, increased domestic production in another economy can coexist with higher required costs, financing burdens, substitution loss, or reduced purchasing power.

Comparative analysis should therefore use the hierarchy:

```text
Sovereign Resilience
  -> Productive Economy
  -> Household Condition
  -> Distribution
  -> Mobility
  -> Opportunity
```

Canada and U.S. national trajectories must be independently reconstructed before comparison. Cross-country conclusions are outputs of those lanes rather than organizing assumptions.

## Historical-depth rule

The Horizons source also exposes a major evidence gap: several household and mobility measures have relatively short directly comparable series.

ERL must not interpret the first year of a modern dataset as the beginning of the phenomenon. Historical reconstruction may use deeper proxy series, but every historical value or relationship must preserve one of the following evidence states:

- `DIRECT_OBSERVATION`
- `DERIVED_HISTORICAL_PROXY`
- `INFERRED_RELATIONSHIP`

Derived proxies must never be represented as direct observations. Overlap periods between direct observations and proxies should be used to test proxy validity before backward extension.

Longitudinal analysis must test whether a change is a new structural break, recurring cycle, continuation of a longer trend, or a measurement artifact.

Candidate long-run reconstruction inputs include real wages/disposable income, housing and rent burden, household debt/debt service, financing costs, homeownership by age/cohort, wealth concentration, education cost/return, labor share, savings, essential-cost burdens, inheritance/family-assisted acquisition where available, and regional opportunity differences.

## Ownership Distribution / Capital Participation

This is a formal component of the Distribution lane and must not be treated as equivalent to wages.

Required measurements include, where evidence permits: employee equity participation rate; employee equity value as a share of compensation; breadth across wage bands; appreciation captured by employees, executives/founders, and external shareholders; retirement-account exposure; dilution/vesting; realized vs unrealized gains; ownership concentration before/after value-creation events; and treatment of contractors, franchise workers, temporary workers, and other non-equity labor.

## Producer Margin relationship

Producer Margin remains separately calculable. It measures the economic space available for distribution; Distribution measures where that space actually goes. Do not infer equitable distribution from high margins, rising productivity, or rising valuation alone.

## Comparative policy research

The lane supports empirical comparison of broad employee equity/profit participation; wage-only compensation; tax-and-transfer redistribution after wealth concentration; wealth taxation; corporate-tax incentives or penalties tied to employee ownership; employee stock ownership plans; and cooperative/broad-based ownership models. Policy proposals are research objects, not endorsed conclusions.

## Mark Cuban evidence seed — 2026-08-26

Research seed: Mark Cuban has publicly advocated broad employee equity participation and higher corporate taxation for companies that do not share equity broadly, framing ownership participation as a mechanism for reducing wealth concentration.

This seed is admitted as a policy/proposal research object. It does not establish causal effectiveness. Comparative outcome evidence is required before promotion of any efficacy finding.

Required follow-up evidence includes exact primary/public statements from Cuban; historical employee-equity practices at Broadcast.com and other Cuban-controlled companies; independently verifiable worker outcome data; comparison with wage-only firms; tax-incidence analysis; dilution/vesting/liquidity constraints; distributional effects across income bands; survivorship-selection controls; acquisition/IPO-event controls; and counterexamples where broad equity participation did not materially improve household wealth.

## Installed implementation

- `docs/ECONOMIC_DISTRIBUTION_MIRROR_HANDOFF.md`
- `standards/economic-distribution-index.v1.md`
- `schemas/economic-distribution-observation.schema.json`
- `research-candidates/2026-08-26-canada-household-mobility-cpi-trajectory.md`

The standard now separates income, producer margin, distribution, household condition, and mobility; defines value channels; formalizes the Ownership Distribution / Capital Participation sub-index; preserves substitution/quality, financing-cost, and unmet-need effects; requires visible residual `unknown_unallocated`; establishes CPI/household-condition boundaries; defines historical evidence classes; adds structural-break controls; and establishes country-comparison promotion boundaries.

The schema currently represents analysis scope/time, created value, distribution channels, ownership breadth/value, producer margin, substitution quality, financing costs, evidence roles, confidence, missing evidence, policy seeds, and an explicit fail-closed `activation_authorized: false` state for pre-activation observations. The new household-state, mobility, historical evidence-class, and structural-break concepts are not yet fully represented in the schema and are therefore implementation gaps rather than completed machine capability.

## Activation criteria

Activation requires:

1. formal index specification;
2. source hierarchy and evidence-admission rules;
3. machine-readable schema covering the complete active model;
4. deterministic validator;
5. fixtures covering positive, negative, missing-data, ambiguous-distribution, household-burden, proxy-history, and structural-break cases;
6. at least one historical dataset with reconstructable inputs;
7. calculation replay producing identical outputs;
8. distribution-vs-margin separation validated;
9. ownership-participation and household-state components validated;
10. independent review of at least one historical comparison.

## Current state

- conceptual model: COMPLETE, including household resilience and mobility extension
- ownership distribution / capital participation promotion: COMPLETE
- CPI / household-condition boundary: COMPLETE conceptually
- historical evidence-class and structural-break rule: COMPLETE conceptually
- bounded handoff: COMPLETE
- formal index specification: COMPLETE (draft v1; requires validator-backed validation)
- machine-readable schema: PARTIAL; does not yet cover full household/mobility/history extension
- validator: PENDING
- fixtures: PENDING
- historical dataset integration: PENDING
- calculation/replay module: PENDING
- automated ingestion: PENDING
- independent review: PENDING
- activation: NOT CLAIMED

## Remaining files/modules to install

Destination: `StegVerse-Labs/Executive_Rhetoric_Ledger`

- extend `schemas/economic-distribution-observation.schema.json` for household state, mobility, evidence classes, and structural-break metadata
- `scripts/validate_economic_distribution_observation.py`
- `tests/test_economic_distribution_observation.py`
- `research-data/economic-distribution/README.md`
- positive/negative/missing/ambiguous fixtures
- household-cost/CPI-divergence fixtures
- direct-observation vs historical-proxy fixtures
- structural-break/continuity fixtures
- Canada historical source receipts and normalized series
- U.S. independently reconstructed comparison series
- calculation and replay module
- automated acquisition/normalization adapter
- independent-review receipt format

Cross-repository propagation is not authorized until the lane reaches release posture. At that point pertinent definitions and evidence boundaries must be reviewed for propagation to `StegVerse-Labs/Site`, `GCAT-BCAT-Engine/Publisher`, `admissibility-wiki`, and `stegguardian-wiki`.

## Completion accounting

Denominator for initial activation build remains 10 capability groups; conceptual expansion does not count as machine activation.

- completed implementation groups: 4/10
- developed durable files: 4
- scaffolding/stubs counted as complete: 0
- validation: 0/3 executable validation groups
- activation completion: 40%
- release/tag posture: NOT READY

Archive readiness: this handoff preserves the lane goal, boundaries, installed state, Canada/Horizons research seed, CPI/household-resilience insight, historical-depth requirements, and next implementation objects; future work can continue from this file without relying on chat history.
