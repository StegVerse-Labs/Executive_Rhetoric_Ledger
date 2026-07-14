# Activation Completion Runbook

## Purpose

This runbook defines the final steps required to move `Executive_Rhetoric_Ledger` from `activation-ready-pending-validation` to `activated`.

## Current State

```yaml
repo_status: "activation-ready-pending-validation"
activation_issue: 2
current_pending_receipt: "validation_results/workflow-run-check-e8df043a.pending.json"
activation_validation_request: "release/activation-validation-request.json"
activation_state_manifest: "release/activation-state.json"
activation_state: "blocked-until-validation"
```

Issue #1 is historical and closed. Issue #2 is the active reconciliation and activation gate.

## Step 1: Run Validation

Preferred local validation path:

```bash
python scripts/run_activation_validation.py
```

This runner calls:

```text
scripts/validate_producer_exports.py
scripts/validate_validation_results.py
scripts/validate_activation_state.py
```

The GitHub workflow also runs these checks, including an explicit activation-state manifest validation step:

```text
.github/workflows/validate-ledger-schemas.yml
```

Validation must cover the default branch at or after the minimum commit recorded in:

```text
release/activation-validation-request.json
```

## Step 2: Record Concrete Result

After a green workflow run or equivalent reviewed validation result exists, add a new validation-result receipt that supersedes the latest pending receipt.

The evidence must identify:

```text
validated commit SHA
validation method
validation timestamp
individual check results
workflow or reviewer identity
workflow URL or repository evidence path
```

Allowed result postures:

```text
passed
failed
blocked
superseded
```

Do not convert `pending` directly into `passed` without a concrete validation result.

## Step 3: Promote Reviewed Receipt

Promote at least one validated producer export from intake-reviewed candidate into a reviewed ledger receipt.

The first reviewed receipt should preserve this distinction:

```text
action-record evidence != factual policy justification
```

## Step 4: Close Activation Gate

After the validation result and reviewed receipt promotion exist:

- update the final activation handoff;
- update `release/activation-state.json`;
- update README status from `activation-ready-pending-validation` to `activated`;
- update the mirror handoff with the validation and promotion evidence;
- close Issue #2 as completed.

## Non-Activation Conditions

Do not mark activated when only the following are true:

- schemas exist;
- examples exist;
- workflows exist;
- a validation request exists;
- pending receipts exist;
- producer exports exist but have not been validated and promoted.

Activation requires concrete validation and reviewed receipt promotion.
