# ERL Research Candidate Activation Mirror Handoff

## Authority

Bounded source of truth for the repository-wide research-candidate activation rollout in `StegVerse-Labs/Executive_Rhetoric_Ledger`. Repository-wide continuity remains governed by `ERL_MIRROR_HANDOFF.md`; candidate-specific issues, task states, PRs, and assessment handoffs remain stronger authorities within their exact scopes.

## Goal

Ensure every ERL research-candidate artifact group is durably discoverable, active while unresolved research remains, assigned to an executable owner, protected from accidental deactivation, and prevented from treating candidate-layer existence as a factual or publication finding.

Goal ID: `ERL-RESEARCH-CANDIDATE-ACTIVATION-001`

Canonical branch: `main`

Umbrella durable owner: Issue `#63`

## Installed control surfaces

- activation registry: `coordination/research-candidate-activation-registry.v1.json`
- validator: `scripts/validate_research_candidate_activation.py`
- hosted validation: `.github/workflows/validate-research-candidate-activation.yml`
- bounded handoff: `docs/RESEARCH_CANDIDATE_ACTIVATION_MIRROR_HANDOFF.md`
- umbrella owner: Issue `#63`

## Reconciled candidate groups

The activation registry contains 12 research groups representing 13 candidate files. The two Iran/Jordan candidate documents are one continuing research group.

1. Ruben Ray Martinez / South Padre Island — active; Issue #30.
2. ICE temporary vehicle-stop limits after fatal shootings — active; Issue #63 umbrella ownership.
3. Iran/Jordan/FirstNet escalation + qualified addendum — active continuing research; Issue #63 umbrella ownership.
4. Ellis–Scavino transfer-of-power chain — active; Issue #49 for bounded validation work plus Issue #63 for continuing candidate continuity.
5. Daniel Siad / Epstein-network death and evidence continuity — active; Issue #63.
6. DOGE/Musk exposure/source acquisition — active; Issue #3.
7. xAI Colossus 2 environmental-justice/regulatory-exemption — active; Issue #63.
8. Trump-administration oil-flow normalization claim — active; Issue #63.
9. Cassidy / Trump IRS audit-protection authority chain — active; Issue #63.
10. AI integration / reservation split — active; Issue #63.
11. UAP disclosure / documentary feedback loop — active; Issue #62 and `task-state/UAP-MEDIA-001.json`.
12. Fauci July 29, 2026 HSGAC silence-causation — active / not assessable; Issue #47 / PR #48.

## Activation semantics

`active=true` means an unresolved research frontier has a durable owner and a concrete next executable task. It does not mean a proposition is true, independently established, admissible for publication, or promoted to a final assessment.

A downstream assessment, review, receipt, or validation artifact does not automatically deactivate the originating research candidate. Later contradictory, corrective, superseding, or newly available evidence remains admissible into the research frontier until a governed terminal transition is recorded.

Allowed terminal transitions are:

- `PROMOTED`
- `SUPERSEDED`
- `MERGED`
- `CLOSED_WITH_REASON`

An inactive registry entry must name a terminal state and durable reason.

## Machine-enforced invariants

The validator fails closed when:

1. a file under `research-candidates/` is missing from the registry;
2. a `*.research-candidate.json` assessment candidate is missing from the registry;
3. a registered candidate path no longer exists;
4. a registered downstream artifact path no longer exists;
5. an active group lacks durable ownership;
6. an active group lacks a next executable task;
7. an active group lacks a terminal condition;
8. the active candidate layer authorizes factual findings or publication;
9. a candidate is inactive without a governed terminal state and reason.

Future research candidates must be admitted into the activation registry in the same repository change that creates them or hosted validation fails.

## Existing stronger owners preserved

No duplicate execution authority was created for already governed workstreams:

- DOGE/Musk remains Issue #3-owned.
- Ruben Ray Martinez remains Issue #30-owned.
- Fauci/HSGAC remains Issue #47 / PR #48-owned.
- UAP media remains Issue #62 / UAP-MEDIA-001-owned.
- Ellis–Scavino Issue #49 remains authoritative only for its bounded validation-evidence work; Issue #63 prevents unrelated candidate continuity from becoming ownerless.

All other currently discovered candidate groups are actively owned by Issue #63 until a stronger candidate-specific owner is installed and the registry is updated.

## Remaining substantive research by destination

Destination: `StegVerse-Labs/Executive_Rhetoric_Ledger`

- ICE vehicle-stop group: authoritative policy/directive custody and implementation evidence.
- Iran/Jordan/FirstNet: continuing correction, contradiction, and later-event intake against preserved reviewed snapshots.
- Ellis–Scavino: native validation evidence plus outstanding source and contradiction review.
- Daniel Siad: primary-source custody, evidence-continuity reconstruction, alternatives/disconfirmers.
- DOGE/Musk: missing receipts, controls, validation supersession, independent governance review.
- xAI Colossus 2: permitting/regulatory/emissions/enforcement/community/control evidence.
- oil-flow normalization: exact primary statements, denominator, and physical-flow reconstruction.
- Cassidy/IRS: May instruments, July 13 judicial order, Cassidy primary statement, confirmation and post-ruling state.
- AI integration reservation split: primary-source, counterexample, adoption, reservation, and governance trajectory evidence.
- UAP media: evidence-class-separated acquisition and provenance enforcement.
- Fauci/HSGAC: WS-A primary custody and WS-C authority/lifecycle graph, then later gated workstreams.
- Ruben Ray Martinez: governed multi-authority review and missing primary records.

No research-candidate activation rollout itself authorizes propagation to Site, Publisher, admissibility-wiki, stegguardian-wiki, or master-records. Reviewed publication remains governed by each candidate's existing release contract.

## Validation and completion

Activation rollout completion requires:

1. every extant candidate path represented exactly once;
2. all groups active or explicitly terminal;
3. every active group durably owned;
4. every active group carrying a concrete next executable task and closure condition;
5. validator and hosted workflow installed on `main`;
6. hosted workflow success observed after installation.

Until hosted success is observed, rollout state is `IMPLEMENTED / VALIDATION_PENDING`.

## Completion accounting

Denominator: 5 rollout deliverable groups.

1. complete candidate inventory and grouping — complete
2. durable umbrella ownership for orphan candidate groups — complete
3. machine-readable activation registry — complete
4. fail-closed validator/workflow — complete as installed; hosted proof pending
5. bounded mirror handoff — complete

Current activation implementation: 5/5 installed.
Current activation proof: pending hosted validation.
Scaffolding/stubs: 0.

## Archive condition

This chat's activation requirements are durably transferred once the registry, validator, workflow, handoff, and Issue #63 exist. A failed hosted validation remains repository-native executable work under Issue #63 and does not require chat history; a successful run closes the activation proof gap.
