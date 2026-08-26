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
For every required attribute, preserve and resolve earliest admissible observation, latest observed/complete date, current-period completeness, release lag, methodology regime/comparability, revision vintage, geography/population/unit scope, source authority/provenance, source-native uncertainty/quality, and missingness/opacity.

Longer attribute-specific history may remain visible as context, but it cannot extend conclusions beyond the shortest required admissible history.

## Deterministic pertinence
Attribute selection is not free-form model discretion. `physical-economics-report-pertinence.matrix.v0.1.json` is the versioned claim-class -> required/contextual attribute protocol. Required evidence cannot be excluded by the user request or silently replaced by contextual evidence. Composed claims inherit the union of required evidence unless a narrower protocol is independently validated.

Canonical claim classes include price change, physical purchasing power, essential affordability, unmet essential need, substitution/quality compression, producer cost pressure, producer margin state, cost-margin transmission, distributional burden, regional burden, household resilience, arrears/deferred obligations, capacity/inventory constraint, tax/fee/regulatory flow, transfer-offset effect, and the full economic-condition state vector.

The canonical matrix version consumed by the public client is exactly `0.1`; descriptive aliases are not protocol-equivalent.

## Immutable evidence snapshots
`physical-economics-evidence-snapshot.schema.json` preserves per-attribute coverage, methodology, vintage, uncertainty, source receipts, and unresolved conflicts. `finalize_physical_economics_evidence_snapshot.py` defines canonical SHA-256 snapshot finalization/self-verification. Tampering changes verification state rather than silently mutating a prior report basis.

## Boundary resolver
`resolve_physical_economics_report_boundary.py` is implemented. It validates request/snapshot structures, resolves attributes only from the pertinence matrix, fails closed on required-attribute exclusion, materializes absent required attributes as opaque boundaries, computes per-attribute history, emits a common comparable/complete window only when supported by all required attributes, preserves partial periods/methodology breaks, carries uncertainty without manufacturing precision, and emits deterministic receipts.

Fixtures include a complete price report, a physical-purchasing-power report missing required physical-content evidence, and a required-attribute exclusion fail-closed case.

## Current-period and methodology rules
Allowed states: `COMPLETE`, `PARTIAL_CURRENT_PERIOD`, `PENDING_RELEASE`, `REVISED_AFTER_INITIAL_RELEASE`, `METHODOLOGY_BREAK`, `UNAVAILABLE`, `OPAQUE`.

Partial periods cannot be silently annualized. Survey design, classification, geography, population, unit, weighting, seasonal-adjustment, rebasing, or other method changes create explicit methodology regimes. Cross-regime trend claims require a validated bridge.

## Vintage/revision integrity
Release-vintage and current-vintage evidence are distinct. A retrospective report cannot silently replace historical knowable state with later revision.

`generate_physical_economics_report_delta.py` emits machine-readable change receipts for new observations, completed periods, revisions/corrections, methodology/classification changes, opacity resolution, source replacement, required-attribute protocol changes, renderer/contract changes, source-conflict resolution, and uncertainty changes.

## Statistical uncertainty
`physical_economics_uncertainty.py` implements fail-closed propagation: linear SE propagation for explicitly independent components, explicit covariance matrices for supported dependence, `UNRESOLVED` when covariance/dependence is unknown, deterministic interval arithmetic labeled non-probabilistic, and no rendering precision beyond source support.

## Source conflicts
`physical_economics_source_conflicts.py` is conservative. Conflicting values are never reconciled by guess. Automatic resolution is limited to explicit correction/replacement chains; declared scope/vintage distinctions may be preserved. Otherwise conflict remains `UNRESOLVED`.

## Deterministic report and renderer
`physical-economics-report-document.schema.json` is the machine output contract. `render_physical_economics_report.py` deterministically builds the report document/Markdown from request, snapshot, boundary, governed findings, prospective gates, and optional delta. It puts the boundary before findings, renders coverage/uncertainty, preserves finding classes, exposes opacity/gates, invents no findings, and retains reproduction receipts.

`validate_physical_economics_report_renderer.py` verifies boundary-before-findings ordering, no invented findings, schema validity, and portable hashing.

## One-transaction backend
`generate_physical_economics_public_report.py` is implemented as the bounded backend transaction. Given request + prepared evidence snapshot draft + optional governed finding/gate/delta objects, it finalizes the snapshot hash, resolves the boundary, builds/renders the report, writes outputs, emits portable verification, and returns `GENERATED_NOT_PUBLICLY_ACTIVATED` only when the receipt is `VERIFIABLE`.

It does not acquire network evidence and does not invent findings. Evidence acquisition and governed finding construction remain upstream responsibilities.

## Portable verification
`physical-economics-report-verification-receipt.schema.json` and its generator bind report content, request, snapshot, boundary, pertinence matrix, contract, renderer, and source receipt identities. Hash/protocol/source-receipt mismatches fail closed.

## ERL validation posture
`validate_physical_economics_reporting.py`, `validate_physical_economics_reporting_integrity.py`, and `validate_physical_economics_report_renderer.py` cover contract/pertinence semantics, fixtures, deterministic replay, uncertainty, delta, snapshot tamper detection, conservative conflicts, report assembly, and verification receipts. `.github/workflows/validate-physical-economics-reporting.yml` runs all three.

Hosted validation is still **not established** for the current umbrella ERL branch. PR #75 remains open, draft, unmerged, and was last fresh-observed `mergeable: false`. No exact-current-head hosted PASS may be inferred from workflow source presence or older heads. Re-query immediately before any merge/release action.

## Site public-client integration
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
- machine pre-work claim for the bounded surfaces.

The Site client preserves ERL authority: required attributes cannot be excluded, matrix version is `0.1`, boundary renders before findings, unverified receipts fail closed, backend absence fails closed, and transport omits credentials.

### Site hosted-validation chronology
Earlier exact implementation head `c09fae59eb1304909520de0e3adb6497bd35a2a4` reached GitHub but failed at provider startup before any steps (`run 32985301150`, job `98230430068`, `runner_id: 0`). That was not a code-test failure.

After archive reconciliation, exact head `c648135c49a97d541b89595823d5ada30e1134c1` executed successfully:

```text
Validate Physical Economics Report UI: run 33006446992 -> success
Site Handoff Orchestrator: run 33006446983 -> success
Site Bootstrap Validate - No Non-TV/TVC Credential Authority: run 33006446938 -> success
Ecosystem Heartbeat Orchestration: run 33006446915 -> success
Check StegFin Phone Projection - Validation Only / No GitHub Token Authority: run 33006446756 -> success
```

On that same validated head PR #499 was fresh-observed open, draft, unmerged, and `mergeable: true`. The subsequent Site handoff-only commit `0d8688d05064e6bf63f160ec3c7eaf556d002cfc` moves the branch head; current mergeability and exact-head checks must be re-queried before merge, but the exact validated parent remains durable proof of the implementation state.

Site public publication is still not verified and the report endpoint remains blank/unconfigured/fail-closed.

## Public button semantics
End-to-end logical chain:

`public Site request -> governed HTTP adapter -> ERL report transaction -> prepared evidence snapshot -> immutable snapshot -> boundary -> governed findings/state -> deterministic report -> portable verification -> Site rendering`.

ERL transaction and Site client are implemented and the Site client is hosted-validated. The missing functional bridge is a **real governed HTTP adapter/runtime** exposing the ERL transaction without moving evidence, pertinence, boundary, uncertainty, conflict, or finding authority into Site.

The Site endpoint must remain blank until that adapter has repository-native validation and live runtime proof. Populating the endpoint is an activation step, not documentation.

## Required report sections
Question/as-of; claim classes/scope; plain-language boundary; coverage matrix; methodology/comparability; uncertainty/quality; current-period completeness; applicable state-vector surfaces; distribution/regional surfaces; producer cost/margin; household burden/unmet need; tax/fee/transfer flows; observed vs reconstructed findings; unresolved/opaque elements; prospective gates; source/vintage receipts; version delta when prior report exists; portable verification receipt.

## Fail-closed conditions
Fail closed if required opacity is hidden, required evidence excluded/replaced by context, coverage exceeds support, partial periods become complete, methodology breaks are crossed without bridge, revisions rewrite historical vintage, proxies become direct measures, missing values become neutral/zero, aggregation erases supported divergence, uncertainty is dropped/fabricated, source conflicts are guessed away, renderer invents findings, hashes/protocols do not reproduce, adapter returns non-`VERIFIABLE` as success, or Site points to an adapter without independent runtime proof.

## Credential / runtime boundary
No NON-TV/TVC credential may be introduced into the reporting transaction, Site, or GitHub-token runtime authority. Render is not authorized.

No manual/iPhone user action is currently proven necessary for this reporting lane. The earlier Site startup condition self-cleared; do not invent a provider credential/settings requirement. If a later public transport provider requires authorization, it must be represented through TV/TVC authority and recorded before activation.

## Remaining work
1. integrate real Physical Economics evidence/state snapshots and governed findings into the transaction;
2. add broader fixtures for composed claims, methodology breaks, corrections, regional/distributional divergence, and partial periods;
3. obtain exact-head hosted ERL CI execution and consume failures;
4. independently review pertinence, boundary, uncertainty, conflict, renderer, and verification semantics;
5. re-query Site #499 after its handoff-only commit, satisfy draft/review/merge governance, merge, and independently verify publication;
6. create a canonical claimed lane for the governed HTTP adapter around `generate_physical_economics_public_report.py` rather than burying transport in Site;
7. validate adapter request/response + portable-verification fixtures and obtain live runtime proof;
8. only after adapter proof populate the Site endpoint and independently execute a real end-to-end `VERIFIABLE` report;
9. only after real-data execution, ERL hosted validation, public transport proof, Site publication/integration, and independent review consider public activation/release.

## Cross-repository propagation obligations
- Site merge/publication proof: record in Site bounded handoff and propagate here.
- HTTP-adapter authority/runtime proof: record in owning repo handoff and reference here.
- ERL real-data/report receipts remain report-content authority.
- Site remains presentation/request consumer.
- No release propagation to Site/Publisher/admissibility-wiki/stegguardian-wiki until actual release posture is reached.

## Current posture
- reporting layer: `FORMAL_IMPLEMENTATION_ACTIVE_NOT_PUBLIC`
- machine contract: complete v0.1
- request/pertinence protocol: implemented; independent review pending
- snapshot/hash runtime: implemented
- boundary resolver: implemented
- uncertainty runtime: implemented/bounded
- conflict runtime: implemented/fail-closed
- report delta: implemented
- report document/renderer: implemented
- one-transaction backend: implemented
- portable verification: implemented
- bounded ERL validators: implemented
- ERL exact-current-head hosted validation: not established
- real-data report execution: pending
- Site public UI/client: implemented and exact-head hosted-validated on parent `c648135...`; not merged/published
- Site PR #499: draft/unmerged; validated parent was mergeable
- governed HTTP adapter/runtime: not implemented
- Site endpoint: intentionally unconfigured
- independent review: pending
- public activation/release: not authorized

Public reporting bounded implementation estimate: `86%` for core ERL reporting + hosted-validated bounded Site consumer integration. This is not public activation completeness; HTTP/runtime, real-data, merge/publication, ERL hosted-validation, and review gates remain material.

## Archive posture
The ERL transaction, Site consumer, protocol-version correction, exact Site hosted PASS evidence, earlier startup chronology, missing HTTP bridge, credential boundary, merge/publication gates, and downstream propagation obligations are durably represented. No continuation for this reporting lane depends on rereading the originating conversation.