# ERL Transition Calculus Mirror Handoff

## Authority

Bounded source of truth for Issue #74 in `StegVerse-Labs/Executive_Rhetoric_Ledger`.

This handoff does not supersede repository-wide `ERL_MIRROR_HANDOFF.md` and does not authorize mutation of the active Fauci silence-causation workstream owned by Issue #47 / PR #48.

## Goal

Formalize ERL as a transition-first evidence framework in which:

- observed state transitions are primitive;
- continuity is evidenced rather than assumed;
- transition construction is preserved even when constituent elements remain unresolved;
- opaque elements are typed unresolved slots, not explanatory guesses;
- reconstruction increases resolution without rewriting canonical observations;
- hypotheses are layered only after continuity is established;
- provenance, dependency, convergence, and uncertain independence are represented explicitly;
- repeated opaque structural slots can trigger controlled ontology review.

## Installed files

- `docs/transition-calculus/ERL_TRANSITION_FIRST_FOUNDATIONS.md`
- `docs/transition-calculus/ERL_TRANSITION_CALCULUS.md`
- `docs/transition-calculus/ERL_TRANSITION_CALCULUS_MIRROR_HANDOFF.md`

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

## Current formal objects

Canonical conceptual transition:

`T = <S_pre, S_post, C, E, P, U, Q>`

Opaque element:

`Ω = <slot, expected_role, observed_constraints, provenance_posture, resolution_state>`

Layer ordering:

`observe -> establish continuity -> construct transition -> resolve -> reconstruct -> hypothesize -> test`

## Initial operator set

Identity/declaration:
- `DECLARE_STATE`
- `DECLARE_TRANSITION`
- `DECLARE_ELEMENT`
- `DECLARE_OPAQUE`

Observation:
- `ATTACH_EVIDENCE`
- `RETRACT_EVIDENCE`
- `CONTRADICT`
- `BOUND`

Resolution:
- `RESOLVE`
- `REFINE`
- `COARSEN`
- `SUSPEND_RESOLUTION`

Structure:
- `COMPOSE`
- `DECOMPOSE`
- `BRANCH`
- `CONVERGE`
- `LINK`

Provenance/convergence:
- `DEPENDENCY`
- `INDEPENDENCE`
- `UNKNOWN_PROVENANCE`
- `CONVERGENCE`

Hypothesis:
- `PROPOSE_HYPOTHESIS`
- `PREDICT_SIGNATURE`
- `ATTACH_DISCONFIRMATION`
- `UPDATE_HYPOTHESIS`
- `REJECT_HYPOTHESIS`

## Forecast calibration adapter requirement

The intended first domain adapter should evaluate analysts such as the currently discussed energy/war forecasting case by separating:

- forecast issuance state;
- stated contingencies;
- world-state transitions;
- whether named contingencies occurred;
- whether forecast timing was delayed or accelerated within the stated model;
- invalidation versus unresolved status;
- source provenance and independent convergence.

Forecast state labels currently include:

- `ACTIVE`
- `DELAYED_BY_STATED_CONTINGENCY`
- `ACCELERATED_BY_STATED_CONTINGENCY`
- `REVISED_WITHIN_MODEL`
- `INVALIDATED`
- `SUPERSEDED`
- `RESOLVED_CORRECT`
- `RESOLVED_INCORRECT`
- `UNRESOLVED`

## Remaining implementation

1. Create machine-readable state/transition/element schema.
2. Create explicit opaque-element schema and constraints.
3. Add validator enforcing continuity gate before canonical transition admission.
4. Add validator enforcing observation/reconstruction/hypothesis separation.
5. Add provenance-lineage and convergence-weight posture.
6. Create fixture: opaque transition element -> later resolved element with preserved historical opacity.
7. Create composition/decomposition fixture with conservation checks.
8. Create forecast-calibration adapter and test case.
9. Review compatibility with `Admissible-Existence/AE` transition tables, transition algebra/dynamics, and reconstructive-singularity work.
10. After stabilization, determine whether Site, Publisher, admissibility-wiki, or stegguardian-wiki require propagated documentation; no propagation is authorized yet.

## Collision boundary

Do not modify `assessments/silence-causation/**` under this lane.

Do not reinterpret existing case findings as canonical transition-calculus outputs until a separately validated adapter exists.

Do not claim mathematical completeness from this first specification.

## Quantified posture

Denominator: 10 implementation groups listed above.

- conceptual foundations: complete for v0.1
- operator calculus: complete for v0.1
- bounded handoff: complete
- machine schemas: not installed
- validators: not installed
- fixtures/tests: not installed
- forecast adapter: not installed
- AE compatibility review: not complete
- downstream propagation: not authorized

Goal activation estimate: 30%.
Developed durable files in this bounded lane: 3/10 implementation groups materially developed; remaining groups are not to be counted as completed scaffolding.

## Canonical continuation

`StegVerse-Labs/Executive_Rhetoric_Ledger` -> Issue #74 -> branch `feature/transition-first-calculus` -> this handoff.

Thread archive posture: the transition-first conceptual work captured in the originating conversation is now durable in this bounded handoff and its two foundational documents. Continued implementation does not require retaining the full conversation thread.
