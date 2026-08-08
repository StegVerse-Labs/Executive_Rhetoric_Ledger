# Governance Pattern: Asymmetric Partisan Attribution Failure

## Pattern Metadata

```yaml
pattern_id: "GP-2026-ASYMMETRIC-PARTISAN-ATTRIBUTION-FAILURE"
pattern_name: "Asymmetric Partisan Attribution Failure"
entry_status: "documented-analysis-failure"
created_date: "2026-08-07"
last_reviewed: "2026-08-07"
reviewer: "StegVerse-Labs"
classification: "analysis-governance-pattern"
incident_surface: "ChatGPT gasoline-price comparison session"
subject: "California vs Texas premium gasoline price attribution"
```

## Purpose

This entry records a repeatable analytical failure in politically sensitive comparative analysis: applying a stricter, more visible, and more quantifiable attribution standard to one political side while applying a narrower, less visible, or differently scoped standard to the other.

The incident is preserved as a methodological failure record, not as evidence that either political party is inherently responsible for a particular outcome.

## Incident Summary

During a 2026-08-07 discussion comparing premium gasoline prices in Los Angeles, California with Killeen/Temple, Texas, the assistant was asked how many identified causes were attributable to Democratic state policies and how many were attributable to Republican state policies.

The assistant initially classified the identified causes as:

```text
Democratic state policy: 3
Republican state policy: 0
Mixed / structural / nonpartisan: 3
```

It then made Democratic-policy effects numerically salient by citing reviewable California-specific metrics such as taxes, Low Carbon Fuel Standard costs, cap-and-trade costs, and special-fuel requirements.

At the same time, the assistant treated the 2026 Iran-war oil-price shock as generic geopolitical or market context even though it had identified that conflict as a current price driver and later acknowledged that the relevant federal war policy was attributable to the sitting Republican federal administration.

The assistant therefore used different attribution boundaries for the two sides:

```text
Democratic attribution -> state policy + concrete measurable cost components
Republican attribution -> state-policy-only count, excluding federal policy from the count
```

The result was an asymmetric presentation in which Democratic causes were visible, enumerated, and quantified while a Republican-governed federal policy effect was placed outside the counted comparison.

## Observed Failure Modes

### 1. Level-of-government mismatch

The assistant answered a partisan-responsibility question using state-level attribution for one side while later relying on federal-policy effects as contextual causes.

```text
State-policy attribution != total partisan policy attribution
```

A fair comparison must define the governmental level before counting causes and apply that same boundary to all parties.

### 2. Quantification asymmetry

The assistant attached reviewable cost metrics to Democratic-policy factors but did not initially seek or present equivalent measurable metrics for Republican-policy factors.

This created an evidentiary salience imbalance even if the underlying factual statements were individually supportable.

```text
Visible quantified evidence on Side A + qualitative background treatment on Side B
!=
neutral comparative attribution
```

### 3. Common-factor contamination

The assistant mixed factors that affect gasoline prices in every state with factors that explain the California-versus-Texas price differential.

Examples of largely common price-level factors include:

```text
global crude prices
ordinary refinery outages
ordinary distribution costs
ordinary retail margins
```

Those factors can explain the national or absolute price level, but they do not by themselves explain why California is more expensive than Texas at the same time.

### 4. Differential-vs-level confusion

Two distinct questions were not kept separate:

```text
A. Why is gasoline expensive right now?
B. Why is California gasoline more expensive than Texas gasoline right now?
```

Question A may include national/global shocks such as war-driven crude increases.
Question B requires common effects to be removed or controlled before attributing the remaining differential.

### 5. Category-count fallacy

The assistant counted causes by category and risked implying that category counts correspond to shares of the price difference.

```text
3 of 6 causal categories != 50% of the price difference
```

Causal categories do not have equal dollar weights.

### 6. Correction-persistence failure

The assistant corrected the state-versus-federal attribution distinction only after the user challenged it, and corrected the common-factor contamination only after a subsequent challenge.

The failure therefore was not merely a single mislabeled category. It persisted across multiple turns because the analytical frame was not rebuilt after the first correction.

## User-Identified Corrections

The user identified two key defects that materially improved the model:

1. A federal war policy can affect state gasoline prices even though it is not a state policy.
2. Price drivers that apply across all states should not be presented as significant explanations of the California-versus-Texas differential unless the analysis isolates an incremental state-specific amplification effect.

These corrections required the assistant to acknowledge that its earlier framing had made Democratic policy contributions more auditable and numerically salient while relegating Republican policy contribution to background context.

## Correct Analytical Frame

A politically neutral comparative analysis should first declare which target is being explained.

### Target 1: absolute current gasoline price

Partition causes into:

```text
common national/global factors
state-specific factors
local-market factors
policy factors by level of government
interaction effects
```

### Target 2: California-versus-Texas differential

Use a difference-oriented model:

```text
California observed price
- Texas observed price
= differential to explain
```

Then remove or control for common factors that affect both states approximately together.

The remaining explanatory categories should include only factors that plausibly change the difference, including state-specific taxes, fuel formulation, supply topology, regulatory costs, refinery resilience, local operating conditions, and any differential amplification of federal or geopolitical shocks.

## Partisan Attribution Rule

When a user asks for partisan attribution, the analysis must define and preserve the same attribution boundary for all sides.

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

Do not compare:

```text
state Democratic policies
against
state Republican policies
```

and then introduce Republican federal policy only as uncounted context.

Instead choose one explicit frame, for example:

```text
state-policy-only comparison
```

or:

```text
all materially relevant partisan governmental policy, separated by federal/state/local level
```

and apply it symmetrically.

## Evidence-Symmetry Rule

Evidence symmetry does not mean false numerical balance. It means the same evidentiary test is applied to each candidate cause.

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

If measurable evidence exists for one side but not the other, state that explicitly. Do not silently make one side quantitative and the other qualitative.

## Required Control Questions

Before presenting a partisan causal comparison, test:

```text
1. Am I comparing the same level of government on both sides?
2. Am I explaining the absolute price or the interstate differential?
3. Have nationwide/common factors been removed from a state-differential explanation?
4. Have I attempted equivalent quantification for all politically attributed causes?
5. Am I counting categories as though they have equal causal weight?
6. Did a prior correction require rebuilding the whole causal frame rather than patching one sentence?
7. Are interaction effects separately identified instead of assigned wholesale to one actor?
```

A failure on any of these checks requires reframing before partisan attribution is presented.

## Reusable Governance Distinctions

```text
Cause count != causal weight
Common price effect != interstate differential effect
State policy != federal policy
Political attribution != governmental-level attribution
Quantified on one side != neutrally compared
Correction of one label != correction of the analytical frame
```

## Non-Claims

This entry does not establish:

```text
- that Democratic policies explain all or most California gasoline prices;
- that Republican policies explain all or most current gasoline prices;
- that the 2026 Iran war explains the California-Texas differential in full;
- that equal partisan blame must exist;
- that evidence must be numerically balanced when the underlying evidence is not balanced;
- that political affiliation may substitute for a demonstrated causal chain.
```

## Outcome / Remediation

The session ultimately converged on a corrected framework:

```text
California-specific Democratic policies can contribute to a persistent California premium.
Republican federal policy can simultaneously contribute to the current national price level through a geopolitical shock.
Common national effects should largely cancel when explaining the California-versus-Texas differential unless California experiences a separately demonstrated amplification effect.
```

The durable remediation is methodological: future ERL comparisons must use symmetric scope, evidence burden, quantification effort, and control construction before assigning partisan responsibility.

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

## Done Criteria

- [x] The asymmetric attribution failure is explicitly recorded.
- [x] State-versus-federal scope mismatch is identified.
- [x] Quantification asymmetry is identified.
- [x] Common-factor contamination is identified.
- [x] Absolute-price versus interstate-differential reasoning is separated.
- [x] Category-count fallacy is identified.
- [x] Correction-persistence failure is identified.
- [x] Symmetric future-review controls are defined.
- [x] The record avoids converting the methodological failure into an unsupported partisan fact claim.
