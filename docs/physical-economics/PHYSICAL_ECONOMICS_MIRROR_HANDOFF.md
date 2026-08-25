# ERL Physical Economics Mirror Handoff

## Authority
Canonical continuation source for the reusable ERL Physical Economics lane. The lane was promoted from Issue #76 / Matt Randolph calibration but is not owned by that assessment; Randolph is one consumer.

## Goal
Reconstruct physical economic value and burden across producers, intermediaries, households, and population strata without treating a headline price index as a sufficient description of economic condition.

## Governing rules
- No economic unit is assumed state-equivalent across time.
- Sticker-price continuity cannot establish unit continuity when mass, volume, count, nutrition, quality, durability, coverage, service level, mandatory fees, or other economically relevant attributes change.
- Underlying essential need is distinct from observed acquisition; constrained quantity does not establish reduced need.
- Existing indexes may be imported only after construction/circularity audit.
- Nominal income/resources are primary; CPI-deflated real income is comparator evidence, not the sole purchasing-power denominator.
- Taxes/fees/regulatory charges are cross-cutting flow objects attached to their initial payer and propagated only where pass-through is evidenced; no double counting.
- Producer input cost, wholesale margin, retail margin, manufacturer accounting profit, corporate profit, and consumer price are distinct states.
- Population averages cannot erase supported distributional strata.
- Observation first, model second, explanation last.

## ERL binding
Physical Economics consumes the canonical transition tuple `T=<S_pre,S_post,C,E,P,U,Q>` and does not replace the core calculus.

## Canonical machine surfaces
- `contracts/physical-economics.contract.json`
- `schemas/physical-economics-state.schema.json`
- Randolph consumer seed retained for provenance: `assessments/forecast-calibration/matt-randolph/physical-economic-condition-index-target.v0.1.json`

Canonical record families: `economic_unit_state`, `essential_need_state`, `population_burden_state`, `producer_cost_margin_state`, `tax_fee_flow`.

## State vector
1. Physical Purchasing Power
2. Nominal Resource Capacity
3. Required Debt-Service Burden
4. Essential Cost Burden
5. Essential Need Satisfaction
6. Substitution and Quality Compression
7. Population Burden Distribution
8. Producer Cost Pressure
9. Producer Margin State
10. Tax/Fee/Regulatory Flow

State vector is primary; scalar composite is not authorized.

## Native sub-indexes
- Essential Need Satisfaction Index: food sufficiency, energy/service-payment stress, transportation sufficiency, housing instability/payment stress, water/utility arrears where available, essential quantity/quality compression.
- Population Burden Distribution Index: median, lower/upper quintile, burden gap, threshold exceedance, geography/tenure/household-size slices where justified.
- Producer Cost-Margin Transmission Index: intermediate inputs, compensation, taxes less subsidies, output/sales, gross operating surplus, profits, trade margins, physical output. Inferred residual margin remains lower-confidence.

## Generalized evidence installed
### Producer food trade-margin divergence
`assessments/physical-economics/producer-food-trade-margin-divergence-2026-03-through-07.json`

BLS PPI directly shows non-equivalence between food producer prices and trade margins. June->July 2026: final-demand foods `-0.9%`, food/alcohol wholesale margins `+2.9%`, retail margins `+2.1%`. July YoY: final-demand foods `-0.1%`, wholesale margins `-1.0%`, retail margins `+5.5%`.

Bounded result: margin state must be separately observed. These values do not establish manufacturer profit expansion, excess profit, motive, or causal consumer pass-through without joined accounting and physical evidence.

### Population distribution baseline
`assessments/physical-economics/population-burden-distribution-baseline-ce-2024.json`

BLS CE 2024 weighted income ranges: lowest `$0-$29,932`; second `$29,933-$57,452`; third `$57,453-$94,511`; fourth `$94,512-$155,925`; highest `>$155,925`.

Average annual expenditures: `$35,046`, `$50,054`, `$66,900`, `$89,972`, `$150,342` respectively. Highest/lowest expenditure-capacity ratio ~`4.29x`. Food + housing + transportation represented `63.3%` of all-consumer-unit expenditures in 2024. This is a distribution baseline, not a 2026 burden claim.

### Official March 2026 HTOPS custody map
`assessments/physical-economics/htops-official-workbook-custody-map-2026-03.json`

Official Census workbooks are resolved for food sufficiency, household energy spending, difficulty paying usual expenses, price stress, and transportation sufficiency, with matching standard-error tables. Census reports roughly 136,000 households for March 13-30. Source discovery is complete; direct workbook numeric extraction/custody remains pending. Secondary reconstructions remain triangulation only.

## Physical food quantity boundary
USDA ERS F-MAP establishes package-weight normalization to grams, but public files currently cover 2012-2018. Method established; current national 2026 grams/calories remain uncustodied. Retail units/volume are proxies, not physical-mass/nutrition equivalents.

## Adjacent-index posture
- Federal Reserve DSR: valid aggregate scheduled mortgage + consumer debt-service input; not distribution-complete.
- BEA Q1 2026 corporate profits from current production: `$4,426.5B` annualized aggregate; not product-level margin. Q2 corporate profits are not admitted before the scheduled `2026-08-26` release.
- Census QFR: direct corporate income-statement/operating-ratio source. Q2 2026 values are not admitted before the scheduled `2026-09-08` release.

## Required validators
1. unit continuity fail-closed;
2. unmet-need semantics;
3. distribution preservation;
4. producer-margin evidence posture;
5. tax/fee flow uniqueness.

Required fixtures: food shrinkflation, electricity delivery charges, insurance deductible/coverage changes, rent-plus-fee transitions.

## Next executable work
1. Directly custody official March 2026 HTOPS values and standard errors.
2. Obtain detailed CE essential-category levels/shares by income quintile and calculate income-relative burden surfaces.
3. Join food producer prices/trade margins with manufacturer/retailer financial evidence plus physical quantity/package state without assuming causality.
4. Admit BEA Q2 corporate profits only after Aug 26 and QFR Q2 only after Sep 8.
5. Continue contemporary 2026 gram/calorie data search.
6. Build semantic validators/fixtures.
7. Prototype food, electricity, motor-fuel, and housing state vectors.
8. Add hosted CI and independent review before any composite/release claim.

## Current posture
- lane: `FORMAL_REUSABLE_ERL_LANE`
- canonical handoff: complete
- reusable machine contract: complete
- five-family state schema: structurally complete
- generalized producer-margin evidence: installed
- generalized population-distribution baseline: installed
- official HTOPS workbook discovery: complete
- official HTOPS numeric custody: pending
- semantic validators: pending
- native sub-index calculations: partial
- hosted exact-head validation: not yet observed
- composite: not authorized
- independent review: incomplete
- release: not authorized

Physical Economics bounded lane implementation/research activation estimate: `58%`. This percentage was reset for the newly promoted lane and is not the Randolph calibration percentage.

## Archive posture
The lane is formally promoted and has meaningful generalized evidence, but direct burden custody, semantic validation, native sub-index execution, independent review, and release remain incomplete.
