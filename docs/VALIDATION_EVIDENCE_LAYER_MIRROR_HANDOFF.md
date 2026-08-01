# Validation Evidence Layer Mirror Handoff

## Status

```yaml
layer_id: ERL-VALIDATION-EVIDENCE-LAYER-001
build_status: built
activation_status: activated-by-main-push
activation_commit: cc59e756deaf1afa884fd2b5af200c2bf76cb831
publication_authority: false
```

## Installed components

- `scripts/capture_validation_evidence.py`
- `.github/workflows/capture-ellis-scavino-validation-evidence.yml`

## Function

The layer runs and preserves direct execution evidence for:

- `python scripts/validate_assessment_trees.py`
- `python scripts/validate_primary_record_intake.py`
- `python scripts/run_activation_validation.py`

For each validator it records:

- exact command;
- start and completion timestamps;
- exit code;
- conclusion;
- stdout;
- stderr;
- log path;
- log SHA-256;
- log byte size.

The receipt also records repository, workflow, event, branch, commit SHA, run ID, run number, run attempt, actor, runner, and canonical run URLs from the GitHub Actions environment.

## Artifact

Each run uploads:

`ellis-scavino-validation-evidence-<run_id>-<run_attempt>`

The artifact contains:

- `validation-execution-receipt.json`;
- `artifact-manifest.json`;
- one complete log per validator.

Retention is 90 days. The workflow uploads evidence before enforcing validator success, so failure evidence remains available.

## Activation behavior

The workflow is activated on:

- pushes to `main` affecting the Ellis-Scavino assessment, validators, schemas, pending validation receipt, capture script, or workflow;
- manual `workflow_dispatch`.

The creation commit `cc59e756deaf1afa884fd2b5af200c2bf76cb831` matched the workflow path filter and is the first activation event.

## Current observation boundary

The connected commit-run query exposes pull-request-triggered runs only. It returned no run for the activation commit, and the combined-status surface returned no status contexts. Those results do not establish that the push-triggered workflow did not execute.

Native evidence remains to be acquired from the generated artifact or an Actions surface exposing push runs. Once acquired, preserve run ID, run attempt, job ID, all steps, conclusions, logs, artifact ID, expiration state, and artifact contents.

## Authority boundary

A successful layer run proves only that the three repository validators exited successfully for the identified commit. It does not prove primary-source completeness, independent corroboration, admissibility, publication readiness, or any factual chain node.

## Next integration candidate

After the first native artifact is preserved, generalize this layer from the Ellis-Scavino assessment to a reusable repository-wide validation evidence workflow and schema, then update the canonical pending validation receipt only if direct execution evidence supports it.

## Archive readiness

This handoff contains the complete build, activation, evidence format, authority boundary, unresolved observation dependency, and next integration target. The complete thread is ready for archiving without any additional part of the thread needed to move forward.
