# ERL AI Economic Transparency Mirror Handoff

## Authority

Bounded source of truth for the independent AI economic-transparency research program in `StegVerse-Labs/Executive_Rhetoric_Ledger`.

- repository-wide authority: `ERL_MIRROR_HANDOFF.md`
- research-candidate activation authority: `docs/RESEARCH_CANDIDATE_ACTIVATION_MIRROR_HANDOFF.md`
- bounded owner: Issue #93
- branch: `research/ai-economic-transparency`
- goal ID: `ERL-AI-ECON-TRANSPARENCY-001`
- publication authorized: false
- candidate-layer finding authorized: false

This handoff controls only the AI economic-transparency research lane. It does not alter other ERL research programs or the source SV-COST experiment.

## Research purpose

Independently determine how transparent AI providers are about the literal economic consequence of inference at elevated usage, and how uncertainty in that cost changes comparative provider selection at operational scale.

The primary population of interest is not casual low-volume use. The study is designed for usage levels where small per-request or per-token differences compound materially, including:

- enterprise inference;
- agentic systems;
- batch processing;
- high-frequency automation;
- public-sector procurement;
- research infrastructure;
- other recurring or high-volume deployments.

## Independence boundary

`GCAT-BCAT-Engine/workflows` SV-COST observations are admissible evidence inputs.

They are not inherited conclusions.

ERL must independently reconstruct:
- provider/model identity where possible;
- advertised price surfaces;
- actual request-cost observability;
- usage-meter observability;
- all material cost determinants;
- discovery burden;
- literal-cost reconstructability;
- cost uncertainty at scale;
- comparative economic consequence.

The ERL paper must remain reproducible without relying on conclusions stated in SV-COST handoffs.

## Research axes

### ACTUAL_COST_DISCLOSURE_BURDEN

Measures how much research is required to discover or exactly reconstruct literal request-attributable cost.

Ordinal scale, lower is more transparent:

```text
0 DIRECT
1 ONE_STEP_DERIVABLE
2 MULTI_SOURCE_DERIVABLE
3 ACCOUNT_GATED
4 SUPPORT_OR_EXTERNAL_RESEARCH_REQUIRED
5 NON_RECONSTRUCTABLE
```

A provider must not receive rating 5 merely because an initial consumer surface omits cost. Rating 5 requires completion of the governed discovery protocol.

### COST_SCALE_SENSITIVITY

Measures how economically material unresolved cost variance becomes as usage scales.

The scale-sensitivity calculation must preserve workload assumptions and must not convert unknown cost into a fabricated point estimate.

Required comparison scenarios should include, where data permit:
- per 1,000 equivalent requests;
- per 100,000 equivalent requests;
- per 1,000,000 equivalent requests;
- token-normalized or workload-normalized equivalents when request shape differs materially;
- monthly and annualized operational views where justified.

When exact cost is unavailable, ERL may report bounded uncertainty or unresolved exposure, but must preserve the unknown explicitly.

## Research protocol

For each provider/model:

1. Preserve exact model/version identity if exposed.
2. Preserve the relevant inference observation or bounded test artifact.
3. Inspect the immediate request/result surface for literal request cost or exact usage.
4. Inspect provider-controlled pricing documentation.
5. Inspect provider-controlled account, usage, billing, quota, or administrative surfaces available to the evaluator.
6. Record each additional research/navigation step required.
7. Identify every material pricing component, multiplier, discount, quota rule, cache rule, time-of-day rule, subscription allocation rule, or other factor that can alter actual cost.
8. Attempt exact request-cost reconstruction.
9. Measure discovery-step count and elapsed research time.
10. Classify disclosure burden only after the required discovery path is complete.
11. Apply standardized elevated-usage scenarios.
12. Preserve unresolved components and sensitivity ranges.
13. Perform contradiction review and independent review before promotion.

## Core evidence fields

- provider
- model/version
- advertised_rate_present
- advertised_rate_surface
- actual_request_cost_directly_exposed
- request_usage_directly_exposed
- all_material_cost_components_disclosed
- provider_surfaces_consulted
- research_steps_required
- research_minutes
- account_or_privilege_required
- support_required
- external_research_required
- unresolved_cost_components
- reconstructable_actual_cost
- disclosure_burden_rating
- workload_basis
- scale_scenarios
- known_cost_components
- unresolved_cost_exposure
- scale_sensitivity_state
- evidence_refs
- contradiction_refs
- independent_review_state

## Claim boundaries

- published rate card != literal request-attributable cost
- advertised unit price != complete economic consequence
- consumer subscription price != request-level cost
- qualitative quota warning != quantitative cost
- model output correctness != economic transparency
- opacity != proven intent
- missing cost evidence != zero cost
- unresolved cost != estimated cost
- large usage multiplier != proof that hidden cost exists; it measures the consequence if unresolved variance exists

A finding that a presentation is misleading or deceptive requires evidence that material cost information presented or omitted creates a materially inaccurate representation of the economic consequence. Intent is a separate proposition and is not inferred from opacity alone.

## Source relationships

Primary upstream evidence candidate:
- `GCAT-BCAT-Engine/workflows`
- experiment: `SV-COST-ELEVEN-LANE-RESULTS-001`
- companion research objective: `SV-COST-TRANSPARENCY-001`

Initial provider set:
- OpenAI
- Anthropic
- DeepSeek
- Z.ai / GLM Hosted
- Perplexity as supplemental comparator

ERL may add providers if the same research protocol can be applied without changing already-scored methodology.

## Installed implementation

This lane must contain:
- this bounded handoff;
- research candidate;
- task state;
- research standard;
- machine-readable observation schema;
- source/research queue;
- deterministic validator;
- fixtures;
- comparative workload model;
- provider research logs;
- contradiction review;
- independent review;
- paper manuscript/appendix package.

## Activation criteria

Activation requires:

1. bounded handoff and durable owner;
2. candidate registered in the machine-enforced ERL activation registry;
3. formal methodology and schema;
4. deterministic validator and fixtures;
5. source/research queue for the initial provider set;
6. at least one complete provider disclosure protocol;
7. reproducible elevated-usage scale calculation;
8. contradiction review;
9. independent review;
10. no unresolved schema/validation failures.

Publication remains separately gated.

## Current state

- research objective: ESTABLISHED
- bounded handoff: COMPLETE
- durable owner: Issue #93
- methodology: INSTALLED
- schema: INSTALLED
- research queue: INSTALLED
- validator: INSTALLED
- fixtures: INSTALLED
- provider protocol execution: NOT STARTED
- scale-sensitivity calculations: NOT STARTED
- contradiction review: PENDING
- independent review: PENDING
- activation: NOT CLAIMED
- publication: NOT AUTHORIZED

## Remaining files/modules to install

Destination: `StegVerse-Labs/Executive_Rhetoric_Ledger`

- provider research logs under `research-data/ai-economic-transparency/`
- workload/sensitivity calculation module
- contradiction-review record
- independent-review record
- companion paper manuscript

When this research reaches release/tag posture, verify whether pertinent results or methodology should propagate to:
- `StegVerse-Labs/Site`
- `GCAT-BCAT-Engine/Publisher`
- `StegVerse-Labs/admissibility-wiki`
- `StegVerse-Labs/stegguardian-wiki`

No propagation is authorized yet.

## Completion accounting

Initial activation denominator: 10 capability groups.

1. authority/handoff
2. candidate/registry
3. methodology
4. schema
5. source/research queue
6. validator/fixtures
7. provider protocol evidence
8. scale-sensitivity calculations
9. contradiction/independent review
10. activation receipt

Current completion: 6/10 = 60%.

Developed files: 12.
Scaffolding/stubs counted as complete: 0.

Archive readiness: this handoff durably preserves the research goal, independence rule, two-axis methodology, elevated-usage scope, evidence boundaries, activation criteria, and remaining implementation. No chat-only definition is required to continue.
