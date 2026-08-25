# ERL Physical Economics Mirror Handoff

## Authority
Canonical continuation source for the reusable ERL Physical Economics lane.

This lane is promoted from research developed inside Issue #76 / the Matt Randolph forecast-calibration work, but it is not owned by that calibration. Randolph calibration is one consumer. The lane is intended to support any ERL assessment involving economic units, physical quantity/quality, essential-need satisfaction, distributional burden, producer cost/margin transmission, debt/financing burden, or taxes/fees/regulatory pass-through.

## Goal
Build a transition-first physical-economics layer that reconstructs the state of economic value and burden across producers, intermediaries, households, and population strata without assuming that a headline price index is sufficient to describe economic condition.

## Governing state rule
No economic unit is assumed state-equivalent across time.

A unit transition may include changes in:
- nominal price;
- package mass, volume, count, or usable quantity;
- calories/nutrition or other domain-specific physical content;
- quality, durability, coverage, or service level;
- mandatory taxes, fees, riders, delivery/access charges, tariffs, or surcharges;
- substitution path;
- quantity acquired;
- producer cost structure and margin;
- household resources, debt service, and unmet essential need.

If any economically relevant attribute changes, continuity of the unit must be evidenced rather than presumed.

## Relationship to ERL transition calculus
The lane consumes the canonical ERL transition tuple and observation/reconstruction/hypothesis ordering. It does not replace or redefine the core calculus.

Physical-economics transition observations map into:
- `S_pre`: prior economic-unit / producer / household / population state;
- `S_post`: subsequent economic-unit / producer / household / population state;
- `C`: evidenced continuity relation for the compared unit/system;
- `E`: price, quantity, quality, income, cost, margin, burden, need, and administrative evidence;
- `P`: provenance and independence posture;
- `U`: opaque/unknown elements, including missing physical quantity or causal pass-through;
- `Q`: transition qualification/state.

Observation first, model second, explanation last remains binding.

## Canonical machine surfaces
- reusable lane contract: `contracts/physical-economics.contract.json`
- canonical state schema: `schemas/physical-economics-state.schema.json`
- consumer seed retained for provenance: `assessments/forecast-calibration/matt-randolph/physical-economic-condition-index-target.v0.1.json`

The reusable contract is authoritative for lane-level machine semantics. The Randolph PECI target remains a consumer-specific seed and must not silently supersede the reusable contract.

## Lane architecture
The reusable lane owns the following component surfaces:
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

A scalar composite is not required and is not currently authorized. The state vector is primary.

## Required native sub-indexes
### Essential Need Satisfaction Index
Purpose: measure how much essential need is satisfied, compressed, substituted, deferred, or unmet.

Must preserve:
- underlying need versus observed quantity;
- food sufficiency;
- energy/service-payment stress and disconnection risk where available;
- transportation sufficiency;
- housing payment difficulty/instability;
- water/utility arrears where available;
- essential quantity/quality compression.

### Population Burden Distribution Index
Purpose: measure who bears physical-economic burden and how unevenly.

Minimum outputs should include where data permit:
- median burden;
- lower-income-quintile burden;
- upper-income-quintile burden;
- burden gap;
- share above frozen essential-burden thresholds;
- geography/tenure/household-size slices where justified.

### Producer Cost-Margin Transmission Index
Purpose: distinguish producer cost compression from margin expansion/contraction and locate where value moves through the chain.

Direct evidence is preferred. Candidate inputs include:
- intermediate input costs;
- labor compensation;
- taxes on production/imports less subsidies;
- gross output/sales;
- gross operating surplus;
- corporate profits from current production;
- wholesale/retail trade margins;
- physical output quantity.

Margin may be inferred only when direct inputs are unavailable, and inferred margin must remain explicitly lower-confidence.

## Canonical record types
`schemas/physical-economics-state.schema.json` currently recognizes:
- `economic_unit_state`
- `essential_need_state`
- `population_burden_state`
- `producer_cost_margin_state`
- `tax_fee_flow`

The schema is structural and does not yet constitute validator activation. Semantic fail-closed validators remain required.

## Adjacent indexes and anti-circularity
Existing indexes may be imported only after validating construction and determining whether they introduce circular assumptions.

### Income
Nominal income/resources are primary.

BLS real earnings may be retained as an adjacent comparator, but CPI-deflated real earnings cannot be the sole purchasing-power denominator for a lane designed partly to test CPI incompleteness.

BEA real DPI is a useful macro comparator, but the lane should preserve nominal DPI and independently reconstruct purchasing power against the physical/essential cost surface.

### Debt and financing
Federal Reserve DSR is a valid aggregate input for scheduled mortgage + consumer debt-service burden relative to DPI, but it does not replace distributional debt burden or non-debt compulsory obligations.

## Taxes, fees, and regulated charges
These are a cross-cutting flow layer, not one undifferentiated scalar.

Each charge must preserve:
- initial/legal payer;
- amount/rate and base where observable;
- producer-side or consumer-side entry point;
- observed downstream pass-through, if any;
- confidence/provenance;
- subsidy/credit offsets where applicable.

No double counting as a charge propagates through the value-flow graph.

## Substitution rule
Substitution is itself a state transition.

Domestic substitution does not erase a decline in mass, nutrition, quality, durability, coverage, service level, or household welfare. Origin and quality/physical state are separate dimensions.

## Physical-unit continuity rule
A product/service compared across time must preserve economically relevant unit attributes. Sticker-price continuity alone is insufficient.

Examples:
- same package price + smaller mass = changed economic unit;
- fixed electricity supply rate + higher mandatory delivery charge = changed delivered-cost state;
- same insurance premium + higher deductible/lower coverage = changed service unit;
- same nominal rent + added mandatory fees = changed housing delivered-cost state.

## Current seed evidence inherited from Randolph research
Research already available to this lane includes:
- USDA ERS F-MAP methodology for package-weight normalization to grams (historical public files, not a 2026 mass series);
- Circana 2026 food dollars/unit/volume/price-mix evidence;
- BEA nominal DPI/PCE and real-DPI comparator evidence;
- Census March 2026 HTOPS direct-burden table structure and secondary-derived burden leads pending direct official-table custody;
- Oncor delivered-electricity charge structure;
- BLS national water/sewer, housing/rent, household-insurance context;
- Federal Reserve DSR methodology;
- BEA industry accounts/corporate profits, BLS trade-margin PPIs, and Census QFR as producer margin/cost sources.

These evidence records remain in the Randolph calibration directory until generalized equivalents are created or linked. Their provenance must not be lost during promotion.

## Promotion boundary
The Physical Economics lane is now a reusable ERL lane with:
- its own canonical mirror handoff;
- a reusable machine contract outside the Randolph assessment directory;
- a canonical JSON Schema for the five core physical-economics record families.

The existing Randolph `physical-economic-condition-index-target.v0.1.json` remains a consumer-specific seed/legacy research artifact and must not be deleted or rewritten merely to hide its origin.

Promotion does NOT yet mean:
- all native sub-indexes are calculated;
- semantic validators are complete;
- a scalar PECI is authorized;
- hosted exact-head validation has passed;
- production activation/release has occurred;
- independent review has occurred.

## Validation requirements
Required fail-closed validators remain:
1. economic-unit continuity: same sticker price cannot establish continuity if quantity/quality/service attributes changed or are materially unknown;
2. unmet-need semantics: lower observed acquisition cannot be mapped to lower essential need without evidence;
3. distribution preservation: aggregate output cannot erase required population strata when source data support them;
4. producer-margin posture: direct/reconstructed/inferred margin evidence modes must remain distinguishable, with inferred residual explicitly lower-confidence;
5. tax/fee flow uniqueness: a charge with the same flow identity cannot be counted twice across propagation nodes.

## Next executable work
1. create semantic fail-closed validators for unit continuity, unmet-need semantics, distribution preservation, margin evidence posture, and tax/fee double counting;
2. create positive and negative fixtures for food shrinkflation, electricity delivery charges, insurance coverage/deductible transitions, and rent-plus-fee transitions;
3. link Randolph calibration explicitly to `contracts/physical-economics.contract.json` without deleting historical research records;
4. prototype the reusable state vector on food, electricity, motor fuel, and housing;
5. add hosted CI for the reusable physical-economics lane;
6. independently review the contract/schema/validator semantics before any composite index or release claim.

## Current posture
- lane promotion: `FORMAL_REUSABLE_ERL_LANE`;
- canonical handoff: complete;
- reusable machine specification: complete;
- canonical state schema: complete for five core record families;
- semantic validators: not yet created;
- hosted exact-head validation: not yet observed;
- native sub-index calculations: not complete;
- composite index: not authorized;
- independent review: not complete;
- release: not authorized.

## Archive posture
This handoff is the source of truth for continuation of ERL Physical Economics work. The lane is formally promoted and machine-addressable, but not yet fully validated, activated, or released.
