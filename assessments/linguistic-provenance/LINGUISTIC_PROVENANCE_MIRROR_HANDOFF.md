# Linguistic Enregisterment / AI Provenance Mirror Handoff

## Authority
Bounded source of truth for Issue #81 in `StegVerse-Labs/Executive_Rhetoric_Ledger`.

## Goal
Prevent stylistic or socially recognized "AI voice" signals from being promoted into AI-authorship provenance claims without independent provenance evidence.

## Core invariant
`observed_feature != socially_enregistered_signal != provenance_evidence != authorship_finding`.

## Status
- lifecycle: COMPLETE
- implementation: SOURCE_COMPLETE
- validation: HOSTED_PASS
- merge: MERGED
- release/publication: NOT_AUTHORIZED / NO_DOWNSTREAM_PROPAGATION_REQUIRED

## Canonical owner
- Issue: #81
- Merged source branch: `feature/linguistic-enregisterment-provenance`
- Merge commit: `324341c80527204537f4f384a9d6e74f20730887`
- Scope: `assessments/linguistic-provenance/**`, `schemas/linguistic-provenance-assessment.schema.json`, `scripts/validate_linguistic_provenance_assessments.py`

## Required machine behavior
1. Record directly observed linguistic features separately from interpretation.
2. Record enregisterment/social-association claims with population/context/time-window metadata.
3. Record provenance evidence independently.
4. Fail closed if an AI-authorship finding is asserted without qualifying provenance evidence.
5. Allow "sounds like AI" / perceived-register findings without implying source attribution.
6. Preserve temporal drift: a feature can become or cease to be socially associated with AI over time.

## Initial evidence trigger
LinkedIn discussion supplied by the user on 2026-08-27 describing enregisterment and examples such as em dashes, tidy three-part lists, and "not X but Y". This trigger is treated as a research-candidate source, not as proof of prevalence or authorship.

## Tasks
- LP-001: install schema
- LP-002: install validator
- LP-003: install deterministic positive/negative fixtures
- LP-004: add fail-closed CI workflow
- LP-005: update root ERL handoff with bounded-lane pointer and status
- LP-006: run hosted validation and preserve receipts
- LP-007: merge only after green validation — COMPLETE
- LP-008: evaluate propagation to Site, Publisher, admissibility-wiki, stegguardian-wiki only after merge/review — COMPLETE / NO PROPAGATION AUTHORIZED

## Release gate
No release or propagation until validator-clean fixtures prove:
- stylistic association can be recorded without provenance promotion;
- an unsupported authorship claim is rejected;
- an independently supported provenance claim can pass.

## Hosted validation evidence
- dedicated workflow run 33144746223: SUCCESS
- repository-wide schema run 33144746184: SUCCESS
- research-candidate activation run 33144746162: SUCCESS
- cross-lane ballroom intake classification repair: validated by repository-wide schema success
- six stale research-candidate registry omissions reconciled under Issue #63

## Archive readiness
This scoped handoff is the durable continuation source for this lane.

## Completion accounting — 2026-08-28
- LP-001 schema: complete
- LP-002 validator: complete
- LP-003 positive/negative fixtures: complete
- LP-004 hosted CI: complete and green
- LP-005 root handoff pointer: complete
- LP-006 hosted validation receipts: complete
- LP-007 merge: next executable boundary
- LP-008 downstream propagation review: blocked until merge/review

Source implementation: 6/6 core lane artifacts = 100%.
Hosted validation: 3/3 relevant runs green = 100%.
Goal activation before merge: 7/8 task groups = 87.5%.


## Downstream propagation review — 2026-08-28
Durable review: `assessments/linguistic-provenance/downstream-propagation-review.json`.

Result: `NO_DOWNSTREAM_PROPAGATION_AUTHORIZED`.

Reasons:
- Site currently rejects externally owned new workloads through its orchestration state and already has a destination-owned ERL sync limited to the reviewed compendium.
- Publisher already imports only `publication/compendium.json` through its destination-owned sync contract.
- admissibility-wiki already acknowledges only the reviewed compendium and explicitly separates publication from proof/admissibility authority.
- stegguardian-wiki has no current ERL linguistic-provenance import authority; its canonical handoff owns unrelated bounded Guardian projection work.
- the current reviewed ERL `publication/compendium.json` does not contain this linguistic-provenance lane.

No raw research-candidate or source-only governance artifact was copied downstream. That is the correct fail-closed result, not an incomplete propagation step.

## Final completion accounting
- LP-001 through LP-008: 8/8 complete
- core source artifacts: 7 durable lane artifacts including downstream review
- hosted validation: green before merge; closeout validator extended to enforce the downstream decision
- scaffolding/stubs: 0
- source goal activation: 100%
- downstream publication/release authority: false

The bounded goal is complete. Future downstream publication requires a separately reviewed ERL publication artifact and destination-owned ingestion; this closed lane does not grant that authority.
