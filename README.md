# Executive_Rhetoric_Ledger

This repository performs cross-administration analysis of:

- executive rhetoric (verbatim statements)
- executive action (policy instruments)
- judicial response (litigation and injunctions)
- measurable outcomes (where supported by sources)

This repo is not an opinion archive.
It is a comparative research layer.

## Inputs

Primary records originate in:
- Trumpality
- Administrations

Ledger outputs are normalized datasets and comparisons.

## Status

```yaml
repo_status: "activation-ready-pending-validation"
readiness_confidence: "high-structural-readiness"
release_boundary: "structurally complete; activation still requires green workflow or equivalent reviewed validation result plus reviewed receipt promotion"
activation_issue: 1
first_upstream_producer_test: "StegVerse-Labs/Trumpality"
first_upstream_producer_commit: "fc032e774ec05b611c114a0549895ac225e6764b"
second_upstream_producer_test: "StegVerse-Labs/Administrations"
second_upstream_producer_commit: "840fa595cc921d223be0a30132c27855b28aba2f"
validation_status: "pending"
current_pending_receipt: "validation_results/workflow-run-check-e8df043a.pending.json"
```

## Key Rule

Fraud-based justifications are included **only** when a control comparison exists:
- comparable program type
- comparable fraud magnitude
- comparable enforcement tools
- comparable judicial posture
across both blue and red jurisdictions.

## Major comparison tracks

- Conditional funding leverage
- Selective enforcement patterns
- Rhetoric-to-action alignment scoring
- Court-block rate by instrument type

## Standards

- [Political Influence Tree Standard](standards/political-influence-tree-standard.md)
- [Source Posture Schema](standards/source-posture-schema.md)

The Political Influence Tree Standard requires politically active topics to be represented as traceable influence trees with evidence posture at each branch.

Core rule:

```text
No political topic is evaluated by alignment.
Every political topic is evaluated by lineage, evidence, authority, control comparison, and outcome.
```

The Source Posture Schema prevents the ledger from treating all sources as equal evidence. A source may prove that a claim was made without proving that the claim is factually true.

## Machine-readable schemas

- [Political Influence Tree JSON Schema](schemas/political-influence-tree.schema.json)
- [Source Posture JSON Schema](schemas/source-posture.schema.json)
- [Producer Export JSON Schema](schemas/producer-export.schema.json)
- [Validation Result JSON Schema](schemas/validation-result.schema.json)

These schemas provide validation targets for converting Markdown ledger entries, upstream producer exports, and validation-result receipts into machine-checkable data objects.

## Machine-readable samples

- [Political Influence Tree Sample](samples/political-influence-tree.sample.json)

The sample mirrors the Powell Memorandum structural tree and provides a test object for schema validation.

## Validation

- [Validate Ledger Schemas workflow](github/workflows/validate-ledger-schemas.yml)
- [Validation Status Note](release/validation-status-note.md)
- [Final Activation Handoff](release/final-activation-handoff.md)

Note: the actual repository path starts with a leading dot. It is shown here without the leading dot as requested: `github/workflows/validate-ledger-schemas.yml`.

The validation workflow checks the sample Political Influence Tree against the Political Influence Tree JSON Schema, validates embedded source receipts against the Source Posture JSON Schema, validates producer export examples against the Producer Export JSON Schema, validates validation-result receipts against the Validation Result JSON Schema, and runs the combined activation validation runner.

The validation status note and final activation handoff record that upstream producer exports and activation receipts exist while green workflow or equivalent reviewed validation confirmation remains pending.

## Cross-repo ingestion

- [Cross-Repo Ingestion Notes](ingestion/cross-repo-ingestion-notes.md)
- [Producer Export Workflow Integration Notes](ingestion/producer-export-workflow-integration-notes.md)

Cross-repo ingestion notes define how producer repositories should send claim text, source receipts, action records, court posture, control candidates, outcome records, and influence nodes into this ledger without converting claim existence into claim truth.

Producer workflow notes define how upstream repositories should generate, validate, and hand off export objects while leaving final admissibility posture to this repository.

## Producer export examples

- [EO 14179 Action Record Export](producer_exports/example/PIT-MODERN-2025-AI-EO-14179__action_record__2025-01-23__SRC-2025-EO14179-FR-001.json)

Producer export examples show how an upstream repo can package a claim, action record, or source receipt for ledger ingestion while leaving final admissibility classification to this repository.

## Producer export test status

- [Producer Export Test Status](release/producer-export-test-status.md)

The first two upstream producer export tests have started from `StegVerse-Labs/Trumpality` and `StegVerse-Labs/Administrations` and are pending ingestion review and validation status confirmation.

## Templates

- [Political Influence Tree Entry Template](templates/political-influence-tree-entry-template.md)
- [Validation Result Receipt Template](templates/validation-result-receipt-template.json)

Use the Political Influence Tree template to create structured topic entries with separate sections for surface claim, factual basis, influence lineage, action conversion, control comparison, institutional response, outcome evidence, ledger classification, and receipts.

Use the validation-result receipt template to replace pending validation receipts only after a concrete green, failed, blocked, or superseded validation result exists.

## Examples

- [Control Comparison Example](examples/control-comparison-example.md)
- [Rhetoric-to-Action Scoring Example](examples/rhetoric-to-action-scoring-example.md)
- [Source Receipt Examples](examples/source-receipt-examples.md)

The examples show how the ledger separates public claim existence from admissible factual basis, action conversion, institutional review, source posture, and measurable outcomes.

## Calibration

- [Rhetoric-to-Action Scoring Calibration](calibration/rhetoric-to-action-scoring-calibration.md)

Calibration notes define how to score claim specificity, factual basis, action conversion, control comparison, institutional response, and outcome evidence without treating the score as an ideological endorsement.

## Political influence trees

- [The Powell Memorandum Influence Tree](trees/fundamental-documents/1971-powell-memo-influence-tree.md)
- [Executive Order 14179 and Federal AI Leadership Framing](trees/modern-topics/2025-ai-leadership-executive-order-14179.md)
- [EO 14179 Control Comparison Expansion](trees/modern-topics/2025-ai-leadership-executive-order-14179-control-comparison.md)
- [AI Human Dignity Warning Language and Consequence Governance](trees/modern-topics/2026-ai-human-dignity-warning-language.md)

The Powell tree is a structural example. The EO 14179 tree is the first modern-topic example and separates official action record from still-untested factual justification and outcome claims. The EO 14179 control expansion defines what evidence is required before those factual justifications can be treated as admissible comparative support. The AI human dignity warning language entry records a May 25, 2026 public-warning convergence as a draft rhetorical marker only; it does not claim endorsement, affiliation, causation, or authority inheritance.

## Governance policy

- [Reviewer, Dispute, and Deprecation Policy](governance/reviewer-dispute-deprecation-policy.md)

The governance policy defines reviewer roles, review states, dispute triggers, deprecation criteria, supersession criteria, and rejection criteria for ledger entries.

## Release readiness

- [Release Readiness Checklist](release/release-readiness-checklist.md)
- [Final Activation Handoff](release/final-activation-handoff.md)

The release checklist and final activation handoff mark the repository as activation-ready-pending-validation and identify the remaining items required before activated status.

## Fundamental document annotations

- [The Powell Memorandum (1971)](annotations/fundamental-documents/1971-powell-memo.md)

The Powell Memorandum is included as a historical anchor for upstream institutional influence. It is not used as proof of causation for later executive action unless a separate evidentiary chain supports that claim. Its proper use is structural and comparative.

## Current repo posture

This repository is now activation-ready-pending-validation. It has standards, schemas, examples, validation scripts, validation-result receipts, ingestion notes, producer export paths, release checklists, review/dispute/deprecation policy, modern-topic control-comparison scaffolding, draft AI human dignity warning-language rhetorical-marker scaffolding, upstream producer export tests from `StegVerse-Labs/Trumpality` and `StegVerse-Labs/Administrations`, and Issue #1 tracking the final activation gate. Activated status still requires a green workflow or equivalent reviewed validation result, supersession of the current pending validation receipt, and promotion of at least one validated producer export into a reviewed ledger receipt.

Current implemented structure:

```text
standards/
  political-influence-tree-standard.md
  source-posture-schema.md

schemas/
  political-influence-tree.schema.json
  source-posture.schema.json
  producer-export.schema.json
  validation-result.schema.json

samples/
  political-influence-tree.sample.json

github/
  workflows/
    validate-ledger-schemas.yml

Note: the actual workflow directory starts with a leading dot in the repository path.

scripts/
  validate_producer_exports.py
  validate_validation_results.py
  run_activation_validation.py

ingestion/
  cross-repo-ingestion-notes.md
  producer-export-workflow-integration-notes.md
  reviewed-producer-export-intake-eo14179.md

producer_exports/
  example/
    PIT-MODERN-2025-AI-EO-14179__action_record__2025-01-23__SRC-2025-EO14179-FR-001.json

validation_results/
  workflow-run-check-a99f8ece.pending.json
  workflow-run-check-2c21eb3e.pending.json
  workflow-run-check-e8df043a.pending.json

templates/
  political-influence-tree-entry-template.md
  validation-result-receipt-template.json

examples/
  control-comparison-example.md
  rhetoric-to-action-scoring-example.md
  source-receipt-examples.md

calibration/
  rhetoric-to-action-scoring-calibration.md

trees/
  fundamental-documents/
    1971-powell-memo-influence-tree.md
  modern-topics/
    2025-ai-leadership-executive-order-14179.md
    2025-ai-leadership-executive-order-14179-control-comparison.md
    2026-ai-human-dignity-warning-language.md

governance/
  reviewer-dispute-deprecation-policy.md

release/
  release-readiness-checklist.md
  producer-export-test-status.md
  validation-status-note.md
  final-activation-handoff.md

annotations/
  fundamental-documents/
    1971-powell-memo.md
```

Next expected additions:

- confirm green workflow or equivalent reviewed validation result
- supersede the latest pending validation-result receipt
- promote at least one validated producer export into a reviewed ledger receipt
- add official primary-source receipt review for the AI human dignity warning-language entry
- add real control evidence receipts for EO 14179
