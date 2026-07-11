# Release Readiness Checklist

## Purpose

This checklist defines what must be true before the Executive Rhetoric Ledger is treated as ready for broader use across StegVerse-Labs producer repositories and before incident assessments are promoted beyond catalogue or review status.

## Core Rule

```text
Release readiness means the ledger can receive, classify, validate, review, compare, and explain records without collapsing claim existence into claim truth or structural validity into factual legitimacy.
```

## Documentation Readiness

- [x] README explains repository purpose.
- [x] README distinguishes opinion archive from comparative research layer.
- [x] Political Influence Tree Standard exists.
- [x] Source Posture Schema exists.
- [x] Cross-repo ingestion notes exist.
- [x] Producer export workflow notes exist.
- [x] Source receipt examples exist.
- [x] Rhetoric-to-action scoring calibration exists.
- [x] At least one fundamental-document annotation exists.
- [x] At least one structural Political Influence Tree exists.
- [x] At least one modern-topic Political Influence Tree exists.
- [x] Governed assessments index exists.
- [x] Delaney Hall narrative and machine-readable assessment are indexed.

## Machine-Readable Readiness

- [x] Political Influence Tree JSON Schema exists.
- [x] Source Posture JSON Schema exists.
- [x] Producer Export JSON Schema exists.
- [x] Validation Result JSON Schema exists.
- [x] Primary Record Intake JSON Schema exists.
- [x] Machine-readable Political Influence Tree sample exists.
- [x] Producer export example exists.
- [x] Machine-readable Delaney Hall assessment exists.
- [x] Machine-readable Delaney Hall intake queue exists.
- [x] Workflow validates Political Influence Tree sample.
- [x] Workflow validates embedded source receipts.
- [x] Workflow validates producer export examples.
- [x] Workflow validates governance patterns.
- [x] Workflow validates assessment trees and required linked records.
- [x] Workflow validates primary-record intake queues.
- [x] Intake validation enforces real receipt IDs in the matching assessment.
- [x] Assessment validation enforces assessment-index visibility.

## Governance Readiness

- [x] Claim existence is separated from claim truth.
- [x] Source posture is required before evidence use.
- [x] Control comparison is required where differential treatment or selective enforcement is asserted.
- [x] Influence lineage is separated from causation.
- [x] Executive action records are separated from factual justification.
- [x] Outcome claims are separated from measured outcomes.
- [x] Producer repositories do not assign final ledger admissibility.
- [x] Review-owner roles are defined.
- [x] Dispute handling policy is defined.
- [x] Deprecation and supersession policy is defined.
- [x] Pending, passed, failed, blocked, and superseded validation receipts are schema-governed.
- [x] Missing evidence is represented through governed intake states.
- [x] Restricted or sealed evidence has an explicit privacy boundary.

## Operational Readiness

- [x] Repository has a validation workflow.
- [x] Repository uses one existing validation workflow rather than adding assessment-specific workflows.
- [x] Repository has at least one producer export example.
- [x] Repository has ingestion guidance for upstream repositories.
- [x] First upstream producer export tests have been initiated.
- [x] A modern incident assessment uses the repository's native governance and validation mechanisms.
- [x] A same-event operational control has been identified for Delaney Hall.
- [ ] Confirmed green workflow or equivalent reviewed validation result exists for the current repository scope.
- [ ] Validation badge or status note reflects a confirmed current green result.
- [ ] At least one validated producer export is promoted into a reviewed ledger receipt.
- [ ] Delaney Hall same-event control contains comparable measured outcomes.
- [ ] Delaney Hall assessment has independent evidence-review and control-review sign-off.
- [ ] Delaney Hall primary-record queue contains sufficient verified records for `accepted-with-limitations` promotion.

## Assessment Promotion Boundary

A review-stage assessment may advance to `accepted-with-limitations` only when:

```text
original or archival media provenance is attached where material
required source receipts validate
required control files exist and limitations remain visible
review ownership is assigned
verified intake items point to real receipts in the matching assessment
current structural validation is confirmed
classification remains no broader than the evidence supports
```

A passing structural validation result does not establish factual truth, lawful authority, constitutional compliance, or liability.

## Repository Release Boundary

The repository may be considered **alpha-operational** when standards, schemas, examples, validation, review policy, and non-overclaim boundaries exist.

The repository may be considered **beta-ready** when:

```text
at least one upstream producer object is validated and reviewed
a current validation result is confirmed green
review, dispute, deprecation, and supersession mechanisms are active
at least one modern-topic control comparison contains sufficient evidence for its stated scope
```

The repository may be considered **public-reference ready** when:

```text
multiple modern-topic trees and assessments exist
control comparisons are documented and reviewable
source receipts and intake transitions are consistent
workflow status is visible and current
release notes explain scope and non-claims
review ownership is declared
```

## Current Status

```yaml
status: "activation-ready-pending-validation"
structural_confidence: "high"
current_validation_result: "pending"
current_delaney_review_status: "needs-source-posture"
current_delaney_control_status: "partial"
current_delaney_intake_status: "active"
release_blockers:
  - "confirmed current green validation"
  - "reviewed producer receipt promotion"
  - "Delaney Hall primary-record population"
  - "Delaney Hall independent evidence and control review"
  - "Delaney Hall measured control comparison"
```

## Immediate Next Actions

1. Confirm the current validation workflow result and create a concrete validation receipt.
2. Promote at least one validated producer export into a reviewed ledger receipt.
3. Process the Delaney Hall critical intake items.
4. Populate the same-event federal-to-state comparison with comparable measures.
5. Assign independent evidence and control reviewers.

## Summary

The repository's core governance and validation mechanisms are developed. Broader activation remains blocked by concrete validation, reviewed producer promotion, and evidence population—not by missing scaffolding.
