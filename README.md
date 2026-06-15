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

These schemas provide validation targets for converting Markdown ledger entries into machine-checkable data objects.

## Machine-readable samples

- [Political Influence Tree Sample](samples/political-influence-tree.sample.json)

The sample mirrors the Powell Memorandum structural tree and provides a test object for schema validation.

## Validation

- [Validate Ledger Schemas workflow](github/workflows/validate-ledger-schemas.yml)

Note: the actual repository path starts with a leading dot. It is shown here without the leading dot as requested: `github/workflows/validate-ledger-schemas.yml`.

The validation workflow checks the sample Political Influence Tree against the Political Influence Tree JSON Schema and validates embedded source receipts against the Source Posture JSON Schema.

## Cross-repo ingestion

- [Cross-Repo Ingestion Notes](ingestion/cross-repo-ingestion-notes.md)

Cross-repo ingestion notes define how producer repositories should send claim text, source receipts, action records, court posture, control candidates, outcome records, and influence nodes into this ledger without converting claim existence into claim truth.

## Producer export examples

- [EO 14179 Action Record Export](producer_exports/example/PIT-MODERN-2025-AI-EO-14179__action_record__2025-01-23__SRC-2025-EO14179-FR-001.json)

Producer export examples show how an upstream repo can package a claim, action record, or source receipt for ledger ingestion while leaving final admissibility classification to this repository.

## Templates

- [Political Influence Tree Entry Template](templates/political-influence-tree-entry-template.md)

Use this template to create structured topic entries with separate sections for surface claim, factual basis, influence lineage, action conversion, control comparison, institutional response, outcome evidence, ledger classification, and receipts.

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

The Powell tree is a structural example. The EO 14179 tree is the first modern-topic example and separates official action record from still-untested factual justification and outcome claims.

## Fundamental document annotations

- [The Powell Memorandum (1971)](annotations/fundamental-documents/1971-powell-memo.md)

The Powell Memorandum is included as a historical anchor for upstream institutional influence. It is not used as proof of causation for later executive action unless a separate evidentiary chain supports that claim. Its proper use is structural and comparative.

## Current repo posture

This repository is in early standardization.

Current implemented structure:

```text
standards/
  political-influence-tree-standard.md
  source-posture-schema.md

schemas/
  political-influence-tree.schema.json
  source-posture.schema.json

samples/
  political-influence-tree.sample.json

github/
  workflows/
    validate-ledger-schemas.yml

Note: the actual workflow directory starts with a leading dot in the repository path.

ingestion/
  cross-repo-ingestion-notes.md

producer_exports/
  example/
    PIT-MODERN-2025-AI-EO-14179__action_record__2025-01-23__SRC-2025-EO14179-FR-001.json

templates/
  political-influence-tree-entry-template.md

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

annotations/
  fundamental-documents/
    1971-powell-memo.md
```

Next expected additions:

- validation result badges or status notes
- additional machine-readable sample entries
- modern-topic control comparison expansion
- producer export schema
