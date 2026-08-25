# United States Economic Trajectory Mirror Handoff

## Authority

Bounded source of truth for the United States historical-to-present economic trajectory lane in `StegVerse-Labs/Executive_Rhetoric_Ledger`.

Canonical coordination: Issue #78.
Canonical branch: `feature/paired-national-economic-trajectories`.

This lane establishes U.S. observations, mechanisms, affected populations, controls, contradictions, and outcomes independently. Canadian evidence may appear only as an external influence or explicit control; it may not define the U.S. finding.

## Goal

Build a reconstructable U.S. trajectory across:

- total, real, per-capita, median, and distributional economic measures;
- productivity, profits, capital investment, labor, wages, and employment quality;
- housing, healthcare, insurance, food, household debt, savings, and material insecurity;
- trade dependence, domestic productive capacity, tariffs, retaliation, and foreign market loss;
- fiscal, tax, regulatory, immigration, public-service, and transfer policy;
- wealth ownership and distribution;
- AI, automation, robotics, and labor displacement;
- sectoral, state, demographic, and household effects.

## Governing rules

```text
Observation != effect.
GDP or market strength != broad household security.
Tariff revenue != foreign payment without incidence evidence.
Protected capacity != competitive capacity.
Policy timing != policy causation.
Same metric in another country != same U.S. meaning.
Missing evidence != permission to infer.
```

Every material finding must identify the measure, unit, price basis, population denominator, geography, time interval, source revision, transmission mechanism, affected groups, controls, contrary evidence, and confidence.

## Current state

```yaml
lane_id: ERL-ECON-US
status: FRAMEWORK_IMPLEMENTATION
national_findings_authorized: false
comparison_promotion_authorized: false
publication_authorized: false
canonical_issue: 78
```

## Initial implementation

- national trajectory schema;
- shared measurement dictionary;
- U.S. seed registry;
- source and gap matrix;
- validator and deterministic fixtures;
- CI integration.

## Evidence acquisition order

1. BEA national accounts, income, profits, investment, and international trade.
2. BLS labor, wages, productivity, prices, and employment quality.
3. Census income, poverty, inequality, housing, business, and population records.
4. Federal Reserve wealth distribution, credit, household finance, production, and regional evidence.
5. CBO, Treasury, USITC, USTR, federal budget, tariff, trade, and regulatory records.
6. State and sector records needed to resolve distribution and regional effects.
7. OECD, IMF, and World Bank controls with definition reconciliation.
8. Academic and independent analysis for mechanisms and alternatives.
9. Media and social claims only as labeled discovery or rhetoric objects.

## Release conditions

A U.S. trajectory finding may advance only when its national evidence chain is reconstructable and reviewable. Comparative use requires a reviewed U.S. finding ID, not an unreviewed raw observation.

## Remaining work

All evidence population, review, and findings remain pending after the initial framework build.
