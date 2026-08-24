# Matt Randolph Forecast Calibration Mirror Handoff

## Authority

Bounded continuation source for the Matt Randolph / Mr Global forecast-calibration research lane.

Canonical owner: Issue #76 — `Calibrate Matt Randolph four-month energy and Iran forecasts`.

This work consumes the transition-first forecast adapter under Issue #74 / PR #75. It does not redefine the transition calculus and does not authorize aggregate credibility findings before source acquisition and independent outcome reconstruction are materially complete.

## Goal

Reconstruct approximately four months of Matt Randolph's substantive energy/Iran-conflict forecasting and evaluate the forecasts against what actually occurred, including whether pre-stated contingencies caused the delays, accelerations, invalidations, or revisions he said they would cause.

## Core evaluation rule

Evaluate the forecast as issued, not a simplified paraphrase.

For every forecast preserve separately:

- issue timestamp at the resolution actually evidenced; never invent clock precision;
- exact or bounded proposition;
- forecast horizon;
- stated assumptions;
- stated contingencies;
- predicted effect of each contingency;
- later forecast-state changes;
- independently reconstructed world-state transitions;
- provenance/dependency posture;
- endpoint, timing, mechanism, and contingency calibration.

## Current durable surfaces

- `research-candidates/matt-randolph-four-month-forecast-calibration.md`
- `assessments/forecast-calibration/matt-randolph/source-manifest.json`
- `assessments/forecast-calibration/matt-randolph/world-event-chronology.json`
- `assessments/forecast-calibration/matt-randolph/MR-2026-03-07-third-week.forecast.json`
- `docs/forecast-calibration/MATT_RANDOLPH_FORECAST_CALIBRATION_MIRROR_HANDOFF.md`
- transition-calculus schemas/validators/fixtures under Issue #74 / PR #75

## Validation state

Transition-calculus validation is now a live-record gate rather than a fixture-only gate.

Hosted evidence:

- run `32688098190`: transition calculus and forecast adapter PASS;
- run `32688562968`: transition calculus, forecast adapter, and negative fail-closed tests PASS;
- run `32688912551`: transition calculus, live forecast-calibration records, and negative fail-closed tests PASS on head `50a8d705ef2ebbbd951411d8010570e99267d4aa`;
- research-candidate activation run `32688912585`: PASS.

The live validation pass followed a fail-closed detection and repair: date-only first-party publication evidence initially exposed a schema precision defect. The schema now accepts bounded date or date-time evidence rather than fabricating an exact clock time.

The repository-wide `Validate Ledger Schemas` workflow remains separately blocked by the pre-existing August 22 White House ballroom primary-record-intake record. That failure is outside this bounded lane and is not masked here.

## Initial primary-source candidates located

- 2026-03-07 — `The 3rd Week Is Critical`
- 2026-03-13 — `Why The U.S. Can't Just Ramp Up Oil Production`
- 2026-03-15 — `The Worst Possible Way`
- 2026-03-18 — `Pay Attention to Shipping Fuel, It's at All Time Record Highs. That's Bad.`
- 2026-03-31 — `The Closure of Bab-El-Mandeb Strait`
- 2026-04-06 — `The Infrastructure War Has Started`
- 2026-04-08 — `Diesel Is Everything`
- 2026-04-10 — `The Greatest Weapon of All. The Strait of Hormuz`
- 2026-04-21 — `They Sold Your Oil But Sent You The Bill`
- 2026-05-01 — `Words Matter, But None More Than The Words Of The President`
- 2026-07-08 — `Higher Diesel Means Higher Inflation`
- 2026-07-13 — `Watch Gas and Diesel Prices Not Oil`
- 2026-07-16 — `It's About The Diesel`

March antecedents are retained because they contain explicit threshold/contingency language that may remain active inside the requested four-month calibration window.

## First encoded forecast — March 7 three-week threshold

The first machine-readable forecast is installed as `MR-2026-03-07-third-week.forecast.json`.

Current state: `UNRESOLVED`.

The source states that Hormuz could not remain closed beyond about three weeks without global recession beginning to take hold and countries acting to stop it. Independent chronology currently establishes:

- the war/de facto-closure boundary reported from February 28;
- an announced temporary commercial reopening on April 17;
- continuing IRGC authorization/restriction and unresolved mine risk on April 17;
- traffic again near standstill by April 20;
- severe closure/disruption still present April 28 despite isolated vessel crossings.

This is deliberately not scored yet. Resolution requires explicit operational definitions for:

1. `closed`;
2. the start of the three-week clock;
3. `global recession begins to take hold`;
4. `countries around the world put a stop to it`.

The provisional March 21 threshold in the machine record is derived from the independently reported February 28 de facto-closure start plus three weeks and is explicitly marked provisional rather than attributed to Randolph as a verified chosen anchor.

## Source acquisition state

`PARTIAL / ACTIVE`.

Required next source work:

1. capture original Randolph source objects/transcripts and stable publication timestamps;
2. resolve exact first-party source URLs for archive-index-only March/April objects;
3. identify additional June–August forecast objects across Substack, YouTube, TikTok, and other first-party surfaces;
4. preserve later Randolph updates separately from original forecasts;
5. extend independent event chronology using EIA, BLS, IEA/public agency records, official government records, Reuters/AP, shipping/refining sources, and other authoritative datasets;
6. encode each sufficiently sourced forecast into `forecast-calibration.schema.json`;
7. calculate no aggregate credibility score until material corpus completeness is established.

## Provenance rule

Randolph's later statement that an earlier forecast occurred is not independent confirmation.

Two outside sources that share the same upstream dataset or reporting lineage must not be double-counted as independent confirmation.

Unknown provenance receives bounded weight until independence or dependency is evidenced.

## Credentials rule

Expertise and credentials may inform source context and the prior reason to examine a forecast closely, but they do not substitute for outcome evidence.

Credentials themselves should be source-postured rather than inferred from biography repetition.

## Current calibration questions

- Did the explicit three-week Hormuz threshold predict the observed timing/mechanism, and what events altered that path?
- Did ceasefires, partial reopening, rerouting, policy interventions, sanctions changes, refinery responses, or other pre-stated contingencies delay rather than falsify later shortage forecasts?
- Were diesel/refined-product indicators more predictive than crude oil price for U.S. and global goods-price stress?
- Which predicted transmission mechanisms materialized first: marine fuel, diesel, freight, food, utilities, industrial inputs, or broader CPI/PPI?
- How should still-open six-to-nine-month claims be weighted after calibration of earlier conditional forecasts?

## Current quantitative posture

For the Randolph calibration lane, denominator = 10 bounded work groups:

1. durable owner/handoff — complete;
2. source policy/manifest — partial;
3. first-party corpus acquisition — partial;
4. independent world-event chronology — partial;
5. machine forecast encoding — started, 1 record;
6. EIA/refined-product data integration — not started;
7. BLS/freight/food inflation integration — not started;
8. conditional state resolution across corpus — not started;
9. aggregate calibration and open-forecast confidence posture — not started;
10. independent review/promotion decision — not started.

Goal activation estimate: 25%.

## Release boundary

No publication, person-level credibility finding, downstream propagation, tag, or release is authorized from this lane yet.

## Archive posture

The research methodology, initial source set, independent chronology seed, first encoded forecast, validation posture, and next acquisition tasks are durable here. Continued acquisition does not require the full originating conversation.
