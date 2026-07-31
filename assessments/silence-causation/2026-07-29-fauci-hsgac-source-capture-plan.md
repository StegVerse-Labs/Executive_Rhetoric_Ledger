# Fauci HSGAC Silence-Causation Source-Capture Plan

## Case

- Assessment: `ERL-SCA-2026-07-29-FAUCI-HSGAC`
- Proceeding: Testimony of Anthony Fauci
- Date: 2026-07-29
- Governing assessment: `2026-07-29-fauci-hsgac.research-candidate.json`

## Purpose

Produce a source-custodied, question-level record sufficient to test bounded explanations for response and refusal patterns without treating invocation of the Fifth Amendment as an admission.

## Required primary objects

1. Official committee hearing page and all linked files.
2. Native official video or the highest-authority preserved stream available.
3. Official transcript, when published.
4. Committee exhibits, letters, subpoenas, notices, and witness correspondence.
5. Written opening statements from the chair, ranking member, witness, and counsel when available.
6. The applicable pardon instrument and authoritative scope record.
7. Prior sworn testimony and documentary records expressly referenced in questions.

## Custody record for each object

Every captured object must record:

- stable source identifier;
- issuing authority;
- canonical URL;
- retrieval timestamp in UTC;
- local repository path or immutable external custody pointer;
- media type and byte length;
- SHA-256 digest;
- capture agent or operator;
- completeness state;
- known omissions or transformations.

A streaming page, news account, or paraphrase does not substitute for the native proceeding record.

## Atomic question ledger procedure

For every speaking turn:

1. Assign a monotonically ordered turn identifier.
2. Preserve exact wording and timestamp.
3. Identify speaker and procedural role.
4. Separate preface, factual premise, accusation, and requested proposition.
5. Split compound questions into atomic propositions while preserving the parent turn.
6. Preserve the complete response and any counsel intervention.
7. Classify the response without inferring motive.
8. Link only explicitly implicated events, participants, documents, and prior statements.
9. Record whether the question is harmless, exposure-bearing, ambiguous, defective, or unresolved; this label remains reviewable.
10. Record transcript/video disagreement rather than silently choosing one.

## Required controls

### Answered versus refused

Compare all substantive answers, partial answers, invocations, memory claims, objections, and withdrawn questions. A selective-silence inference is prohibited until the full distribution exists.

### Harmless versus exposure-bearing

Test whether apparently low-risk identity, chronology, or procedural questions received the same response posture as questions containing legal or documentary predicates.

### Actor and administration

Compare questions involving Fauci personally, agency personnel, contractors, grantees, the first Trump administration, the Biden administration, Congress, and outside institutions.

### Topic and document

Compare origins, funding, research classification, records retention, communications, public statements, prior testimony, and post-pardon conduct.

### Sequence

Test whether response posture changes after exhibits, recesses, counsel consultations, warnings, or particular named participants enter the record.

## Hypothesis discrimination requirements

The ledger must seek evidence capable of separating at least:

- blanket counsel strategy;
- personal legal exposure;
- conflict with prior statements;
- protection of another actor;
- institutional liability or reputational containment;
- political pressure or coercion;
- defective or hostile question premises;
- privilege, security, or confidentiality restrictions;
- memory or record limitations.

Political-pressure or coercion claims require a documented communication, threat, benefit, intermediary, instruction, or independently corroborated pressure channel. Political proximity alone is insufficient.

## Advancement gates

The assessment remains `research_candidate` and `not_assessable` until:

- primary proceeding capture is complete enough to reconstruct every relevant turn;
- the atomic ledger passes schema and governance validation;
- all cited participant and authority edges have traceable evidence posture;
- control comparisons are executed;
- contradiction review is complete;
- independent review is complete.

No score is a probability of guilt, motive, or concealed fact. Scores express bounded comparative support within the captured record only.
