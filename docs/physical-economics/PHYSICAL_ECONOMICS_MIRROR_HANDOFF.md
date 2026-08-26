# ERL Physical Economics Mirror Handoff

## Authority
Canonical continuation source for the reusable ERL Physical Economics lane. The lane was promoted from Issue #76 / Matt Randolph calibration but is not owned by that assessment; Randolph remains one governed consumer.

## Goal
Reconstruct physical economic value and burden across producers, intermediaries, households, and population strata without treating a headline price index as a sufficient description of economic condition.

## Governing rules
- No economic unit is assumed state-equivalent across time.
- Sticker-price continuity cannot establish unit continuity when mass, volume, count, nutrition, quality, durability, coverage, service level, mandatory fees, or other economically relevant attributes change.
- Underlying essential need is distinct from observed acquisition; constrained quantity does not establish reduced need.
- Existing indexes may be imported only after construction/circularity audit.
- Nominal income/resources are primary; CPI-deflated real income is comparator evidence, not the sole purchasing-power denominator.
- Taxes/fees/regulatory charges are cross-cutting flow objects attached to their initial payer and propagated only where pass-through is evidenced; no double counting.
- Producer input cost, COGS, operating expense, wholesale margin, retail margin, manufacturer accounting profit, corporate profit, pre-tax income, taxable income, and consumer price are distinct states.
- Population averages cannot erase supported distributional or regional strata.
- Current consumption cannot establish affordability when arrears, delinquency, balance-sheet drawdown, or deferred obligations are increasing.
- Public transfers/subsidies are explicit offset flows, not negative prices, and cannot be counted twice.
- Observation first, model second, explanation last.

## Inflation-index / unit-state boundary
Physical Economics does **not** claim that CPI is generically blind to shrinkflation or incorrect at its intended constant-quality price-index task. BLS CPI methodology includes quality adjustment and can recognize identified package downsizing through effective price per standard quantity; BLS PPI likewise applies relevant quality adjustments.

The ERL distinction is one of scope/sufficiency:

```text
inflation index:
constant-quality price change over time

Physical Economics reconstruction:
input/operating cost state
-> physical quantity/quality/service state
-> effective delivered consumer cost
-> revenue/margin/profit state
-> household quantity/access/need satisfaction
```

A valid CPI/PPI observation can remain insufficient to establish producer cause, shock absorption, margin distribution, physical-unit continuity, mandatory delivered cost, household access, or unmet essential need.

Canonical public-method references:
- `https://www.bls.gov/cpi/quality-adjustment/questions-and-answers.htm`
- `https://www.bls.gov/ppi/quality-adjustment/`
- `https://www.bls.gov/opub/btn/volume-12/measuring-shrinkflation-and-its-impact-on-inflation.htm`
- `https://www.bls.gov/cpi/research-series/r-cpi-sc.htm`
- `https://www.bls.gov/opub/hom/cpi/calculation.htm`
- `https://www.bls.gov/cpi/methods-overview.htm`

Do not convert this boundary into the unsupported claim `CPI ignores shrinkflation`.

## Producer-consumer physical-value bridge
Candidate reconstruction path:

```text
input costs
+ non-overlapping operating/production/distribution costs
-> total company cost structure
-> physical output/package/service state
-> wholesale/retail effective price per physical/service unit
-> revenue
-> gross margin / operating margin / profit states
-> household quantity or service acquired
-> unmet essential-need/access gap where evidenced
```

Illustrative inference classes remain evidence-gated:
1. cost rises + sticker price constrained + physical unit shrinks + margin flat/falls -> cost-pressure absorption/transmission candidate;
2. cost flat/falls + physical unit shrinks + price flat/rises + margin rises -> margin-capture candidate;
3. cost rises + sticker price rises + physical unit shrinks -> mixed burden candidate;
4. incomplete/contradictory evidence -> unresolved.

Margin movement alone does not establish causal mechanism or motive. Manufacturer, wholesaler, and retailer states remain separate unless evidence joins them.

## ERL binding
Physical Economics consumes the canonical transition tuple `T=<S_pre,S_post,C,E,P,U,Q>` and does not replace the core calculus.

## Canonical machine surfaces
- `contracts/physical-economics.contract.json`
- `schemas/physical-economics-state.schema.json`
- `assessments/physical-economics/extended-physical-economics-surfaces-2026.v0.1.json`
- Randolph provenance seed: `assessments/forecast-calibration/matt-randolph/physical-economic-condition-index-target.v0.1.json`

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
11. Household Balance-Sheet Resilience
12. Arrears / Deferred Obligation State
13. Capacity / Inventory Constraint State
14. Regional Burden Surface
15. Net Public Transfer / Offset Flow

State vector remains primary; scalar composite is not authorized.

## Native evidence/state posture
### Essential need / direct burden
Census HTOPS official March 2026 workbooks have been resolved for food sufficiency, household energy spending, usual-expense difficulty, price stress, transportation sufficiency, and matching standard errors. Direct official workbook numeric extraction/custody remains pending; secondary reconstructions remain triangulation only.

### Household balance-sheet resilience
BEA saving-rate and Federal Reserve delinquency/balance-sheet evidence are installed as aggregate seeds. Aggregate household strength cannot erase distressed subgroups. BEA released July 2026 Personal Income and Outlays on 2026-08-26; those values are available but not yet admitted into a governed Physical Economics machine evidence object.

### Producer cost/margin
`assessments/physical-economics/producer-food-trade-margin-divergence-2026-03-through-07.json` preserves the non-equivalence between food producer prices and wholesale/retail trade margins without converting margin divergence into motive or product-level profit claims.

BEA released Q2 2026 corporate profits on 2026-08-26. Those aggregate values are publicly available but not yet promoted into a governed Physical Economics evidence record and do not establish product/company-specific margin behavior.

### Capacity / inventory
Federal Reserve G.17 and Census inventory seeds are installed. Earlier session timing was corrected: July Advance Economic Indicators are scheduled for 2026-08-27 and the full Manufacturers' Shipments, Inventories and Orders release for 2026-09-02; do not invent a July M3 value from an Aug. 26 date.

### Population / regional burden
BLS CE national income/expenditure and metro burden baselines are installed as distribution/weighting structures, not current 2026 universal household-condition claims.

### Physical food quantity
USDA ERS F-MAP establishes package-weight normalization to grams, but currently public files cover 2012-2018. Method established; current national 2026 grams/calories remain uncustodied. Retail units/vendor volume are proxies, not physical-mass/nutrition equivalents.

## Required semantic validators
1. unit continuity fail-closed;
2. unmet-need semantics;
3. distribution preservation;
4. producer-margin evidence posture;
5. tax/fee flow uniqueness;
6. balance-sheet-resilience anti-aggregation;
7. arrears-versus-affordability;
8. capacity/inventory sector-scope;
9. regional aggregation preservation;
10. transfer-offset single-count.

Required fixtures include food shrinkflation, electricity delivery charges, insurance deductible/coverage changes, rent-plus-fee transitions, credit-maintained consumption, arrears-maintained service, low-utilization margin expansion, metro burden divergence, and transfer-offset accounting.

## Cross-repository public-report relationship
Reporting transaction authority:
`docs/physical-economics/reporting/PHYSICAL_ECONOMICS_REPORTING_MIRROR_HANDOFF.md`.

Site consumer:

```text
repo: StegVerse-Labs/Site
issue: #496
PR: #499
handoff: docs/physical-economics/PUBLIC_REPORT_UI_MIRROR_HANDOFF.md
```

Current Site proof:
- page/client/tests/workflow implemented;
- local deterministic tests PASS;
- exact feature-head hosted Site validators PASS;
- PR #499 merged by squash on 2026-08-26;
- merge commit `c9ec2d1b106063fc295a11cb39fe25b6111d4c5e` installed `Physical-Economics.html` on Site `main`;
- exact merge commit produced successful `pages build and deployment` run `33008628651`;
- Pages deploy job `98308846026` reported success and environment URL `http://stegverse.org/`;
- separate HTTP/content observation of `https://stegverse.org/Physical-Economics.html` remains pending through available tooling;
- Site report endpoint remains blank/fail-closed;
- Site Issue #496 remains open under its stricter independent-public-observation gate.

Thus Site merge and Pages deployment are proven. Functional report activation is **not** proven because the governed report HTTP adapter/runtime does not yet exist and the endpoint is intentionally unconfigured.

## Next executable work
1. Directly custody official March 2026 HTOPS values and standard errors.
2. Admit 2026-08-26 BEA Q2 corporate-profit and July income/outlay releases through governed evidence objects before calculations use them.
3. Obtain detailed CE essential-category levels/shares by income quintile and calculate income-relative burden surfaces.
4. Join producer prices/trade margins with manufacturer/retailer financial evidence plus physical quantity/package state without assuming causality.
5. Add household liquid-buffer distribution and asset-drawdown evidence at best authoritative cadence.
6. Add sector-specific capacity/inventory joins for food, electricity, motor fuel, housing inputs, and insurance service capacity.
7. Expand authoritative 2026 transfer-offset evidence as available.
8. Continue contemporary 2026 gram/calorie data search.
9. Build semantic validators/fixtures for all 15 state-vector surfaces.
10. Prototype food, electricity, motor-fuel, and housing state vectors.
11. Obtain exact-current-head hosted ERL CI and independent review before composite/release claims.
12. Independently observe the deployed Site Physical Economics page and propagate that proof.
13. Continue the single canonical ERL HTTP-adapter lane: source implementation/validation are complete; obtain authorized resident deployment and live runtime proof, then and only then configure the Site endpoint.

## Validation / integration posture
Umbrella PR #75 remains the active integration lane on `feature/transition-first-calculus`. It is open/draft/unmerged and was last observed non-mergeable. This handoff mutation moves the branch head. Exact-current-head hosted validation must be queried anew; no older PASS is current proof.

## Current posture
- lane: `FORMAL_REUSABLE_ERL_LANE`
- reusable machine contract: complete
- five-family state schema: structurally complete
- extended state-surface target bundle: installed
- generalized producer-margin evidence: installed
- generalized population-distribution baseline: installed
- official HTOPS workbook discovery: complete
- official HTOPS numeric custody: pending
- BLS CPI/PPI shrinkflation-quality boundary: explicit
- producer/consumer physical-value bridge: explicit and evidence-gated
- balance-sheet/arrears/capacity/regional/transfer surfaces: formalized at seed level
- 2026-08-26 BEA releases: available, not yet machine-custodied
- semantic validators: pending
- native sub-index calculations: partial
- ERL repository-wide hosted validation: PASS at `c0638c0c10cbbf218b2ca178ee8dc74a9ea89d28` via run `33011563705`; subsequent handoff-only heads require normal exact-head recheck
- Site consumer: implemented, validated, merged, Pages-deployed; separate HTTP page observation pending
- governed report HTTP adapter source: implemented and bounded-hosted-validated; resident deployment/live runtime proof pending
- composite: not authorized
- independent review: incomplete
- release: not authorized

Physical Economics bounded lane implementation/research activation estimate: `67%`. This percentage is for the promoted reusable lane and is not Randolph calibration completeness or public activation completeness.

## Archive posture
The unit-state/shrinkflation distinction, CPI/PPI boundary, producer/consumer bridge, current evidence gates, Site merge/deployment proof, HTTP-observation boundary, and remaining machine work are durably represented here. Continued work does not require rereading the originating conversation.