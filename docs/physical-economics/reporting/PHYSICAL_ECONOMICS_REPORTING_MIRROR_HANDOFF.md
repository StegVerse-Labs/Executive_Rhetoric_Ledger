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
- `schemas/physical-economics-report-document.schema.json`
- `scripts/finalize_physical_economics_evidence_snapshot.py`
- `scripts/resolve_physical_economics_report_boundary.py`
- `scripts/physical_economics_uncertainty.py`
- `scripts/physical_economics_source_conflicts.py`
- `scripts/generate_physical_economics_report_delta.py`
- `scripts/render_physical_economics_report.py`
- `scripts/generate_physical_economics_report_verification_receipt.py`
- `scripts/generate_physical_economics_public_report.py`
- `scripts/validate_physical_economics_reporting.py`
- `scripts/validate_physical_economics_reporting_integrity.py`
- `scripts/validate_physical_economics_report_renderer.py`
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

The canonical matrix version consumed by the public client is exactly `0.1`. Descriptive aliases are not protocol-equivalent.

## Immutable evidence snapshots
`physical-economics-evidence-snapshot.schema.json` preserves per-attribute coverage, methodology, vintage, uncertainty, source receipts, and unresolved conflicts.

`finalize_physical_economics_evidence_snapshot.py` defines canonical SHA-256 snapshot finalization and self-verification. Hashing is performed with the snapshot hash field blanked, then persisted as `sha256:<digest>`. Tampering changes verification state rather than silently mutating a prior report basis.

## Boundary resolver
`resolve_physical_economics_report_boundary.py` is implemented.

It validates request/snapshot structures, resolves required/contextual attributes only from the versioned pertinence matrix, fails closed on required-attribute exclusion, materializes absent required attributes as opaque boundaries, computes per-attribute history, emits a common comparable/complete window only when all required attributes support one, preserves partial periods and methodology breaks, carries uncertainty without manufacturing precision, and emits deterministic receipts binding request/snapshot/boundary/source/protocol state.

Current resolver fixtures include a complete price report, a physical-purchasing-power report missing required physical-content evidence, and a required-attribute exclusion fail-closed case.

## Current-period and methodology rules
Allowed current-period states:
- `COMPLETE`
- `PARTIAL_CURRENT_PERIOD`
- `PENDING_RELEASE`
- `REVISED_AFTER_INITIAL_RELEASE`
- `METHODOLOGY_BREAK`
- `UNAVAILABLE`
- `OPAQUE`

Partial periods cannot be silently annualized. Survey design, classification, geography, population, unit, weighting, seasonal-adjustment, rebasing, or other source-method changes create explicit methodology regimes. Cross-regime trend claims require a validated bridge.

## Vintage/revision integrity
Release-vintage and current-vintage evidence are distinct. A retrospective report cannot silently replace what was knowable at the historical time with a later revision.

`generate_physical_economics_report_delta.py` emits machine-readable change receipts for new observations, completed periods, revisions/corrections, methodology/classification changes, opacity resolution, source replacement, required-attribute protocol changes, renderer/contract changes, source-conflict resolution, and uncertainty changes.

## Statistical uncertainty
`physical_economics_uncertainty.py` implements bounded fail-closed propagation:
- linear standard-error propagation for explicitly independent components;
- explicit covariance matrices for supported dependent propagation;
- `UNRESOLVED` for unknown dependence/covariance rather than fabricated aggregate precision;
- deterministic interval arithmetic labeled non-probabilistic;
- rendering precision no greater than source-supported precision.

## Source conflicts
`physical_economics_source_conflicts.py` is implemented conservatively. Conflicting values are never reconciled by guess. Automatic resolution is limited to explicit correction/replacement chains; declared scope/vintage distinctions may be preserved. Otherwise the conflict remains `UNRESOLVED`.

## Deterministic report document and renderer
`physical-economics-report-document.schema.json` is now the machine output contract for the public report.

`render_physical_economics_report.py` deterministically builds the report document and Markdown representation from the request, snapshot, boundary manifest, governed findings, prospective gates, and optional prior-report delta.

The renderer:
- puts the explicit report boundary before substantive findings;
- renders the data-coverage matrix and uncertainty surface;
- keeps observed/reconstructed/proxy/partial/unresolved/not-comparable finding classes explicit;
- exposes opaque elements and prospective evidence gates;
- does **not** invent findings when no governed finding objects are supplied;
- preserves reproduction receipts in the report itself.

`validate_physical_economics_report_renderer.py` provides an end-to-end smoke test using the complete-price fixture and verifies boundary-before-findings ordering, no invented findings, schema validity, and portable content hashing.

## One-transaction backend
`generate_physical_economics_public_report.py` is implemented as the bounded backend transaction behind the future public button.

Given a report request and prepared evidence-snapshot draft, plus optional governed finding/gate/delta objects, it:
1. finalizes the immutable snapshot hash;
2. resolves the evidence-derived boundary;
3. builds the deterministic report document;
4. renders Markdown;
5. writes the finalized snapshot, boundary manifest, report document, and report;
6. emits a portable verification receipt;
7. returns `GENERATED_NOT_PUBLICLY_ACTIVATED` only when the receipt is `VERIFIABLE`.

It does not acquire network evidence and does not invent substantive findings. Evidence acquisition and governed finding construction remain upstream Physical Economics responsibilities.

## Portable verification
`physical-economics-report-verification-receipt.schema.json` and `generate_physical_economics_report_verification_receipt.py` bind report content, request, evidence snapshot, boundary manifest, pertinence matrix, contract, renderer, and source receipt identities. Hash/protocol/source-receipt mismatches fail closed.

## Validation
`validate_physical_economics_reporting.py` validates claim-class alignment, pertinence semantics, evidence references, resolver fixtures, deterministic replay, uncertainty runtime, and report-delta runtime.

`validate_physical_economics_reporting_integrity.py` validates snapshot self-verification/tamper detection, conservative source-conflict handling, and portable verification receipts.

`validate_physical_economics_report_renderer.py` validates deterministic report assembly/rendering and portable hashing.

`.github/workflows/validate-physical-economics-reporting.yml` runs all three validators and covers the reporting contracts, schemas, runtimes, fixtures, evidence, renderer/backend, and handoff.

Hosted validation is still **not established** for the current umbrella branch. Fresh inspection on 2026-08-26 of PR #75 at observed head `64a0ced3c72e3d667699bc10801cf901844d53bb` returned no pull-request workflow runs and no combined commit statuses. This archive reconciliation moves the branch head again, so workflow source presence or any older head must not be reported as current PASS.

PR #75 is fresh-observed as open, draft, unmerged, and `mergeable: false`. Mergeability remains a live property and must be re-queried before any future merge action.

## Site public-client integration
A bounded Site consumer now exists; this supersedes the older state `external public UI/API integration: pending` with the more precise split below.

Canonical Site lane:

```text
repo: StegVerse-Labs/Site
issue: #496
branch: feature/physical-economics-public-report-ui-496
PR: #499
handoff: docs/physical-economics/PUBLIC_REPORT_UI_MIRROR_HANDOFF.md
```

Implemented there:
- `Physical-Economics.html` public request/render surface;
- `js/physical-economics-report.js` fail-closed browser/CommonJS client;
- deterministic Node contract tests;
- dedicated credential-free validation workflow;
- machine pre-work claim for the exact bounded surfaces.

The Site client preserves ERL authority: required attributes cannot be excluded, matrix version is `0.1`, boundary renders before findings, unverified receipts fail closed, backend absence fails closed, and transport omits credentials.

Fresh Site integration state on 2026-08-26:

```text
Site issue #496: open
Site PR #499: open draft, unmerged, currently mergeable=false
Site head observed before archive handoff update: c09fae59eb1304909520de0e3adb6497bd35a2a4
local deterministic Node suite: PASS
hosted Physical Economics run 32985301150: startup_failure
hosted validation job 98230430068: cancelled before steps
runner_id: 0
steps executed: 0
public page publication: not verified
report endpoint: blank / unconfigured / fail-closed
```

The hosted Site failure is a runner/startup gate, not evidence that the report contract tests failed. No job log was retrievable. Root cause remains unresolved and must be diagnosed before assigning a manual provider/settings action.

## Public button semantics
The end-to-end logical chain is now represented by:

`public Site request -> governed HTTP adapter -> ERL report transaction -> prepared evidence snapshot -> immutable snapshot -> boundary -> governed findings/state -> deterministic report -> portable verification -> Site rendering`.

The ERL transaction and Site client are implemented. The missing functional bridge is a **real governed HTTP adapter/runtime** that exposes the ERL transaction without moving evidence, pertinence, boundary, uncertainty, conflict, or finding authority into Site.

The Site endpoint must remain blank until that adapter has repository-native validation and live runtime proof. Populating an endpoint is an activation step, not a documentation change.

## Required public report sections
- question and generated-as-of time;
- claim classes and scope;
- plain-language boundary statement;
- data coverage matrix;
- methodology/comparability regimes;
- uncertainty/quality surface;
- current-period completeness;
- Physical Economics state vector / applicable surfaces;
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
- findings are invented by the renderer;
- the snapshot, boundary, report, or protocol hashes do not reproduce;
- the public adapter returns a non-`VERIFIABLE` receipt as success;
- the public client is configured to an adapter that has not been independently runtime-verified.

## Credential / runtime boundary
No NON-TV/TVC credential may be introduced into the reporting transaction, Site, or GitHub-token runtime authority. Render is not an authorized dependency.

No manual/iPhone user action is currently proven necessary for this reporting lane. If a later public transport provider requires secrets or authorization, the provider credential must be represented through TV/TVC authority and the user action must be recorded here before activation. Do not invent a credential requirement merely because Site hosted CI currently has a provider-level `startup_failure`.

## Remaining work
1. integrate real Physical Economics evidence/state snapshots and governed finding objects into the transaction;
2. add broader fixtures for composed claim classes, methodology breaks, source corrections, regional/distributional divergence, and partial current periods;
3. obtain exact-head hosted ERL CI execution and consume any failures;
4. independently review pertinence, boundary, uncertainty, conflict, renderer, and verification semantics;
5. diagnose and clear the Site #499 hosted-runner startup gate, then consume exact-head claim/orchestration/Node validation;
6. resolve Site #499 mergeability/review gates, merge, and independently verify actual public page publication;
7. create the governed HTTP adapter around `generate_physical_economics_public_report.py` under a canonical claimed lane rather than burying transport logic in Site;
8. validate the adapter with deterministic request/response and portable-verification fixtures, then obtain live runtime proof;
9. only after adapter runtime proof populate the Site endpoint and execute an independently verified real end-to-end `VERIFIABLE` report;
10. only after real-data execution, hosted validation, public transport proof, Site integration, and independent review consider public activation/release.

## Cross-repository propagation obligations
When a downstream transition is actually proven:
- Site merge/publication proof must be recorded in the Site bounded handoff and propagated here;
- HTTP-adapter authority/runtime proof must be recorded in its owning repo handoff and referenced here;
- ERL real-data/report receipts remain authoritative for report content;
- Site remains a presentation/request consumer, not evidence authority;
- no release propagation to Site/Publisher/admissibility-wiki/stegguardian-wiki is authorized until release posture is actually reached.

## Current posture
- reporting layer: `FORMAL_IMPLEMENTATION_ACTIVE_NOT_PUBLIC`
- machine contract: complete v0.1
- request schema/pertinence matrix: implemented; independent validation pending
- evidence snapshot schema/hash runtime: implemented
- boundary schema/resolver: implemented
- uncertainty runtime: implemented, deliberately bounded
- source-conflict runtime: implemented, fail closed
- report delta schema/runtime: implemented
- report document schema/renderer: implemented
- one-transaction report backend: implemented
- portable verification schema/runtime: implemented
- semantic/integrity/renderer validators: implemented for current bounded cases
- ERL hosted workflow: configured; no current exact-head hosted result established
- real-data report execution: pending
- Site public UI/client: implemented on draft PR, locally validated, not merged or publicly verified
- Site hosted validation: startup-blocked before steps
- governed HTTP adapter/runtime: not implemented
- Site report endpoint: intentionally unconfigured
- independent review: pending
- public activation/release: not authorized

Public reporting bounded implementation estimate: `84%` for core ERL reporting + bounded Site client integration. This does not represent public activation completeness; the HTTP/runtime and release gates remain material.

## Archive posture
The ERL report transaction, Site consumer integration, exact protocol-version correction, hosted-validation states, missing HTTP bridge, credential boundary, merge/publication gates, and downstream propagation obligations are now durably represented in canonical repo handoffs. No continuation for this reporting lane depends on rereading the originating conversation.