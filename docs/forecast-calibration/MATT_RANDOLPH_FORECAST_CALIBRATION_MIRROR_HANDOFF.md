# Matt Randolph Forecast Calibration Mirror Handoff

## Authority
Canonical continuation source for Issue #76 — `Calibrate Matt Randolph four-month energy and Iran forecasts`.

This lane consumes the transition-first forecast adapter under Issue #74 / PR #75. No aggregate person-level credibility finding, publication finding, downstream propagation, tag, or release is authorized until source custody, clean outcome reconstruction, governed scoring, and independent review are materially complete.

## Goal
Reconstruct roughly four months of Matt Randolph / Mr Global energy and Iran-conflict forecasting while preserving exact propositions, timing, contingencies, provenance, partial mechanism support, unresolved elements, and clean separation between source text and later interpretation.

## Governing rules
- Evaluate each forecast as issued, never a simplified paraphrase.
- Never invent transcript content, clock precision, lag, target variable, mechanism, or contingency language.
- Later publication does not make an outcome prospectively clean if its reference period overlaps forecast issuance.
- Intermediate mechanism support may be recorded without promoting the terminal forecast to `RESOLVED_CORRECT`.
- Later Randolph retrospectives are new source objects, not independent confirmation of earlier forecasts.
- Title/subtitle-only sources impose a hard proposition ceiling until transcript or directly inspectable first-party video content is preserved.

## Durable research surfaces
- `source-manifest.json`
- `world-event-chronology.json`
- `official-economic-series-2026-06-08-through-08-17.json`
- `refinery-distillate-series-2026-07-10-through-08-14.json`
- `diesel-vs-crude-benchmark-2026-06-01-through-08-14.json`
- `freight-food-transmission-2026-07.json`
- `multimonth-transmission-history-2026-03-through-07.json`
- `shipping-fuel-food-chain-evidence-2026-03-through-06.json`
- `july-video-transcript-acquisition.json`
- `prospective-outcome-gating-2026-07.json`
- `indicator-lag-test-execution-v0.1.json`

Machine forecast records:
- `MR-2026-03-07-third-week.forecast.json`
- `MR-2026-03-18-shipping-fuel-food.forecast.json`
- `MR-2026-07-08-diesel-inflation.forecast.json`
- `MR-2026-07-13-watch-diesel.forecast.json`

Component-resolution records:
- `MR-2026-03-18-shipping-fuel-food.component-resolution.json`
- `MR-2026-07-13-watch-diesel.component-resolution.json`

## First-party video/source custody
Exact bindings now include:
- June 25 `How Gas Prices Work` -> Substack `c-282558841` -> YouTube `0VE3LOxm4eY`;
- July 1 `When Cheap Oil Doesn’t Mean Cheap Gas` -> Substack `c-286379948` -> YouTube `BwTtIlOBL40`;
- July 8 `Higher Diesel Means Higher Inflation` -> Substack `c-290789385` -> YouTube `XqiDEUHs9nY`;
- July 13 `Watch Gas and Diesel Prices Not Oil` -> Substack `c-293975586` -> YouTube `C1twq1liA_4`.

July 16 `It's About The Diesel` still requires richer first-party object discovery. Current retrievable first-party pages do not expose substantive transcripts, so titles remain proposition ceilings.

## March 18 mechanism posture
First-party subtitle: `High Shipping Fuel Costs Hit Food Prices First.`

Independent USDA/BLS evidence currently supports:
- marine bunker-fuel shock — `SUPPORTED`;
- grain ocean-freight increase — `SUPPORTED`;
- domestic diesel cost pressure — `SUPPORTED`;
- transportation/fuel-surcharge pass-through — `SUPPORTED`;
- later consumer food-price movement — `PARTIAL_MIXED`;
- terminal `food prices first` ordering — `UNRESOLVED`;
- shipping fuel as sole/dominant cause — not authorized.

The terminal claim remains unresolved until a comparator set and ordering clock for `first` are frozen.

## Refined-products versus crude
EIA evidence preserves high refinery utilization, substantial distillate production, low imports relative to exports, inventory tightness, trade flows, and large crude-price moves. A simple `refineries stopped -> diesel rose` explanation is rejected as inadequate for the observed interval.

The first governed indicator-lag execution uses the previously fixed target and lag lanes. Most adjacent July-August weekly movements had WTI, Brent, and retail diesel moving in the same direction; late July shows a divergence candidate where crude weekly means fell while retail diesel remained approximately flat-to-higher.

Current test conclusion:
`NO_PREDICTIVE_SUPERIORITY_SCORE_AUTHORIZED_YET`

July 13 component posture:
- refined-product/crude structural divergence possibility — `SUPPORTED_AS_STRUCTURAL_POSSIBILITY`;
- directional diesel superiority in current weekly steps — `LIMITED_SUPPORT`;
- diesel predicts inflation better than crude — `UNRESOLVED`;
- diesel predicts freight better than crude — `UNRESOLVED`;
- intended target/horizon behind `watch` — `UNRESOLVED_SOURCE_MEANING`.

## Prospective-outcome guard
For the July 8 and July 13 forecasts:
- July CPI is context-only because CPI prices are collected throughout July and the reference period overlaps forecast issuance.
- July PPI is context-only for prospective scoring because BLS treats the monthly PPI as representative of the reference month even though many prices are requested around the week containing the 13th.
- July Freight TSI is context-only and its reference month overlaps the forecasts.
- August PPI is the first clean post-forecast PPI reference period and is scheduled for September 10, 2026.
- August CPI is the first clean post-forecast CPI reference period and is scheduled for September 11, 2026.
- August Freight TSI is a clean post-forecast freight period and is scheduled for October 14, 2026.

This prevents release-date leakage: `published after` is not treated as equivalent to `measured after`.

## Forecast states
- March 7 three-week Hormuz threshold — `UNRESOLVED`.
- March 18 shipping fuel / food first — `UNRESOLVED`, with multiple supported intermediate mechanism components.
- July 8 higher diesel / higher inflation — `UNRESOLVED`; transcript-defined lag/measure remains unknown and clean August targets are pending.
- July 13 watch gas/diesel, not oil — `UNRESOLVED`; structural divergence is plausible but predictive superiority is not established.

## Validation posture
Current exact-head commit: `496dea7136a70a71a3168be7fbe90828fbdb3b6a`.

Hosted validation:
- transition-calculus workflow run `32787292031` — `SUCCESS`;
- live forecast-calibration validation — `PASS`;
- fail-closed negative fixtures — `PASS`;
- research-candidate activation run `32787292036` — `SUCCESS`.

The separate repository-wide `Validate Ledger Schemas` workflow remains red because of the pre-existing August 22 White House ballroom primary-record-intake problem. That blocker is outside this lane and remains visible.

## Next executable work
1. acquire July 8 and July 13 captions/transcripts;
2. recover July 16 first-party video identity/transcript;
3. acquire June 25 and July 1 transcripts to reconstruct the gas-price/refining mechanism preceding July 13;
4. freeze a comparator set and ordering clock for March 18 `food prices first`;
5. preserve and score August PPI on September 10 and August CPI on September 11 against every applicable predeclared lag lane;
6. preserve July Freight TSI on September 9 as context-only and August Freight TSI October 14 as the clean freight outcome period;
7. expand component resolution across other sufficiently bounded forecasts;
8. keep six-to-nine-month open forecasts outside the historical aggregate until earlier calibration is materially complete;
9. perform independent review before any aggregate credibility or publication decision.

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

## Archive posture
Current continuation state is durable, but the project is not complete. Transcript custody, clean post-forecast August outcome periods, aggregate calibration, and independent review remain outstanding.
