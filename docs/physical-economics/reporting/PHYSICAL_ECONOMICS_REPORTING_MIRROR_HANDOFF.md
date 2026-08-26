# ERL Physical Economics Public Reporting Mirror Handoff

## Authority
Canonical continuation source for the public, attribute-bounded report-generation layer of the ERL Physical Economics lane.

Parent lane authority: `docs/physical-economics/PHYSICAL_ECONOMICS_MIRROR_HANDOFF.md`.

## Goal
Allow a public user to request a reproducible Physical Economics report whose historical, temporal, geographic, population, unit, completeness, uncertainty, and evidentiary boundaries are derived from attributes pertinent to the requested claim at request time.

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

## Governing semantics
Required attributes preserve earliest admissible observation, latest observed/complete date, current-period completeness, release lag, methodology regime/comparability, revision vintage, geography/population/unit scope, source authority/provenance, uncertainty/quality, and missingness/opacity.

Attribute selection is deterministic through pertinence matrix version `0.1`; required evidence cannot be excluded or replaced by contextual evidence. Partial periods cannot silently become complete. Methodology breaks require validated bridges. Release-vintage evidence cannot be rewritten by current-vintage revisions. Unknown covariance/dependence remains unresolved rather than acquiring fabricated precision. Source conflicts are never reconciled by guess.

## Implemented report transaction
The reporting layer contains:
- immutable evidence-snapshot finalization/self-verification;
- evidence-derived boundary resolution;
- bounded uncertainty propagation;
- conservative source-conflict handling;
- deterministic report delta generation;
- deterministic report document + Markdown renderer;
- one-transaction report backend;
- portable verification receipts;
- semantic/integrity/renderer validators and fixtures.

`generate_physical_economics_public_report.py` does not acquire network evidence and does not invent findings. It returns `GENERATED_NOT_PUBLICLY_ACTIVATED` only when portable verification is `VERIFIABLE`.

## ERL validation posture
The dedicated reporting workflow is configured, but exact-current-head hosted validation is still not established for the umbrella branch. PR #75 remains an open/draft/unmerged integration lane and was last observed non-mergeable. No older workflow result or workflow source presence is a substitute for an exact-current-head hosted result.

## Site public-client integration
Canonical Site lane:

```text
repo: StegVerse-Labs/Site
issue: #496
PR: #499
handoff: docs/physical-economics/PUBLIC_REPORT_UI_MIRROR_HANDOFF.md
```

The Site client preserves ERL authority: required attributes cannot be excluded, matrix version is `0.1`, boundary renders before findings, backend absence fails closed, non-`VERIFIABLE` receipts fail closed, and transport omits credentials.

### Validation chronology
A historical Site head had provider-level `startup_failure` with no runner and zero validation steps. This was not a code-test failure and was superseded by exact-head hosted success.

Feature head `0d8688d05064e6bf63f160ec3c7eaf556d002cfc` passed the Physical Economics UI validator, Site handoff orchestrator, Site bootstrap validation, ecosystem heartbeat, and StegFin validation before merge.

### Merge proof
PR #499 was moved out of draft only after current validation/mergeability checks and then merged by squash:

```text
source head: 0d8688d05064e6bf63f160ec3c7eaf556d002cfc
merged: true
merge commit: c9ec2d1b106063fc295a11cb39fe25b6111d4c5e
merged_at: 2026-08-26T20:05:37Z
```

`Physical-Economics.html` was then independently read from Site `main`, proving repository installation. Its report-endpoint meta value remains blank, so merger/publication cannot be treated as functional report activation.

### Pages deployment proof
Exact merge commit `c9ec2d1b106063fc295a11cb39fe25b6111d4c5e` produced successful main-branch Site orchestration/bootstrap/heartbeat runs and GitHub `pages build and deployment` run `33008628651`.

Pages jobs:

```text
build: 98308804543 -> success
deploy: 98308846026 -> success
report-build-status: 98308846048 -> success
```

The deploy log records:

```text
pages_build_version: c9ec2d1b106063fc295a11cb39fe25b6111d4c5e
Created deployment for c9ec2d1b106063fc295a11cb39fe25b6111d4c5e
Reported success!
Evaluated environment url: http://stegverse.org/
```

This establishes successful deployment of the exact merge commit to the configured public Pages environment.

A separate HTTP/content observation of `https://stegverse.org/Physical-Economics.html` has not yet been obtained through the available web-access path. Preserve the distinction: `MERGED_AND_PAGES_DEPLOYED` is proven; independently observed public page response remains pending. Site Issue #496 remains open under that stricter gate.

## Public button semantics
Logical chain:

`public Site request -> governed HTTP adapter -> ERL report transaction -> prepared evidence snapshot -> immutable snapshot -> boundary -> governed findings/state -> deterministic report -> portable verification -> Site rendering`.

Site request/presentation is merged and Pages-deployed. ERL report transaction is implemented. The canonical ERL-owned HTTP adapter source is now implemented and bounded-hosted-validated under `docs/physical-economics/reporting/transport/PHYSICAL_ECONOMICS_HTTP_ADAPTER_MIRROR_HANDOFF.md`. The remaining functional bridge is **resident deployment/runtime activation** of that validated adapter with a real governed admitted-snapshot registry; evidence, pertinence, boundary, uncertainty, conflict, and finding authority remain in ERL.

The Site endpoint must remain blank until the adapter has independent live runtime proof. Populating the endpoint is an activation step.

## Fail-closed conditions
Fail closed if required opacity is hidden, required evidence excluded/replaced by context, coverage exceeds support, partial periods become complete, methodology breaks are crossed without bridge, revisions rewrite historical vintage, proxies become direct measures, missing values become neutral/zero, aggregation erases supported divergence, uncertainty is dropped/fabricated, source conflicts are guessed away, renderer invents findings, hashes/protocols do not reproduce, adapter returns non-`VERIFIABLE` as success, or Site points to an adapter without independent runtime proof.

## Credential / runtime boundary
No NON-TV/TVC credential may be introduced into the reporting transaction, Site, or GitHub-token runtime authority. Render is not authorized.

No manual/iPhone user action is currently proven necessary. If a future public transport provider requires authorization, it must be represented through TV/TVC authority and recorded before activation.

## Remaining work
1. consume current hosted ERL reporting/ledger validation after each final handoff-only head and any failures;
2. integrate real Physical Economics evidence/state snapshots and governed findings into report execution;
3. add broader composed-claim/methodology-break/revision/distribution/partial-period fixtures;
4. independently review pertinence, boundary, uncertainty, conflict, renderer, and verification semantics;
5. independently observe the deployed Site Physical Economics page response/content and then close Site Issue #496 if its publication gate is satisfied;
6. retain the single canonical ERL transport lane; do not create a duplicate Site or communications transport owner;
7. install the validated adapter in the authorized resident execution substrate, bind a real governed admitted-snapshot registry, and obtain independent live runtime proof;
8. only after live adapter proof populate the Site endpoint and independently execute a real end-to-end `VERIFIABLE` report;
9. only after real-data execution, current ERL hosted validation, public transport proof, Site integration, and independent review consider public activation/release.

## Cross-repository propagation obligations
- Site publication-observation proof must be recorded in the Site handoff and propagated here.
- HTTP-adapter authority/runtime proof must be recorded in its owning repo handoff and referenced here.
- ERL real-data/report receipts remain report-content authority.
- Site remains presentation/request consumer.
- No release propagation to Publisher/admissibility-wiki/stegguardian-wiki until actual release posture is reached.

## Current posture
- reporting layer: `FORMAL_IMPLEMENTATION_ACTIVE_NOT_PUBLIC`
- machine contract/pertinence matrix: implemented v0.1
- snapshot/boundary/uncertainty/conflict/delta/renderer/backend/verification runtimes: implemented
- bounded ERL validators: implemented
- repository-wide ERL hosted validation: PASS at `c0638c0c10cbbf218b2ca178ee8dc74a9ea89d28` via `Validate Ledger Schemas` run `33011563705`; final handoff-only heads require normal exact-head recheck
- real-data report execution: pending
- Site public UI/client: implemented, hosted-validated, merged, and Pages-deployed
- independent HTTP observation of Site page: pending
- Site Issue #496: open pending separate public observation
- governed HTTP adapter source/runtime wrapper: implemented; `Validate Physical Economics HTTP Adapter` run `33011540044` PASS at `6c351ea0b7e89a96454865dae0ea896a1a757738`; resident deployment/runtime proof pending
- Site report endpoint: intentionally blank
- independent review: pending
- public end-to-end activation/release: not authorized

Public reporting bounded **source implementation** estimate: `94%` for core ERL reporting, validated ERL HTTP transport source, and merged/Pages-deployed Site consumer. This is not activation completeness; resident runtime deployment, real admitted evidence, independent runtime/page observation, Site endpoint binding, end-to-end execution, and review remain material.

## Archive posture
All current ERL reporting and downstream Site merge/deployment state is durably represented here. Continued reporting work does not require rereading the originating conversation.