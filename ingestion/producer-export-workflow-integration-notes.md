# Producer Export Workflow Integration Notes

## Purpose

These notes define how producer repositories should generate, validate, and hand off export objects for the Executive Rhetoric Ledger.

The goal is to let upstream repositories contribute records without deciding final ledger admissibility.

## Core Rule

```text
Producer repos export structured evidence.
The Executive Rhetoric Ledger assigns final admissibility posture.
```

## Producer Responsibilities

Producer repositories should:

1. identify the object class being exported;
2. attach at least one source receipt;
3. record the producer repo, path, and commit;
4. distinguish claim text from factual basis;
5. declare the requested admissibility use;
6. leave final ledger classification to this repository.

## Recommended Producer Directory

```text
ledger_exports/executive_rhetoric_ledger/
```

## Recommended Filename Pattern

```text
<topic-id>__<object-class>__<date>__<source-id>.json
```

Example:

```text
PIT-MODERN-2025-AI-EO-14179__action_record__2025-01-23__SRC-2025-EO14179-FR-001.json
```

## Export Object Validation

Producer exports should validate against:

```text
schemas/producer-export.schema.json
```

Source receipts inside the export should validate against:

```text
schemas/source-posture.schema.json
```

## Minimal Producer Workflow

```yaml
name: Validate Ledger Export

on:
  pull_request:
  push:
    branches:
      - main
  workflow_dispatch:

jobs:
  validate-ledger-export:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - run: python -m pip install --upgrade jsonschema

      - name: Validate export JSON files
        run: |
          python scripts/validate_ledger_exports.py
```

## Suggested Producer Script Behavior

A producer validation script should:

- locate files in `ledger_exports/executive_rhetoric_ledger/`;
- load the Executive Rhetoric Ledger producer export schema;
- validate every export object;
- validate every embedded source receipt;
- fail if any object upgrades claim existence into factual truth without posture;
- report which export file failed and why.

## Handoff Options

Producer repos may hand off export objects through:

```text
manual copy
pull request into Executive_Rhetoric_Ledger
artifact upload
release bundle
cross-repo ingestion automation
```

Manual copy is acceptable in early development if the producer commit is recorded.

## Required Review at Ledger Side

When an export arrives, the Executive Rhetoric Ledger should review:

- whether the object class is appropriate;
- whether the source posture is adequate;
- whether the requested admissibility use is too broad;
- whether controls are required;
- whether the export maps to an existing tree or requires a new tree;
- whether the producer source proves claim text, factual basis, action conversion, court posture, outcome evidence, or context only.

## Anti-Misuse Notes

A producer export must not:

- treat social-media repetition as factual proof;
- treat media amplification as independent evidence;
- treat a policy memo as proof of causation;
- treat an executive order as proof that its factual justification is true;
- treat missing controls as satisfied;
- fill unknown influence nodes with assumptions.

## Summary

Producer export workflow integration allows StegVerse-Labs repositories to contribute structured records while preserving the Executive Rhetoric Ledger's evidentiary boundaries.

The producer exports evidence.

The ledger evaluates admissibility.
