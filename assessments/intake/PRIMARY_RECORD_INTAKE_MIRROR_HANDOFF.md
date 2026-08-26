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

## Current state
- handoff: established
- queue normalization: pending
- machine topic binding: pending
- validator rerun: pending
- release/publication impact: none authorized

## Archive posture
Once queue normalization, machine topic binding, and validation evidence are durable, this bounded repair can be continued without conversation context.
