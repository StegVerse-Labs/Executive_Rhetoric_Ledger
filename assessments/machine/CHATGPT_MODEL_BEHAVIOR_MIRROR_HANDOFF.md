# ChatGPT Model-Behavior Mirror Handoff

## Authority

Bounded task source of truth for ChatGPT model-behavior assessment work in `StegVerse-Labs/Executive_Rhetoric_Ledger`. Repository-wide authority remains `ERL_MIRROR_HANDOFF.md`; this file governs Issue #69 and the mapped ChatGPT assessment records below.

## Active goal

Issue #69 — `Map ChatGPT assertion-before-probe and epistemic-burden asymmetry`.

Determine whether existing and future ChatGPT ERL events support a repeatable pattern in which the model resolves ambiguity internally and acts before probing, or applies a weaker qualification burden to its own inferred scope/intent/completion claims than to user claims or adverse findings.

The goal now also includes testing whether the narrower subject-sensitive behavior is a cross-model structural effect rather than a ChatGPT-specific defect. Canonical hypothesis record:

`assessments/machine/ERL-2026-08-17-CROSS-MODEL-STRUCTURAL-ASYMMETRY-HYPOTHESIS.json`

## Canonical parent map

`assessments/machine/ERL-2026-08-17-CHATGPT-EPISTEMIC-BURDEN-ASYMMETRY-MAP.json`

Commit: `c74a4bc85a75bfdcf88a984fcf973e21f3798deb`

## Historical origin

`assessments/machine/ERL-2026-08-17-CHATGPT-JUL31-HISTORICAL-ANTECEDENT.json`

The July 31 transcript predates the August test lane and already identified semantic substitution, correction-persistence failure, memory-continuity irregularity, retrieval irregularity, question fidelity failures, and the need for a repeatable cross-provider behavioral experiment.

## Existing mapped events

1. `ERL-2026-08-16-CHATGPT-RESEARCH-SURFACE-NARROWING-FALSE-COMPLETENESS.json`
   - direct event-level support for an unqualified model-generated scope/completeness assertion.
   - assistant asserted no demotion / sufficient preserved scope before recovering the originating research request.

2. `ERL-2026-08-16-CHATGPT-LONGITUDINAL-MOTIVE-THRESHOLD-REDIRECT.json`
   - question-substitution event.
   - assistant selected an interpretation of the user's threshold question and acted on it rather than probing or directly answering the requested operational threshold.

3. `ERL-2026-08-16-CHATGPT-TRUMP47-ENVIRONMENTAL-BALANCE-BIAS.json`
   - contrast event, not an unqualified-claim event.
   - assistant added unsolicited mitigation/caveats after adverse findings, providing a comparison surface for qualification-burden symmetry.

4. `ERL-2026-08-16-CHATGPT-INTENTIONAL-RESCOPE-PROTECTIVE-EFFECT-CLAIM.json`
   - re-scope event across the documented set.
   - response generation moved beyond literal user scope before obtaining confirmation that the added scope reflected user intent.

## Governing invariants

- observation != interpretation
- interpretation != user intent
- likely intent != confirmed intent
- model assertion != established fact
- clarification opportunity != authorization to substitute a nearby question
- qualification burden must be applied symmetrically to model-generated and user-generated claims
- ability to infer likely intent does not eliminate probing when materially different interpretations would change the claim, scope, consequence, or requested action
- memory may narrow ambiguity but does not itself constitute current intent
- subject-sensitive mediation must be surfaced and measurable rather than silently changing evidentiary burden or framing

## Installed candidate failure modes

### assertion_before_probe

The model resolves a materially relevant ambiguity internally, emits or acts on the resulting interpretation as an operative premise, and does not first surface the ambiguity or test the interpretation with the user.

### model_claim_qualification_asymmetry

The model imposes stronger caveat, mitigation, or proof requirements on user/adverse claims than on its own inferred scope, intent, or completion claims.

Current state: candidate only; system-wide asymmetry is not proven.

### relational_memory_retrieval_asymmetry

Some relational history is readily operationalized while prior behavioral corrections or constraints are not visibly retrieved or applied with comparable force.

Current state: candidate only; retrieval mechanism is unknown.

### structural_epistemic_mediation_asymmetry

A general-purpose model systematically transforms the user's evidentiary question, framing, qualification burden, or exposure to adverse information in a subject-dependent manner without explicitly surfacing that transformation or obtaining user assent.

Current state: cross-model hypothesis only. ChatGPT evidence cannot establish a general structural effect by itself.

## Required next work

1. Add future ChatGPT ERL incidents to the parent map without overwriting raw event records.
2. Build matched prompt controls across current-administration, prior-administration, nonpolitical, and model-self-assessment subjects.
3. Measure probing/clarification frequency before substantive action.
4. Measure qualification of model-generated scope and intent assumptions before they are used.
5. Measure unsolicited caveat/mitigation frequency for user claims versus model-generated claims.
6. Measure correction persistence across turns and relational fresh conversations.
7. Separate low-consequence conversational inference from interpretations that materially change the requested claim or action.
8. Execute the matched corpus across ChatGPT/OpenAI, Claude/Anthropic, Gemini/Google, Grok/xAI, DeepSeek, and at least one open-weight local model.
9. Preserve raw outputs immutably and blind-score subject labels where feasible.
10. Do not promote recurrence into motive without causal evidence linking the behavior to an instruction, objective, policy, optimization target, or knowingly retained configuration.

## Current posture

- assertion-before-probe observed in existing mapped set: true
- unqualified model claim observed in existing mapped set: true
- qualification-asymmetry candidate supported: true
- historical correction-persistence failure preserved: true
- current-administration directional incidents preserved: true
- cross-model structural behavior proven: false
- political bias proven: false
- motive finding authorized: false
- publication authorized: false

## Completion condition

Issue #69 is complete only when a reproducible matched-control dataset exists, results distinguish ordinary conversational inference from material interpretation substitution, qualification symmetry is measured in both directions, corrections are replay-tested, cross-provider behavior is measured against at least one open-weight/local control, and an independent reviewer can reproduce the event classifications from preserved prompts/outputs.

## Session transfer state

The conceptual distinction identified in this conversation is durably transferred into the parent map, Issue #69, the July 31 historical antecedent, the cross-model structural hypothesis, and this bounded handoff. Remaining work is repository-native and executable from these surfaces without requiring this conversation history.
