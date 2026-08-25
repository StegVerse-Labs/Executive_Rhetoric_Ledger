# ERL Transition Calculus — Admissible Existence Compatibility Review

Status: bounded compatibility review; no AE mutation
Owner: ERL Issue #74 / PR #75
Compared against AE canonical `main` surfaces:

- `AE_MIRROR_HANDOFF.md`
- `docs/STATE_MANIFOLD_RELATIONAL_GOVERNANCE_MIRROR_HANDOFF.md`
- `docs/STATE_MANIFOLD_RELATIONAL_GOVERNANCE_MATHEMATICS.md`
- `docs/papers/RECONSTRUCTIVE_SINGULARITY_MIRROR_HANDOFF.md`

## Result

The ERL transition-first calculus is structurally compatible with the current AE direction, but it is not identical to AE mathematics and must not be promoted as a replacement or alternate canonical mathematics.

The appropriate relationship is:

- AE remains the mathematical/protocol authority for admissible existence, resolution-indexed causal relations, refinement preservation, and governor-indexed admissibility.
- ERL is an evidence/reconstruction consumer that can represent observed transitions, evidence resolution history, opaque construction slots, provenance posture, and post-continuity hypotheses.
- ERL adapters may bind to AE semantics only where an explicit mapping exists.

## Strong alignments

### 1. Snapshots do not establish continuity

AE:

`(x,y) in C_rho` requires an observation-established relation; two snapshots alone are insufficient.

ERL:

A canonical transition requires `continuity.posture = ESTABLISHED` plus evidence receipts. Chronological adjacency is not enough.

Compatibility: **direct**.

### 2. Refinement preserves established transition identity

AE permits finer factorization without erasing the coarse established relation.

ERL preserves the original transition and its resolution history while allowing `REFINE`, `DECOMPOSE`, and opaque-slot resolution.

Compatibility: **direct**, subject to future formal mapping between AE refinement maps and ERL resolution/decomposition events.

### 3. Historical opacity is compatible with refinement

ERL's `Opaque(Ω)` adds an evidence/reconstruction concept not presently defined as a primitive in the AE state-manifold seed: a structural slot is known to participate in an established transition while its identity remains unresolved.

This does not conflict with AE so long as ERL does **not** claim that the opaque slot itself proves a causal mechanism beyond the evidence-supported transition construction.

Compatibility: **extension at the evidence layer**, not a new AE causal primitive.

### 4. Governance does not determine whether an observed transition existed

AE explicitly separates first-order realized/observed transition from higher-order governance admissibility.

ERL must preserve the same separation. A transition can be canonically reconstructed as having occurred while a separate governance adapter may classify it as allowed, denied, reviewed, noncompliant, or otherwise inadmissible under a governor.

Compatibility: **direct**.

### 5. Classification is not enforcement

AE requires a causal intervention operator before a governance classification changes reachable transitions.

ERL rhetoric, claims, policy classifications, forecast labels, or governance assessments are evidence objects or Layer-H interpretations unless evidence establishes an implemented state-changing action.

Compatibility: **direct**.

### 6. No implicit lineage taint

AE rejects automatic contamination of later transitions merely because an earlier transition was restricted or inadmissible.

ERL provenance relations therefore must not imply that a dependency, contradiction, or problematic source automatically invalidates every descendant record. Any lineage effect requires an explicit rule and evidence.

Compatibility: **direct**.

### 7. Reconstructive Singularity boundary

AE's Reconstructive Singularity work preserves `RELATIONALLY_UNESTABLISHED` rather than treating absence of an established relation as nonexistence, and explicitly retains uncertainty, unknown unknowns, residuals, and identity-continuity requirements.

ERL's opaque slots and candidate edges fit this boundary when used fail-closed:

- unresolved relation != canonical transition;
- opaque element != invented mechanism;
- missing relation != proof of absence;
- greater reconstruction resolution != retroactive certainty.

Compatibility: **direct at the epistemic boundary**.

## Required semantic boundaries

### Boundary A — ERL `canonical` is evidentiary, not metaphysical

ERL `canonical_status = canonical` means the repository admits the transition into its observed graph under its evidence rules. It does not mean the record is metaphysically complete, mathematically unique, legally valid, or governance-admissible.

### Boundary B — timestamps are evidence metadata

ERL records timestamps because historical reconstruction needs them. AE states that elapsed time is not a transition primitive.

Therefore ERL timestamps must remain boundary/evidence metadata unless a domain-specific governor explicitly consumes time as state.

### Boundary C — opaque expected role is constrained description, not causal assertion

`expected_role` must describe the structural role supported by current evidence. It must not smuggle in a causal mechanism merely because a mechanism would explain the observed states.

### Boundary D — ERL composition is reconstruction composition

`COMPOSE(T1,T2)` indicates that evidenced boundaries permit a composed historical view. It does not automatically create an AE theorem of causal equivalence, governance equivalence, or decomposition-invariant admissibility.

### Boundary E — forecast states are Layer-H/domain-adapter states

`DELAYED_BY_STATED_CONTINGENCY`, `RESOLVED_CORRECT`, and related labels describe the lifecycle of a forecast model. They are not AE causal-transition classes and must not be inserted into AE's causal relation as if they were physical state primitives.

## Identified gap requiring future mapping

ERL currently has one term that should remain provisional until mapped more rigorously: `expected_role` on opaque elements.

A future adapter should distinguish at least:

- `observed_structural_role` — directly constrained by transition evidence;
- `candidate_role_class` — induced from recurrence across multiple transitions;
- `hypothesized_mechanism` — Layer H only.

This prevents ontology review from quietly converting repeated absence into a claimed mechanism.

## Compatibility decision

```text
AE mathematical replacement authorized: false
AE mutation authorized by this review: false
ERL evidence-layer compatibility: yes, bounded
ERL opaque-slot concept compatible: yes, as reconstruction metadata
formal equivalence proven: false
cross-repository semantic merge authorized: false
future explicit adapter required: true
```

## Next compatibility work

1. Add an explicit `observed_structural_role` / `candidate_role_class` separation if fixtures expose ambiguity.
2. Define a mapping from ERL transition records to AE `tau_rho=(x,C_rho,y)` without claiming all ERL metadata is part of `tau_rho`.
3. Define refinement mapping from ERL resolution/decomposition history to AE refinement witnesses.
4. Test no-taint behavior in provenance chains.
5. Test that governance classification never changes historical transition existence without an evidenced intervention transition.
6. Revisit only after AE-AUTO-0011 reaches a terminal validated source state; the current AE handoff explicitly says full derivation remains active machine work.
