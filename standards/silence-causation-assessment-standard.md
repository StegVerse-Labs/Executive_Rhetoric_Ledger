# Silence-Causation Assessment Standard

## Purpose

This standard governs analysis of testimony, interviews, depositions, oversight appearances, or other proceedings where a person refuses, declines, cannot recall, invokes privilege, invokes a constitutional protection, or answers selectively.

It is designed to answer a bounded question:

> Given the exact question set, observed response pattern, event record, participant graph, prior statements, and available documents, which explanations for silence remain plausible, which are contradicted, and what evidence would discriminate among them?

## Non-admission rule

A refusal is not an admission. A Fifth Amendment invocation is not proof that the premise of a question is true. No assessment may infer guilt, coordination, coercion, deception, or protection of another person solely from silence.

## Required layers

### 1. Proceeding record

Record the proceeding authority, date, venue, witness, oath status, subpoena or invitation posture, counsel presence, and source custody.

### 2. Atomic question ledger

Each compound question must be decomposed into atomic propositions. Every question record must contain:

- exact wording or a source-linked transcription;
- questioner;
- timestamp or transcript location;
- referenced person, event, document, date, and prior statement;
- response class;
- response text;
- stated refusal basis;
- source receipt.

### 3. Response classes

Allowed response classes:

- `substantive_answer`
- `partial_answer`
- `fifth_amendment`
- `other_privilege`
- `cannot_recall`
- `declined`
- `counsel_intervention`
- `procedural_objection`
- `question_withdrawn`
- `inaudible_or_unresolved`

### 4. Event chronology

Separate physical event time, knowledge time, communication time, decision time, statement time, publication time, testimony time, and later analysis time. Unknown dimensions remain unknown.

### 5. Participant and authority graph

Map role-specific edges, including formal supervision, advisory authority, funding authority, records custody, legal representation, political appointment, communications control, investigatory authority, prosecutorial authority, and documented private contact.

An authority edge does not establish influence over the refusal decision.

### 6. Conflict and exposure mapping

For each atomic question, identify whether each possible answer class could:

- conflict with a preserved document;
- conflict with prior sworn testimony;
- expose post-pardon or post-immunity conduct;
- implicate another actor;
- reveal institutional decision authority;
- create civil, criminal, administrative, political, or reputational exposure;
- waive privilege or create selective-disclosure consequences;
- remain harmless under the known record.

### 7. Hypothesis register

Default hypothesis classes:

- `personal_legal_exposure`
- `prior_statement_conflict`
- `protection_of_other_actor`
- `institutional_liability_or_reputation`
- `blanket_counsel_strategy`
- `political_pressure_or_coercion`
- `question_defect_or_hostile_premise`
- `privilege_security_or_confidentiality`
- `memory_or_record_limit`
- `other_bounded_hypothesis`

Every hypothesis requires supporting evidence, contrary evidence, assumptions, and a discriminating-evidence request.

### 8. Controls

At minimum, compare:

- answered versus refused questions;
- harmless versus exposure-bearing questions;
- questions inside versus outside the pardon or immunity period;
- questions with versus without documentary predicates;
- questions naming different actors or administrations;
- repeated questions phrased differently;
- blanket invocation patterns versus selective invocation patterns.

### 9. Scoring

Scores are analytic aids, not probabilities of guilt.

Each hypothesis receives integer values from 0 to 4 for:

- `evidence_support`
- `pattern_fit`
- `document_conflict_fit`
- `authority_network_fit`
- `alternative_explanation_penalty`
- `missing_evidence_penalty`

The bounded score is:

`support + pattern + document + authority - alternative penalty - missing evidence penalty`

The score must not be converted into a percentage probability unless a separately validated statistical model exists.

### 10. Classification

Allowed classifications:

- `not_assessable`
- `plausible_but_unranked`
- `ranked_bounded_hypotheses`
- `single_hypothesis_materially_preferred`
- `hypothesis_contradicted`

`single_hypothesis_materially_preferred` requires complete primary question capture, adequate controls, at least one discriminating item of evidence, contradiction review, and independent review.

## Anti-misuse constraints

The assessment must not:

- describe silence as confession;
- infer private advice or coercion without evidence;
- treat a reporting relationship as proof of direction;
- collapse legal, political, reputational, and institutional exposure;
- score a named person as responsible for pressure without a sourced interaction edge;
- omit harmless-question controls;
- publish a final motive determination from an incomplete transcript.

## Initial Fauci test posture

The July 29, 2026 HSGAC appearance is initially classified `not_assessable` at the question-causation level because the repository does not yet contain a complete, source-custodied atomic question ledger. Publicly established facts may be recorded, but motive hypotheses remain bounded and unranked until primary capture is complete.

## Done criteria

A silence-causation assessment is complete only when:

1. the complete proceeding is preserved or bounded omissions are documented;
2. questions are atomic and source-linked;
3. responses are classified reproducibly;
4. chronology and actor edges are sourced;
5. prior statements and documentary predicates are linked;
6. controls are populated;
7. hypotheses include support, contradiction, assumptions, and discriminators;
8. the schema validates;
9. contradiction review is complete;
10. independent review is recorded.
