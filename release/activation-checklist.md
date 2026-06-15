# Repo Activation Checklist

## Purpose

This checklist defines what remains before Executive_Rhetoric_Ledger can move from beta activation to activated repo status.

## Current Status

```yaml
repo_status: "beta-activation-started"
activation_status: "in-progress"
producer_paths_started: 2
intake_review_exists: true
validation_script_exists: true
workflow_uses_validation_script: true
confirmed_green_workflow: false
final_reviewed_ingestion: false
```

## Completed

- [x] Standards exist.
- [x] Machine-readable schemas exist.
- [x] Sample Political Influence Tree exists.
- [x] Producer export schema exists.
- [x] Producer export example exists.
- [x] Validation workflow exists.
- [x] Producer export validation script exists.
- [x] Producer export validation quickstart exists.
- [x] Trumpality producer export path exists.
- [x] Administrations producer export path exists.
- [x] EO 14179 intake review note exists.
- [x] Intake review preserves final admissibility boundary.

## Remaining Activation Gates

- [ ] Confirm green workflow status.
- [ ] Record green workflow status in release notes.
- [ ] Promote validated producer exports from intake-reviewed candidates to reviewed ledger receipts.
- [ ] Add real control evidence receipts for EO 14179.
- [ ] Add activation summary with final repo activation state.

## Activation Rule

```text
The repo activates when producer exports validate, intake review is complete, and at least one producer export is promoted to a reviewed ledger receipt without collapsing action-record evidence into factual justification.
```

## Summary

Executive_Rhetoric_Ledger is structurally complete and activation is underway.

The next hard gate is confirmed validation or green workflow status.
