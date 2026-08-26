# Primary Record Intake Mirror Handoff

## Authority
Bounded continuation source for `assessments/intake/**` in `StegVerse-Labs/Executive_Rhetoric_Ledger`.

Parent authority: `ERL_MIRROR_HANDOFF.md`.

## Governing machine contract
- schema: `schemas/primary-record-intake.schema.json`
- validator: `scripts/validate_primary_record_intake.py`
- queue root fields: `queue_id`, `topic_id`, `queue_status`, `created_date`, `last_reviewed`, `items`
- each item uses the canonical intake vocabulary and may not substitute a bespoke task object for the governed schema.
- machine-readable topic binding must resolve to an assessment under `assessments/machine/**` or `assessments/pit/**`.
- verified intake states require governed source receipt IDs already present in the topic's assessment/source packets or standalone receipt registry.
- queue completion is invalid while unresolved items remain.

## Current repair lane — White House ballroom taxpayer-cost intake
Target queue:
`assessments/intake/2026-08-22-white-house-ballroom-taxpayer-cost-intake.json`

Topic:
`ERL-2026-08-22-WHITE-HOUSE-BALLROOM-TAXPAYER-COST`

Observed pre-existing defects:
1. queue used bespoke root fields not admitted by the primary-record intake schema;
2. `queue_id` and `items` were absent;
3. bespoke task entries were stored under `tasks`;
4. no machine-readable assessment under `assessments/machine/**` or `assessments/pit/**` carried the topic ID, so topic binding failed.

Repair boundary:
- normalize the queue without weakening the schema;
- preserve all ten research objects and their release intent;
- map located primary objects to `located`, not `verified-primary`, unless the queue can bind a governed receipt ID;
- map outstanding accounting/custody objects to `requested`;
- create a bounded machine-readable topic record that preserves the existing rhetoric/source-posture finding boundaries and does not promote motive, final legal conclusion, or final taxpayer allocation.

## Collision boundary
Do not mutate `assessments/silence-causation/**` or PR #48 while repairing this intake lane.

## Repair result
The White House ballroom queue was normalized to the canonical primary-record intake schema while preserving all ten evidence targets. Located official sources remain `located`; outstanding accounting records remain `requested`. No structural repair promoted custody or factual posture.

A matching machine-readable Political Influence Tree assessment was created at:
`assessments/machine/ERL-2026-08-22-WHITE-HOUSE-BALLROOM-TAXPAYER-COST.json`

The assessment was added to `assessments/README.md`, establishing the required topic/index binding without changing the evidence promotion boundary.

## Validation evidence
```text
workflow: Validate Ledger Schemas
run: 33011563705
validated head: c0638c0c10cbbf218b2ca178ee8dc74a9ea89d28
event: push
conclusion: success
```

Relevant steps:
- Capture assessment Political Influence Tree validation: PASS
- Enforce assessment Political Influence Tree validation: PASS
- Validate primary-record intake queues: PASS
- combined repository activation validation: PASS
- complete 40-stage job: PASS

This clears the pre-existing ledger-schema blocker formerly caused by this queue.

## Current state
- handoff: current
- queue normalization: complete
- machine topic binding: complete
- assessment index visibility: complete
- hosted primary-record intake validation: PASS
- hosted repository-wide ledger validation: PASS
- primary accounting research: still active
- release/publication impact: none authorized

## Archive posture
The structural blocker is repaired and validated. Remaining work is substantive primary-accounting evidence acquisition under this durable queue, not schema repair. This bounded repair no longer depends on conversation context.
