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
- Population averages cannot erase supported distributional or regional strata.
- Current consumption cannot establish affordability when arrears, delinquency, balance-sheet drawdown, or deferred obligations are increasing.
- Public transfers/subsidies are explicit offset flows, not negative prices, and cannot be counted twice.
- Observation first, model second, explanation last.

## ERL binding
Physical Economics consumes the canonical transition tuple `T=<S_pre,S_post,C,E,P,U,Q>` and does not replace the core calculus.

## Canonical machine surfaces
- `contracts/physical-economics.contract.json`
- `schemas/physical-economics-state.schema.json`
- `assessments/physical-economics/extended-physical-economics-surfaces-2026.v0.1.json`
- Randolph consumer seed retained for provenance: `assessments/forecast-calibration/matt-randolph/physical-economic-condition-index-target.v0.1.json`

Canonical record families remain `economic_unit_state`, `essential_need_state`, `population_burden_state`, `producer_cost_margin_state`, `tax_fee_flow`. Extended native analytical surfaces are defined below and are to be bound into future schema/validator expansion rather than silently overloaded into existing fields.

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
11. Household Balance-Sheet Resilience
12. Arrears / Deferred Obligation State
13. Capacity / Inventory Constraint State
14. Regional Burden Surface
15. Net Public Transfer / Offset Flow

State vector is primary; scalar composite is not authorized.

## Native sub-indexes / surfaces
### Essential Need Satisfaction Index
Food sufficiency, energy/service-payment stress, transportation sufficiency, housing instability/payment stress, water/utility arrears where available, and essential quantity/quality compression.

### Population Burden Distribution Index
Median, lower/upper quintile, burden gap, threshold exceedance, geography/tenure/household-size slices where justified.

### Producer Cost-Margin Transmission Index
Intermediate inputs, compensation, taxes less subsidies, output/sales, gross operating surplus, profits, trade margins, physical output. Inferred residual margin remains lower-confidence.

### Household Balance-Sheet Resilience
Tracks nominal DPI/resources, personal saving, saving rate, liquid buffers where available, required debt service, delinquencies, and observable asset drawdown or credit substitution.

Current seed: BEA saving rate declined from `3.5%` in March 2026 to `2.7%` in June 2026. Federal Reserve May 2026 stability reporting says household balance sheets were strong overall while credit-card and auto-loan delinquencies remained elevated relative to the past decade. Aggregate strength cannot erase distressed subgroups.

### Arrears / Deferred Obligation State
Tracks housing payment status, utility/expense difficulty, credit delinquency, eviction/disconnection risk, and deferred required expenses. Continued housing, service, or spending does not establish affordability where payment is deferred.

Census HTOPS provides housing-payment, expense-difficulty, energy, transportation, and related direct-burden paths. Federal Reserve delinquency evidence supplies a separate credit-obligation layer.

### Capacity / Inventory Constraint State
Tracks industrial production, utilization, capacity growth, inventories, inventory-to-sales where available, shipments, new orders, and unfilled orders.

Current seed: Federal Reserve G.17 July 2026 total-industry utilization `76.3%` versus `79.4%` 1972-2025 average; manufacturing `76.0%` versus `78.2%` average. Census June 2026 business inventories were `$2,740.2B`, unchanged from May at the published one-decimal growth rate. These aggregate values weigh against a blanket economy-wide capacity-shortage claim but do not resolve sector-specific scarcity.

Prospective lane gates: Census M3 July advance `2026-08-26`; full July M3 `2026-09-02`.

### Regional Burden Surface
BLS CE metro data establish that essential expenditure composition varies materially across geography. 2023-24 U.S. shares: housing `33.2%`, transportation `17.0%`, food `12.9%`. Examples: Miami housing `40.0%`; Houston transportation `19.8%`; Honolulu food `16.4%`; St. Louis housing `29.1%`. These are multiyear baselines, not current 2026 burden values; they define regional weighting structure to join with current local delivered costs/resources.

### Net Public Transfer / Offset Flow
Tracks cash transfers, food assistance, energy assistance, housing assistance, tax credits, rebates, insurance subsidies, eligibility/take-up, and distribution. Missing current program data remain opaque rather than treated as zero.

USDA FNS provides national/state SNAP persons, households, benefits, and average benefits, but the current public source observed in this research is lagged to November 2025; no 2026 SNAP numeric promotion is authorized from that source yet.

## Generalized evidence installed
- `assessments/physical-economics/producer-food-trade-margin-divergence-2026-03-through-07.json`
- `assessments/physical-economics/population-burden-distribution-baseline-ce-2024.json`
- `assessments/physical-economics/htops-official-workbook-custody-map-2026-03.json`
- `assessments/physical-economics/extended-physical-economics-surfaces-2026.v0.1.json`

### Producer food trade-margin divergence
BLS PPI shows non-equivalence between food producer prices and trade margins. June->July 2026: final-demand foods `-0.9%`, food/alcohol wholesale margins `+2.9%`, retail margins `+2.1%`. July YoY: final-demand foods `-0.1%`, wholesale margins `-1.0%`, retail margins `+5.5%`. These values do not establish manufacturer profit expansion, excess profit, motive, or causal consumer pass-through without joined accounting and physical evidence.

### Population distribution baseline
BLS CE 2024 weighted income ranges: lowest `$0-$29,932`; second `$29,933-$57,452`; third `$57,453-$94,511`; fourth `$94,512-$155,925`; highest `>$155,925`. Average annual expenditures: `$35,046`, `$50,054`, `$66,900`, `$89,972`, `$150,342`. Highest/lowest expenditure-capacity ratio ~`4.29x`. Food + housing + transportation represented `63.3%` of all-consumer-unit expenditures in 2024. This is a distribution baseline, not a 2026 burden claim.

### Official March 2026 HTOPS custody map
Official Census workbooks are resolved for food sufficiency, household energy spending, difficulty paying usual expenses, price stress, and transportation sufficiency, with matching standard-error tables. Census reports roughly 136,000 households for March 13-30. Source discovery is complete; direct workbook numeric extraction/custody remains pending. Secondary reconstructions remain triangulation only.

## Physical food quantity boundary
USDA ERS F-MAP establishes package-weight normalization to grams, but public files currently cover 2012-2018. Method established; current national 2026 grams/calories remain uncustodied. Retail units/volume are proxies, not physical-mass/nutrition equivalents.

## Adjacent-index posture
- Federal Reserve DSR: valid aggregate scheduled mortgage + consumer debt-service input; not distribution-complete.
- BEA Q1 2026 corporate profits from current production: `$4,426.5B` annualized aggregate; not product-level margin. Q2 corporate profits are not admitted before scheduled `2026-08-26` release.
- Census QFR: direct corporate income-statement/operating-ratio source. Q2 2026 values are not admitted before scheduled `2026-09-08` release.
- Future releases are lane-native prospective evidence gates; no separate user monitoring task is required.

## Required validators
1. unit continuity fail-closed;
2. unmet-need semantics;
3. distribution preservation;
4. producer-margin evidence posture;
5. tax/fee flow uniqueness;
6. balance-sheet-resilience anti-aggregation rule;
7. arrears-versus-affordability rule;
8. capacity/inventory sector-scope rule;
9. regional aggregation preservation;
10. transfer-offset single-count rule.

Required fixtures: food shrinkflation, electricity delivery charges, insurance deductible/coverage changes, rent-plus-fee transitions, credit-maintained consumption, arrears-maintained service, low-utilization margin expansion, metro burden divergence, and transfer-offset accounting.

## Next executable work
1. Directly custody official March 2026 HTOPS values and standard errors.
2. Obtain detailed CE essential-category levels/shares by income quintile and calculate income-relative burden surfaces.
3. Join food producer prices/trade margins with manufacturer/retailer financial evidence plus physical quantity/package state without assuming causality.
4. Add household liquid-buffer distribution and asset-drawdown evidence at the best available authoritative cadence.
5. Add sector-specific capacity/inventory joins for food, electricity, motor fuel, housing inputs, and insurance service capacity.
6. Expand current transfer data as authoritative 2026 program values become publicly available.
7. Continue contemporary 2026 gram/calorie data search.
8. Build semantic validators/fixtures for all 15 state-vector surfaces.
9. Prototype food, electricity, motor-fuel, and housing state vectors.
10. Add hosted CI and independent review before any composite/release claim.

## Current posture
- lane: `FORMAL_REUSABLE_ERL_LANE`
- canonical handoff: complete
- reusable machine contract: complete
- five-family state schema: structurally complete
- extended five-surface bundle: complete at target/current-seed level
- generalized producer-margin evidence: installed
- generalized population-distribution baseline: installed
- official HTOPS workbook discovery: complete
- official HTOPS numeric custody: pending
- balance-sheet surface: formalized with current aggregate seed
- arrears surface: formalized with authoritative source paths
- capacity/inventory surface: formalized with current federal seed
- regional burden surface: formalized with BLS metro baseline
- transfer-offset surface: formalized; current program-value lags remain explicit
- semantic validators: pending
- native sub-index calculations: partial
- hosted exact-head validation: not yet observed
- composite: not authorized
- independent review: incomplete
- release: not authorized

Physical Economics bounded lane implementation/research activation estimate: `66%`. This percentage is for the promoted Physical Economics lane and is not the Randolph calibration percentage.

## Archive posture
The five identified research blind spots are now formally represented in the lane with source hierarchies and evidence seeds. Remaining work is predominantly direct data custody, executable validation, sector/population joins, native sub-index execution, independent review, and release governance.
