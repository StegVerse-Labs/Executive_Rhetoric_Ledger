# ERL Transition Calculus Mirror Handoff

## Authority

Bounded source of truth for Issue #74 / PR #75 in `StegVerse-Labs/Executive_Rhetoric_Ledger`.

This handoff does not supersede repository-wide `ERL_MIRROR_HANDOFF.md` and does not authorize mutation of the active Fauci silence-causation workstream owned by Issue #47 / PR #48.

## Goal

Formalize ERL as a transition-first evidence framework in which observed state transitions are primitive, continuity is evidenced rather than assumed, unresolved construction remains explicit, reconstruction increases resolution without rewriting canonical observations, and hypotheses are layered only after continuity is established.

## Governing invariants

1. Observation precedes explanation.
2. Continuity is evidenced, never presumed.
3. Hypotheses never mutate the canonical observed transition record.
4. Resolution refines characterization while preserving prior opacity and provenance.
5. Similarity does not establish dependency.
6. Known common provenance cannot be double-counted as independent confirmation.
7. Unknown provenance receives bounded evidentiary weight.
8. Ontology expansion is driven by repeated observed structural need, not explanatory convenience.
9. Removing all hypotheses must leave a coherent observed/reconstructed transition graph.
10. Transition composition requires evidenced compatible boundaries.

## Installed conceptual surfaces

- `docs/transition-calculus/ERL_TRANSITION_FIRST_FOUNDATIONS.md`
- `docs/transition-calculus/ERL_TRANSITION_CALCULUS.md`
- `docs/transition-calculus/AE_COMPATIBILITY_REVIEW.md`
- `docs/transition-calculus/ERL_TRANSITION_CALCULUS_MIRROR_HANDOFF.md`

Canonical conceptual transition:

`T = <S_pre, S_post, C, E, P, U, Q>`

Opaque element:

`Ω = <slot, expected_role, observed_constraints, provenance_posture, resolution_state>`

Layer ordering:

`observe -> establish continuity -> construct transition -> resolve -> reconstruct -> hypothesize -> test`

## Installed machine-readable surfaces

### Schemas

- `schemas/transition-record.schema.json`
- `schemas/opaque-transition-element.schema.json`
- `schemas/forecast-calibration.schema.json`

### Validators

- `scripts/validate_transition_calculus.py`
- `scripts/validate_forecast_calibration.py`

### Fixtures

- `tests/transition-calculus/opaque-resolution.transition.json`
- `tests/transition-calculus/composition-conservation.composition.json`
- `tests/transition-calculus/conditional-delay.forecast.json`

### CI

- `.github/workflows/validate-transition-calculus.yml`

## Machine rules now enforced

### Continuity gate

A record marked `canonical` requires `continuity.posture = ESTABLISHED` and evidence receipts. Candidate records may not silently carry established continuity.

### Hypothesis separation

The observed transition schema permits only external `hypothesis_refs`; Layer-H hypothesis objects cannot be embedded into the canonical Layer-O transition record.

### Evidence recoverability

Every evidence identifier referenced by state boundaries, continuity, observed elements, opaque elements, provenance relations, and resolution history must resolve to a receipt in the record.

### Historical-opacity preservation

A resolved opaque element remains present in the transition record with `resolution_state = RESOLVED`, must point to a concrete observed element, and must retain a `RESOLVE_OPAQUE` history event.

### Provenance weighting

- known dependency: independent-confirmation weight must be `0`;
- common upstream: independent-confirmation weight must be `0`;
- unknown provenance: weight is capped at `0.5`;
- evidenced independence may receive full independent-confirmation weight.

### Composition conservation

The composition fixture and validator require:

- left post-state = right pre-state;
- composed pre-state = left pre-state;
- composed post-state = right post-state;
- composed evidence lineage must contain the component evidence lineage.

## Forecast-calibration adapter

Installed as schema + validator + conditional-delay fixture.

The adapter separates:

- issuance state;
- original forecast window;
- stated contingencies;
- observed contingency status;
- linked world-state events;
- forecast-state history;
- current calibration state.

Supported forecast states:

- `ACTIVE`
- `DELAYED_BY_STATED_CONTINGENCY`
- `ACCELERATED_BY_STATED_CONTINGENCY`
- `REVISED_WITHIN_MODEL`
- `INVALIDATED`
- `SUPERSEDED`
- `RESOLVED_CORRECT`
- `RESOLVED_INCORRECT`
- `UNRESOLVED`

A delayed state requires an actually observed contingency that the original forecast identified as delay-producing. A resolved forecast requires linked world-state evidence. This is the intended structure for the later Matt Randolph four-month calibration; no real-person score has yet been installed.

## AE compatibility review

Compared against current AE canonical handoffs and `docs/STATE_MANIFOLD_RELATIONAL_GOVERNANCE_MATHEMATICS.md`.

Current bounded result:

```text
AE mathematical replacement authorized: false
AE mutation authorized by this lane: false
ERL evidence-layer compatibility: yes, bounded
ERL opaque-slot concept compatible: yes, as reconstruction metadata
formal equivalence proven: false
cross-repository semantic merge authorized: false
future explicit adapter required: true
```

Key alignments:

- snapshots alone do not establish continuity;
- refinement may expose finer transitions without erasing an established coarse transition;
- governance classification does not determine whether an observed transition existed;
- classification is not enforcement;
- no implicit lineage taint;
- unresolved relation is not proof of absence.

Required boundary: ERL timestamps remain reconstruction/evidence metadata, not causal transition primitives. ERL composition remains reconstruction composition and does not claim AE causal or governance equivalence.

Compatibility re-review is required after AE-AUTO-0011 reaches terminal validated source state.

## Validation posture

Dedicated transition-calculus CI source is installed. Hosted validation evidence for the latest exact PR head is still pending observation.

A repository-wide `Validate Ledger Schemas` run on an intermediate PR head failed at `Validate primary-record intake queues`. The logged failure is in the pre-existing `assessments/intake/2026-08-22-white-house-ballroom-taxpayer-cost-intake.json`, which does not conform to the primary-record-intake schema and lacks a matching machine-readable assessment. That failure is outside Issue #74's changed paths and is not counted as transition-calculus validation failure or success.

Local clone execution was attempted but unavailable because the execution container could not resolve `github.com`; it is not counted as validation evidence.

## Remaining implementation

1. Observe exact-head hosted pass for `validate-transition-calculus.yml` or obtain equivalent repository-native validation receipt.
2. Add negative fixtures proving invalid canonical continuity, provenance over-weighting, opacity-history deletion, and composition boundary mismatch fail closed.
3. Consider splitting opaque `expected_role` into `observed_structural_role` and `candidate_role_class` if empirical fixtures show ambiguity.
4. Define an explicit ERL -> AE `tau_rho=(x,C_rho,y)` adapter after AE source stabilizes.
5. Build the real Matt Randolph four-month source/acquisition and calibration record only from preserved posts and independently reconstructed world events.
6. Do not propagate to Site, Publisher, admissibility-wiki, or stegguardian-wiki until this bounded lane reaches validated/reviewed release posture.

## Collision boundary

Do not modify `assessments/silence-causation/**` under this lane.

Do not reinterpret existing case findings as canonical transition-calculus outputs until a separately validated adapter exists.

Do not claim mathematical completeness or AE equivalence from this specification.

## Quantified posture

Denominator: 10 implementation groups.

1. conceptual foundations — complete v0.1
2. operator calculus — complete v0.1
3. bounded handoff — complete
4. machine transition/opaque schemas — complete v0.1
5. continuity/hypothesis/provenance validators — complete v0.1
6. resolution/composition fixtures — complete v0.1
7. forecast calibration adapter — complete v0.1 structural adapter
8. dedicated CI source — installed; exact-head hosted result pending
9. AE compatibility review — complete as bounded review; formal adapter deferred
10. downstream propagation/release integration — not authorized

Implementation groups materially built: 8/10.
Goal activation estimate: **80%**.
No scaffolding-only group is counted as complete.

## Canonical continuation

`StegVerse-Labs/Executive_Rhetoric_Ledger` -> Issue #74 -> PR #75 -> branch `feature/transition-first-calculus` -> this handoff.

## Archive posture

The originating transition-first insights, machine implementation, validation boundaries, forecast adapter design, and AE compatibility posture are durably represented in repository files. The complete conversation thread is not required to continue implementation.
