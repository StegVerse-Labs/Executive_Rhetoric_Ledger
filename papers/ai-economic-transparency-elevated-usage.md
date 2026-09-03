# Literal AI Cost Transparency at Elevated Usage

Status: research manuscript — methods complete, empirical results pending
Research program: ERL-AI-ECON-TRANSPARENCY-001
Repository: StegVerse-Labs/Executive_Rhetoric_Ledger

## Abstract

This study evaluates whether the literal economic consequence of AI inference is directly observable or independently reconstructable, how much research effort is required to obtain that information, and how unresolved cost uncertainty compounds at elevated usage. The study is designed for enterprise, agentic, batch, automated, procurement, and other materially scaled workloads rather than casual low-volume use.

Empirical provider rankings and comparative conclusions are intentionally withheld until provider disclosure protocols, scale calculations, contradiction review, and independent review are complete.

## Research questions

1. Can a reasonable evaluator determine the literal request-attributable cost of an AI inference?
2. How much navigation, documentation research, privilege escalation, or support interaction is required?
3. Which material cost determinants are absent from the initially advertised pricing surface?
4. Is exact request usage exposed?
5. Is the actual cost directly reported, exactly reconstructable, bounded, or unresolved?
6. How does cost uncertainty change at 1,000, 100,000, and 1,000,000 equivalent requests?
7. Does provider selection change when transparency burden and cost uncertainty are considered alongside nominal rate cards?

## Scope

The study focuses on operationally material usage levels. It does not assume that the same transparency burden has equal consequence for casual use.

Initial providers:
- OpenAI
- Anthropic
- DeepSeek
- Z.ai / GLM Hosted
- Perplexity as a supplemental comparator

Additional providers may be admitted only under the same methodology.

## Independence

Upstream SV-COST artifacts may be admitted as evidence inputs. ERL independently reconstructs pricing, usage, cost determinants, disclosure burden, and scale sensitivity. No upstream conclusion is inherited.

## Metric 1 — ACTUAL_COST_DISCLOSURE_BURDEN

0 DIRECT
1 ONE_STEP_DERIVABLE
2 MULTI_SOURCE_DERIVABLE
3 ACCOUNT_GATED
4 SUPPORT_OR_EXTERNAL_RESEARCH_REQUIRED
5 NON_RECONSTRUCTABLE

A score of 5 requires completion of the governed discovery protocol. Initial opacity alone is insufficient.

## Metric 2 — COST_SCALE_SENSITIVITY

Exact cost:
known_total_cost = exact_request_cost × equivalent_request_count

Bounded cost:
lower_total = lower_request_bound × equivalent_request_count
upper_total = upper_request_bound × equivalent_request_count

Unknown cost:
UNBOUNDED_UNKNOWN remains unknown at every scale. The study does not manufacture a numeric estimate.

## Provider protocol

For each provider:
1. preserve model/version identity where exposed;
2. preserve a bounded inference observation;
3. inspect the immediate request/result surface;
4. inspect official pricing documentation;
5. inspect official usage/billing/account surfaces available to the evaluator;
6. record every additional discovery step;
7. enumerate all material cost rules;
8. attempt exact request-cost reconstruction;
9. measure discovery steps and elapsed research time;
10. classify disclosure burden only after protocol completion;
11. calculate elevated-usage consequences from exact or bounded evidence only;
12. conduct contradiction review;
13. conduct independent review.

## Evidence hierarchy

Highest-value evidence includes:
- direct request receipts containing literal cost;
- direct request receipts containing exact usage plus complete, version-bound provider pricing;
- official billing/usage records attributable to one request;
- official provider pricing and billing rules;
- preserved provider UI observations.

Secondary sources may locate evidence but do not substitute for decisive provider-controlled or direct transactional evidence when those are required.

## Claims discipline

A published rate card is not treated as literal request-cost evidence by itself.

Unknown cost is not treated as zero or as high.

Opacity does not establish intent.

A misleading or deceptive-effect finding requires evidence that presented or omitted material cost information creates a materially inaccurate representation of economic consequence.

Intent-based findings require separate evidence.

## Elevated-usage interpretation

The economic relevance of small unit-cost differences increases with repeated use. The study therefore reports standardized workload scenarios rather than treating one consumer prompt as the principal decision environment.

Comparative results will distinguish:
- exact cost;
- bounded cost;
- unresolved exposure;
- discovery burden;
- privilege/account barriers;
- pricing-rule complexity;
- sensitivity to caching, tools, context, time, routing, or other documented modifiers.

## Results

Pending provider protocol completion.

No ranking is authorized at this stage.

## Contradiction review

Pending.

## Independent review

Pending.

## Limitations

The study distinguishes consumer product surfaces from API/enterprise surfaces where their billing models differ. A provider may be transparent in one channel and opaque in another. Results must therefore remain surface-specific.

Pricing can change over time. Every final result must preserve observation date and pricing-document version or retrieval date.

The study cannot infer undisclosed costs merely from the existence of unresolved variables.

## Publication gate

Publication requires:
- completed provider protocols for the compared set;
- validator-clean observations;
- reproducible scale calculations;
- contradiction review;
- independent review;
- explicit ERL activation/publication decision.
