# ERL Household Economic Conditions Site Mirror Handoff

## Canonical identity

- Goal Task ID: `ERL-HOUSEHOLD-ECONOMIC-CONDITIONS-SITE-001`
- central handoff: `StegVerse-Labs/.github/docs/ERL_HOUSEHOLD_ECONOMIC_CONDITIONS_SITE_MIRROR_HANDOFF.md`
- ERL issue: `#163`
- Site issue: `StegVerse-Labs/Site#1368`
- coordination state: `ACTIVE`

## ERL authority boundary

ERL owns the evidence/analysis contract for the household economic-conditions surface. Site remains presentation-only. Neither aggregate macro observations nor source acquisition alone may be promoted into a household-welfare finding.

## Merged implementation evidence

PR `#164` merged with expected-head protection at merge commit `03aab5fe5eb75a1d8955d82d820bdd46be015316` after exact head `d47311c2cb7f33a7fa1c460d7756efab8f504ab3` passed all applicable validation lanes. It established:

- `research-data/household-economic-conditions/official-series-inventory.v1.json`;
- `schemas/household-economic-conditions-output.schema.json`;
- `fixtures/household-economic-conditions/fail-closed.fixture.json`;
- `scripts/validate_household_economic_conditions_contract.py`;
- README household-economic-conditions documentation.

PR `#165` merged with expected-head protection at merge commit `b0d51340238b798ba46b36ab13988f1255d43642` after exact head `555d9717e2046653af8ca61ece23617a919217f9` passed:

- `Validate Household Economic Source Bindings` run `35167747226`: `SUCCESS`;
- `Validate Ledger Schemas` run `35167747146`: `SUCCESS`.

It added:

- `research-data/household-economic-conditions/official-series-bindings.v1.json`;
- `scripts/acquire_household_economic_conditions.py`;
- `scripts/validate_household_economic_source_bindings.py`;
- `.github/workflows/validate-household-economic-source-bindings.yml`.

## Exact official source bindings

The current binding manifest records:

- BLS real production/nonsupervisory hourly earnings: `CES0500000032`;
- BLS real production/nonsupervisory weekly earnings: `CES0500000031`;
- BLS CPI-U U.S. city average all items, not seasonally adjusted: `CUUR0000SA0`;
- BEA NIPA monthly Table 2.6: dataset `NIPA`, table `T20600`, line `27` disposable personal income, line `29` PCE, line `35` personal saving rate, line `37` real disposable personal income;
- Board of Governors Household Debt Service Ratios via FRED: `TDSP`, `MDSP`, and `CDSP`, current-method history from 2005;
- New York Fed Household Debt and Credit Q2 2026 release plus exact underlying-workbook URL, with debt-balance and serious-delinquency category semantics retained;
- Census ACS 1-year detailed table `B25140`, including explicit total, owner-with/without-mortgage, renter, over-30-percent, and over-50-percent variables; 2020 remains excluded from standard comparison.

## Acquisition and normalization state

`scripts/acquire_household_economic_conditions.py` now provides fail-closed candidate acquisition and normalization for BLS, BEA, FRED/Board, Census, and New York Fed source material.

- BLS, BEA, FRED, and Census have deterministic normalizers covered by synthetic provider-shaped validation inputs.
- BEA live acquisition requires `BEA_API_KEY`; absence fails closed and does not block other source families.
- New York Fed official workbook bytes can be retained and SHA-256 bound, but worksheet/column-level normalization remains `WORKBOOK_COLUMN_BINDING_PENDING`; no values are guessed or converted to zeros.
- every candidate output carries `finding_authority=false` and `public_activation_authorized=false`.
- raw-source retention and source-vintage metadata precede normalization.

## Household-state and history invariants

The output contract preserves gross labor income, net disposable resources, required-cost burden, debt service, necessary consumption, discretionary residual, saving/dissaving, new borrowing, delinquency/arrears, and unmet/foregone consumption.

Historical rules remain:

- 2000 is a requested horizon, not a forced start;
- series begin at the earliest defensible comparable observation;
- methodology and coverage breaks remain visible;
- incompatible definitions are not silently spliced;
- same-axis absolute comparison requires compatible units/definitions;
- cross-metric trajectories use selected-start normalized indexing;
- historical proxies remain explicitly labeled;
- missing observations remain missing unless a governed reconstruction exists.

## Current state

- official-series inventory: MERGED
- household output schema: MERGED
- fail-closed fixture: MERGED
- deterministic contract/fixture validation: MERGED / PASS
- README reconciliation: MERGED
- exact official source identifiers: MERGED / BOUND
- deterministic BLS/BEA/FRED/Census normalizers: MERGED / PASS
- New York Fed raw workbook binding: MERGED
- New York Fed workbook cell/column normalization: PENDING EXACT BINDING
- cohort joins and required-cost composite construction: PENDING
- live governed household-state generation: NOT IMPLEMENTED
- authentic ERL-to-Site live output binding: NOT IMPLEMENTED
- public activation / served-body verification: NOT OBSERVED

## Next work

Resolve the exact New York Fed workbook worksheet/column map from retained official source evidence, execute bounded live candidate acquisition for credential-free BLS/FRED/Census sources, preserve raw hashes/vintages, add BEA acquisition when TV/TVC-governed API-key custody is available, then construct the first governed multi-source household-state candidate without authorizing public activation. Site may consume only an authenticated governed ERL output after those evidence predicates are satisfied.

## Credential-free required-cost distribution source — ACS B25140

The U.S. Census Bureau ACS 1-year detailed table `B25140` is now bound not only to exact published counts but also to six deterministic non-authorizing housing-cost-burden shares: over-30% and over-50% for owner units with a mortgage, owner units without a mortgage, and renters. These ratios are computed only from the exact B25140 numerator/denominator variables already bound in the manifest.

This advances `required_cost_burden` evidence only for housing-cost distribution. It does not represent total household required costs, disposable residual capacity, or welfare. Standard ACS 1-year comparability begins at 2005 here, and 2020 experimental 1-year estimates remain excluded. The source requires no provider credential; raw Census API bytes are still hashed before normalization and the candidate retains `finding_authority=false` and `public_activation_authorized=false`.

## Live ACS B25140 acquisition alignment — 2026-09-21

The credential-free live acquisition entrypoint `scripts/acquire_census_b25140.py` now emits the same six bounded housing-cost-burden shares as the canonical binding: over-30% and over-50% for mortgaged owners, owners without mortgages, and renters. The direct ACS counts and margins of error remain retained, the raw official Table-Based Summary File is SHA-256 bound before normalization, and the derived shares are labeled `DERIVED_FROM_DIRECT_OBSERVATIONS` with `finding_authority=false`.

This remains only `HOUSING_COST_BURDEN_ONLY`; it does not establish total required-cost burden or public activation.

