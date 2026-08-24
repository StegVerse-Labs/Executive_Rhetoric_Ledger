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

A title-only source may support only the proposition literally bounded by the title until the embedded video/transcript is acquired. A displayed clock time without a verified timezone is not promoted to an absolute timestamp.

## Current durable surfaces

- `research-candidates/matt-randolph-four-month-forecast-calibration.md`
- `assessments/forecast-calibration/matt-randolph/source-manifest.json`
- `assessments/forecast-calibration/matt-randolph/world-event-chronology.json`
- `assessments/forecast-calibration/matt-randolph/official-economic-series-2026-06-08-through-08-17.json`
- `assessments/forecast-calibration/matt-randolph/MR-2026-03-07-third-week.forecast.json`
- `assessments/forecast-calibration/matt-randolph/MR-2026-07-08-diesel-inflation.forecast.json`
- `assessments/forecast-calibration/matt-randolph/MR-2026-07-13-watch-diesel.forecast.json`
- `docs/forecast-calibration/MATT_RANDOLPH_FORECAST_CALIBRATION_MIRROR_HANDOFF.md`
- transition-calculus schemas/validators/fixtures under Issue #74 / PR #75

## Validation state

Transition-calculus validation is a live-record gate rather than a fixture-only gate.

Previously hosted evidence:

- run `32688098190`: transition calculus and forecast adapter PASS;
- run `32688562968`: transition calculus, forecast adapter, and negative fail-closed tests PASS;
- run `32688912551`: transition calculus, live forecast-calibration records, and negative fail-closed tests PASS on head `50a8d705ef2ebbbd951411d8010570e99267d4aa`;
- research-candidate activation runs `32688912585` and subsequent validated heads: PASS.

The live validation pass followed a fail-closed detection and repair: date-only first-party publication evidence initially exposed a schema precision defect. The schema now accepts bounded date or date-time evidence rather than fabricating an exact clock time.

The current branch adds two additional live Randolph forecast records and an official-series bundle. Changes below `assessments/forecast-calibration/**` are included in the transition-calculus workflow trigger paths, so these records remain inside the hosted validation boundary.

At this handoff update the connector has not yet surfaced a completed hosted workflow run specifically for the newest head. Therefore no exact-head PASS is claimed for the newest commit until such a run is observable.

The repository-wide `Validate Ledger Schemas` workflow remains separately blocked by the pre-existing August 22 White House ballroom primary-record-intake record. That failure is outside this bounded lane and is not masked here.

## First-party corpus acquisition

Source manifest now contains March/April antecedents plus materially expanded June-August first-party candidates.

Newly located June-August objects include:

- 2026-06-17 — `My Opening Statement To The Senate Energy and Natural Resources Committee`
- 2026-06-19 — `Iran Suspends Negotiations`
- 2026-06-24 — `Trump Blames Oil Companies For High Gas Prices`
- 2026-06-25 — `How Gas Prices Work`
- 2026-07-01 — `When Cheap Oil Doesn’t Mean Cheap Gas`
- 2026-07-06 — `Impact Of Two New Canadian Oil Pipelines`
- 2026-07-08 — `Higher Diesel Means Higher Inflation`
- 2026-07-13 — `Watch Gas and Diesel Prices Not Oil`
- 2026-07-16 — `It's About The Diesel`
- 2026-07-17 — `The New Oil`
- 2026-07-17 — `MAJOR Escalation In Middle East`
- 2026-07-20 — `Why Isn’t Oil Higher?`
- 2026-07-25 — `Iran Isn’t Out of Options We Are`
- 2026-08-03 — `Trump Demands Oil Companies Return Profits To The People`
- 2026-08-04 — `Thirty Dollar Discount On Iraqi Oil`
- 2026-08-06 — `Oil Up Big As Markets Start To See Reality`
- 2026-08-07 — `Words Matter`
- 2026-08-10 — `Oil Up Big Today`
- 2026-08-11 — `Our own version of OPEC`
- 2026-08-14 — `I Report The News`
- 2026-08-15 — `Is The Global Oil Machine Robbing You?`

These are `LOCATED`, not automatically fully custodied. Embedded video/transcript acquisition remains required before extracting propositions stronger than displayed titles.

Retrospective/self-characterization objects such as `I Report The News` are explicitly excluded from independent outcome verification.

## Independent official-series evidence installed

The official-series bundle now preserves:

### EIA weekly U.S. on-highway diesel

- 2026-06-08 — $5.210/gal
- 2026-06-15 — $5.059
- 2026-06-22 — $4.832
- 2026-06-29 — $4.668
- 2026-07-06 — $4.578
- 2026-07-13 — $4.796
- 2026-07-20 — $5.134
- 2026-07-27 — $5.313
- 2026-08-03 — $5.348
- 2026-08-10 — $5.257
- 2026-08-17 — $5.454

This establishes a decline into July 6 followed by a sharp reversal upward after the July 8 and July 13 diesel-focused notes. Temporal ordering is preserved without promoting it to causation or predictive superiority.

### EIA distillate inventory posture

For the week ending July 17, distillate inventories increased 1.4 million barrels but remained 10% below the previous five-year average. This distinguishes short-term replenishment from persistent inventory tightness.

### BLS July CPI

- all items: +0.1% month over month, +3.4% year over year;
- food: +0.1% month over month, +3.0% year over year;
- energy: -1.5% month over month, +14.7% year over year;
- gasoline: -2.9% month over month, +24.6% year over year;
- fuel oil: -1.7% month over month, +39.1% year over year.

### BLS July PPI/freight

- final demand: unchanged month over month, +4.7% year over year;
- final-demand energy: -3.1% month over month;
- truck transportation of freight: -1.8% month over month;
- processed-goods intermediate-demand diesel: -6.7% month over month.

The resulting calibration rule is important: elevated annual energy stress and rising later-July/August retail diesel do not imply every monthly inflation/freight measure must rise simultaneously. Lead/lag structure must come from the original forecast, not be invented after observing the data.

## Machine forecast records

### March 7 — three-week Hormuz threshold

File: `MR-2026-03-07-third-week.forecast.json`

State: `UNRESOLVED`.

Resolution still requires explicit operational definitions for `closed`, the three-week start boundary, `global recession begins to take hold`, and what counts as international intervention stopping the closure.

### July 8 — higher diesel / higher inflation

File: `MR-2026-07-08-diesel-inflation.forecast.json`

State: `UNRESOLVED`.

Current evidence supports a real test but not a verdict. Diesel accelerated materially after the note; year-over-year consumer energy inflation remained high. At the same time, July monthly CPI energy, PPI energy, freight, and intermediate diesel measures declined. The embedded video must establish whether Randolph predicted immediate movement, lagged pass-through, level persistence, or directional acceleration.

### July 13 — watch gas/diesel, not oil

File: `MR-2026-07-13-watch-diesel.forecast.json`

State: `UNRESOLVED`.

The title defines an indicator-selection proposition. Official data show diesel rose sharply after July 13 and distillate inventories remained below normal, but predictive superiority over crude cannot be scored until a fixed target variable, lag structure, and comparison rule are defined from the source rather than retrospectively selected.

## Next acquisition/build queue

1. Acquire embedded videos/transcripts behind the June-August source candidates and hash/preserve stable source objects where possible.
2. Add EIA weekly refinery utilization/capacity utilization.
3. Add EIA distillate refinery production, imports, and exports.
4. Add crude benchmark series for direct gas/diesel-versus-crude predictive comparison.
5. Add BLS detailed trucking/freight service series over March-August, not only release-summary values.
6. Add food-price and agriculture/freight series sufficient to test the March 18 shipping-fuel-to-food mechanism.
7. Encode the April 8 `Diesel Is Everything`, June 25 `How Gas Prices Work`, July 1 `When Cheap Oil Doesn’t Mean Cheap Gas`, and July 16 `It's About The Diesel` records once their proposition text is adequately preserved.
8. Define predeclared lag and scoring lanes before resolving the July indicator/inflation records.
9. Keep open six-to-nine-month forecasts separate from resolved historical calibration until earlier forecast scoring is materially complete.

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
- What lag did Randolph actually specify between diesel/refined-product shocks and CPI/PPI/freight/food transmission?
- Which predicted transmission mechanisms materialized first: marine fuel, diesel, freight, food, utilities, industrial inputs, or broader CPI/PPI?
- How should still-open six-to-nine-month claims be weighted after calibration of earlier conditional forecasts?

## Current quantitative posture

For the Randolph calibration lane, denominator = 10 bounded work groups:

1. durable owner/handoff — complete;
2. source policy/manifest — materially developed, still acquiring full objects;
3. first-party corpus acquisition — materially expanded, transcript custody incomplete;
4. independent world-event chronology — materially developed, more shipping/policy events remain;
5. machine forecast encoding — 3 live records installed;
6. EIA/refined-product data integration — started with weekly diesel and distillate inventory; refinery/import/export lanes remain;
7. BLS/freight/food inflation integration — started with July CPI/PPI; detailed freight/food history remains;
8. conditional state resolution across corpus — methodology active, no premature final resolutions;
9. aggregate calibration and open-forecast confidence posture — not started;
10. independent review/promotion decision — not started.

Goal activation estimate: 40%.

## Release boundary

No publication, person-level credibility finding, downstream propagation, tag, or release is authorized from this lane yet.

## Archive posture

The research methodology, expanded source corpus, independent Hormuz/economic chronology, official EIA/BLS series, three encoded forecast records, validation posture, and next acquisition tasks are durable here. Continued acquisition does not require the full originating conversation.
