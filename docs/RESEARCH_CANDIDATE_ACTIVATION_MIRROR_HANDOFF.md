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
- additive registry overlays: `coordination/research-candidate-activation-registry.overlay.*.json`
- validator: `scripts/validate_research_candidate_activation.py`
- hosted validation: `.github/workflows/validate-research-candidate-activation.yml`
- bounded handoff: `docs/RESEARCH_CANDIDATE_ACTIVATION_MIRROR_HANDOFF.md`
- umbrella owner: Issue `#63`

## Reconciled candidate groups

The original activation rollout contained 12 research groups representing 13 candidate files. Subsequent addenda expanded that set. The base registry remains the historical rollout body; additive overlay files admit later candidate groups without requiring destructive rewrites of the monolithic registry.

The two Iran/Jordan candidate documents remain one continuing research group. The September 9 Meta AI child-data assembly/privacy candidate is registered through `coordination/research-candidate-activation-registry.overlay.2026-09.json` under Issue #63 ownership.

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

1. a candidate file under `research-candidates/` is missing from the base registry plus validated overlays;
2. a `*.research-candidate.json` assessment candidate is missing from the base registry plus validated overlays;
3. a registered candidate path no longer exists;
4. a registered mainline downstream artifact path no longer exists;
5. an active group lacks durable ownership;
6. an active group lacks a next executable task;
7. an active group lacks a terminal condition;
8. the active candidate layer authorizes factual findings or publication;
9. a candidate is inactive without a governed terminal state and reason;
10. a registry overlay has the wrong schema, repository binding, base-registry binding, or repository authority;
11. an overlay duplicates a group ID or candidate path already present in the base registry or another overlay.

Directory documentation such as `research-candidates/README.md` is explicitly excluded from candidate discovery and cannot itself trigger an unregistered-candidate failure.

Future research candidates must be admitted into either the base registry or a validated additive overlay in the same repository change that creates them or hosted validation fails.

Branch-owned artifacts remain represented separately from `main` artifacts. In particular, Fauci/HSGAC remains owned by Issue #47 / PR #48 on `feature/fauci-hsgac-source-custody`; its workstream, source-receipt manifest, acquisition queue, and verified-metadata chronology are recorded as `owner_branch_artifact_paths` rather than falsely asserted as current `main` paths.

## Existing stronger owners preserved

No duplicate execution authority is created for already governed workstreams. Candidate-specific owners remain stronger within their exact scopes, while Issue #63 retains umbrella ownership for candidates that otherwise lack a stronger durable owner.

## Validation evidence history

Initial hosted runs correctly failed because the first registry version treated Fauci feature-branch artifacts as if they already existed on `main`. The registry was repaired in commit `97937da5915ceec04a6619065a9d125bb8d06e43` to distinguish mainline artifacts from branch-owned artifacts.

A later reconciliation added six post-rollout candidate groups in commit `20a223496bd56aeaf7a95ba386c0b3c809053691`; hosted activation validation run `33144746162` succeeded.

On 2026-09-10, PR #152 exposed a new drift condition. The activation validator reported two unregistered paths: `research-candidates/README.md`, which is documentation rather than a candidate, and `research-candidates/2026-09-09-meta-ai-child-data-assembly-privacy.md`, which was a real candidate that had been added without activation-registry admission. This was not caused by the Iran intake itself; the Iran evidence was correctly folded into the already-registered cyber-physical sabotage lineage.

The remediation installs an additive overlay contract, registers the Meta privacy candidate in `coordination/research-candidate-activation-registry.overlay.2026-09.json`, excludes `README.md` from candidate discovery, validates overlay repository/base-registry/authority bindings, enforces duplicate group/path detection across base plus overlays, and updates the workflow path filters so overlay changes always execute the activation validator.

## Validation and completion

The activation-control goal remains complete only when every extant candidate path is represented exactly once across the base registry plus validated overlays, all active groups remain durably owned with concrete next actions and terminal conditions, and the hosted validator succeeds on the current `main` state.

The September 10 drift repair is not considered complete until its pull-request validation succeeds and the repair is merged.

## Release and propagation posture

This bounded activation-control goal does not authorize raw research-candidate propagation to `StegVerse-Labs/Site`, `GCAT-BCAT-Engine/Publisher`, `admissibility-wiki`, `stegguardian-wiki`, or `master-records`. Those destinations remain governed by reviewed/publication release conditions rather than candidate activation.

## Archive condition

The historical activation rollout remains archived as completed, but the September 10 registry-drift remediation is an active maintenance correction until hosted validation succeeds and the resulting repair is merged into `main`.
