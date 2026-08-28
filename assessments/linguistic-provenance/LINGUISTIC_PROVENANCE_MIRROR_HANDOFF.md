# Linguistic Enregisterment / AI Provenance Mirror Handoff

## Authority
Bounded source of truth for Issue #81 in `StegVerse-Labs/Executive_Rhetoric_Ledger`.

## Goal
Prevent stylistic or socially recognized "AI voice" signals from being promoted into AI-authorship provenance claims without independent provenance evidence.

## Core invariant
`observed_feature != socially_enregistered_signal != provenance_evidence != authorship_finding`.

## Status
- lifecycle: ACTIVE
- implementation: IN_PROGRESS
- validation: PENDING
- merge: PENDING
- release/publication: NOT_AUTHORIZED

## Canonical owner
- Issue: #81
- Branch: `feature/linguistic-enregisterment-provenance`
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
- LP-007: merge only after green validation
- LP-008: evaluate propagation to Site, Publisher, admissibility-wiki, stegguardian-wiki only after merge/review

## Release gate
No release or propagation until validator-clean fixtures prove:
- stylistic association can be recorded without provenance promotion;
- an unsupported authorship claim is rejected;
- an independently supported provenance claim can pass.

## Archive readiness
This scoped handoff is the durable continuation source for this lane.