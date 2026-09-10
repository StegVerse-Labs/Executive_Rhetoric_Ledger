# Reclamation Target Reconciliation

## Purpose

The reclamation runtime must not wait for a search engine or data broker to expose a user's information before deciding where to look. It should derive an evidence-bounded target set from two independent discovery surfaces:

1. the user's authorized SKAP account topology and provider-disclosure graph; and
2. the observed Data Propagation Graph produced by external discovery and prior reclamation activity.

The reconciler at `scripts/build_reclamation_target_set.py` combines those surfaces without collapsing evidence classes.

## Target posture

A SKAP account provider is a `PRIMARY / DIRECT / ELIGIBLE` target because the existence of an authorized account is direct evidence that the provider holds at least account-associated data for that subject.

Downstream disclosure edges are mapped according to evidence posture. Provider declarations, observed transfers, and regulator/court records may produce eligible downstream targets. Credible third-party reporting remains watch-only unless strengthened. `INFERRED_UNVERIFIED` and `UNKNOWN` relationships are blocked from eligible execution and remain watch targets.

Observed propagation nodes such as data brokers, downstream recipients, indexes/caches, and model/retrieval surfaces may become eligible downstream targets when currently observed or reappeared. Prior removal/restriction/deletion states remain watch or complete posture rather than silently returning to active execution.

## Fail-closed boundaries

The reconciler refuses cross-subject joins. A SKAP graph for one subject cannot be reconciled with a propagation graph for another subject.

Distinct evidence lanes remain distinct even when they point at the same organization. A provider disclosure and an independently observed propagation node are not silently collapsed into one proof claim.

No target-set state proves that deletion occurred. It only determines where an authorized reclamation process may next investigate, request, restrict, verify, or watch.

## Deterministic validation

`schemas/reclamation-target-set.schema.json` defines the output contract. `fixtures/digital-data-reclamation/reclamation-target-set.sample.json` is the expected deterministic result for the paired SKAP and propagation reconciliation fixtures.

The repository validator reconstructs the target set, compares it byte-semanticly to the expected fixture, rejects cross-subject reconciliation, and ensures unverified targets cannot become `ELIGIBLE`.
