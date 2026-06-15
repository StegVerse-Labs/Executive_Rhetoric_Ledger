# Producer Export Validation Quickstart

## Purpose

This quickstart documents the local validation command for producer export JSON files.

## Default Command

```bash
python scripts/validate_producer_exports.py
```

Default target:

```text
producer_exports/example/*.json
```

## Validate Specific Files

```bash
python scripts/validate_producer_exports.py path/to/export.json
```

Multiple files may be passed in one command.

## Checks Performed

The script checks producer export objects against:

```text
schemas/producer-export.schema.json
```

The script checks embedded source receipts against:

```text
schemas/source-posture.schema.json
```

## CI Path

The validation workflow calls the same script.

Actual path:

```text
.github/workflows/validate-ledger-schemas.yml
```

Displayed README path:

```text
github/workflows/validate-ledger-schemas.yml
```

## Current Producer Paths

```text
StegVerse-Labs/Trumpality
StegVerse-Labs/Administrations
```

## Summary

Producer export validation is now available as both a local script and a workflow step.
