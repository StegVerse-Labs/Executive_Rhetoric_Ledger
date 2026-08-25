# ERL Physical Economics Public Reporting Mirror Handoff

## Authority
Canonical continuation source for the public, attribute-bounded report-generation layer of the ERL Physical Economics lane.

Parent lane authority: `docs/physical-economics/PHYSICAL_ECONOMICS_MIRROR_HANDOFF.md`.
Canonical machine surfaces:
- `contracts/physical-economics-report-generation.contract.json`
- `schemas/physical-economics-report-request.schema.json`
- `schemas/physical-economics-report-boundary-manifest.schema.json`

## Goal
Allow a public user to press `GENERATE_REPORT` and receive a reproducible Physical Economics report whose historical, temporal, geographic, population, unit, completeness, uncertainty, and evidentiary boundaries are derived from attributes pertinent to the requested claim at request time.

A report must never manufacture a uniform historical window merely because the UI prefers one.

## Governing boundary rule
For every required attribute, resolve:
- earliest admissible observation;
- latest observed date;
- latest complete date;
- current-period completeness state;
- release/observation lag;
- methodology regime;
- cross-regime comparability;
- revision vintage;
- geography/population/unit scope;
- source authority and provenance posture;
- uncertainty where supplied by the source;
- missingness/opacity state.

The report boundary is derived from those states. Longer historical context may be shown separately, but conclusions requiring a shorter-history attribute remain bounded to that shorter period.

## Attribute pertinence
Attribute selection is not free-form model discretion.

The report request schema freezes claim classes and requires `DETERMINISTIC_CLAIM_CLASS_MAPPING` against a versioned required-attribute set. Optional contextual attributes may be added only as explicitly contextual; they cannot change the required evidence gate invisibly.

This is the next major protocol to implement: a versioned claim-class -> required-attribute matrix.

## Historical-depth rule
Historical depth is attribute-specific.

Example: a price series may reach back decades while package-level mass exists for three years and direct household-burden evidence for a shorter survey regime. The report may show all three, but physical purchasing-power conclusions cannot be projected backward beyond the physical-unit evidence without a declared reconstruction method.

## Current-period rule
Current observations may be incomplete when the button is pressed. Allowed states:
- `COMPLETE`
- `PARTIAL_CURRENT_PERIOD`
- `PENDING_RELEASE`
- `REVISED_AFTER_INITIAL_RELEASE`
- `METHODOLOGY_BREAK`
- `UNAVAILABLE`
- `OPAQUE`

Partial periods cannot be silently annualized or treated as equivalent to completed periods.

## Methodology/comparability rule
Survey design, classification, geography, population, unit, weighting, seasonal-adjustment, rebasing, or source-method changes create explicit methodology regimes.

Cross-regime trend claims require an explicit bridge. Without a bridge, adjacent regimes may be displayed but are `NOT_COMPARABLE` as a continuous series.

Known examples include HTOPS design changes, CPI rebasing/corrections/method changes, scanner grams versus unit-volume proxies, and national commodity price versus local delivered utility cost.

## Vintage/revision rule
Current-vintage and release-vintage evidence are distinct.

Retrospective forecast, decision, and accountability reports must preserve what was knowable at the historical time. Later revisions may be shown but cannot silently overwrite historical epistemic state.

## Statistical uncertainty rule
Source-provided standard errors, confidence intervals, sampling error, suppression flags, and quality measures must remain attached to the attribute state through boundary resolution and rendering.

A precise scalar generated from uncertain inputs must not be rendered with greater apparent precision than the underlying evidence supports. Uncertainty propagation semantics remain to be implemented and independently reviewed.

## Source conflict / disappearance rule
The runtime must freeze an evidence/vintage snapshot before generation. A later source correction, disappearance, replacement, or contradictory official release creates a new evidence snapshot rather than silently mutating an already generated report.

Source precedence must preserve direct authoritative evidence, release vintage, corrections, and unresolved conflicts; conflicting official values may not be reconciled by guess.

## Public button semantics
`GENERATE_REPORT` must:
1. freeze request attributes and requested-as-of time;
2. resolve claim class -> required attributes deterministically;
3. freeze an evidence/vintage snapshot;
4. derive per-attribute boundaries;
5. derive common-comparable/common-complete boundaries where they actually exist;
6. retain asymmetric historical coverage explicitly;
7. preserve source uncertainty and methodology regimes;
8. classify findings as observed, reconstructed, comparator-only, proxy, partial, unresolved, or not-comparable;
9. render a plain-language boundary statement before substantive conclusions;
10. expose opaque elements and prospective evidence gates;
11. emit deterministic reproduction receipts.

## Required public report sections
- question and generated-as-of timestamp
- scope attributes and claim classes
- boundary statement
- data coverage matrix
- methodology/comparability regimes
- uncertainty/quality surface
- current-period completeness
- Physical Economics state vector
- distribution/regional surfaces
- producer cost/margin surface
- household burden/unmet-need surface
- tax/fee/transfer flows
- observed findings
- reconstructed findings
- unresolved/opaque elements
- prospective evidence gates
- source/vintage receipts
- report-version change summary when prior report exists

## Determinism and report evolution
Identical request attributes against the same evidence/vintage snapshot must produce the same boundary manifest and materially equivalent findings.

Required receipts include request hash, evidence snapshot ID, boundary manifest hash, source receipt set, renderer version, contract version, and required-attribute-set version.

When a later report differs, the system should generate a machine-readable delta identifying whether the change came from:
- new observations;
- prior-period completion;
- source revision/correction;
- methodology change;
- newly resolved opaque attribute;
- changed required-attribute protocol;
- renderer/contract version change.

## Fail-closed conditions
Fail closed if:
- required opaque attributes are hidden;
- historical coverage exceeds required-attribute support;
- partial periods are treated as complete;
- methodology breaks are crossed without a bridge;
- later revisions silently rewrite release-vintage state;
- proxies are rendered as direct measures;
- missing values become zero/neutral;
- aggregate results erase materially supported distributional/regional divergence;
- source uncertainty is dropped where material;
- attribute pertinence is changed ad hoc without a versioned protocol.

## Remaining runtime work
1. build the versioned claim-class -> required-attribute matrix;
2. implement the boundary resolver;
3. implement frozen evidence/vintage snapshots;
4. implement uncertainty propagation;
5. implement source-conflict/correction handling;
6. implement report-version delta receipts;
7. create semantic validators and negative fixtures;
8. build the public UI action and renderer;
9. generate portable verification receipts;
10. independently review boundary-selection and uncertainty semantics before public activation.

## Current posture
- reporting layer: `FORMAL_RESEARCH_CONTRACT`
- machine contract: complete v0.1
- reporting handoff: complete
- report-request schema: complete v0.1
- boundary-manifest schema: complete v0.1
- deterministic pertinence matrix: pending
- boundary resolver: pending
- evidence/vintage snapshot runtime: pending
- uncertainty propagation: pending
- report delta receipts: pending
- public UI: not activated
- portable verification: pending
- independent review: pending
- release: not authorized

Public reporting bounded implementation estimate: `42%`.

## Archive posture
The public-report architecture is formally specified and machine-addressable. Runtime boundary resolution, snapshotting, uncertainty propagation, public rendering, verification, and independent review remain incomplete.