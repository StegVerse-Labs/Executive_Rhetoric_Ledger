# Progress Footer Specification

## Purpose

This file records the four-line progress footer format used for this repo build stream.

## Footer Format

At the end of each build/status response, include exactly four lines:

```text
<ORG.NAME> - %complete
<REPO.NAME> - %complete
<REPO.NAME> - %complete TO GOAL ACTIVATION;
Δ [<REPO.NAME>: <ACTUAL>vs<BUILT>] - EXPLANATION.
```

## Current Values

```text
StegVerse-Labs - 5% complete
Executive_Rhetoric_Ledger - 100% complete
Executive_Rhetoric_Ledger - 99% complete TO GOAL ACTIVATION;
Δ [Executive_Rhetoric_Ledger: 0 missing critical paths vs 5 README-list delta paths] - Repo structure verification shows no activation-critical missing paths; README structure list trails the verified repo by five newer activation files.
```

## Reset Rule

When the goal changes, completes, or a new goal is added, reset the displayed completion values for the new goal baseline.

## Delta Source

The current file-structure delta is recorded in:

```text
release/repo-structure-delta.md
```
