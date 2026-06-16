# Activation Completion Runbook

## Purpose

This runbook defines the final steps required to move `Executive_Rhetoric_Ledger` from `activation-ready-pending-validation` to `activated`.

## Current State

```yaml
repo_status: "activation-ready-pending-validation"
activation_issue: 1
current_pending_receipt: "validation_results/workflow-run-check-e8df043a.pending.json"
activation_state: "blocked-until-validation"
```

## Step 1: Run Validation

Preferred validation path:

```bash
python scripts/run_activation_validation.py
```

This runner calls:

```text
scripts/validate_producer_exports.py
scripts/validate_validation_results.py
```

## Step 2: Record Concrete Result

After a green workflow run or equivalent reviewed validation result exists, add a new validation-result receipt that supersedes the latest pending receipt.

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
- update README status from `activation-ready-pending-validation` to `activated`;
- close Issue #1 as completed.

## Non-Activation Conditions

Do not mark activated when only the following are true:

- schemas exist;
- examples exist;
- workflows exist;
- pending receipts exist;
- producer exports exist but have not been validated and promoted.

Activation requires concrete validation and reviewed receipt promotion.
