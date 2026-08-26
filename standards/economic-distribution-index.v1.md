# Economic Distribution Index Standard v1

## Purpose

Define a reproducible ERL method for measuring how newly created economic value is distributed across labor, capital, consumers, government, creditors, retained enterprise value, and unmet household need.

## Principle

Income, producer margin, and distribution are separate observables.

```text
income != total household value capture
producer margin != distribution
enterprise valuation gain != worker gain
price stability != equitable distribution
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

## Substitution and quality

Domestic or alternative production of lower-quality goods does not count as an unqualified consumer benefit merely because nominal availability rises. Quantity, quality, durability, utility, and effective price must be considered when observable.

## Debt and financing costs

Interest and financing costs affecting households or firms must be tracked separately from income and prices. They may transfer value to creditors without appearing in ordinary consumption-price measures.

## Unmet need

Observed spending is not equivalent to need satisfaction. Where defensible proxies exist, the model may measure foregone or unmet demand due to price, income, availability, financing, or substitution constraints.

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
- missing-data note where applicable.

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

## Promotion gate

No distributional-effect conclusion may be promoted from a single anecdote, policy proposal, enterprise sale, or valuation event. Comparative evidence and explicit controls are required.

## Version state

- version: `1.0-draft`
- conceptual specification: implemented
- machine implementation: pending schema/validator/fixtures
- activation: not claimed
