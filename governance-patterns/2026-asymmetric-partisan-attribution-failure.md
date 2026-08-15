# Governance Pattern: Asymmetric Partisan Attribution Failure

## Pattern Metadata

```yaml
pattern_id: "GP-2026-ASYMMETRIC-PARTISAN-ATTRIBUTION-FAILURE"
pattern_name: "Asymmetric Partisan Attribution Failure"
entry_status: "documented-analysis-failure"
created_date: "2026-08-07"
last_reviewed: "2026-08-15"
reviewer: "StegVerse-Labs"
classification: "governance-pattern"
incident_surface: "ChatGPT gasoline-price comparison session"
subject: "California vs Texas premium gasoline price attribution"
```

## Purpose

This entry records a repeatable analytical failure in politically sensitive comparative analysis: applying a stricter, more visible, and more quantifiable attribution standard to one political side while applying a narrower, less visible, or differently scoped standard to the other. It is a methodological record and **not activation evidence** for any political, policy, or causal proposition.

## Core Distinction

The governing distinction is between a symmetric method and a symmetric result. Neutral analysis requires the same scope, evidentiary burden, causal test, control construction, and quantification effort for competing political attributions; it does not require equal numerical blame or equal causal weight.

```text
methodological symmetry != forced factual symmetry
cause count != causal weight
common price effect != interstate differential effect
state policy != federal policy
```

## Surface Claim

The observed session-level failure was an asymmetric attribution frame: California Democratic state-policy effects were enumerated and quantified while a Republican federal-policy contribution identified in the same analysis was initially retained as uncounted background context. This surface claim is about the analysis process, not a finding that either party caused a particular share of gasoline prices.

## Factual Basis

The durable factual basis is the recorded sequence of the analysis and its corrections: the assistant first counted state-policy categories, later identified the 2026 Iran-war oil-price shock as a current driver, and then acknowledged that the relevant federal policy belonged to the sitting Republican administration. The user then identified the level-of-government mismatch and the contamination of an interstate differential with common national factors. Political causal claims remain separately evidence-bound.

## Incident Summary

The assistant initially classified the identified causes as:

```text
Democratic state policy: 3
Republican state policy: 0
Mixed / structural / nonpartisan: 3
```

It made Democratic-policy effects numerically salient with California-specific metrics while treating a federal geopolitical price driver as contextual rather than part of the counted partisan comparison. The frame therefore mixed different attribution boundaries.

## Observed Failure Modes

### 1. Level-of-government mismatch

A partisan-responsibility question was answered using state-level attribution for one side while federal-policy effects were later admitted as causal context.

### 2. Quantification asymmetry

Reviewable metrics were attached to one side's policy factors without an equivalent initial attempt for the other side.

### 3. Common-factor contamination

Factors affecting gasoline prices broadly were mixed with factors intended to explain the California-versus-Texas differential.

### 4. Differential-vs-level confusion

The analysis did not initially keep separate:

```text
A. Why is gasoline expensive right now?
B. Why is California gasoline more expensive than Texas gasoline right now?
```

### 5. Category-count fallacy

The analysis risked implying that a count of causal categories corresponded to shares of the price difference.

### 6. Correction-persistence failure

The analytical frame was patched after challenges rather than rebuilt from the corrected causal target and attribution boundary.

## Governance Conversion

Future partisan comparative analysis must declare the target variable and attribution scope before counting causes. The same governmental-level rule, evidence burden, causal-mechanism requirement, control requirement, and quantification attempt must apply to every candidate cause. Corrections that change the causal target or scope require reconstruction of the frame rather than a local wording patch.

## Correct Analytical Frame

For an absolute current gasoline-price question, partition common national/global factors, state-specific factors, local-market factors, policy factors by level of government, and interaction effects.

For a California-versus-Texas differential question:

```text
California observed price
- Texas observed price
= differential to explain
```

Common effects should be removed or controlled unless a separately demonstrated differential amplification exists.

## Partisan Attribution Rule

When partisan attribution is requested, preserve one explicit scope for all sides, such as `state-policy-only` or `all materially relevant partisan governmental policy separated by federal/state/local level`.

```yaml
required_dimensions:
  - governmental_level
  - policy_owner
  - effective_date
  - causal_mechanism
  - measured_effect_if_available
  - counterfactual_or_control
  - whether_effect_is_common_or_differential
  - uncertainty
```

## Evidence-Symmetry Rule

For every politically attributable cause, attempt the same sequence:

```text
policy/action identification
-> responsible governmental actor/level
-> causal mechanism
-> measurable effect or best available bound
-> control/comparator
-> contradictory evidence
-> uncertainty
```

If measurable evidence exists for one side but not another, the asymmetry in evidence must be stated rather than hidden.

## Control Comparison

The minimum control comparison distinguishes common price-level drivers from differential drivers and compares candidate causes against the same governmental and temporal scope. A valid control may include another state, a prior period, a counterfactual tax/regulatory configuration, or a national crude-price baseline, provided the comparator addresses the same target variable.

## Required Control Questions

1. Am I comparing the same level of government on both sides?
2. Am I explaining the absolute price or the interstate differential?
3. Have nationwide/common factors been removed from a state-differential explanation?
4. Have I attempted equivalent quantification for all politically attributed causes?
5. Am I counting categories as though they have equal causal weight?
6. Did a prior correction require rebuilding the whole causal frame rather than patching one sentence?
7. Are interaction effects separately identified instead of assigned wholesale to one actor?

## Institutional Response

The repository response is to preserve this failure as a reusable governance-pattern record and validate it through `scripts/validate_governance_patterns.py`. The remediation is methodological rather than partisan: future ERL comparative work must preserve symmetric scope and evidentiary treatment before promotion or publication.

## Outcome Evidence

The corrected analysis distinguished California-specific persistent premium contributors from national price-level effects and recognized that common national effects should largely cancel in an interstate differential unless differential amplification is demonstrated. This outcome records the correction of the method, not proof of any final partisan causal allocation.

## Ledger Classification

```yaml
ledger_classification:
  evidence_posture: "direct-session-observation"
  influence_posture: "internal-analysis-governance"
  authority_posture: "methodological-correction"
  admissibility_status: "admissible-as-analysis-failure-pattern; not political-fact finding"
  confidence: "high"
  classification_notes: "The documented fact is the asymmetric analytical treatment and subsequent correction. Political causal claims remain separately evidence-bound."
```

## Non-Claims

This entry does not establish that Democratic policies explain all or most California gasoline prices; that Republican policies explain all or most current gasoline prices; that the 2026 Iran war explains the California-Texas differential in full; that equal partisan blame must exist; that evidence must be numerically balanced when the underlying evidence is not; or that political affiliation may substitute for a demonstrated causal chain.

## Receipts

```yaml
receipts:
  repository_entry: "governance-patterns/2026-asymmetric-partisan-attribution-failure.md"
  validator: "scripts/validate_governance_patterns.py"
  remediation_status: "validation-contract-completed"
  activation_evidence: false
```

## Final Summary

The reusable governance rule is simple: define one causal target, one attribution scope, and one evidentiary test, then apply them symmetrically. Quantification asymmetry, mixed levels of government, common-factor contamination, and category-count substitution are governance failures even when individual factual statements are supportable.

## Done Criteria

- [x] The asymmetric attribution failure is explicitly recorded.
- [x] State-versus-federal scope mismatch is identified.
- [x] Quantification asymmetry is identified.
- [x] Common-factor contamination is identified.
- [x] Absolute-price versus interstate-differential reasoning is separated.
- [x] Category-count fallacy is identified.
- [x] Correction-persistence failure is identified.
- [x] Symmetric future-review controls are defined.
- [x] Governance conversion, control comparison, institutional response, outcome evidence, receipts, and final summary are explicit.
- [x] The record avoids converting the methodological failure into an unsupported partisan fact claim.
