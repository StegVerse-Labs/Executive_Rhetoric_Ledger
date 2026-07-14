# Incident Evidence Streams

## Purpose

An incident evidence stream preserves the complete reconstructable path for:

```text
who
what
why
when
where
```

The stream does not merely preserve a conclusion. It preserves the evidence, authority, decision, override, action, consequence, correction, custody, and replication events needed to reconstruct how the incident occurred and who was responsible for each transition.

## Core rule

```text
No incident may be marked reconstructable unless who, what, why, when, and where are each complete.
No missing information may disappear into a generic "insufficient data" conclusion.
Every missing element must itself produce a gap receipt identifying the missing item, its last known custodian, and its last known status.
```

This does not guarantee that every participant will create or surrender every record. It makes absence observable and attributable instead of allowing it to be silently collapsed into uncertainty.

## Evidence-stream structure

```text
source event
-> canonical payload hash
-> parent hash links
-> ordered evidence event
-> incident Merkle root
-> replica acknowledgments
-> network anchors
-> reconstruction status
```

Each stream records:

- **Who:** actors, authority sources, custodians, approvers, override authorities, and responsibility holders.
- **What:** requested decision, actual decision, resulting action, and known or disputed consequences.
- **Why:** stated reason, evidence used, authority applied, conflicts observed, and unknown reason components.
- **When:** incident time, decision time, recording time, correction time, and custody time.
- **Where:** physical location, jurisdiction, operational system, and evidence-custody destination.

## Merkle construction

1. Every evidence event receives a canonical SHA-256 payload hash.
2. Events are ordered by ascending sequence.
3. Parent hashes preserve causal and evidentiary lineage.
4. Ordered event hashes become Merkle leaves.
5. Odd leaf counts duplicate the final leaf at that tree level.
6. The resulting root identifies the complete recorded incident state.
7. Corrections and supersessions append events and produce a new root; they do not replace prior roots.
8. Each root may reference the previous stream root, creating incident-state succession.

## Network replication

A local root is not sufficient for durable continuity. Each stream declares a minimum number of replicas and records acknowledgments from independent custody endpoints.

A replication acknowledgment must include:

- replica identity;
- acknowledged Merkle root;
- acknowledgment time;
- custody status.

A stream fails validation when it lacks the required number of stored or verified acknowledgments or when replicas acknowledge different roots.

Candidate network roles include:

- originating agency or producer;
- independent oversight repository;
- master-record endpoint;
- public or restricted evidence archive;
- court, inspector-general, legislative, or authorized external custodian.

The schema does not presume that every replica is public. It requires that custody and root agreement be reconstructable.

## Missing-data behavior

The system must never represent missing evidence as though nothing is known about the absence.

An incomplete dimension requires a `missing_data_receipt` containing:

- the affected dimension;
- the specific missing item;
- the responsible or last-known custodian;
- the last known status.

A `gap` event prevents the stream from being marked complete until it is corrected or superseded by evidence that resolves the gap.

## Relationship to decision-attribution receipts

Decision-attribution receipts identify the directive, evidence, decision, override, consequence, why, and who for one decision transition.

Incident evidence streams network those receipts with all other relevant events and custody records:

```text
decision-attribution receipt
+ observations
+ source evidence
+ authority records
+ action records
+ consequence records
+ corrections
+ custody and replication receipts
= reconstructable incident evidence stream
```

## Validation

Run:

```bash
python scripts/validate_incident_evidence_streams.py
```

The validator checks:

- JSON Schema conformance;
- contiguous event sequencing;
- resolvable parent hashes;
- Merkle-root consistency when computed;
- replica count and root agreement;
- consistency between dimension statuses and reconstruction completion;
- mandatory gap receipts for incomplete incidents;
- prohibition on marking a stream complete while unresolved gap events remain.

## Evidence boundary

```text
A complete stream proves what the recorded evidence stream contains and how it is linked.
It does not automatically prove that every source assertion is true.
It makes source posture, contradiction, absence, custody, alteration, and responsibility inspectable.
```
