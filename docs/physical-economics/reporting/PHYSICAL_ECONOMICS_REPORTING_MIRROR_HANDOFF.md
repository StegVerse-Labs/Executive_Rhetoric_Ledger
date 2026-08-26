# ERL Physical Economics Public Reporting Mirror Handoff

## Authority
Canonical continuation source for the public, attribute-bounded report-generation layer of the ERL Physical Economics lane.

Parent lane authority: `docs/physical-economics/PHYSICAL_ECONOMICS_MIRROR_HANDOFF.md`.

## Goal
Allow a public user to press `GENERATE_REPORT` and receive a reproducible Physical Economics report whose historical, temporal, geographic, population, unit, completeness, uncertainty, and evidentiary boundaries are derived from attributes pertinent to the requested claim at request time.

The report boundary is an output of evidence, not a cosmetic date selector.

## Canonical machine surfaces
- `contracts/physical-economics-report-generation.contract.json`
- `contracts/physical-economics-report-pertinence.matrix.v0.1.json`
- `schemas/physical-economics-report-request.schema.json`
- `schemas/physical-economics-evidence-snapshot.schema.json`
- `schemas/physical-economics-report-boundary-manifest.schema.json`
- `schemas/physical-economics-report-delta.schema.json`
- `schemas/physical-economics-report-verification-receipt.schema.json`
- `scripts/finalize_physical_economics_evidence_snapshot.py`
- `scripts/resolve_physical_economics_report_boundary.py`
- `scripts/physical_economics_uncertainty.py`
- `scripts/physical_economics_source_conflicts.py`
- `scripts/generate_physical_economics_report_delta.py`
- `scripts/generate_physical_economics_report_verification_receipt.py`
- `scripts/validate_physical_economics_reporting.py`
- `scripts/validate_physical_economics_reporting_integrity.py`
- `tests/physical-economics-reporting/boundary-resolver.cases.json`
- `.github/workflows/validate-physical-economics-reporting.yml`
- `assessments/physical-economics/reporting/uncertainty-vintage-revision-research-2026.v0.1.json`

## Governing boundary rule
For every required attribute, preserve and resolve:
- earliest admissible observation;
- latest observed date;
- latest complete date;
- current-period completeness state;
- release/observation lag;
- methodology regime and cross-regime comparability;
- revision vintage;
- geography/population/unit scope;
- source authority and provenance posture;
- source-native uncertainty and quality flags;
- missingness/opacity state.

Longer attribute-specific history may remain visible as context, but it cannot extend conclusions beyond the shortest required admissible history.

## Deterministic pertinence
Attribute selection is not free-form model discretion.

`physical-economics-report-pertinence.matrix.v0.1.json` is the versioned claim-class -> required/contextual attribute protocol. Public request claim-class vocabulary has been normalized to the matrix. Required evidence cannot be excluded by the user request or silently replaced by contextual evidence. Composed claims inherit the union of required evidence unless a narrower protocol is independently validated.

Canonical claim classes currently include price change, physical purchasing power, essential affordability, unmet essential need, substitution/quality compression, producer cost pressure, producer margin state, cost-margin transmission, distributional burden, regional burden, household resilience, arrears/deferred obligations, capacity/inventory constraint, tax/fee/regulatory flow, transfer-offset effect, and the full economic-condition state vector.

## Immutable evidence snapshots
`physical-economics-evidence-snapshot.schema.json` preserves per-attribute coverage, methodology, vintage, uncertainty, source receipts, and unresolved conflicts.

`finalize_physical_economics_evidence_snapshot.py` defines canonical SHA-256 snapshot finalization and self-verification. Hashing is performed with the snapshot hash field blanked, then persisted as `sha256:<digest>`. Tampering must therefore change verification state rather than silently mutating a prior report basis.

## Boundary resolver
`resolve_physical_economics_report_boundary.py` is implemented.

It:
1. validates request/snapshot structures;
2. resolves required/contextual attributes only from the versioned pertinence matrix;
3. fails closed when a request attempts to exclude required evidence;
4. materializes absent required attributes as explicit opaque boundaries;
5. computes per-attribute historical depth;
6. emits a common comparable/complete window only when every required attribute supports one;
7. preserves partial periods and methodology breaks;
8. carries uncertainty posture without manufacturing precision;
9. emits deterministic hashes and receipts binding the request, evidence snapshot, boundary manifest, source receipt set, contract version, and pertinence-matrix version.

Current resolver fixtures include a complete price report, a physical-purchasing-power report missing required physical-content evidence, and a required-attribute exclusion fail-closed case.

## Current-period and methodology rules
Allowed current-period states remain:
- `COMPLETE`
- `PARTIAL_CURRENT_PERIOD`
- `PENDING_RELEASE`
- `REVISED_AFTER_INITIAL_RELEASE`
- `METHODOLOGY_BREAK`
- `UNAVAILABLE`
- `OPAQUE`

Partial periods cannot be silently annualized. Survey design, classification, geography, population, unit, weighting, seasonal-adjustment, rebasing, or other source-method changes create explicit methodology regimes. Cross-regime trend claims require a validated bridge.

## Vintage/revision integrity
Release-vintage and current-vintage evidence remain distinct. A retrospective report cannot silently replace what was knowable at the historical time with a later revision.

Report delta classes include:
- `NEW_OBSERVATION`
- `PRIOR_PERIOD_COMPLETED`
- `ROUTINE_REVISION`
- `SOURCE_CORRECTION`
- `SEASONAL_FACTOR_REVISION`
- `METHODOLOGY_CHANGE`
- `CLASSIFICATION_CHANGE`
- `OPAQUE_ATTRIBUTE_RESOLVED`
- `SOURCE_WITHDRAWN_OR_REPLACED`
- `REQUIRED_ATTRIBUTE_PROTOCOL_CHANGE`
- `RENDERER_OR_CONTRACT_CHANGE`
- `SOURCE_CONFLICT_RESOLVED`
- `UNCERTAINTY_POSTURE_CHANGED`

`generate_physical_economics_report_delta.py` now emits machine-readable report-version change receipts across these states.

## Statistical uncertainty
Source-provided standard errors, confidence intervals, sampling error, suppression flags, and quality measures remain attached through resolution and rendering.

`physical_economics_uncertainty.py` implements deliberately narrow fail-closed propagation:
- linear standard-error propagation is allowed for explicitly declared independent components;
- an explicit covariance matrix may authorize dependent propagation;
- unknown dependence/covariance returns `UNRESOLVED` rather than a fabricated aggregate standard error;
- deterministic interval arithmetic may produce bounds but is explicitly non-probabilistic;
- rendered precision cannot exceed source-supported precision.

## Source conflicts
`physical_economics_source_conflicts.py` is implemented conservatively.

No conflicting values are reconciled by guess. Automatic resolution is limited to explicit correction/replacement chains; declared scope/vintage distinctions may be preserved. Otherwise the conflict remains `UNRESOLVED`.

## Portable verification
`physical-economics-report-verification-receipt.schema.json` and `generate_physical_economics_report_verification_receipt.py` are implemented.

A portable report receipt binds:
- report content hash;
- report request hash;
- evidence snapshot ID/hash;
- boundary manifest ID/hash;
- pertinence-matrix version;
- report contract version;
- renderer version;
- source receipt IDs.

Hash/protocol/source-receipt mismatches fail closed rather than producing a `VERIFIABLE` state.

## Validation
`validate_physical_economics_reporting.py` validates claim-class alignment, pertinence semantics, evidence references, resolver fixtures, deterministic replay, uncertainty runtime, and report-delta runtime.

`validate_physical_economics_reporting_integrity.py` validates snapshot self-verification/tamper detection, conservative source-conflict handling, and portable verification receipts.

`.github/workflows/validate-physical-economics-reporting.yml` runs both validators and is wired to the reporting contracts, schemas, runtimes, fixtures, evidence, and handoff.

**Hosted validation is not yet established.** Exact-head queries on `217b0a5afbbb7df43465cb636d689031ff94a5a4` returned no workflow runs and no combined statuses. Presence of the workflow therefore does not equal CI activation/pass.

PR #75 remains open, draft, unmerged, and currently reports `mergeable: false`; exact PR head at the last query was `217b0a5afbbb7df43465cb636d689031ff94a5a4` before this handoff update.

## Public button semantics
A public `GENERATE_REPORT` action must execute the following chain:
1. freeze question/scope/requested-as-of time;
2. map claim class -> required attributes deterministically;
3. acquire/finalize an immutable evidence snapshot;
4. resolve report boundaries;
5. preserve asymmetric historical coverage;
6. preserve methodology/vintage/uncertainty/source-conflict state;
7. classify findings as observed, reconstructed, comparator-only, proxy, partial, unresolved, or not-comparable;
8. render the boundary/completeness statement before substantive conclusions;
9. expose opaque elements and prospective lane-native evidence gates;
10. emit source, boundary, report-delta, and portable verification receipts.

## Required public report sections
- question and generated-as-of time;
- claim classes and scope;
- plain-language boundary statement;
- data coverage matrix;
- methodology/comparability regimes;
- uncertainty/quality surface;
- current-period completeness;
- Physical Economics state vector;
- distribution/regional surfaces;
- producer cost/margin surface;
- household burden/unmet-need surface;
- tax/fee/transfer flows;
- observed and reconstructed findings separated;
- unresolved/opaque elements;
- prospective evidence gates;
- source/vintage receipts;
- report-version change summary when a prior report exists;
- portable verification receipt.

## Fail-closed conditions
Fail closed if:
- required opaque attributes are hidden;
- required evidence is excluded or replaced by context;
- historical coverage exceeds required-attribute support;
- partial periods are treated as complete;
- methodology breaks are crossed without a bridge;
- revisions silently rewrite release-vintage state;
- proxies are rendered as direct measures;
- missing values become zero/neutral;
- aggregate results erase supported distributional/regional divergence;
- source uncertainty is dropped;
- aggregate precision is fabricated from unknown dependence/covariance;
- source conflicts are reconciled without an evidenced basis;
- the snapshot, boundary, report, or protocol hashes do not reproduce.

## Remaining work
1. build the public report renderer/output contract and deterministic report document model;
2. build the public UI/API action that executes the request -> snapshot -> boundary -> report -> verification chain;
3. add broader positive/negative fixtures across composed claim classes, methodology breaks, source corrections, and regional/distributional divergence;
4. integrate real Physical Economics data snapshots rather than only synthetic resolver fixtures;
5. obtain exact-head hosted CI execution and consume any failures;
6. independently review pertinence, boundary, uncertainty, conflict, and verification semantics;
7. only after validation/review consider public activation or release.

## Current posture
- reporting layer: `FORMAL_IMPLEMENTATION_ACTIVE_NOT_PUBLIC`
- machine contract: complete v0.1
- request schema: complete v0.1
- pertinence matrix: complete v0.1 at research-contract level; independent validation pending
- evidence snapshot schema: complete v0.1
- immutable snapshot hash runtime: implemented
- boundary manifest schema: complete v0.1
- boundary resolver: implemented
- uncertainty runtime: implemented, deliberately bounded
- source-conflict runtime: implemented, fail closed
- report delta schema/runtime: implemented
- portable verification schema/runtime: implemented
- semantic validators: implemented for current bounded cases
- hosted workflow: configured but no exact-head run observed
- real-data report execution: pending
- public renderer/UI: pending
- independent review: pending
- public activation/release: not authorized

Public reporting bounded implementation estimate: `72%`.

## Archive posture
The report-generation sub-lane is no longer only architectural research: the deterministic boundary, snapshot, uncertainty, conflict, delta, validation, and portable-verification runtimes are implemented. The remaining critical gap is converting those machine states into a real public report renderer/UI backed by real snapshots and hosted validation, followed by independent review. No public activation or release is claimed.
