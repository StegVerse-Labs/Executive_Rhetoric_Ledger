# Economic Distribution Index Standard v1

## Purpose

Define a reproducible ERL method for measuring how newly created economic value is distributed across labor, capital, consumers, government, creditors, retained enterprise value, and unmet household need.

## Principle

Income, producer margin, distribution, household condition, and mobility are separate observables.

```text
income != total household value capture
producer margin != distribution
enterprise valuation gain != worker gain
price stability != equitable distribution
CPI != household economic condition
national economic resilience != household economic resilience
household resilience != upward social mobility
```

## Unit of analysis

A calculation may be performed at enterprise, sector, region, household cohort, or economy level, but every observation must declare its unit and time window.

## Required value channels

An admissible distribution observation should classify available value into as many of the following channels as evidence supports:

- `labor_cash_compensation`
- `labor_non_cash_benefits`
- `employee_equity_grants`
- `employee_equity_appreciation`
- `executive_founder_equity_appreciation`
- `external_shareholder_appreciation`
- `retirement_household_asset_appreciation`
- `consumer_price_or_quality_benefit`
- `government_tax_capture`
- `creditor_financing_capture`
- `retained_enterprise_surplus`
- `unmet_need_or_foregone_consumption`
- `unknown_unallocated`

## Ownership Distribution / Capital Participation sub-index

The ownership component must preserve both breadth and value. At minimum, where evidence exists, calculate:

1. participation rate among covered workers;
2. participation rate by wage/income band;
3. equity grant value relative to compensation;
4. vested versus unvested value;
5. realized versus unrealized gains;
6. employee share of total equity appreciation;
7. executive/founder share of total equity appreciation;
8. external shareholder share of total equity appreciation;
9. household retirement-account exposure where traceable;
10. ownership concentration before and after the measurement period.

A high employee participation rate with negligible value must not be scored as equivalent to meaningful capital participation.

## Producer Margin separation

Producer Margin answers: how much distributable economic space exists?

Distribution answers: where did created value go?

A valid implementation must permit cases such as:

- rising margin with falling labor share;
- falling margin with stable labor share;
- rising wages funded by higher consumer prices;
- flat wages with substantial employee equity appreciation;
- rising enterprise valuation with no broad employee participation.

## CPI and household-cost boundary

CPI is an admissible price-change input, not a complete household-welfare or household-resilience measure.

A household-level implementation should distinguish, where evidence permits:

- `price_level_change`;
- `household_required_cost_burden`;
- `household_discretionary_capacity`;
- `substitution_quality_loss`;
- `financing_cost_burden`;
- `unmet_need`;
- `asset_access_and_accumulation`;
- `mobility_probability`.

Observed expenditure must not be interpreted as proof that household needs were fully met. Consumption that disappears because it becomes unaffordable, unavailable, or inaccessible must remain eligible for explicit unmet-need treatment.

## Household Economic State

Where source quality supports reconstruction, ERL may calculate a household or household-cohort state using required costs rather than relying on representative-basket inflation alone:

```text
earned_and_transfer_income
- housing_required_cost
- food_required_cost
- energy_and_utilities
- transportation_required_cost
- healthcare_required_cost
- childcare_required_cost
- taxes
- debt_and_financing_costs
- quantified_substitution_or_quality_loss
- quantified_unmet_need
= usable_household_capacity
```

The household state should preserve separate variables for savings capacity, wealth accumulation/depletion, asset access, intergenerational transfer dependence, education cost/return, geographic opportunity access, and mobility where evidence exists.

## National-to-household hierarchy

Cross-economy comparison should preserve distinct analytical layers:

```text
Sovereign Resilience
  -> Productive Economy
  -> Household Condition
  -> Distribution
  -> Mobility
  -> Opportunity
```

Improvement at one layer does not establish improvement at another. Increased trade diversification may coexist with worsening household affordability. Increased domestic production may coexist with higher required-cost burden, financing costs, quality loss, or reduced purchasing power.

## Substitution and quality

Domestic or alternative production of lower-quality goods does not count as an unqualified consumer benefit merely because nominal availability rises. Quantity, quality, durability, utility, and effective price must be considered when observable.

## Debt and financing costs

Interest and financing costs affecting households or firms must be tracked separately from income and prices. They may transfer value to creditors without appearing in ordinary consumption-price measures.

## Unmet need

Observed spending is not equivalent to need satisfaction. Where defensible proxies exist, the model may measure foregone or unmet demand due to price, income, availability, financing, or substitution constraints.

## Mobility and opportunity transmission

Mobility is a longitudinal consequence lane, not a synonym for current income or current consumption.

Where evidence permits, ERL should preserve:

- parent-child income or wealth mobility;
- movement across income/wealth quantiles;
- homeownership and asset access by cohort;
- dependence on inheritance or family-assisted acquisition;
- education cost, debt, and realized earnings return;
- geographic opportunity access;
- labor-market access and stability;
- social/opportunity-network access where measurable.

A household may meet current consumption needs while losing savings capacity, asset access, or future mobility. Those states must not be collapsed into a single present-period welfare score.

## Historical-depth and proxy rule

The start date of a modern dataset must not be treated as the start date of the underlying phenomenon.

When direct historical observations are unavailable, ERL may extend a trajectory using documented proxy series, but every datum or derived component must retain an evidence class:

- `DIRECT_OBSERVATION`;
- `DERIVED_HISTORICAL_PROXY`;
- `INFERRED_RELATIONSHIP`.

Derived historical proxies must never be represented as direct observations. Missing or incomparable historical data must remain visible and reduce confidence.

Historical reconstruction may use, where defensible, long-run series for real wages/disposable income, housing burden, rent burden, household debt, debt service, financing costs, homeownership by age/cohort, wealth concentration, education cost and returns, labor share, savings, essential-cost burdens, and regional opportunity differences.

Where direct and proxy measures overlap, the implementation should validate whether the proxy tracks the direct series before using it to characterize earlier periods.

## Structural-break test

Longitudinal interpretation should explicitly distinguish among:

- a new structural break;
- a recurring cycle;
- continuation of a longer trend;
- measurement artifacts caused by source or definition changes.

No structural-break conclusion should be promoted solely because a short modern series changes direction.

## Distribution identity

For a bounded observation period, the implementation should attempt reconciliation:

```text
created_or_available_value
≈ labor_capture
+ employee_capital_capture
+ nonemployee_capital_capture
+ consumer_capture
+ government_capture
+ creditor_capture
+ retained_enterprise_surplus
+ unmet_need_effect
+ unknown_unallocated
```

The equality may be imperfect because sources use different accounting boundaries. Any residual must remain visible as `unknown_unallocated`; it must not be silently assigned.

## Missing evidence

Missing or incomparable data must reduce confidence, not be replaced with assumed neutral values.

Every calculated component must carry:

- source reference;
- observation date/range;
- accounting basis where known;
- nominal/real status;
- confidence;
- missing-data note where applicable;
- evidence class when a historical proxy or inference is used.

## Policy comparison

The index may compare mechanisms such as broad employee equity, ESOPs, profit sharing, wage-only compensation, tax-and-transfer systems, wealth taxation, and cooperative ownership. It must not equate advocacy with evidence of causal effectiveness.

For the Mark Cuban policy seed, ERL must preserve separately:

- proposal text;
- claimed mechanism;
- historical examples;
- observed outcomes;
- selection effects;
- acquisition/IPO effects;
- counterexamples;
- tax-incidence consequences.

## Country comparison rule

Canada, United States, and other national lanes should be reconstructed independently before comparison. ERL must not force one country's definitions, household composition, tax treatment, housing tenure, or consumption basket onto another without explicit normalization.

A categorical claim that one country is economically "better" than another is not admissible from a single macro indicator, CPI series, or foresight scenario. Comparative findings require explicit layer, time range, normalization, and evidence boundaries.

## Promotion gate

No distributional-effect conclusion may be promoted from a single anecdote, policy proposal, enterprise sale, valuation event, macro indicator, or foresight scenario. Comparative evidence and explicit controls are required.

## Version state

- version: `1.0-draft`
- conceptual specification: implemented and extended for household resilience/mobility
- machine implementation: pending schema/validator/fixtures
- activation: not claimed
