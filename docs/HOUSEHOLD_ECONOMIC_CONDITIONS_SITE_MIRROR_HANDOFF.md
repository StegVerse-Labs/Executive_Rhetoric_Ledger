# ERL Household Economic Conditions Site Mirror Handoff

## Canonical identity

- Goal Task ID: `ERL-HOUSEHOLD-ECONOMIC-CONDITIONS-SITE-001`
- central handoff: `StegVerse-Labs/.github/docs/ERL_HOUSEHOLD_ECONOMIC_CONDITIONS_SITE_MIRROR_HANDOFF.md`
- ERL issue: `#163`
- ERL PR: `#164`
- Site issue: `StegVerse-Labs/Site#1368`
- branch: `feat/household-economic-conditions-series-163`
- coordination state: `ACTIVE`

## Scope

ERL owns the evidence/analysis contract for the persistent household economic-conditions surface. Site is presentation-only and may not derive unsupported findings.

## Implemented in this branch

1. `research-data/household-economic-conditions/official-series-inventory.v1.json`
   - records source agency, source family, frequency, units, earliest comparable date, page display start, revision semantics, structural breaks, limitations, and current admission state;
   - explicitly records the Federal Reserve DSR methodology replacement and limits the current-method series to 2005 forward;
   - records the NY Fed main CCP continuity boundary at 2003, separate 1999-2003 historical material, and the 2003 student-loan reporting reliability boundary;
   - records ACS 2020 experimental 1-year noncomparability and the Census-2000-to-ACS comparison boundary.
2. `schemas/household-economic-conditions-output.schema.json`
   - machine contract for current household-state components, evidence states, freshness, series observations, source vintage, comparison mode, and methodology breaks;
   - `public_activation_authorized` is explicit and fail-closed.
3. `fixtures/household-economic-conditions/fail-closed.fixture.json`
   - UI-only normalized-index fixture;
   - carries no live finding and sets `public_activation_authorized=false`.

## Required household state

The output contract preserves gross labor income, net disposable resources, required-cost burden, debt service, necessary consumption, discretionary residual, saving/dissaving, new borrowing, delinquency/arrears, and unmet/foregone consumption.

No positive macro or spending indicator may be promoted into a household-welfare finding without the required household-state evidence.

## Historical comparison rules

- 2000 is a requested display horizon, not a promise that every series begins there.
- A series begins at the earliest defensible directly comparable date.
- Incompatible definitions are separate segments; no silent splicing.
- Methodology and coverage breaks are visible.
- Same-axis absolute overlays require same unit and definition.
- Cross-metric trajectories use selected-start normalized index mode.
- Historical proxies remain `DERIVED_HISTORICAL_PROXY`.
- Gaps remain gaps without a governed reconstruction method.

## Source inventory findings

- BLS CPI-U all-items supports history well before 2000; 2000 is therefore a safe page floor for the selected current series.
- BLS CES production/nonsupervisory real earnings reaches back at least to the 1960s depending on series/industry; 2000 is a safe page floor for total-private context, but gross earnings are not net take-home pay.
- BEA monthly personal-income/disposition series provide history before 2000 and are revision-sensitive; every public observation must expose vintage.
- Federal Reserve current-method DSR is available from 2005 forward. The archived prior-method 1980-2024 series is a separate methodology segment and must not be spliced into the current line.
- New York Fed Consumer Credit Panel public household-debt reporting has a main continuity lane from 2003, with separately provided 1999-2003 historical data. Student-loan data are reliable from 2003.
- ACS standard 1-year comparisons begin in 2005 for this lane; the 2020 experimental 1-year release is noncomparable, and Census 2000 comparison requires table/universe/question review rather than direct splicing.

## Validation evidence

Current exact head: `432697db308fa183a566f69af88219c910e1912c`.

- `Validate Ledger Schemas` run `35162542553`: `SUCCESS`.

This establishes repository schema consistency for the branch only. It does not establish authentic official-data acquisition, live household-state generation, Site transport, deployment, or public activation.

## Current state

- official-series inventory: IMPLEMENTED ON PR #164
- household output schema: IMPLEMENTED ON PR #164
- fail-closed fixture: IMPLEMENTED ON PR #164
- exact-head ledger validation: PASS
- README.md reconciliation: PENDING
- exact agency-series identifiers and automated acquisition bindings: PENDING
- dedicated deterministic schema/fixture tests: PENDING
- cohort joins and required-cost composite construction: PENDING
- live governed household-state generation: NOT IMPLEMENTED
- authentic ERL-to-Site output binding: NOT IMPLEMENTED
- public activation / served-body verification: NOT OBSERVED

## Next work

Reconcile `README.md`, add dedicated deterministic validator/tests for the output contract and fixture, bind exact official series identifiers and acquisition/normalization semantics, re-run exact-head validation, and only then merge with expected-head protection. Live output and public activation remain separate later evidence predicates.
