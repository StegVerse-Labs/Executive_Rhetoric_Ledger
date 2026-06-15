# Rhetoric-to-Action Scoring Example

## Purpose

This example defines a minimal scoring pattern for comparing executive rhetoric against later action, institutional response, and measurable outcome evidence.

The score does not decide whether a policy is good or bad.

It measures whether a public claim moved into institutional action and whether the stated factual basis remained supported through review.

## Core Rule

```text
Rhetoric-to-action scoring measures conversion, support, and consequence. It does not measure ideological agreement.
```

## Score Dimensions

```yaml
score_dimensions:
  claim_specificity:
    range: "0-3"
    meaning: "How specific and testable the public claim is."
  factual_basis:
    range: "0-3"
    meaning: "How well the claim is supported by admissible records."
  action_conversion:
    range: "0-3"
    meaning: "Whether the rhetoric became policy, enforcement, litigation posture, or other institutional action."
  control_comparison:
    range: "0-3"
    meaning: "Whether comparable cases were checked before treating the justification as admissible."
  institutional_response:
    range: "0-3"
    meaning: "Whether courts, agencies, legislatures, or oversight bodies upheld, modified, blocked, or rejected the action."
  outcome_evidence:
    range: "0-3"
    meaning: "Whether measurable outcomes support, fail to support, or contradict the claimed effect."
```

## Scoring Scale

```text
0 = absent, unsupported, contradicted, or not found
1 = weak, rhetorical, incomplete, or pending
2 = partially supported or partially converted
3 = strongly supported, documented, and reviewable
```

## Example Scoring Object

```yaml
rhetoric_to_action_score:
  claim_specificity:
    score: 2
    notes: "The claim identifies a problem class but lacks exact scope."
  factual_basis:
    score: 1
    notes: "Some secondary evidence exists, but primary records are incomplete."
  action_conversion:
    score: 3
    notes: "The claim became an executive directive and agency implementation step."
  control_comparison:
    score: 0
    notes: "No comparable jurisdiction or prior-administration controls supplied."
  institutional_response:
    score: 1
    notes: "Litigation pending; no final judicial posture."
  outcome_evidence:
    score: 0
    notes: "No measured outcomes available yet."
  total_score: 7
  max_score: 18
  percentage: 38.9
```

## Interpretive Bands

```yaml
interpretive_bands:
  "0-25": "rhetorical-only or unsupported"
  "26-50": "converted but weakly supported or under-tested"
  "51-75": "partially supported and institutionally developed"
  "76-100": "strongly supported, converted, controlled, reviewed, and outcome-linked"
```

## Ledger Classification Mapping

```yaml
classification_mapping:
  rhetorical_only:
    condition: "low action conversion and low factual basis"
  action_without_admissible_basis:
    condition: "high action conversion with low factual basis or missing controls"
  supported_action:
    condition: "high factual basis, action conversion, and institutional response"
  contradicted_action:
    condition: "outcome evidence or court records contradict stated basis"
  pending_review:
    condition: "action exists but judicial, oversight, or outcome evidence remains incomplete"
```

## Example Summary

```text
The claim was specific enough to evaluate and did convert into action, but the factual basis remains weak and no control comparison has been supplied. The score therefore identifies a high rhetoric-to-action conversion with low admissibility support.
```

## Anti-Misuse Note

A high score is not an endorsement.

A low score is not a partisan rejection.

The score only measures how well rhetoric, evidence, authority, comparison, response, and outcome connect inside the ledger.

## Summary

Rhetoric-to-action scoring helps the Executive Rhetoric Ledger distinguish between claims that remain rhetorical, claims that convert into authority without adequate support, and claims that become institutionally reviewable action with documented factual basis and outcome evidence.
