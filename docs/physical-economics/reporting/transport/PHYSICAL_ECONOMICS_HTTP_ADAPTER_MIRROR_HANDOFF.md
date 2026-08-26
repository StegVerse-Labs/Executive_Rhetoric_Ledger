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

## Current state
- collision search: complete
- owner: ERL reporting lane
- handoff: established
- HTTP adapter implementation: pending
- snapshot registry schema/runtime: pending
- deterministic adapter tests: pending
- hosted CI: pending
- live runtime deployment: not performed
- live runtime proof: absent
- Site endpoint population: not authorized
- end-to-end public report activation: not authorized

## Next executable boundary
Implement registry schema + adapter + deterministic fail-closed tests, validate them repository-natively, then update this handoff. Do not configure the Site endpoint until an independently reachable deployed adapter produces a `VERIFIABLE` response under real admitted evidence.
