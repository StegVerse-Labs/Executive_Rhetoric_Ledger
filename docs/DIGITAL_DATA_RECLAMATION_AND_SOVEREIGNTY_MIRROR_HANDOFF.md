# Digital Data Reclamation and Sovereignty Mirror Handoff

Updated: 2026-09-09

## Goal Task ID

`SS-EVIDENCE-COMPARISON-001`

Canonical task record: `StegVerse-Labs/.github/data/canonical-task-records/SS-EVIDENCE-COMPARISON-001.json`
COSV: `40000100100000`

## Scope

This scoped handoff governs the documentation and first implementation foundation created from the ERL privacy/derived-data intake. It does not replace `docs/ERL_KV_STORAGE_MIRROR_HANDOFF.md` for ERL-to-KnowledgeVault storage proof.

The current parent task remains canonical because it is the registered ACTIVE task that established the ERL/KV evidence boundary. This implementation slice is bounded to schemas, deterministic validation, fail-closed authority semantics, and evidence-bounded discovery topology; it does not claim a live deletion service.

## Installed architecture and implementation

- `docs/DIGITAL_DATA_RECLAMATION_AND_SOVEREIGNTY.md`
- `docs/SKAP_ACCOUNT_DISCLOSURE_GRAPH.md`
- `schemas/personal-data-inventory.schema.json`
- `schemas/data-propagation-graph.schema.json`
- `schemas/derived-data-authority-receipt.schema.json`
- `schemas/skap-account-disclosure-graph.schema.json`
- `fixtures/digital-data-reclamation/`
- `scripts/validate_digital_data_reclamation.py`
- `.github/workflows/validate-digital-data-reclamation.yml`

The Personal Data Inventory models source objects, external appearances, removal state, and five separable authority dimensions. The Data Propagation Graph models source/copy/index/broker/derived/downstream/model nodes. The Derived Data Authority receipt fails closed when no derivation authority exists.

The SKAP Account Disclosure Graph extends discovery upstream from known harvesting sites. Every authorized SKAP account can seed an evidence-bounded account-provider topology:

`SKAP account -> account provider -> declared/observed downstream organization -> additional recipient -> broker/search/public surface`

This graph distinguishes evidence-backed distribution relationships from unverified inference. A provider privacy disclosure, subprocessor list, regulator/court record, user export, or authentic transfer observation may establish a downstream candidate. It does not by itself prove that a particular user's datum traversed that edge.

The deterministic validator enforces SKAP account/provider referential integrity, organization and edge uniqueness, retained evidence references for evidence-backed edges, and a fail-closed rule preventing `INFERRED_UNVERIFIED` or `UNKNOWN` edges from becoming `PRIMARY` reclamation targets.

## Canonical concepts

Digital ownership separates custody, access, correlation, derivation, and propagation. Technical readability does not automatically confer authority to correlate or derive.

The reclamation lifecycle is:

`discover -> classify -> establish authority -> request/execute deletion or restriction -> propagate revocation -> verify -> receipt -> monitor recurrence`

Discovery itself now has two complementary origins:

`known external harvesting/removal targets`

plus

`known SKAP accounts -> account providers -> evidence-backed customer-data distribution graph`

KnowledgeVault is the intended authoritative private inventory/continuity surface for account topology, source objects, external appearances, provider-distribution evidence, requests, responses, revocation state, receipts, and recurrence observations. Graph membership is discovery context, not execution authority; Interlock/InTr remains the governed transition authority.

## Evidence boundary

The architecture refuses universal Internet-erasure claims. A submitted request is not proof of deletion. A provider disclosure relationship is not proof that a specific user's data traversed it. An inferred relationship cannot be promoted to a primary reclamation target without stronger evidence.

## Observed Google baseline — 2026-09-09

The user supplied current-iPhone screenshots of Google's `Results about you` interface showing result checking and removal-request states such as `In progress` and `Approved`, including visible people-search targets. This is retained only as a bounded comparison point for search-surface removal; it does not establish source-site deletion or full downstream propagation control.

## Current state

`FOUNDATION_IMPLEMENTED / HOSTED_VALIDATION_OF_BASE_FOUNDATION_PASSED / SKAP_DISCLOSURE_GRAPH_IMPLEMENTED_PENDING_CURRENT_PR_VALIDATION / LIVE_RECLAMATION_RUNTIME_NOT_YET_CLAIMED`

No live deletion/reclamation service, provider adapter set, legal-rights router, recurrence monitor, or cross-provider verification runtime is claimed yet.

## Remaining implementation decomposition

1. Bind Personal Data Inventory and SKAP account topology to concrete KnowledgeVault writer/readback receipts.
2. Build evidence ingestion that derives disclosure-graph edges from provider policies, subprocessor lists, regulatory records, user exports, and authentic observations.
3. Reconcile the SKAP Account Disclosure Graph into the Data Propagation Graph without converting candidate relationships into user-specific transfer facts.
4. Bind Derived Data Authority receipts to Interlock/InTr governed transition evaluation.
5. Build provider discovery/removal/restriction adapters and verification/proof-class engine.
6. Build recurrence/reappearance monitoring and legal-rights/jurisdiction routing.
7. Add prospective disclosure authority envelopes for new StegVerse-originated data.

By Goal Prompt Count 20, genuinely separable implementation lanes must move into new canonical Goal Task IDs rather than extending this evidence-comparison parent indefinitely.

## Manual work

None for this implementation slice.
