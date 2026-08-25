# ERL Physical Economics Public Reporting Mirror Handoff

## Authority
Canonical continuation source for the public, attribute-bounded report-generation layer of the ERL Physical Economics lane.

Parent lane authority: `docs/physical-economics/PHYSICAL_ECONOMICS_MIRROR_HANDOFF.md`.
Machine contract: `contracts/physical-economics-report-generation.contract.json`.

## Goal
Allow a public user to press a report-generation control and receive a reproducible Physical Economics report whose historical, temporal, geographic, population, unit, completeness, and evidentiary boundaries are derived from the attributes pertinent to that report at request time.

The renderer must not impose a cosmetically uniform time window when the underlying attributes have different historical coverage.

## Governing report rule
The admissible report boundary is derived from the evidence attributes required for the requested claim class.

Each pertinent attribute carries its own:
- earliest admissible observation;
- latest observed date;
- latest complete date;
- current-period partial state;
- release/observation lag;
- methodology regime;
- cross-regime comparability state;
- revision vintage;
- geography scope;
- population scope;
- unit scope;
- provenance posture;
- missingness/opacity state.

The generated report must explicitly expose these differences.

## Historical-depth rule
Historical depth is attribute-specific.

A price series may reach back decades while physical package mass, direct household burden, local delivered-cost, or margin evidence reaches back only a few years. The report may preserve the older context, but conclusions requiring the shorter-history attribute are bounded to the shorter admissible period.

No false common historical window is authorized.

## Current-period rule
A report may be requested before the current month, quarter, year, or survey wave is complete.

The report must distinguish:
- `COMPLETE`;
- `PARTIAL_CURRENT_PERIOD`;
- `PENDING_RELEASE`;
- `REVISED_AFTER_INITIAL_RELEASE`;
- `METHODOLOGY_BREAK`;
- `UNAVAILABLE`;
- `OPAQUE`.

Partial current-period data cannot be silently annualized or treated as equivalent to a completed prior period.

## Methodology and comparability rule
A methodology, survey-design, classification, geographic, population, unit, or weighting change creates a regime boundary.

Cross-regime trend claims require an explicit bridge. Without a bridge, the report may display adjacent regimes but must not render them as one continuous comparable series.

Known examples include:
- HTOPS longitudinal design versus the March 2026 cross-sectional regime;
- CPI rebasing, corrections, seasonal-factor changes, and classification/title changes;
- physical scanner grams versus retail unit-count/volume proxies;
- national commodity price versus local delivered utility cost.

## Vintage rule
Current-vintage data and release-vintage evidence are distinct.

For retrospective forecast, decision, or accountability reports, later revisions may refine the present record but cannot silently replace what was knowable at the historical decision/forecast date.

Required receipt fields include source release date, reference period, vintage used, revision status, and prior-vintage reference where material.

## Public button semantics
`GENERATE_REPORT` must:
1. freeze the user request attributes and requested-as-of time;
2. resolve pertinent Physical Economics state-vector attributes;
3. freeze an evidence/vintage snapshot;
4. derive per-attribute boundaries;
5. derive the report-wide common-comparable and common-complete boundaries where such boundaries exist;
6. retain longer/shorter attribute-specific history without erasing asymmetry;
7. classify each finding as observed, reconstructed, comparator-only, proxy, partial, unresolved, or not-comparable;
8. render a plain-language boundary statement before substantive conclusions;
9. expose unresolved/opaque elements and prospective evidence gates;
10. emit deterministic receipts sufficient to reproduce the report.

## Required public report sections
- report question and generated-as-of timestamp;
- scope attributes;
- plain-language boundary statement;
- data coverage matrix;
- methodology/comparability regimes;
- current-period completeness;
- Physical Economics state vector;
- distribution/regional surfaces;
- producer cost/margin surface;
- household burden/unmet-need surface;
- tax/fee/transfer flows;
- observed findings;
- reconstructed findings;
- unresolved/opaque elements;
- prospective evidence gates;
- source/vintage receipts.

## Determinism
Identical request attributes against the same frozen evidence/vintage snapshot must generate the same boundary manifest and materially equivalent findings.

Required receipts:
- report request hash;
- evidence snapshot ID;
- boundary manifest hash;
- source receipt set;
- renderer version;
- contract version.

## Fail-closed conditions
The report fails closed if:
- a required opaque attribute is omitted from disclosure;
- a historical window exceeds required-attribute support;
- a partial current period is rendered as complete;
- a methodology break is crossed without a bridge;
- a later revision silently rewrites release-vintage state in a retrospective assessment;
- a proxy is presented as direct measurement;
- missing data are treated as zero or neutral;
- aggregate conditions erase materially supported distributional or regional divergence.

## Research gaps now explicitly covered
- attribute-specific historical depth;
- incomplete present-period evidence;
- methodology/comparability regime changes;
- release-vintage versus current-vintage integrity;
- public completeness disclosure;
- deterministic report reproducibility;
- prospective evidence gates native to the lane.

## Remaining implementation
1. create machine schemas for report requests and boundary manifests;
2. build the boundary resolver;
3. build frozen evidence/vintage snapshots;
4. create validators and negative fixtures for boundary overreach, incomplete periods, methodology breaks, proxy substitution, revision leakage, and aggregation erasure;
5. build the public UI report action and renderer;
6. generate portable verification receipts;
7. independently review boundary-selection semantics before public activation.

## Current posture
- reporting layer: `FORMAL_RESEARCH_CONTRACT`
- machine contract: complete v0.1
- reporting handoff: complete
- request schema: pending
- boundary-manifest schema: pending
- boundary resolver: pending
- public UI: not activated
- portable report verification: pending
- independent review: pending
- release: not authorized

## Archive posture
The public reporting goal is durably transferred to this handoff. Architectural formalization is complete; runtime implementation and public activation are not.