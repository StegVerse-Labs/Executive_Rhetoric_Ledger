# ERL Research Candidate Transport Contract v1

Status: active implementation contract
Canonical task: Issue #60
Evaluation authority: StegVerse-Labs/Executive_Rhetoric_Ledger
Credential authority: TV/TVC where applicable
GitHub token authority: NONE

## Purpose

Define the transport boundary for moving source candidates from registered ERL-domain acquisition repositories into ERL without changing evidentiary standing or evaluation state.

## Source repositories

Registered acquisition surfaces may emit candidate packets only after local discovery. A source repository may preserve native context, source bytes, hashes, query history, and acquisition receipts. It may not convert discovery into a factual, causal, culpability, coordination, motive, or legal conclusion.

## Destination

All packets governed by this contract target `StegVerse-Labs/Executive_Rhetoric_Ledger` for intake validation and later review.

## Required packet invariants

- schema: `stegverse.erl.research_source_candidate.v1`
- at least one trajectory ID
- acquisition request ID
- source repository and source URL
- retrieval time and source class
- verification state
- evidence role limited to `lead-only` or `context-only`
- `native_records_mutated=false`
- `evaluation_changed=false`
- `transport.authority_effect=NONE`
- `transport.credential_authority=TV/TVC`
- `transport.github_token_authority=NONE`
- destination repository is ERL
- source repository in transport equals packet repository

## Fail-closed conditions

Reject the packet when any required field is absent, trajectory linkage is empty, source provenance is malformed, candidate posture exceeds lead/context, native mutation/evaluation change is claimed, the source repository does not match, destination is not ERL, authority effect is not NONE, TV/TVC is displaced as credential authority, or any GitHub token is represented as authority.

Rejected packets do not update ERL graphs, propositions, trajectories, current-state indices, or reviewed projections.

## Deduplication and collision handling

Candidate IDs must be unique within a batch. Cross-repository duplicate source identity/hash must be reconciled later by the ERL graph/frontier update gate; transport itself preserves each acquisition receipt rather than silently deleting provenance.

## Validation

Canonical validator: `scripts/validate_research_candidate_intake.py`
Canonical schema: `schemas/research-source-candidate-intake.schema.json`
Local validation receipt: `research/receipts/2026-08-11-research-candidate-intake-local-validation.json`

## Authority effect

Successful transport means only `VALID_CANDIDATE_PACKET`. It does not mean verified fact, corroborated evidence, admissible evidence, reviewed conclusion, publication approval, or release readiness.
