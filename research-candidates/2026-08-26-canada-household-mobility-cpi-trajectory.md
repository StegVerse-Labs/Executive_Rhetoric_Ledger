# Canada household mobility, CPI, and trajectory research seed

Date: 2026-08-26
Status: `research_candidate`
Lane: economic distribution / household value capture

## Source seed

Primary foresight source:

- Policy Horizons Canada, *Future Lives: Social mobility in question* (2025-01-10)
- https://horizons.service.canada.ca/en/2025/01/10/future-lives-social-mobility/index.shtml

The source is admitted as a foresight and taxonomy source, not as proof that its 2040 scenario will occur.

## Research insight

The Canada source operates closer to the household and intergenerational level than headline macroeconomic indicators. It raises a distinction that must be preserved in ERL:

```text
national economic resilience
!= household economic resilience
!= upward social mobility
```

An economy can remain resilient in aggregate while households experience declining purchasing power, affordability, asset access, savings capacity, and opportunity transmission.

## CPI boundary

CPI remains a useful price-change input but is not treated as a complete measure of household economic condition.

ERL must distinguish:

1. `price_level_change` — representative-basket price movement;
2. `household_required_cost_burden` — actual required costs relative to household resources;
3. `household_discretionary_capacity` — resources remaining after required costs;
4. `substitution_quality_loss` — maintenance of consumption through lower quality, durability, utility, or quantity;
5. `financing_cost_burden` — interest and credit costs that may rise independently of CPI;
6. `unmet_need` — required or welfare-relevant consumption that no longer occurs because it is unaffordable, unavailable, or inaccessible;
7. `asset_access_and_accumulation` — ability to acquire housing, savings, retirement assets, or other wealth-bearing assets;
8. `mobility_probability` — ability of a household or its children to improve economic position over time.

Observed spending must not be interpreted as full need satisfaction. A household may reduce or cease consumption of an item because of cost pressure, causing the unmet need to disappear from expenditure data rather than appear as a larger observed price increase.

## Household Economic State model

Where evidence permits, ERL should reconstruct:

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

This is followed by separate state variables for:

- savings capacity;
- wealth accumulation/depletion;
- homeownership and other asset access;
- intergenerational wealth transfer dependence;
- education cost and return;
- geographic opportunity access;
- social/opportunity-network access;
- upward/downward mobility probability.

## National-to-household comparison hierarchy

Comparative economy work should not collapse all performance into one national score. The preferred hierarchy is:

```text
Sovereign Resilience
  -> Productive Economy
  -> Household Condition
  -> Distribution
  -> Mobility
  -> Opportunity
```

Canada and United States lanes should remain independently reconstructed. Cross-country comparisons are outputs of those lanes, not organizing assumptions.

A country may improve trade-market diversification and sovereign resilience while household affordability or mobility deteriorates. A country may increase domestic production while households absorb higher prices, financing costs, lower-quality substitution, or reduced purchasing power.

## Historical-depth limitation

The Horizons source is useful as a modern framework but several mobility and household measures lack long directly comparable histories. ERL must not mistake the start date of a modern dataset for the start date of the underlying phenomenon.

Historical reconstruction should use deeper proxy series where direct observations do not exist, including where defensible:

- real wages and disposable income;
- housing-price-to-income and rent-to-income ratios;
- household debt and debt-service burden;
- interest and financing costs;
- homeownership by age/cohort;
- wealth and asset concentration;
- education attainment, cost, debt, and earnings premium;
- labor share and compensation share;
- household savings rates;
- food, energy, transportation, healthcare, and childcare burden;
- regional/geographic opportunity differences;
- inheritance and family-assisted asset acquisition where data permit.

## Evidence-state rule

Historical extensions must preserve evidence class:

- `DIRECT_OBSERVATION` — directly measured series or administrative observation;
- `DERIVED_HISTORICAL_PROXY` — reconstructed indicator supported by documented inputs and method;
- `INFERRED_RELATIONSHIP` — hypothesized or modeled relationship not directly observed.

Derived proxies must never be represented as direct observations. Missing historical data reduces confidence and remains visible.

## Structural-break question

The lane should explicitly test whether observed deterioration represents:

- a new structural break;
- a recurring economic cycle;
- a continuation of a longer historical trend;
- or a measurement artifact caused by a change in available data.

## Integration with Economic Distribution Index

This research seed extends the existing Economic Distribution lane rather than creating an unrelated Canada-only framework.

Required integrations:

- CPI becomes one input to household cost exposure rather than a proxy for household welfare;
- distribution measures who captures newly created value;
- substitution and unmet need capture hidden welfare losses;
- financing cost remains separate from ordinary consumer prices;
- household condition connects current distribution to savings and asset access;
- mobility measures the longitudinal/intergenerational consequence of household conditions;
- national resilience remains analytically separate from household resilience.

## Research gap queue

1. Identify Statistics Canada and other official Canadian series capable of extending household burden history before the recent mobility datasets.
2. Build directly comparable U.S. series without forcing Canadian definitions onto U.S. data.
3. Define normalization rules across changes in household composition, tax treatment, housing tenure, consumption baskets, and demographic structure.
4. Build overlap periods where direct mobility observations and historical proxies coexist, then test proxy validity.
5. Add structural-break and trend-continuity tests.
6. Add household cohort segmentation so averages cannot conceal divergent outcomes by income, age, housing tenure, geography, or wealth position.
7. Preserve uncertainty around AI/labor and social-network effects where historical evidence is shallow.

## Promotion boundary

No claim that Canada or the United States is categorically "doing better" may be promoted from a single macro indicator, CPI series, or foresight scenario. Comparative findings require independent national trajectories and explicit household/distribution/mobility evidence.

Activation authorized: `false`
