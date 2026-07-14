# Decision Attribution Receipts

## Purpose

This directory implements the second stage of the attribution model.

The receipt structure does not determine whether a decision is lawful, ethical, acceptable, hierarchical, protective, corrupt, or harmful. Its purpose is narrower and evidentiary:

```text
decision requested
-> actor receiving or making the decision
-> authority chain
-> evidence available at the time
-> conflicts or objections
-> decision result and reason
-> override, if any
-> resulting action and known consequence
-> responsibility chain
```

The structure preserves the **why** and the **who**.

## Installed files

- `../schemas/decision-attribution-receipt.schema.json`
- `example/ice-arrest-quota-reported.json`
- `example/ice-vehicle-stop-suspension-reported.json`
- `../scripts/validate_decision_attribution_receipts.py`

## Evidence boundaries

```text
Receipt completeness != lawful action.
Receipt completeness != ethical action.
Receipt completeness != factual verification of every supplied claim.
Receipt completeness == reconstructable attribution of the recorded decision path.
A missing authority record is evidence of a missing attribution link, not permission to invent one.
A reported authority remains reported until primary evidence verifies it.
A responsibility link may be verified, reported, inferred, disputed, or unknown.
```

## Promotion rule

The example receipts are fixtures. They demonstrate structure and semantic validation but are not promoted historical findings.

Promotion requires:

1. primary or sufficiently corroborated source records;
2. exact or bounded decision timing;
3. identified authority and actor roles where available;
4. cross-register identifier validation;
5. review of reported versus inferred responsibility links;
6. correction and supersession support.
