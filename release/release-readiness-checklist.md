# Release Readiness Checklist

## Purpose

This checklist defines what must be true before the Executive Rhetoric Ledger is treated as ready for broader use across StegVerse-Labs producer repositories.

The repo is usable before every box is checked, but broader adoption should wait until the release boundary is clear.

## Core Rule

```text
Release readiness means the ledger can receive, classify, validate, and explain records without collapsing claim existence into claim truth.
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

## Machine-Readable Readiness

- [x] Political Influence Tree JSON Schema exists.
- [x] Source Posture JSON Schema exists.
- [x] Producer Export JSON Schema exists.
- [x] Machine-readable Political Influence Tree sample exists.
- [x] Producer export example exists.
- [x] Validation workflow exists.
- [x] Workflow validates Political Influence Tree sample.
- [x] Workflow validates embedded source receipts.
- [x] Workflow validates producer export examples.

## Governance Readiness

- [x] Claim existence is separated from claim truth.
- [x] Source posture is required before evidence use.
- [x] Control comparison is required where differential treatment or selective enforcement is asserted.
- [x] Influence lineage is separated from causation.
- [x] Executive action records are separated from factual justification.
- [x] Outcome claims are separated from measured outcomes.
- [x] Producer repositories do not assign final ledger admissibility.
- [ ] Review-owner roles are defined.
- [ ] Dispute handling policy is defined.
- [ ] Deprecation policy is defined.

## Operational Readiness

- [x] Repo has a validation workflow.
- [x] Repo has at least one producer export example.
- [x] Repo has ingestion guidance for upstream repositories.
- [ ] Validation badge or status note is added to README after first confirmed green run.
- [ ] Producer export schema is adopted by at least one upstream repo.
- [ ] First upstream ingestion PR is tested.
- [ ] First modern-topic control comparison expansion is completed.

## Release Boundary

The repository may be considered **alpha-operational** when:

```text
standards exist
schemas exist
examples exist
validation exists
one structural tree exists
one modern-topic tree exists
producer export path exists
claim truth remains separated from claim existence
```

The repository may be considered **beta-ready** when:

```text
at least one upstream producer repo exports a valid object
a validation run is confirmed green
a reviewer policy exists
a dispute/deprecation policy exists
at least one modern-topic control comparison is completed
```

The repository may be considered **public-reference ready** when:

```text
multiple modern-topic trees exist
control comparisons are documented
source receipts are consistent
workflow status is visible
release notes explain scope and non-claims
review ownership is declared
```

## Current Status

```yaml
status: "alpha-operational"
confidence: "medium"
reason: "The repo can now structure, validate, and explain entries, but still needs reviewer policy, dispute/deprecation policy, green-run badge/status, and upstream producer testing."
```

## Immediate Next Actions

1. Add validation status note after confirming the workflow run.
2. Add reviewer and dispute policy.
3. Add deprecation policy.
4. Expand the EO 14179 tree with a control comparison branch.
5. Test export adoption from a producer repository.

## Summary

Executive_Rhetoric_Ledger is now structurally usable as an alpha-operational ledger.

It should not yet be treated as beta-ready until review ownership, dispute handling, deprecation policy, and at least one upstream producer export test are completed.
