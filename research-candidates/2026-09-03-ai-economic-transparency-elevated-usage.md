# AI economic transparency at elevated usage — research candidate

Date: 2026-09-03
Status: `research_candidate`
Goal: `ERL-AI-ECON-TRANSPARENCY-001`
Owner: Issue #93
Bounded handoff: `docs/AI_ECONOMIC_TRANSPARENCY_MIRROR_HANDOFF.md`
Activation authorized: `false`
Publication authorized: `false`

## Candidate proposition

AI providers differ materially in how much effort is required to discover or exactly reconstruct the literal economic cost of inference, and that disclosure burden becomes increasingly consequential as workload volume rises.

## Study population

Primary intended comparison population:
- enterprise inference;
- agentic workloads;
- batch inference;
- high-frequency automated use;
- public-sector procurement;
- other usage where small unit-cost variance compounds materially.

Casual consumer usage is not the principal decision context for this research.

## Research questions

1. Can an evaluator determine the literal request-attributable cost of one inference?
2. How many research/navigation steps and how much elapsed effort are required?
3. Which material pricing components are visible on the initial price surface, and which appear only elsewhere?
4. Does exact reconstruction require account, billing, administrative, support, or external-research access?
5. How does unresolved cost variance scale at 1K, 100K, and 1M equivalent requests?
6. Does provider ranking change when disclosure burden and scale sensitivity are considered alongside raw unit pricing?

## Required controls

- preserve identical or normalized workload definitions;
- do not equate advertised unit rates to literal request cost;
- do not assign zero cost to unknown components;
- do not infer provider intent from opacity;
- preserve provider/model version uncertainty;
- preserve subscription and API economics as separate surfaces where applicable;
- independently reconstruct findings in ERL rather than importing SV-COST conclusions.

## Initial evidence seed

SV-COST provider observations may be used as upstream evidence candidates:
- OpenAI
- Anthropic
- DeepSeek
- Z.ai / GLM Hosted
- Perplexity supplemental comparator

These inputs establish only what the supplied observation surfaces actually showed. They do not establish final ERL transparency scores.

## Promotion boundary

Promotion requires machine-valid provider observations, completed discovery protocols, scale-sensitivity calculations, contradiction review, and independent review.

No comparative ranking or deceptive-pricing finding is authorized at candidate stage.
