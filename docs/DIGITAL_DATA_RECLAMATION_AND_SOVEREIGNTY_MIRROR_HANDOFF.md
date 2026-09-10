# Digital Data Reclamation and Sovereignty Mirror Handoff

Updated: 2026-09-09

## Goal Task ID

`SS-EVIDENCE-COMPARISON-001`

Canonical task record: `StegVerse-Labs/.github/data/canonical-task-records/SS-EVIDENCE-COMPARISON-001.json`
COSV: `40000100100000`

## Scope

This scoped handoff governs the documentation and first implementation foundation created from the ERL privacy/derived-data intake. It does not replace `docs/ERL_KV_STORAGE_MIRROR_HANDOFF.md` for ERL-to-KnowledgeVault storage proof.

The current parent task remains canonical because it is the registered ACTIVE task that established the ERL/KV evidence boundary. This implementation slice is bounded to schemas, deterministic validation, and fail-closed authority semantics; it does not claim a live deletion service.

## Installed architecture

- `docs/DIGITAL_DATA_RECLAMATION_AND_SOVEREIGNTY.md`
- `research-candidates/2026-09-09-meta-ai-child-data-assembly-privacy.md`
- `research-candidates/README.md`

## First implementation foundation

Implemented on branch `impl/digital-data-reclamation-foundation-20260909`:

- `schemas/personal-data-inventory.schema.json`
- `schemas/data-propagation-graph.schema.json`
- `schemas/derived-data-authority-receipt.schema.json`
- `fixtures/digital-data-reclamation/personal-data-inventory.sample.json`
- `fixtures/digital-data-reclamation/data-propagation-graph.sample.json`
- `fixtures/digital-data-reclamation/derived-data-authority-receipt.sample.json`
- `fixtures/digital-data-reclamation/invalid-no-authority-allows-derivation.json`
- `scripts/validate_digital_data_reclamation.py`
- `.github/workflows/validate-digital-data-reclamation.yml`

The Personal Data Inventory provides a machine-readable user-centered inventory for source objects, external appearances, current removal state, and the five separable authority dimensions. The Data Propagation Graph provides explicit source/copy/index/broker/derived/downstream/model nodes and provenance-bearing edges. The Derived Data Authority receipt requires actor, requester, source objects, requested derivation, purpose, authority basis, decision, and downstream-use constraints.

The receipt schema fails closed when `authority_basis=NO_AUTHORITY`: the only valid decision is `DENY`. The deterministic validator also checks inventory object references, graph node/edge referential integrity, duplicate graph identifiers, and a negative fixture proving that `NO_AUTHORITY + ALLOW` is rejected.

## Canonical concepts

The installed design separates five digital-data rights: custody, access, correlation, derivation, and propagation.

`Derived Data Authority` is a separate governed question from source-object access. Technical readability of several objects does not automatically authorize joining them into a sensitive inference.

The reclamation lifecycle is:

`discover -> classify -> establish authority -> request/execute deletion or restriction -> propagate revocation -> verify -> receipt -> monitor recurrence`

KnowledgeVault is the intended authoritative private inventory/continuity surface for known personal-data objects, external appearances, requests, responses, evidence, revocation state, and recurrence observations. KnowledgeVault custody itself must not be interpreted as blanket authority for AI correlation across all stored objects.

## Evidence boundary

The architecture explicitly refuses a universal Internet-erasure claim. Removal success must be expressed by source-specific evidence posture. A request receipt proves submission, not deletion. Provider acknowledgement proves acknowledgement, not independent erasure. Current external non-observability proves only the checked surface at the checked time.

The model also distinguishes direct copies from indexes, caches, embeddings, independently sourced copies, relationship edges, derived attributes, retrieval surfaces, and trained-model behavior. Source deletion is not proof that those downstream representations were removed.

## Observed Google baseline — 2026-09-09

The user supplied two current-iPhone screenshots of Google's `Results about you` surface. The visible interface shows Google checking for results about the user and displaying removal-request state such as `In progress` and `Approved`. Visible result targets include Whitepages, Anywho, USPhonebook, SearchPeopleFREE, and True People Search.

This is recorded as a bounded industry-comparison observation, not a claim about Google's complete internal feature set. The screenshots show a useful search-result discovery/removal workflow, but do not establish source-site deletion, downstream propagation tracing, derived-data revocation, model-training erasure, prospective correlation authority, or user-owned cross-provider custody.

StegVerse therefore treats search-engine result removal as one provider-adapter lane inside the broader reclamation architecture rather than as the complete reclamation model.

## Product direction

Working capability name: `Digital Data Reclamation and Sovereignty`.

The intended StegVerse service combines KnowledgeVault, governed execution, provider adapters, legal-rights routing, Data Propagation Graphs, recurrence monitoring, provenance, and verifiable receipts.

The long-term differentiator is prospective sovereignty: new disclosures can carry explicit purpose, recipient, duration, redistribution, correlation, and derivation authority rather than reducing consent to a one-time opaque permission.

## Current state

`FOUNDATION_IMPLEMENTED / SCHEMAS_AND_FAIL_CLOSED_VALIDATOR_PRESENT / HOSTED_VALIDATION_PENDING / LIVE_RECLAMATION_RUNTIME_NOT_YET_CLAIMED`

No live deletion/reclamation service, provider adapter set, legal-rights router, recurrence monitor, or cross-provider verification runtime is claimed yet.

## Remaining implementation decomposition

1. Bind Personal Data Inventory to a concrete KnowledgeVault storage contract and writer/readback receipt.
2. Add Data Propagation Graph mutation/reconciliation logic from observed provider/search evidence.
3. Bind Derived Data Authority receipts to Interlock/InTr governed transition evaluation.
4. Build provider discovery/removal/restriction adapter framework, beginning with search-result and people-search lanes.
5. Build verification/proof-class engine that cannot promote request/acknowledgement into deletion.
6. Build recurrence/reappearance monitor.
7. Add legal-rights/jurisdiction routing with explicit non-legal-advice boundaries.
8. Add prospective disclosure authority envelope for new StegVerse-originated data.

By Goal Prompt Count 20, any genuinely separable remaining implementation lanes must be transferred into new canonical Goal Task IDs rather than extending this evidence-comparison parent indefinitely.

## Manual work

None for this implementation foundation.
