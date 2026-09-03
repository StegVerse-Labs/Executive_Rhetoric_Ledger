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
- provider protocol execution: PARTIAL COMPLETE — exhausted consumer surfaces finalized for OpenAI, Anthropic, and DeepSeek; API/enterprise and remaining provider surfaces continue separately
- scale-sensitivity calculation engine: INSTALLED; OpenAI/Anthropic/DeepSeek consumer surfaces now carry reproducible UNBOUNDED_UNKNOWN 1K/100K/1M scenarios; exact/bounded API/enterprise calculations remain evidence-dependent
- contradiction review execution: PARTIAL COMPLETE — exhausted OpenAI/Anthropic/DeepSeek consumer-surface findings reviewed with no material cross-surface contradiction; broader comparison review remains pending
- independent review execution: PENDING; schema/template installed
- activation: NOT CLAIMED
- publication: NOT AUTHORIZED

## Remaining files/modules to install

Destination: `StegVerse-Labs/Executive_Rhetoric_Ledger`


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

Current completion: 8/10 = 80%.

Developed files: 31.
Scaffolding/stubs counted as complete: 0.

Archive readiness: this handoff durably preserves the research goal, independence rule, two-axis methodology, elevated-usage scope, evidence boundaries, activation criteria, and remaining implementation. No chat-only definition is required to continue.


## 2026-09-03 machine-execution advancement — public pricing/usage discovery and scale engine

Issue: #95

Installed:
- `scripts/calculate_ai_cost_scale_sensitivity.py`
- `tests/test_ai_cost_scale_sensitivity.py`
- `schemas/ai-economic-transparency-research-log.schema.json`
- `research-data/ai-economic-transparency/provider-research-log.template.json`
- provider research logs for OpenAI, Anthropic, DeepSeek, Z.ai, and Perplexity
- dedicated validation workflow coverage for the new calculator/log surfaces

The scale engine supports exact request cost, bounded request-cost intervals, and explicit `UNBOUNDED_UNKNOWN`. It projects supported evidence to 1K, 100K, and 1M equivalent requests without converting unknown cost into a numeric estimate.

Independent public-source discovery has begun for all five initial providers. No final disclosure-burden score has been assigned because no provider protocol has yet satisfied its complete evidence boundary.

Research-progress posture:
- OpenAI: official API documentation exposes per-response token usage; public model documentation exposes multiple cost modifiers. Authentic SV-RECON request usage remains unobserved.
- Anthropic: official API documentation exposes per-response token usage and multiple token/tool/cache pricing components. Authentic SV-RECON request usage remains unobserved.
- DeepSeek: official API documentation exposes returned token usage and peak/off-peak plus cache-hit/cache-miss rates. The preserved consumer observation still lacks exact model identity.
- Z.ai: public API platform surface exposes usage-bundle/billing entry points, but the inspected public surface has not yet yielded a request-level GLM-5.3-Flash pricing/usage basis sufficient for exact reconstruction.
- Perplexity: official Agent API documentation defines a per-response cost object including total cost and component costs. Authentic SV-RECON Agent API execution remains unobserved.

These are research-progress observations, not provider rankings or final transparency findings.


## 2026-09-03 review/paper execution surfaces

Issue: #97

Evidence-independent review and publication-preparation machinery is now installed:
- contradiction-review schema and pending template;
- independent-review schema and pending template;
- machine-readable review state;
- companion paper manuscript with complete scope, independence boundary, methodology, evidence hierarchy, claims discipline, scale equations, limitations, and publication gate.

The paper deliberately leaves Results, Contradiction Review, and Independent Review pending. Installing these surfaces does not satisfy capability group 9 and does not authorize activation or publication.

At this point the remaining substantive machine work is evidence-dependent:
1. complete at least one provider disclosure protocol from authentic request-level evidence or a governed exhausted-surface determination;
2. generate exact or bounded elevated-usage calculations from that evidence;
3. execute contradiction review;
4. execute independent review;
5. emit activation receipt only if all gates pass.


## Hosted validation receipts — 2026-09-03

Provider-research / scale-engine branch head `1a93b885255da9f94d4eeb388785538aa86e61c6`:
- Validate AI economic transparency: run `33766240838` — SUCCESS
- Validate durable task state: run `33766240840` — SUCCESS
- Validate Ledger Schemas: run `33766240914` — SUCCESS

Review/paper branch head `aabd1899d6521dc8c0d63ba0408b3378fea0d644`:
- Validate AI economic transparency: run `33766432985` — SUCCESS
- Validate durable task state: run `33766432923` — SUCCESS
- Validate Ledger Schemas: run `33766432976` — observed IN_PROGRESS at receipt capture; no success claim is made from that run.

These hosted validations prove the checked source/validation surfaces only. They do not satisfy provider empirical protocols, contradiction review, independent review, activation, or publication.


## 2026-09-03 prior-process reconciliation — exhausted consumer surfaces

Issue: #100

The earlier canonical SV-COST cost-evidence process was re-read before continuing this lane.

Prior authority:
`GCAT-BCAT-Engine/workflows/experiments/sv-cost-program/nine-lane-results/cost-evidence-request.json`

That record already established:
- OpenAI consumer/plan and aggregate-usage searches did not expose request-attributable SV-RECON-001 cost or exact request usage;
- Anthropic consumer plan/session/credit observations did not provide a request-attributable delta;
- DeepSeek remained blocked on admissible request-bound cost evidence;
- the explicit next-action rule was: **do not repeat already-exhausted plan/aggregate searches unless the UI gains request-level identity, per-message cost, exact tokens, or before/after usage deltas.**

The user has confirmed the same provider surfaces have not materially changed. ERL therefore treats the consumer/non-account-attributed discovery phase as historical completed evidence for OpenAI, Anthropic, and DeepSeek rather than pending user work.

The 2026-09-03 Z.ai/GLM observation likewise exposes no numeric request-attributable usage or cost on the observed hosted consumer surface. The supplemental Perplexity consumer result likewise exposes neither model/version identity nor request-attributable cost/usage. These current observations do not justify repeat consumer capture absent a material surface change.

### Surface-separation rule

Consumer/non-account-attributed product surfaces and API/enterprise billing surfaces are separate research objects.

An API that exposes exact usage or direct cost does **not** erase an opaque consumer surface. Conversely, consumer-surface opacity does not prove the API surface is opaque.

Final reporting must therefore preserve surface-specific findings rather than collapse them into one provider-wide transparency score.

### User-action rule

No repeat provider UI capture is required from the user for the already-exhausted surfaces. Re-opening capture is authorized only when:
- a provider visibly changes the relevant UI;
- a new request-attributable cost/usage field appears;
- exact per-message tokens become exposed;
- a before/after usage delta becomes attributable to one request; or
- a materially different provider surface is intentionally added to the study.

This supersedes any current task wording that implied the user should repeat the same consumer-surface process.


## 2026-09-03 exhausted consumer-surface finalization

Issue: #102

ERL now emits surface-specific final observations for the historically exhausted consumer/non-account-attributed surfaces of OpenAI, Anthropic, and DeepSeek.

Each observation:
- is explicitly scoped `SURFACE_SPECIFIC`, never provider-wide;
- records the governed discovery protocol as complete for that consumer surface;
- assigns `ACTUAL_COST_DISCLOSURE_BURDEN = 5 / NON_RECONSTRUCTABLE` only for that exhausted surface;
- preserves literal request cost as unknown;
- emits 1K, 100K, and 1M `UNBOUNDED_UNKNOWN` scale scenarios rather than numerical estimates;
- keeps independent review pending;
- authorizes no activation or publication.

The observation schema and validator now require `surface_class` and `rating_scope`, and the validator rejects `PROVIDER_WIDE` ratings.

A contradiction review was executed for these three finalized surface findings. Official API documentation showing request usage or pricing on distinct API/enterprise surfaces was tested as counterevidence and classified as `NONE` because it concerns a different research surface. No provider-wide conclusion is promoted.

Activation capability groups now satisfied:
- group 7 provider protocol evidence: satisfied by multiple completed consumer-surface protocols;
- group 8 reproducible elevated-usage scale calculation: satisfied for those surfaces through deterministic `UNBOUNDED_UNKNOWN` propagation.

Group 9 remains incomplete because independent review is still pending. Group 10 activation receipt remains blocked on group 9 and final validation.


## 2026-09-03 independent-review package

Issue: #104

A bounded independent-review package is now installed for the finalized OpenAI, Anthropic, and DeepSeek consumer/non-account-attributed findings:

`assessments/reviews/ai-economic-transparency-consumer-surface-independent-review-package.2026-09-03.json`

The package fixes the review scope, required inputs, review questions, forbidden promotions, and required terminal output schema/path. It prevents the independent-review step from expanding into provider-wide ranking, intent claims, Z.ai/Perplexity findings, activation, or publication.

This package makes the remaining review gate machine-addressable, but it is not itself an independent review and does not satisfy capability group 9.


## 2026-09-03 candidate-results integration

Issue: #106

The finalized OpenAI, Anthropic, and DeepSeek consumer-surface observations are now integrated into a machine-readable candidate-results summary:

`research-data/ai-economic-transparency/candidate-results.consumer-surfaces.2026-09-03.json`

The companion manuscript now includes these candidate results while preserving:
- surface-specific scope;
- rating 5 / NON_RECONSTRUCTABLE only for the exhausted consumer surface;
- unresolved literal request cost;
- `UNBOUNDED_UNKNOWN` at 1K / 100K / 1M;
- separate API/enterprise surfaces;
- no provider-wide ranking;
- independent-review pending status.

The previously observed PR #105 validation state is now fully resolved:
- Validate AI economic transparency run `33772683787` — SUCCESS
- Validate durable task state run `33772683638` — SUCCESS
- Validate Ledger Schemas run `33772683540` — SUCCESS

These validation receipts prove source/schema/task consistency only. They do not satisfy independent review or activation.


## 2026-09-03 API/enterprise surface materialization

Issue: #108

Surface-specific API/enterprise observations are now materialized for all five initial providers:
- OpenAI
- Anthropic
- DeepSeek
- Z.ai / GLM
- supplemental Perplexity

These records convert the already-preserved official-document research into machine-readable `API_ENTERPRISE` observations without assigning final scores.

Current boundaries:
- OpenAI: official API usage and pricing behavior documented; authentic bounded SV-RECON-001 API receipt remains unobserved.
- Anthropic: official API usage and pricing behavior documented; authentic bounded SV-RECON-001 API receipt remains unobserved.
- DeepSeek: official API usage and pricing behavior documented; exact comparison-model binding and authentic bounded API receipt remain unobserved.
- Z.ai: preserved public platform material remains insufficient to reconstruct a request-level GLM-5.3-Flash cost basis.
- Perplexity: official Agent API documentation specifies a direct per-response cost object, but no authentic bounded SV-RECON-001 Agent API receipt has been observed.

All five API/enterprise protocols therefore remain `protocol_complete=false` with no final disclosure-burden rating. Their scale state remains `UNBOUNDED_UNKNOWN` until authentic exact/bounded request evidence exists.

No consumer recapture was performed or reopened. API/enterprise observations remain separate from finalized consumer-surface findings.


## 2026-09-03 machine-owned independent reviewer binding

Issue: #110

A separate resident reviewer executor is now released in the canonical organization worker plane:

- implementation issue: `StegVerse-Labs/.github#927`
- implementation PR: `StegVerse-Labs/.github#929`
- released commit: `66b5d942f7ba7f1e9c4fe3b6a3f4616b15c72ee5`
- worker task: `SHWP-ERL-AI-ECON-TRANSPARENCY-REVIEW-001`
- worker: `StegVerse-Labs/.github/workers/erl_ai_economic_transparency_review_worker.py`
- handoff: `StegVerse-Labs/.github/handoffs/SHWP-ERL-AI-ECON-TRANSPARENCY-REVIEW-001.json`
- registry: `StegVerse-Labs/.github/control/worker-registry.d/erl-ai-economic-transparency-review-001.json`
- adapter: `StegVerse-Labs/.github/control/process-worker-adapters.d/erl-ai-economic-transparency-review-001.json`
- runtime authority: recommendation receipt only
- research-promotion authority: false
- activation authority: false
- publication authority: false
- repository-writeback authority: false
- GitHub token runtime authority: NONE

The worker independently reconstructs the fixed OpenAI/Anthropic/DeepSeek consumer-surface review package from already-materialized local ERL source and emits a bounded `APPROVE` or `REVISE` recommendation receipt.

This transfer changes the review gate from **UNOWNED/WAITING_FOR_REVIEWER** to **MACHINE_OWNED_PENDING_RUNTIME_RECEIPT**.

It does **not** satisfy independent review yet. Source merge, registry presence, worker availability, handoff readiness, CI, or heartbeat progression do not count as a completed review.

The independent-review gate is satisfied only when an authentic fenced resident execution emits:
`receipts/erl-ai-economic-transparency-review/SHWP-ERL-AI-ECON-TRANSPARENCY-REVIEW-001.json`

and that receipt is admitted into ERL's review record without widening the worker's authority.

No user/device action is required.


## 2026-09-03 independent-review worker control-plane reconciliation

Issue: #112

The machine-owned independent reviewer remains the canonical execution owner for capability group 9. Its organization-plane integration has now been reconciled beyond the initial implementation merge:

- initial worker release: `66b5d942f7ba7f1e9c4fe3b6a3f4616b15c72ee5`
- Admissible-Existence repair: `0f4214b13373741124ef79dd37774b0585f0721b`
- COSV denominator/index repair: `ddebfc0aa31a58c4b41e02fc871d254af1813133`
- reconciliation documentation merge: `365c983d3c276f204a5d9ef3c3df4dac9c00d0da`

Current organization-plane source/control state:
- worker task: `SHWP-ERL-AI-ECON-TRANSPARENCY-REVIEW-001`
- AE phase: `ADMISSIBLE`
- COSV vector: `50000000101000`
- runtime receipt observed: false
- independent review complete: false
- research-promotion authority: false
- activation authority: false
- publication authority: false
- repository-writeback authority: false

No runtime conclusion is inferred from these repository mutations. Capability group 9 remains pending an authentic fenced resident review receipt.


## 2026-09-03 self-contained resident review package binding

Issue: #114

The canonical resident independent-review worker has been advanced beyond the prior cross-repository materialization dependency.

Organization-plane source:
- PR: `StegVerse-Labs/.github#947`
- merge: `ed63987fb10cf034de0ee140234147a73f744cdf`
- bundled review manifest: `review-packages/erl-ai-economic-transparency-001/manifest.json`

The package contains byte-preserving copies of the fixed ERL review inputs and binds each file by source Git blob identity and SHA-256. The worker verifies the SHA-256 manifest before accepting the bundled package.

The worker still permits an independently materialized canonical ERL source tree as fallback, but the normal path no longer requires local cross-repository materialization or network checkout.

The remaining independent-review blocker is now strictly:
`RESIDENT_EXECUTION_RECEIPT_PENDING`

Required runtime evidence remains:
`receipts/erl-ai-economic-transparency-review/SHWP-ERL-AI-ECON-TRANSPARENCY-REVIEW-001.json`

No review completion, activation, publication, or provider-wide finding is inferred from the bundled source package.


## 2026-09-03 resident independent-review dispatch binding

Issue: #116

The canonical organization-plane reviewer is now wired into the existing resident request-dispatch path:

- organization implementation issue: `StegVerse-Labs/.github#949`
- implementation PR: `StegVerse-Labs/.github#950`
- merge: `c9033ce3cd336646d7f7c27c80dfd580fd976153`
- request: `control/resident-execution-request.d/erl-ai-economic-transparency-review-001.json`
- consumer: `scripts/consume_erl_ai_economic_transparency_review_request.py`
- generic dispatcher selector: `erl_ai_economic_transparency_review`
- resident review package: `review-packages/erl-ai-economic-transparency-001/manifest.json`

The existing local source-refresh path now copies `review-packages/` and the request consumer into resident runtime. The existing rootless source-refresh watcher also observes the review-package path. This adds no second scheduler, heartbeat, claim source, fence source, credential path, or authority plane.

The dedicated request is intent-only and asks the already-admitted WorkerCoordinator to attempt:
`SHWP-ERL-AI-ECON-TRANSPARENCY-REVIEW-001`
through the existing targeted task execution path.

Observed source/control validations for PR #950:
- Heartbeat Worker Project validation run `33784116021`: SUCCESS
- Cross-Framework Current-Basis Resident Request validation run `33784113544`: SUCCESS
- Workspace DEVICE_KV validation run `33784113905`: SUCCESS
- organization control-plane validation run `33784113903`: SUCCESS

Those validations are non-authorizing and are not runtime evidence.

Current review state:
`MACHINE_OWNED_SELF_CONTAINED_RESIDENT_DISPATCH_READY_PENDING_RUNTIME_RECEIPT`

The authentic review receipt remains unobserved:
`receipts/erl-ai-economic-transparency-review/SHWP-ERL-AI-ECON-TRANSPARENCY-REVIEW-001.json`

Therefore independent review, activation, and publication remain unclaimed.


## 2026-09-03 final resident-dispatch validation receipts

Issue: #118

PR #117 / head `39a74b7227ca8d9478324d85b3989a3cfe0d73c2` completed all observed ERL validation surfaces successfully:

- Validate AI economic transparency: run `33784383315` — SUCCESS
- Validate durable task state: run `33784383397` — SUCCESS
- Validate Ledger Schemas: run `33784383350` — SUCCESS

These receipts establish source/schema/task-state consistency for the resident-review dispatch integration only. They do not establish that the resident reviewer executed.

The authentic runtime receipt remains absent:
`receipts/erl-ai-economic-transparency-review/SHWP-ERL-AI-ECON-TRANSPARENCY-REVIEW-001.json`

No independent-review completion, activation, or publication is inferred.
