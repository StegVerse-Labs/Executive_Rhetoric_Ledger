# ERL Transition-First Foundations

Status: initial bounded specification
Owner: Issue #74
Branch: `feature/transition-first-calculus`

## Purpose

ERL treats the state transition, not the claim, as the primitive object of reconstruction.

The framework is designed to preserve observed continuity, increase resolution over time, and keep explanation separate from evidence. It must remain useful when actors are human, automated, mixed, institutional, or unknown.

## Foundational axioms

### Axiom 1 — Observation precedes explanation

A transition record may contain only what is supported by evidence at the time of recording.

No hypothesis, motive attribution, causal narrative, inferred dependency, or unstated assumption may be inserted into the canonical observed transition merely because it would make the transition easier to explain.

### Axiom 2 — Continuity is evidenced, never presumed

A relation from state `S_i` to state `S_j` becomes a canonical transition only when evidence supports continuity between those states.

If continuity is not established, ERL stores candidate relation evidence separately. It does not promote the relation to a transition.

### Axiom 3 — Transition construction precedes transition explanation

Once continuity is established, the transition has a construction whether or not every constituent element has been resolved.

Unresolved construction is represented explicitly rather than silently omitted.

### Axiom 4 — Opaque elements are typed unresolved slots, not voids

An opaque transition element means:

- the transition is established;
- the construction requires one or more unresolved elements at a known structural location or role;
- the element's identity, value, actor, mechanism, or provenance is not yet sufficiently evidenced.

Opacity records bounded non-resolution. It does not authorize speculative filling.

### Axiom 5 — Resolution refines; it does not rewrite

Increasing evidence may resolve an opaque element, split an element into finer-grained elements, add provenance, or refine timestamps and boundaries.

Resolution must preserve prior canonical observations and append or supersede them transparently. It may not retroactively convert an inference into an observation.

### Axiom 6 — Hypotheses are post-continuity overlays

Hypotheses may be generated only after the observed transition record is sufficiently stable to distinguish:

1. what is observed;
2. what remains unresolved;
3. what explanatory proposition is being tested.

Hypotheses are attached to transition records; they are never part of the canonical transition itself.

### Axiom 7 — Similarity is not dependency

Two sources, analysts, systems, or actors may independently converge on similar outputs.

ERL must distinguish:

- semantic similarity;
- chronological precedence;
- known dependency;
- suspected dependency;
- unknown provenance;
- independently supported convergence.

No source receives double-counted confirmation merely because a second source repeats or resembles it.

### Axiom 8 — Unknown provenance receives bounded weight

When independence cannot be established, ERL records provenance as unresolved and assigns only bounded evidentiary weight.

Subsequent evidence may raise or lower the independence posture without rewriting the original source event.

### Axiom 9 — Ontology expands by repeated observation, not convenience

A recurrent opaque structural slot across multiple transitions may indicate an unmodeled element class.

A new element class is eligible for admission only when repeated observations require it. The need to explain a case is not itself evidence for ontology expansion.

## Three-layer separation

ERL transition reconstruction is divided into three non-interchangeable layers.

### Layer O — Observed transition record

Contains only:

- source state boundary;
- destination state boundary;
- evidenced continuity;
- observed transition elements;
- opaque element slots;
- timestamps or bounded intervals;
- provenance;
- custody and integrity posture;
- contradiction markers;
- uncertainty directly supported by the evidence.

### Layer R — Reconstruction and resolution

May:

- increase granularity;
- resolve opaque elements;
- join corroborating evidence;
- separate conflated elements;
- add provenance relationships;
- identify dependencies or independent convergence;
- revise confidence in characterization.

It may not modify the historical fact that an earlier record was unresolved.

### Layer H — Hypothesis and explanation

Contains:

- causal hypotheses;
- motives;
- forecasts;
- counterfactuals;
- explanatory models;
- competing interpretations;
- predicted signatures;
- disconfirming conditions.

Layer H can be promoted, rejected, suspended, or superseded without changing Layer O.

## Canonical transition object

Let a transition be represented as:

`T = <S_pre, S_post, C, E, P, U, Q>`

Where:

- `S_pre` = pre-transition state boundary;
- `S_post` = post-transition state boundary;
- `C` = evidenced continuity relation;
- `E` = set or ordered structure of transition elements;
- `P` = provenance and custody graph;
- `U` = unresolved or opaque element set;
- `Q` = quality / evidence posture metadata.

A transition is admissible into the canonical observed graph only if `C` is evidence-supported.

## Opaque transition element

An opaque element is represented conceptually as:

`Ω = <slot, expected_role, observed_constraints, provenance_posture, resolution_state>`

An opaque element says, in effect:

> something structurally participates here, and the transition evidence constrains what it can be, but the present record does not authorize identification.

This distinction is important: unknown identity is not absence of construction.

## Reconstruction invariant

For any transition `T` and later higher-resolution form `T'`:

- `T'` may contain more resolved structure than `T`;
- every still-valid observed fact in `T` must remain recoverable from `T'`;
- provenance for corrections and supersessions must remain reconstructable;
- explanatory hypotheses attached to either form must remain separable from observed facts.

## First methodological consequence

ERL should stop asking first:

> What claim is being made?

and instead ask:

> What state changed, what evidence establishes continuity, what transition construction is observed, and which parts remain unresolved?

Claims, rhetoric, forecasts, refusals, policy announcements, economic signals, and governance actions then become domain-specific evidence sources attached to a shared transition substrate.
