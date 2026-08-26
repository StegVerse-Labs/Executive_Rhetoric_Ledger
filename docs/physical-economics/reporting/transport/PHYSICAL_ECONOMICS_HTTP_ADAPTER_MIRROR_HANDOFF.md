# Physical Economics HTTP Adapter Mirror Handoff

## Authority
Canonical continuation source for the narrow HTTP transport adapter around the ERL Physical Economics public report transaction.

Parent authority: `docs/physical-economics/reporting/PHYSICAL_ECONOMICS_REPORTING_MIRROR_HANDOFF.md`.
Umbrella integration branch: `feature/transition-first-calculus` / PR #75.

## Ownership decision
Collision search on 2026-08-26 found no existing Physical Economics report HTTP adapter lane. `StegVerse-Labs/Comms-Gateway` is **not** the owner because its canonical boundary explicitly excludes execution and publication. `StegVerse-Labs/External-Actor-Gateway` is empty and has no established handoff/runtime authority. Site is presentation/request only and must not own report evidence or generation authority.

Therefore this adapter is an ERL-owned transport surface colocated with the authoritative report transaction. Runtime deployment/activation remains separate from source implementation.

## Goal
Expose one bounded HTTP POST transaction that accepts only the canonical public report request, selects only a pre-admitted prepared evidence snapshot through a deterministic registry, invokes the existing ERL report transaction, and returns the exact report-document / verification-receipt shape consumed by Site.

## Non-authority boundary
The adapter MUST NOT:
- acquire evidence from the network;
- decide pertinence;
- construct substantive findings;
- widen evidence boundaries;
- reconcile source conflicts;
- fabricate uncertainty;
- use a non-admitted snapshot;
- use Site as evidence authority;
- return successful report state when portable verification is not `VERIFIABLE`;
- require NON-TV/TVC credentials;
- use GitHub-token runtime authority;
- require Render.

## Snapshot-provider boundary
The public Site sends only the report request. The underlying ERL report transaction requires a prepared snapshot draft. Therefore transport needs an explicit snapshot-selection boundary rather than silently becoming an evidence-acquisition layer.

V0.1 design:
- runtime is configured with a registry file;
- registry entries bind a deterministic scope/claim signature to a prepared snapshot-template path;
- request identity and requested-as-of time may be rebound into a copy of the template only after registry selection;
- evidence attributes and source receipts are never altered by transport;
- no exact compatible admitted registry entry -> fail closed with service unavailable;
- duplicate compatible entries -> fail closed as ambiguous;
- template pertinence-matrix version must equal request version;
- historical/as-known-at-time requests cannot select evidence released after the requested as-of time;
- report execution remains the existing `generate_physical_economics_public_report.py` transaction.

This registry is an admission/selection surface, not a data downloader.

## Planned machine surfaces
- `schemas/physical-economics-report-snapshot-registry.schema.json`
- `scripts/serve_physical_economics_public_report.py`
- `scripts/validate_physical_economics_http_adapter.py`
- `tests/physical-economics-reporting/http-adapter.registry.fixture.json`
- `.github/workflows/validate-physical-economics-http-adapter.yml`
- this handoff.

## Expected HTTP contract

```text
POST /v1/physical-economics/reports
Content-Type: application/json
body: canonical physical-economics report request only
```

Success JSON must contain:
- `state: GENERATED_NOT_PUBLICLY_ACTIVATED`
- `report_document`
- `verification_receipt`
- `report_markdown`

Site already independently validates those fields and rejects non-`VERIFIABLE` receipts.

Operational endpoints may expose only non-authorizing liveness/readiness state. No evidence contents or credentials may be exposed through health responses.

## Implemented machine surfaces
- `schemas/physical-economics-report-snapshot-registry.schema.json`
- `scripts/serve_physical_economics_public_report.py`
- `scripts/validate_physical_economics_http_adapter.py`
- `tests/physical-economics-reporting/http-adapter.registry.fixture.json`
- `tests/physical-economics-reporting/http-adapter.snapshot.fixture.json`
- `.github/workflows/validate-physical-economics-http-adapter.yml`

The HTTP runtime uses only Python standard-library HTTP transport plus the repository's existing validation/runtime dependencies. It accepts bounded JSON POST requests at `/v1/physical-economics/reports`, exposes non-authorizing `/healthz` and `/readyz`, enforces a bounded request size, validates request/registry/snapshot schemas, rejects unmatched or ambiguous admissions, rejects repository-path escape, preserves evidence attributes and source receipts, enforces the historical-vintage release-date boundary, and returns only Site-compatible report/verification payloads after the existing report transaction yields `GENERATED_NOT_PUBLICLY_ACTIVATED` plus `VERIFIABLE`.

## Hosted validation evidence
Feature-branch push execution was added because GitHub API commits were not emitting PR-synchronize workflow runs and the previous push trigger covered only `main`.

```text
workflow: Validate Physical Economics HTTP Adapter
run: 33011540044
validated head: 6c351ea0b7e89a96454865dae0ea896a1a757738
event: push
conclusion: success
```

That run exercised the real underlying report transaction and proved:
- registry schema validity;
- exact admitted snapshot selection;
- unmatched and ambiguous admission fail-closed behavior;
- historical-vintage release guard;
- preservation of evidence attributes/source receipts;
- Site-compatible `VERIFIABLE` response;
- omission of internal runtime paths;
- invalid-registry rejection before execution.

Later repository-wide `Validate Ledger Schemas` run `33011563705` at `c0638c0c10cbbf218b2ca178ee8dc74a9ea89d28` also completed successfully. A final exact-head adapter run must still be consumed after this handoff mutation.

## Current state
- collision search: complete
- owner: ERL reporting lane
- handoff: current
- HTTP adapter source implementation: complete
- snapshot registry schema/runtime: complete
- deterministic adapter tests: complete
- bounded hosted adapter validation: PASS
- repository-wide ledger validation: PASS
- live runtime deployment: not performed
- live runtime proof: absent
- real admitted production snapshot registry: not activated
- Site endpoint population: not authorized
- end-to-end public report activation: not authorized

## Next executable boundary
Source implementation is no longer the blocker. The next transition is runtime activation: install the validated adapter in the authorized resident execution substrate, bind a real governed admitted-snapshot registry, obtain independent live HTTP/runtime proof, and only then populate the Site endpoint. If that runtime transition is owned by Interlock/InTr/TVC resident control, continue there rather than creating another transport implementation.

Do not configure the Site endpoint until an independently reachable deployed adapter produces a `VERIFIABLE` response under real admitted evidence.

## Archive posture
All source implementation, ownership, fail-closed semantics, and bounded validation evidence are durable here. Continuation does not require this conversation. Remaining adapter work is activation/runtime work, not missing repository implementation.


## Final source-continuity checkpoint — 2026-08-26

Parent reporting and Physical Economics handoffs have been reconciled to the same ownership/state boundary. The former White House ballroom ledger-schema blocker was separately repaired and the full repository ledger validation passed at `c0638c0c10cbbf218b2ca178ee8dc74a9ea89d28` in run `33011563705`.

This handoff mutation is intentionally the final ERL source-continuity checkpoint for the session so both branch-enabled validators can execute on one exact final head.

No new runtime claim is created by this checkpoint:
- resident HTTP deployment: absent;
- real production admitted-snapshot registry: absent;
- Site endpoint: blank;
- live end-to-end public report: absent;
- release: not authorized.

If exact-head validation passes, the remaining adapter/public-report transition is runtime/evidence activation and can continue entirely from repository handoffs without conversation context.
