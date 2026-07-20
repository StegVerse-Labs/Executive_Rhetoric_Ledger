# Activation Validation Trigger

This file exists to create a pull-request-bound validation run for the current repository state.

## Purpose

The GitHub connector exposes pull-request workflow runs but did not expose push-triggered validation for the current default-branch commits. This branch introduces no schema, policy, assessment, receipt, or activation-state change. It exists only to cause `.github/workflows/validate-ledger-schemas.yml` to execute through the `pull_request` event.

## Boundaries

```text
This trigger is not validation evidence.
This trigger is not a validation-result receipt.
This trigger is not a reviewed ledger receipt.
This trigger is not activation evidence.
```

The workflow result and its commit SHA must be reviewed before any pending receipt is superseded or activation state is changed.
