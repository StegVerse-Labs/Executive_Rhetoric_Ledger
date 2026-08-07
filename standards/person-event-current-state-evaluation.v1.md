# Person/Event Current-State Evaluation Standard v1

## Purpose

This standard governs repositories and Site projections whose primary purpose is to preserve, evaluate, or publicly explain evidence about a person, institution, event, incident, decision, or related subject cluster.

ERL is the canonical evaluation authority. Subject-specific repositories may consume reviewed ERL projections and preserve their own append-only local histories, but must not create competing truth, culpability, causation, coordination, or motive authority.

## Required evaluation structure

Every governed person/event current-state evaluation MUST expose, directly or by stable reference:

1. `subject_id` and `evaluation_id`.
2. `as_of` timestamp and source/custody coverage boundary.
3. current classification (`OBSERVED`, `INFERRED`, `UNRESOLVED`, or a governed compound state).
4. DPOI inventory.
5. proposition-relative evidence movements: `strengthen`, `weaken`, `disambiguate`, `contextualize`, or `no-update`.
6. evidence for, evidence against, and alternative explanations for each material DPOI.
7. chronology and authority assignment, keeping knowledge, authority, approval, recommendation, execution, and later consequence distinct.
8. explicit inference ceiling for each material proposition.
9. evidence-gap register naming the missing object, affected DPOI, why it matters, owner, and machine-observable release condition.
10. append-only Evidence Movement Ledger.
11. current-state index derived from the ledger rather than silently replacing historical state.
12. source/custody references sufficient to reconstruct why each change occurred.
13. review state and publication authority state.

## Directional evidence rule

Directional evidence is proposition-relative, never a label on the source itself. The same record may strengthen one proposition while weakening another. Discovery output is candidate-only until governed review.

A zero-result search has `no-update` effect unless independent coverage-completeness evidence establishes that the absence is itself probative.

## Evidence Movement Ledger

Every newly acquired or newly reviewed evidence object that is relevant to a governed DPOI MUST create an append-only ledger event before or with any derived current-state update.

Minimum event semantics:

- `event_id`
- `observed_at`
- `subject_id`
- `evidence_ref`
- `custody_ref`
- `dpoi_ids`
- `direction` (`strengthen|weaken|disambiguate|contextualize|no-update`)
- `previous_state_ref`
- `resulting_state_ref`
- `reason`
- `review_state`
- `authority_effect` (must remain false unless separately governed)
- `publication_effect` (must remain false unless separately governed)

Prior events remain immutable. Corrections and reversals are new events referencing the superseded interpretation.

## Subject-repository consumer rule

A repository whose primary purpose is a person/event/incident/institution/decision subject MUST do one of the following:

- declare conformance to this standard and consume reviewed ERL evaluation/projection records; or
- register an explicit, reviewed exemption identifying why ERL's epistemic model is unsuitable and which equivalent controls replace it.

Subject repositories MUST preserve append-only imported evidence/update history, a current-state evaluation index, ERL source projection and custody references, inference ceilings and unresolved states, and non-mutation of native records unless separately governed.

Receipt/import activity alone does not establish factual truth.

## Public Site cluster projection

For a public subject cluster, Site SHOULD expose a human-readable projection with at least:

1. Overview / Current State
2. Evidence
3. DPOIs
4. Chronology & Authority
5. Analysis
6. Evidence Gaps
7. Method

The cluster home page MUST contain, near the lower portion of the principal explanatory content, a visible **Evidence Update Ledger**. It MUST show at least date/time, evidence/source, affected DPOI(s), directional effect, previous/current state summary, review state, and a link/reference to the detailed evidence/custody record.

The public ledger MUST visibly support `NO UPDATE` so users can see that acquisition of a new record did not necessarily change the assessment.

Human-readable Site content is a projection of governed records; it is not a separate evidence authority.

## Fauci cluster baseline

The Fauci/HSGAC cluster is the first named Site application of this standard. Until ERL promotion gates are satisfied, its home page must visibly state the repository's current classification (`research_candidate`, `not_assessable`, or successor governed state) and must not present a motive or culpability finding as established.

## Required ecosystem behavior

- ERL owns evaluation semantics and reviewed directional state changes.
- Person/event repositories own subject-specific receipt/history presentation and may add local non-conflicting context.
- Site owns public rendering, accessibility, navigation, and readable explanation.
- Publisher/wiki/master-records propagation does not occur merely because discovery or a candidate directional label exists.
- Any downstream projection must preserve source authority, review state, inference ceiling, and unresolved evidence gaps.

## Completion rule

A person/event evaluation implementation is complete only when an independent reviewer can trace the public or local current state back through the append-only evidence movements to the reviewed source/custody objects and reproduce why the DPOI state strengthened, weakened, remained unresolved, or did not update.
