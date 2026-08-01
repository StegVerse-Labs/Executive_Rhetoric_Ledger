# Silence-Causation Governance — Next Execution Session Prompt

Use the connected GitHub repository directly and continue the governed silence-causation capability in:

- Organization: `StegVerse-Labs`
- Repository: `StegVerse-Labs/Executive_Rhetoric_Ledger`
- Active branch: `feature/silence-causation-governance`
- Active pull request: `#46`

Do not rely on prior chat claims as proof. Repository state, preserved primary evidence, workflow results, and committed receipts are authoritative.

## Required reading order

Before making any decision or mutation, read these files in full and in this order:

1. `ERL_MIRROR_HANDOFF.md`
2. `docs/SILENCE_CAUSATION_NEXT_SESSION_PROMPT.md`
3. `standards/silence-causation-assessment-standard.md`
4. `assessments/silence-causation/2026-07-29-fauci-hsgac-source-capture-plan.md`
5. `schemas/silence-causation-assessment.schema.json`
6. `assessments/silence-causation/2026-07-29-fauci-hsgac.research-candidate.json`
7. `scripts/validate_silence_causation_assessment.py`
8. `.github/workflows/validate-silence-causation.yml`
9. Every newer or more specific applicable `*_MIRROR_HANDOFF.md` or `*_NEXT_SESSION_PROMPT.md`.

Then inspect PR `#46`, the latest branch commits, every workflow run attached to the current head, failed jobs, steps, complete logs, and every changed file.

## Latest directly verified state

- PR `#46` was open, mergeable, and non-draft.
- Verified pre-update branch head: `9b8a36bfa6e15565007cb95a55d4acb8832197e0`.
- Run `30593683918`, `Validate silence-causation assessments`, concluded `success`.
- Run `30593683913`, `Validate Ledger Schemas`, concluded `failure`.
- Failed job: `91041276028`, `validate-json-schemas`.
- Failed step: `Validate validation result receipts`.
- Complete logs show that `validation_results/ellis-scavino-transfer-assessment.pending.json`, introduced from newer `main` state into the PR merge test, does not conform to `schemas/validation-result.schema.json`. It uses parallel fields including `topic_id`, `recorded_at`, `status`, `validated_commit`, `validators_required`, `direct_execution_evidence`, `ci_evidence`, `structural_checks_completed`, and `unresolved`; the schema requires `validation_status`, `checked_commit`, `checked_paths`, `validator`, `result_summary`, and `activation_effect` and rejects additional properties.
- The incompatible file is not present on the silence-causation branch itself. Do not create a competing same-path branch file without first reading the Ellis–Scavino handoff and preserving that task's evidence semantics.
- Handoff evidence update commit: `f9ee03d66dd3d840122707dd0eb4ed1aef183052`.
- This prompt update commit must be inspected from repository state before use as proof.

## Immediate blocking sequence

1. Read the applicable Ellis–Scavino task handoff and schema/validator authority governing `validation_results/ellis-scavino-transfer-assessment.pending.json`.
2. Convert that receipt to the canonical validation-result schema without discarding its unresolved items or falsely claiming validator success; use `notes` and `result_summary` to preserve bounded detail where the schema provides no dedicated field.
3. Preserve the correction in the authorized task scope, then inspect the new PR merge-head runs.
4. Do not claim repository-wide CI success until both `Validate silence-causation assessments` and `Validate Ledger Schemas` are green on the same effective head.

## Governing analytical boundary

Silence, refusal, privilege, memory failure, and invocation of constitutional rights are observable response states, not admissions.

The system may narrow plausible causal or exposure hypotheses only through preserved evidence and controlled comparison. Political proximity, hostility, pressure, or institutional interest may justify preserving a hypothesis but may not be treated as proof of coercion, coordination, concealed guilt, or motive.

Every conclusion must distinguish observed fact, sourced proposition, inference, hypothesis, missing discriminating evidence, disconfirming condition, and publication boundary.

## Primary objective

Advance the capability from framework status toward an executable, source-custodied, question-level assessment of Anthony Fauci's July 29, 2026 HSGAC appearance.

## Required execution sequence after CI repair

1. Capture the official committee hearing page, official video, official transcript when available, exhibits, witness correspondence, process records, relevant pardon instrument, cited prior testimony, and relevant official communications. Prefer government and primary sources.
2. For each object preserve source authority, retrieval timestamp, canonical locator, media type, byte length where available, SHA-256 where bytes can be captured, completeness, custody path or immutable pointer, and transformation history.
3. Create an atomic question ledger preserving exact question-turn wording and timestamps, parent turns, embedded premises, requested facts, people, organizations, dates, documents, response text, counsel intervention, refusal basis, response class, and evidence references.
4. Distinguish complete refusal, partial answer, qualified answer, memory limitation, privilege assertion, constitutional invocation, procedural objection, nonresponsive answer, and interrupted or withdrawn question.
5. Construct a normalized chronology and participant/authority graph separating formal decision, advisory, funding, scientific-review, communications, records-custody, reporting, shared-representation, political-affiliation, alleged informal-pressure, and documented intermediary edges. Do not infer informal pressure from proximity alone.
6. Run answered/refused, harmless/exposure-bearing, topic, document, sequence, questioner, administration-era, non-administration, blanket-counsel, malformed/compound, argumentative, privilege-sensitive, memory, and record-access controls before ranking hypotheses.
7. Preserve and test H1 personal legal exposure; H2 contradiction with prior testimony or public representation; H3 protection of another participant; H4 institutional liability or narrative containment; H5 political pressure or coercion; H6 blanket counsel strategy; H7 defective/ambiguous/compound/hostile framing; H8 privilege/confidentiality/classification/records restriction; H9 genuine memory limitation.
8. No political-pressure or coercion hypothesis may receive an affirmative evidentiary score without a sourced communication, instruction, threat, offered benefit, intermediary edge, independently corroborated pressure channel, or equivalent direct or strongly reconstructable evidence identifying actor, channel, timing, and nature.
9. Preserve non-findings exactly. Keep the case at `research_candidate` or `not_assessable` wherever evidence does not authorize a stronger classification. Absence of explanation is not proof of concealment, and Fifth Amendment invocation is not proof an allegation is true.

## Required artifacts

Create or complete according to repository conventions:

- source-receipt manifest;
- machine-readable atomic question ledger;
- human-readable question-ledger review;
- normalized chronology;
- participant and authority graph;
- prior-testimony and documentary-conflict map;
- control-comparison report;
- updated silence-causation assessment;
- contradiction-review records;
- independent-review records;
- positive, negative, and indeterminate validator tests and fixtures.

Use existing registries, indexes, schemas, naming conventions, and validators. Do not create parallel formats without inspecting repository authority files.

## Continuity and publication boundary

Update `ERL_MIRROR_HANDOFF.md` and this prompt whenever execution state materially changes, preserving exact commits, run IDs, job and step conclusions, source hashes, custody state, completed artifacts, blockers, and next actions.

Do not publish a motive determination merely because one hypothesis ranks above another. Publication requires primary evidence capture, reproducible scoring, contradiction review, independent review, explicit uncertainty, and separation of fact from inference.

When release posture is reached, inspect destination handoffs before any mutation in `StegVerse-Labs/Site`, `GCAT-BCAT-Engine/Publisher`, `admissibility-wiki`, or `stegguardian-wiki`.

## Completion condition

The activation goal is complete when an independent reviewer can reconstruct every atomic question and response from preserved primary records; reproduce chronology, authority edges, controls, and hypothesis scores; distinguish observed silence from inferred motive; identify evidence that would change the result; and obtain the same bounded classification from the validator.

Continue autonomously within repository authority. Do not ask for confirmation where a reversible, evidence-preserving action is authorized. Stop only at a genuine external dependency, unavailable authority, or unresolved high-impact ambiguity, and record the blocker precisely in the handoff.
