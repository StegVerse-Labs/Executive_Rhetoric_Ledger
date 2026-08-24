# Matt Randolph Forecast Calibration Mirror Handoff

## Authority

Bounded continuation source for the Matt Randolph / Mr Global forecast-calibration research lane.

Canonical owner: Issue #76 — `Calibrate Matt Randolph four-month energy and Iran forecasts`.

This lane consumes the transition-first forecast adapter under Issue #74 / PR #75. It does not authorize aggregate credibility findings before source acquisition, independent outcome reconstruction, governed component scoring, and independent review are materially complete.

## Goal

Reconstruct approximately four months of Matt Randolph's substantive energy/Iran-conflict forecasting and evaluate forecasts against observed events while preserving assumptions, contingencies, timing, provenance, partial mechanism support, and unresolved state.

## Core evidence rules

- Evaluate the forecast as issued, not a simplified paraphrase.
- Never invent clock precision, lag, target variable, mechanism, contingency language, or missing transcript content.
- A later publication date does not make an outcome prospectively clean if its reference period overlaps the forecast date.
- Intermediate mechanism support may be recorded without promoting the terminal forecast to `RESOLVED_CORRECT`.
- Later Randolph retrospectives are new source objects, not independent verification of earlier forecasts.
- Title/subtitle-only sources define a hard proposition ceiling until transcript or directly inspectable first-party video evidence is preserved.

## Durable surfaces

Research/data:

- `research-candidates/matt-randolph-four-month-forecast-calibration.md`
- `assessments/forecast-calibration/matt-randolph/source-manifest.json`
- `assessments/forecast-calibration/matt-randolph/world-event-chronology.json`
- `assessments/forecast-calibration/matt-randolph/official-economic-series-2026-06-08-through-08-17.json`
- `assessments/forecast-calibration/matt-randolph/refinery-distillate-series-2026-07-10-through-08-14.json`
- `assessments/forecast-calibration/matt-randolph/diesel-vs-crude-benchmark-2026-06-01-through-08-14.json`
- `assessments/forecast-calibration/matt-randolph/freight-food-transmission-2026-07.json`
- `assessments/forecast-calibration/matt-randolph/multimonth-transmission-history-2026-03-through-07.json`
- `assessments/forecast-calibration/matt-randolph/shipping-fuel-food-chain-evidence-2026-03-through-06.json`
- `assessments/forecast-calibration/matt-randolph/july-video-transcript-acquisition.json`
- `assessments/forecast-calibration/matt-randolph/prospective-outcome-gating-2026-07.json`
- `assessments/forecast-calibration/matt-randolph/indicator-lag-test-execution-v0.1.json`

Machine forecasts:

- `MR-2026-03-07-third-week.forecast.json`
- `MR-2026-03-18-shipping-fuel-food.forecast.json`
- `MR-2026-07-08-diesel-inflation.forecast.json`
- `MR-2026-07-13-watch-diesel.forecast.json`

Component resolution:

- `MR-2026-03-18-shipping-fuel-food.component-resolution.json`
- `MR-2026-07-13-watch-diesel.component-resolution.json`

## First-party source custody

### March 18

First-party title/subtitle establish:

- `Pay Attention to Shipping Fuel, It's at All Time Record Highs. That's Bad.`
- `High Shipping Fuel Costs Hit Food Prices First.`

That is sufficient for a bounded ordering/mechanism record, but not a precise lag, magnitude, or exclusivity claim.

### June/July video bindings

Exact first-party bindings now include:

- June 25 `How Gas Prices Work` -> Substack `c-282558841` -> YouTube `0VE3LOxm4eY`;
- July 1 `When Cheap Oil Doesn’t Mean Cheap Gas` -> Substack `c-286379948` -> YouTube `BwTtIlOBL40`;
- July 8 `Higher Diesel Means Higher Inflation` -> Substack `c-290789385` -> YouTube `XqiDEUHs9nY`;
- July 13 `Watch Gas and Diesel Prices Not Oil` -> Substack `c-293975586` -> YouTube `C1twq1liA_4`;
- July 16 `It's About The Diesel` still requires richer first-party object discovery.

The available first-party pages do not currently expose substantive transcripts. Search snippets remain discovery aids rather than transcript custody.

## Independent mechanism evidence

### Refined-product system

The current EIA lane preserves high U.S. refinery utilization, substantial distillate production, low imports relative to exports, inventory tightness, and large crude-price movement. This rules out a simple `refineries stopped -> diesel rose` model and requires separate transition elements for refinery throughput, product yield, inventories, trade flows, logistics, and global product demand.

### March shipping-fuel / food chain

Independent USDA/BLS evidence supports:

- marine bunker-fuel shock — `SUPPORTED`;
- grain ocean-freight increase — `SUPPORTED`;
- domestic diesel cost pressure — `SUPPORTED`;
- transportation/fuel-surcharge pass-through — `SUPPORTED`;
- later consumer food-price movement — `PARTIAL_MIXED`;
- terminal `food prices first` ordering — `UNRESOLVED`;
- shipping fuel as sole/dominant cause — not authorized from the preserved source/evidence.

The component posture is durable in `MR-2026-03-18-shipping-fuel-food.component-resolution.json`.

## Prospective-outcome guard

A new gate prevents release-date leakage.

For the July 8 and July 13 forecasts:

- July CPI is context-only because CPI prices are collected throughout July, so its reference period spans both before and after forecast issuance.
- July PPI is also barred from clean prospective scoring because BLS treats the monthly index as representative of the month even though many prices are requested around the week containing the 13th.
- July Freight TSI is context-only and not yet released; its reference period also overlaps the forecasts.
- August PPI is a clean post-forecast reference period when released September 10, 2026.
- August CPI is a clean post-forecast reference period when released September 11, 2026.
- August Freight TSI is a clean post-forecast reference period when released October 14, 2026.

Durable record: `prospective-outcome-gating-2026-07.json`.

## First governed diesel-vs-crude lag execution

`indicator-lag-test-execution-v0.1.json` executes the already predeclared target and lag lanes without changing them after observing data.

Observed weekly signal diagnostic:

- most adjacent July-August steps had WTI, Brent, and retail diesel moving in the same direction;
- late July contains a divergence candidate where crude weekly means fell while retail diesel remained approximately flat-to-higher;
- different amplitudes and limited divergence justify continued testing but do not establish predictive superiority.

Current test conclusion:

`NO_PREDICTIVE_SUPERIORITY_SCORE_AUTHORIZED_YET`

Current July 13 components:

- refined-product/crude structural divergence possibility — `SUPPORTED_AS_STRUCTURAL_POSSIBILITY`;
- directional diesel superiority over crude in the observed weekly steps — `LIMITED_SUPPORT`;
- diesel predicts inflation better than crude — `UNRESOLVED`;
- diesel predicts freight better than crude — `UNRESOLVED`;
- intended target/horizon behind `watch` — `UNRESOLVED_SOURCE_MEANING` pending transcript custody.

## Machine forecast states

### March 7 — three-week Hormuz threshold
`UNRESOLVED`.

### March 18 — shipping fuel hits food prices first
`UNRESOLVED`, with multiple supported intermediate mechanism components.

### July 8 — higher diesel / higher inflation
`UNRESOLVED`. Clean August inflation reference periods have not yet been released, and transcript-defined lag/measure remains unknown.

### July 13 — watch gas/diesel, not oil
`UNRESOLVED`. Structural divergence is plausible, but current weekly signal behavior does not establish predictive superiority and clean macro/freight outcomes are pending.

## Validation posture

Exact-head hosted evidence prior to the latest component/gating additions:

- transition-calculus run `32691214420`: SUCCESS;
- live forecast-calibration validation: PASS;
- fail-closed negative fixtures: PASS;
- research-candidate activation run `32691214453`: SUCCESS.

The newest component-resolution, prospective-gating, lag-execution, and video-binding changes require their own hosted head result before a new exact-head PASS is claimed.

The repository-wide `Validate Ledger Schemas` workflow remains separately red because of the pre-existing August 22 White House ballroom primary-record-intake problem. It is outside this lane and remains visible.

## Next executable work

1. acquire July 8 and July 13 video/caption transcripts;
2. recover July 16 first-party video identity and transcript;
3. acquire June 25 / July 1 transcripts to reconstruct the gas-price/refining mechanism preceding the July 13 indicator claim;
4. freeze a comparator set and ordering clock for March 18 `food prices first`;
5. preserve August PPI on September 10 and August CPI on September 11 as the first clean post-July inflation target periods;
6. preserve July Freight TSI September 9 as context-only for July forecasts, then August Freight TSI October 14 as a clean post-forecast freight period;
7. execute every predeclared lag lane when each clean target becomes available without changing target definitions;
8. expand component resolution across additional sufficiently bounded forecasts;
9. keep six-to-nine-month open forecasts outside the historical aggregate until earlier calibration is materially complete;
10. perform independent review before any person-level credibility or publication finding.

## Quantified posture

Denominator = 10 bounded work groups.

1. durable owner/handoff — complete;
2. source policy/manifest — materially developed;
3. first-party corpus acquisition — materially developed, transcript custody incomplete;
4. independent world-event chronology — materially developed;
5. machine forecast encoding — 4 live forecast records;
6. EIA/refined-product integration — materially developed;
7. BLS/BTS/USDA freight-food integration — materially developed;
8. governed conditional/component resolution — materially developed; prospective leakage guard and first lag execution installed;
9. aggregate calibration/open-forecast confidence — not started;
10. independent review/promotion — not started.

Goal activation estimate: 72%.

## Release boundary

No publication, aggregate person-level credibility finding, downstream propagation, tag, or release is authorized from this lane yet.

## Archive posture

The methodology and current continuation state are durable here, but the project is not complete: clean prospective outcome periods, transcript custody, aggregate calibration, and independent review remain outstanding.
