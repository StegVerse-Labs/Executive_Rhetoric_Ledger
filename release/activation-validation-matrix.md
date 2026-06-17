# Activation Validation Matrix

## Purpose

This matrix maps each activation-relevant artifact to its schema, validator, workflow coverage, and activation effect.

## Matrix

| Artifact | Schema | Validator | Workflow Step | Activation Effect |
|---|---|---|---|---|
| Political Influence Tree sample | `schemas/political-influence-tree.schema.json` | inline workflow validator | `Validate sample political influence tree` | Confirms base sample shape only |
| Embedded source receipts | `schemas/source-posture.schema.json` | inline workflow validator | `Validate embedded source receipts` | Confirms source posture shape only |
| Producer export examples | `schemas/producer-export.schema.json` | `scripts/validate_producer_exports.py` | `Validate producer export examples` | Confirms producer export shape only |
| Validation-result receipts | `schemas/validation-result.schema.json` | `scripts/validate_validation_results.py` | `Validate validation result receipts` | Confirms pending/result receipt shape only |
| Activation-state manifest | `schemas/activation-state.schema.json` | `scripts/validate_activation_state.py` | `Validate activation state manifest` | Confirms machine-readable activation posture only |
| Combined activation validation | Multiple schemas | `scripts/run_activation_validation.py` | `Run combined activation validation` | Confirms local validators run as a group |

## Activation Boundary

Passing all shape validators does not automatically activate the repository.

Activation still requires:

1. a green workflow run or equivalent reviewed validation result;
2. supersession of the latest pending validation-result receipt;
3. promotion of at least one validated producer export into a reviewed ledger receipt;
4. final activation summary;
5. Issue #1 closure as completed.

## Current Posture

```yaml
repo_status: "activation-ready-pending-validation"
activation_state_manifest: "release/activation-state.json"
activation_runbook: "release/activation-runbook.md"
final_handoff: "release/final-activation-handoff.md"
```
