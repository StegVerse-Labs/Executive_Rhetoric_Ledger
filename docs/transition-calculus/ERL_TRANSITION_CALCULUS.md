# ERL Transition Calculus

Status: initial formal layer
Owner: Issue #74
Depends on: `ERL_TRANSITION_FIRST_FOUNDATIONS.md`

## 1. Primitive types

ERL defines four primitive record types:

- `State(S)` — a minimally distinguishable condition at a bounded observation point.
- `Transition(T)` — an evidenced continuity from one state boundary to another.
- `Element(e)` — an observed constituent of a transition construction.
- `Opaque(Ω)` — a structurally constrained but unresolved transition element.

Evidence records and hypotheses are attachments, not primitives of the transition itself.

## 2. Identity and declaration operators

### `DECLARE_STATE(S, evidence)`
Creates a bounded state record from evidence.

### `DECLARE_TRANSITION(S_i, S_j, continuity_evidence)`
Creates a transition only when continuity evidence satisfies the active admissibility rule.

### `DECLARE_ELEMENT(T, e, evidence)`
Attaches an observed element to an established transition.

### `DECLARE_OPAQUE(T, slot, constraints, evidence)`
Attaches an unresolved but structurally evidenced slot to an established transition.

No declaration operator accepts a hypothesis as substitute evidence.

## 3. Observational operators

### `ATTACH_EVIDENCE(target, receipt)`
Adds a provenance-bearing evidence receipt to a state, transition, element, or opaque slot.

### `RETRACT_EVIDENCE(target, receipt, reason)`
Marks evidence as retracted, invalidated, corrupted, or superseded while preserving its historical existence.

### `CONTRADICT(target, evidence_a, evidence_b)`
Records unresolved contradiction without forcing reconciliation.

### `BOUND(target, constraint)`
Adds an evidence-supported limit: temporal, spatial, actor, value, authority, mechanism, or provenance constraint.

## 4. Resolution operators

### `RESOLVE(Ω, e, evidence)`
Promotes an opaque slot to a resolved element when evidence supports the identification.

Invariant: the prior opaque state remains reconstructable.

### `REFINE(e, {e_1 ... e_n}, evidence)`
Increases granularity by decomposing an observed element into more precise observed sub-elements.

### `COARSEN({e_1 ... e_n}, e_summary)`
Creates a derived summary view without deleting the higher-resolution elements.

### `SUSPEND_RESOLUTION(target, reason)`
Explicitly records that present evidence cannot support further characterization.

Resolution operators are monotonic with respect to preserved evidence history, not necessarily with respect to confidence.

## 5. Structural operators

### `COMPOSE(T_1, T_2) -> T_c`
Permitted when the post-state boundary of `T_1` is evidenced as continuous with the pre-state boundary of `T_2`.

Composition does not erase the component transitions.

### `DECOMPOSE(T, partition_evidence) -> {T_1 ... T_n}`
Splits a transition into finer transitions when new evidence supports intermediate state boundaries.

### `BRANCH(T_origin, {T_a, T_b ...})`
Represents multiple evidenced successor transitions from a common state or transition boundary.

### `CONVERGE({T_a, T_b ...}, T_join)`
Represents separately evidenced transition paths that join at a common later state boundary.

### `LINK(T_a, T_b, relation_evidence)`
Records a non-compositional evidenced relation such as shared actor, authority, resource, document, mechanism, or provenance.

A link is not automatically a causal edge.

## 6. Continuity operations

Continuity is a property established by evidence, not by chronological adjacency.

ERL recognizes at least these continuity postures:

- `ESTABLISHED`
- `PARTIAL`
- `DISPUTED`
- `UNRESOLVED`
- `REJECTED`

Only `ESTABLISHED` continuity may create a canonical transition edge.

`PARTIAL`, `DISPUTED`, and `UNRESOLVED` relations remain candidate-edge records outside the canonical observed transition graph.

## 7. Provenance and convergence operations

### `DEPENDENCY(source_a, source_b, evidence)`
Records evidence that one source or output derives from another.

### `INDEPENDENCE(source_a, source_b, evidence)`
Records evidence supporting separate generation paths.

### `UNKNOWN_PROVENANCE(source_a, source_b)`
Records that neither dependence nor independence is sufficiently established.

### `CONVERGENCE({sources}, proposition, posture)`
Records agreement on a proposition while preserving dependency posture.

Convergence weight is constrained by provenance posture:

- known dependency: no independent-confirmation increment;
- unknown provenance: bounded increment only;
- evidenced independence: independent-confirmation increment permitted;
- common upstream source: treat as one evidentiary lineage unless additional independent evidence exists.

## 8. Hypothesis operators

Hypotheses attach only after continuity is established.

### `PROPOSE_HYPOTHESIS(scope, H)`
Creates an explanatory proposition over established observed records.

### `PREDICT_SIGNATURE(H, signature)`
Defines observable consequences expected if the hypothesis is materially correct.

### `ATTACH_DISCONFIRMATION(H, evidence)`
Attaches evidence against the hypothesis.

### `UPDATE_HYPOTHESIS(H, posture, reason)`
Updates hypothesis confidence without altering observed transitions.

### `REJECT_HYPOTHESIS(H, evidence)`
Rejects the explanation while preserving its historical evaluation record.

## 9. Forecast-state operators

For forecasts and analyst evaluations, ERL distinguishes forecast state from world state.

A forecast can transition through:

- `ACTIVE`
- `DELAYED_BY_STATED_CONTINGENCY`
- `ACCELERATED_BY_STATED_CONTINGENCY`
- `REVISED_WITHIN_MODEL`
- `INVALIDATED`
- `SUPERSEDED`
- `RESOLVED_CORRECT`
- `RESOLVED_INCORRECT`
- `UNRESOLVED`

This prevents a conditional forecast from being scored as a simple date hit/miss when the analyst explicitly named conditions that would alter timing.

## 10. Transition invariants

### I1 — Evidence recoverability
Every canonical fact must retain its evidence lineage.

### I2 — Historical opacity preservation
Resolving an opaque slot must not erase the fact that it was previously unresolved.

### I3 — Hypothesis non-contamination
No hypothesis may mutate Layer O observed records.

### I4 — Composition continuity
Transitions may compose only across evidenced compatible boundaries.

### I5 — Decomposition conservation
Decomposing a transition may add intermediate structure but must preserve the externally evidenced pre/post boundaries unless those boundaries themselves are superseded with receipts.

### I6 — Provenance non-duplication
Evidence sharing a known upstream lineage cannot be counted as multiple independent confirmations.

### I7 — Uncertain-independence boundedness
Unknown provenance may increase attention or provisional confidence but cannot receive the full weight of established independent convergence.

### I8 — Ontology restraint
No new element class is canonical merely because an unexplained gap exists in one case.

### I9 — Recurrent-opacity trigger
Repeated structurally similar opaque slots across independent transitions create a candidate ontology-review event.

### I10 — Explanation reversibility
Removing every Layer H hypothesis must leave a coherent Layer O + Layer R reconstruction.

## 11. Reconstruction

Let the canonical observed transition graph be `G_O`.

Reconstruction is the operation:

`R(G_O, evidence_stream) -> G_R`

where `G_R` preserves `G_O` while increasing resolution through admissible resolution, provenance, decomposition, and relation operations.

Hypothesis analysis is then:

`H(G_R, model_set) -> hypothesis_postures`

The ordering is intentional:

`observe -> establish continuity -> construct transition -> resolve -> reconstruct -> hypothesize -> test`

not:

`hypothesize -> search for a transition that fits`.

## 12. Opaque-slot discovery rule

For a set of transitions `{T_1 ... T_n}`, suppose opaque elements `{Ω_1 ... Ω_k}` repeatedly occupy materially similar structural roles under independently observed conditions.

ERL may emit an `ONTOLOGY_REVIEW_CANDIDATE` when:

1. the transitions are canonical;
2. the opaque roles are structurally comparable;
3. the recurrence cannot be explained solely by missing copies of the same source;
4. adding a candidate element class would improve descriptive resolution without importing a causal explanation;
5. the candidate class remains provisional until tested against additional transitions.

The table therefore becomes not only a record of known transition construction, but a disciplined detector of where the current element ontology may be incomplete.

## 13. Governance symmetry

The same transition substrate can support both forward governance and backward reconstruction.

Forward view:

`current state -> proposed action -> admissibility/governance -> next state`

Backward ERL view:

`observed later state -> evidenced transition construction -> prior state reconstruction`

The actors may be human, AI, mixed, institutional, device-level, network-level, or vault-level. The governance substrate need not be AI-specific.

This symmetry is structural only. ERL does not infer metaphysical identity or causal equivalence from shared representation.

## 14. Immediate implementation targets

The next implementation layer should add:

1. a machine-readable transition schema;
2. an opaque-element schema fragment;
3. validators for continuity and hypothesis separation;
4. provenance/dependency posture fields;
5. a minimal test fixture showing one transition refined from opaque to resolved without history loss;
6. a forecast-calibration adapter using conditional state transitions;
7. cross-repository compatibility review with `Admissible-Existence/AE` transition-table and transition-algebra work.
