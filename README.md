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

## Templates

- [Political Influence Tree Entry Template](templates/political-influence-tree-entry-template.md)

Use this template to create structured topic entries with separate sections for surface claim, factual basis, influence lineage, action conversion, control comparison, institutional response, outcome evidence, ledger classification, and receipts.

## Examples

- [Control Comparison Example](examples/control-comparison-example.md)
- [Rhetoric-to-Action Scoring Example](examples/rhetoric-to-action-scoring-example.md)

The examples show how the ledger separates public claim existence from admissible factual basis, action conversion, institutional review, and measurable outcomes.

## Political influence trees

- [The Powell Memorandum Influence Tree](trees/fundamental-documents/1971-powell-memo-influence-tree.md)

The first populated tree is a structural example. It treats the Powell Memorandum as a primary historical artifact and does not assert downstream causation without separate evidence.

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

templates/
  political-influence-tree-entry-template.md

examples/
  control-comparison-example.md
  rhetoric-to-action-scoring-example.md

trees/
  fundamental-documents/
    1971-powell-memo-influence-tree.md

annotations/
  fundamental-documents/
    1971-powell-memo.md
```

Next expected additions:

- scoring calibration notes
- source receipt examples
- first modern-topic political influence tree
- validation workflow
