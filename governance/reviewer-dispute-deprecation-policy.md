# Reviewer, Dispute, and Deprecation Policy

## Purpose

This policy defines how Executive_Rhetoric_Ledger entries are reviewed, challenged, corrected, deprecated, or replaced.

The policy exists because ledger entries can affect how political claims, executive actions, source posture, and institutional outcomes are interpreted across StegVerse-Labs.

## Core Rule

```text
A ledger entry is never final because it is convenient.
It remains active only while its receipts, source posture, controls, and classifications remain reviewable.
```

## Reviewer Roles

### 1. Entry Author

The entry author drafts or updates a ledger entry.

The author is responsible for:

- separating claim existence from claim truth;
- attaching receipts;
- assigning initial source posture;
- identifying missing controls;
- marking unknowns as unknown;
- avoiding unsupported influence or causation claims.

### 2. Evidence Reviewer

The evidence reviewer checks source posture.

The reviewer is responsible for:

- confirming whether sources are primary, secondary, contextual, or inadmissible;
- confirming whether receipts prove the claimed evidentiary role;
- identifying unsupported factual basis claims;
- flagging missing archives, broken links, or screenshot-only sources.

### 3. Control Reviewer

The control reviewer checks whether comparison claims are admissible.

The reviewer is responsible for:

- checking comparable jurisdictions;
- checking comparable policy instruments;
- checking comparable enforcement tools;
- checking comparable harm or fraud magnitude;
- checking comparable judicial posture;
- marking missing controls explicitly.

### 4. Ledger Maintainer

The ledger maintainer accepts, rejects, deprecates, or requests changes to entries.

The maintainer is responsible for:

- enforcing repository standards;
- ensuring disputed entries are visibly marked;
- approving deprecation or replacement;
- preserving historical receipts.

## Review States

```text
draft
under-review
accepted
accepted-with-limitations
disputed
needs-source-posture
needs-control-comparison
needs-outcome-evidence
deprecated
superseded
rejected
```

## Acceptance Criteria

An entry may be accepted when:

- the surface claim is identifiable;
- source receipts are attached;
- source posture is assigned;
- action conversion is separated from factual justification;
- influence lineage is separated from causation;
- control comparison is completed or marked missing/not required;
- outcome claims are separated from measured outcomes;
- confidence and admissibility status are assigned.

## Dispute Triggers

An entry should be marked `disputed` if any of the following occur:

- a source no longer supports its assigned evidentiary role;
- a factual basis claim is challenged by a stronger source;
- a primary source is missing, altered, or unavailable;
- control comparison is incomplete but treated as complete;
- influence lineage is overstated as causation;
- outcome evidence is contradicted by later records;
- a reviewer identifies partisan framing not grounded in source posture.

## Dispute Handling Process

1. Mark the entry status as `disputed`.
2. Identify the disputed branch.
3. Preserve the existing receipt trail.
4. Add the dispute source or objection.
5. Assign a reviewer.
6. Decide whether the entry should be corrected, limited, deprecated, superseded, or rejected.

## Deprecation Criteria

An entry should be deprecated when:

- it has been replaced by a better-supported entry;
- the source posture is materially wrong;
- the entry depends on unavailable or unverifiable sources;
- control comparison was required but cannot be supplied;
- a later institutional record materially changes the classification;
- the entry structure no longer matches the current schema or standard.

Deprecation does not mean deletion.

Deprecated entries should remain available when possible, with status and reason visible.

## Supersession Criteria

An entry should be superseded when a newer entry:

- preserves the original receipts;
- adds better source posture;
- corrects classification errors;
- completes missing controls;
- adds mature institutional response;
- adds measured outcome evidence.

## Rejection Criteria

An entry should be rejected when:

- no source receipts are supplied;
- claim text cannot be verified;
- the entry relies on unsupported assumptions;
- the entry treats opinion as factual basis;
- the entry treats influence as causation without evidence;
- the entry cannot be mapped to ledger standards.

## Required Status Note Format

```yaml
review_status: ""
reviewer: ""
review_date: ""
status_reason: ""
affected_branches: []
required_next_actions: []
```

## Anti-Misuse Rule

Reviewers must not use this policy to suppress an entry because it is politically inconvenient.

Reviewers also must not use this policy to preserve an entry because it is politically useful.

The only permitted review basis is source posture, control comparison, authority posture, institutional response, outcome evidence, and ledger standards.

## Summary

This policy gives the repo a path from alpha-operational to beta-ready by defining who reviews entries, how disputes are marked, and how entries are deprecated or superseded without erasing the evidentiary record.
