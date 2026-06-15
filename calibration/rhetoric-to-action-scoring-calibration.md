# Rhetoric-to-Action Scoring Calibration

## Purpose

This document calibrates the scoring pattern used by the Executive Rhetoric Ledger when comparing public rhetoric, factual basis, authority conversion, institutional response, and outcome evidence.

The score is not an endorsement score.

The score is not an ideological score.

The score measures how completely a claim can be traced from public statement to evidence, authority, review, and consequence.

## Core Rule

```text
Score the trace, not the politics.
```

## Standard Dimensions

Each scored entry uses six dimensions.

```yaml
score_dimensions:
  claim_specificity:
    range: "0-3"
    question: "Can the claim be tested?"
  factual_basis:
    range: "0-3"
    question: "Is the claim supported by admissible records?"
  action_conversion:
    range: "0-3"
    question: "Did rhetoric become institutional action?"
  control_comparison:
    range: "0-3"
    question: "Were comparable cases checked?"
  institutional_response:
    range: "0-3"
    question: "Was the action reviewed by courts, agencies, legislatures, or oversight bodies?"
  outcome_evidence:
    range: "0-3"
    question: "Are claimed consequences measurable and supported?"
```

## Dimension Calibration

### 1. Claim Specificity

```yaml
0: "No clear claim, slogan only, or non-testable assertion."
1: "General claim with vague target, scope, or time frame."
2: "Specific claim with identifiable target but incomplete scope or measurement basis."
3: "Specific, testable claim with clear target, time frame, jurisdiction, and measurable terms."
```

### 2. Factual Basis

```yaml
0: "No evidence supplied, contradicted by record, or purely rhetorical basis."
1: "Weak or secondary evidence only; primary records missing."
2: "Some primary or official evidence exists, but gaps or unresolved contradictions remain."
3: "Primary records, official data, or court records strongly support the claim."
```

### 3. Action Conversion

```yaml
0: "No institutional action found."
1: "Informal pressure, campaign promise, public directive, or unclear implementation."
2: "Partial action through agency guidance, draft rule, litigation posture, or limited enforcement step."
3: "Formal executive order, final agency rule, legislation, enforcement action, budget condition, or judicial position."
```

### 4. Control Comparison

```yaml
0: "No control comparison supplied where one is required."
1: "Controls are named but incomplete, weak, or not comparable."
2: "Comparable cases exist but some jurisdictional, temporal, or magnitude gaps remain."
3: "Comparable cases are documented across relevant jurisdictions, instruments, magnitudes, and review posture."
```

### 5. Institutional Response

```yaml
0: "No review found, or action rejected/contradicted by available institutional response."
1: "Review pending, informal response only, or early litigation posture."
2: "Partial review exists, such as preliminary injunction, stay, remand, oversight report, or agency revision."
3: "Final or mature review posture exists through court decision, legislative action, oversight finding, or completed administrative review."
```

### 6. Outcome Evidence

```yaml
0: "No measurable outcome evidence, or outcomes contradict stated claim."
1: "Projected or claimed outcomes only."
2: "Some measured outcomes exist, but causation, scope, or timeframe remains uncertain."
3: "Measured outcomes are documented and tied to the action with adequate source posture."
```

## Percentage Calculation

```text
total_score = sum(all six dimension scores)
max_score = 18
percentage = round((total_score / max_score) * 100, 1)
```

## Interpretive Bands

```yaml
"0-25":
  label: "rhetorical-only or unsupported"
  meaning: "The entry mainly records claim existence, not admissible governing basis."

"26-50":
  label: "converted but weakly supported or under-tested"
  meaning: "Some action or evidence exists, but controls, review, or outcome support are incomplete."

"51-75":
  label: "partially supported and institutionally developed"
  meaning: "The claim has meaningful evidence, action, and/or review, but not full outcome support."

"76-100":
  label: "strongly supported, converted, controlled, reviewed, and outcome-linked"
  meaning: "The claim is strongly traceable across evidence, authority, controls, review, and outcomes."
```

## Required Classification Notes

Every score must include notes explaining:

- why each dimension received its score;
- whether the claim was evaluated as rhetoric only or as governing justification;
- whether controls were required and present;
- whether the action was formally binding or merely rhetorical;
- whether outcome evidence is measured, projected, claimed, or absent.

## Anti-Misuse Rule

Do not use the score as a truth label without reading the notes.

A high action-conversion score with a low factual-basis score may indicate an important governance concern.

A low score may simply mean the claim has not been reviewed yet.

A high score does not mean the policy is normatively good.

A low score does not mean the speaker is wrong.

## Summary

Rhetoric-to-action scoring gives the ledger a repeatable method for comparing public claims against evidence, authority, controls, review, and outcomes.

The score exists to reveal trace quality, not political preference.
