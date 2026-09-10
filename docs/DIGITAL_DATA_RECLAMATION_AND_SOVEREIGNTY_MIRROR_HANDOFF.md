# Digital Data Reclamation and Sovereignty Mirror Handoff

Updated: 2026-09-09

## Goal Task ID

`SS-EVIDENCE-COMPARISON-001`

Canonical task record: `StegVerse-Labs/.github/data/canonical-task-records/SS-EVIDENCE-COMPARISON-001.json`
COSV: `40000100100000`

## Scope

This scoped handoff governs the documentation and implementation foundation created from the ERL privacy/derived-data intake. It does not replace `docs/ERL_KV_STORAGE_MIRROR_HANDOFF.md` for ERL-to-KnowledgeVault storage proof.

The current parent task remains canonical because it is the registered ACTIVE task that established the ERL/KV evidence boundary. This implementation slice is bounded to schemas, deterministic validation, fail-closed authority semantics, evidence-bounded discovery topology, and deterministic reclamation-target reconciliation; it does not claim a live deletion service.

## Installed architecture and implementation

- `docs/DIGITAL_DATA_RECLAMATION_AND_SOVEREIGNTY.md`
- `docs/SKAP_ACCOUNT_DISCLOSURE_GRAPH.md`
- `docs/RECLAMATION_TARGET_RECONCILIATION.md`
- `schemas/personal-data-inventory.schema.json`
- `schemas/data-propagation-graph.schema.json`
- `schemas/derived-data-authority-receipt.schema.json`
- `schemas/skap-account-disclosure-graph.schema.json`
- `schemas/reclamation-target-set.schema.json`
- `fixtures/digital-data-reclamation/`
- `scripts/build_reclamation_target_set.py`
- `scripts/validate_digital_data_reclamation.py`
- `.github/workflows/validate-digital-data-reclamation.yml`

The Personal Data Inventory models source objects, external appearances, removal state, and five separable authority dimensions. The Data Propagation Graph models source/copy/index/broker/derived/downstream/model nodes. The Derived Data Authority receipt fails closed when no derivation authority exists.

The SKAP Account Disclosure Graph extends discovery upstream from known harvesting sites. Every authorized SKAP account can seed an evidence-bounded account-provider topology:

`SKAP account -> account provider -> declared/observed downstream organization -> additional recipient -> broker/search/public surface`

This graph distinguishes evidence-backed distribution relationships from unverified inference. A provider privacy disclosure, subprocessor list, regulator/court record, user export, or authentic transfer observation may establish a downstream candidate. It does not by itself prove that a particular user's datum traversed that edge.

The deterministic validator enforces SKAP account/provider referential integrity, organization and edge uniqueness, retained evidence references for evidence-backed edges, and a fail-closed rule preventing `INFERRED_UNVERIFIED` or `UNKNOWN` edges from becoming `PRIMARY` reclamation targets.

## Reclamation target reconciliation

`build_reclamation_target_set.py` combines the SKAP disclosure graph with an observed Data Propagation Graph to produce `stegverse.reclamation-target-set/v1`.

Target posture is evidence bounded:

- authorized SKAP account providers -> `PRIMARY / DIRECT / ELIGIBLE`;
- provider-declared, observed-transfer, and regulator/court downstream edges -> eligible downstream targets unless the source graph deliberately makes them more conservative;
- credible third-party reports -> watch-only;
- inferred or unknown downstream edges -> `WATCH / BLOCKED_UNVERIFIED`;
- currently observed or reappeared propagation nodes -> eligible downstream targets;
- already requested/restricted/provider-asserted-deleted propagation nodes -> watch posture;
- independently verified deleted propagation nodes -> complete posture.

The reconciler refuses cross-subject joins and preserves distinct evidence lanes even when multiple lanes identify the same organization. The target set is a governed investigation/action candidate surface, not proof that deletion occurred or that a specific datum traversed any unobserved edge.

The paired reconciliation fixtures and `reclamation-target-set.sample.json` provide deterministic expected output. Repository validation reconstructs and compares that target set, rejects a cross-subject join, and verifies that unverified targets cannot become `ELIGIBLE`.

## Validation evidence

PR #146 installed the SKAP Account Disclosure Graph and passed both the dedicated Digital Data Reclamation workflow and the full Ledger validation before merge at `26208c5c17cd6cc4bc0594f789d9803e9dc5f3f8`.

PR #147 installed deterministic reclamation-target reconciliation. Before merge, dedicated Digital Data Reclamation workflow run `34435166055` completed `success`, and full Ledger validation run `34435165897` completed `success`, both against head `d68dd5ad6eeb00577c85ff487ede42a1d56c0453`. PR #147 then merged to `main` at `c78b2fe4be29dc4e9e15167281b35be8105a922a`.

These runs validate repository implementation and deterministic evidence boundaries. They do not prove live provider deletion, external network execution, or KnowledgeVault write/readback for generated target sets.

## Canonical concepts

Digital ownership separates custody, access, correlation, derivation, and propagation. Technical readability does not automatically confer authority to correlate or derive.

The reclamation lifecycle is:

`discover -> classify -> establish authority -> reconcile targets -> request/execute deletion or restriction -> propagate revocation -> verify -> receipt -> monitor recurrence`

Discovery has two complementary origins:

`known external harvesting/removal targets`

plus

`known SKAP accounts -> account providers -> evidence-backed customer-data distribution graph`

KnowledgeVault is the intended authoritative private inventory/continuity surface for account topology, source objects, external appearances, provider-distribution evidence, generated target sets, requests, responses, revocation state, receipts, and recurrence observations. Graph membership is discovery context, not execution authority; Interlock/InTr remains the governed transition authority.

## Evidence boundary

The architecture refuses universal Internet-erasure claims. A submitted request is not proof of deletion. A provider disclosure relationship is not proof that a specific user's data traversed it. An inferred relationship cannot be promoted to an eligible reclamation target without stronger evidence.

## Observed Google baseline — 2026-09-09

The user supplied current-iPhone screenshots of Google's `Results about you` interface showing result checking and removal-request states such as `In progress` and `Approved`, including visible people-search targets. This is retained only as a bounded comparison point for search-surface removal; it does not establish source-site deletion or full downstream propagation control.

## Current state

`FOUNDATION_IMPLEMENTED / SKAP_DISCLOSURE_GRAPH_VALIDATED / DETERMINISTIC_TARGET_RECONCILIATION_VALIDATED_AND_MERGED / LIVE_RECLAMATION_RUNTIME_NOT_YET_CLAIMED`

No live deletion/reclamation service, provider adapter set, legal-rights router, recurrence monitor, KnowledgeVault target-set writer/readback receipt, or cross-provider verification runtime is claimed yet.

## Remaining implementation decomposition

1. Bind Personal Data Inventory, SKAP account topology, and generated reclamation target sets to concrete KnowledgeVault writer/readback receipts.
2. Build evidence ingestion that derives disclosure-graph edges from provider policies, subprocessor lists, regulatory records, user exports, and authentic observations.
3. Bind Derived Data Authority and target execution to Interlock/InTr governed transition evaluation.
4. Build provider discovery/removal/restriction adapters and verification/proof-class engine.
5. Build recurrence/reappearance monitoring and legal-rights/jurisdiction routing.
6. Add prospective disclosure authority envelopes for new StegVerse-originated data.

By Goal Prompt Count 20, genuinely separable implementation lanes must move into new canonical Goal Task IDs rather than extending this evidence-comparison parent indefinitely.

## Manual work

None for this implementation slice.
