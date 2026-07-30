# Iran–Jordan–FirstNet Executive Rhetoric Ledger Session Handoff

## Purpose

This handoff is the authoritative continuity document for the July 2026 Iran–Jordan–FirstNet escalation reconstruction in the Executive Rhetoric Ledger (ERL). A new session must review this file before making claims, modifying records, or extending the event graph.

## Current research objective

Reconstruct the relationship among:

1. Iranian ballistic-missile launches toward U.S. facilities in Jordan and later reported attacks involving Jordan and Kuwait;
2. rapid U.S. executive and CENTCOM rhetoric, including the phrase "attempted surprise attack";
3. delayed or separately indexed Jordanian public disclosures;
4. the activation of a broad, pre-existing U.S. strike architecture;
5. unexplained simultaneous degradation of an AT&T FirstNet line and Astound fixed broadband;
6. later regional expansion involving Kuwait, Damietta, Hormuz, Saudi–Iraq operations, and Houthi maritime pressure;
7. the distinction between physical event time, statement time, publication time, confirmation time, and later analysis time.

The end goal is a reconstructable, claim-level, source-custodied, independently reviewed ERL record that can determine which bounded findings are admissible without converting hypotheses into facts.

## Governing evidentiary posture

The assessment remains a research candidate. The following are not established findings:

- Iran compromised FirstNet or U.S. telecom infrastructure;
- the United States staged the network degradation;
- the United States induced or orchestrated the Iranian missile launch;
- Jordan was forced into political alignment;
- identical reports of five interceptions refer to the same launch event;
- Damietta was attacked by Iran or an Iranian proxy;
- the regional branches form one coordinated package;
- prior U.S. operational preparation proves prior knowledge or preauthorization.

Promotion requires primary-source capture, source custody, hashes, timestamp normalization, contradiction review, machine validation, and independent review.

## Completed work

The repository contains:

- `research-candidates/2026-07-28-iran-jordan-firstnet-escalation-rhetoric.md`
  - Parent narrative candidate and competing hypotheses H1–H6.
- `research-candidates/2026-07-30-iran-war-24h-qualified-addendum.md`
  - Correction separating newly occurred, newly announced, newly confirmed, unresolved-time, and older-context events.
- `assessments/pit/PIT-MODERN-2026-IRAN-JORDAN-FIRSTNET.assessment.json`
  - Machine-readable assessment, actors, observations, rhetorical transitions, prohibited collapses, and promotion requirements.
- `assessments/chronology/2026-07-28-30-iran-jordan-firstnet.normalized.json`
  - Chronology schema preserving source-local time, timezone, UTC normalization, precision, and event identity.
- `assessments/contradictions/2026-07-iran-jordan-firstnet.matrix.md`
  - Contradiction and non-equivalence controls.
- `assessments/intake/2026-07-iran-jordan-firstnet-primary-record-intake.json`
  - Primary-record acquisition targets.
- `assessments/source-posture/2026-07-iran-jordan-firstnet-initial-source-receipts.json`
  - Initial source posture and claim classifications.
- `assessments/receipts/2026-07-iran-jordan-firstnet.receipt-manifest.json`
  - Receipt slots, custody policy, hash requirements, and expanded regional branches.
- `assessments/reviews/PIT-MODERN-2026-IRAN-JORDAN-FIRSTNET.review.md`
  - Human-readable review boundary.
- `assessments/reviews/PIT-MODERN-2026-IRAN-JORDAN-FIRSTNET.independent-review.json`
  - Independent-review intake; currently unassigned and unsigned.
- `scripts/validate_iran_jordan_firstnet_assessment.py`
  - Structural validator preventing premature promotion and chronology precision violations.
- `.github/workflows/validate-iran-jordan-firstnet.yml`
  - CI workflow for the governed assessment.

## Important conclusions already reached

1. Iran publicly claimed an IRGC missile operation through an official Sepah News communiqué, not merely through an English journalistic article.
2. The Persian original described the missile quantity only as "several" and did not supply an exact count.
3. Jordan's reported count of five intercepted missiles cannot be converted into five missiles launched.
4. Iran did not publish a located after-action assessment explaining success, failure, Jordan's political posture, or anticipated U.S. retaliation.
5. The broad U.S. strike operation necessarily relied on prior contingency planning and target development, but this does not prove prior knowledge, inducement, or preauthorization.
6. The FirstNet and Astound degradation is preserved as a firsthand cross-domain antecedent; cause and attribution remain unresolved.
7. The prior broad "last 24 hours" synthesis was corrected. Event time, announcement time, publication time, confirmation time, and analytical publication time must remain separate.
8. Reports of five Jordanian interceptions on adjacent dates may represent separate episodes. Same count plus same jurisdiction plus adjacent date does not prove event identity.

## Immediate next goals

Proceed in this order:

1. Acquire and preserve original primary objects for the first six public claims:
   - CENTCOM original missile statement and metadata;
   - Jordanian Armed Forces and Petra original interception statement(s);
   - Sepah News Notice No. 52 Persian original;
   - IRNA Persian and English derivatives linked to the original;
   - original U.S. executive retaliation remarks or recording;
   - official U.S. description of the two-hour strike wave and target set.
2. Record original URLs, retrieval timestamps, source-local timestamps, content paths, and SHA-256 hashes in the receipt manifest.
3. Populate chronology entries only to the precision supported by the primary source.
4. Resolve whether the July 28 and July 30 Jordan five-interception reports are distinct events.
5. Add bounded branches for Kuwait, Damietta, controlled Hormuz transit, Saudi–Iraq operations, and Houthi maritime declarations only after original-source capture.
6. Run `python scripts/validate_iran_jordan_firstnet_assessment.py` locally or through GitHub Actions and preserve the result.
7. Do not mark the independent-review requirement complete until a named reviewer, conflict declaration, answers, determination, timestamp, and signature or receipt are present.
8. Update this handoff after every substantial repository change so a new chat can resume without relying on conversation memory.

## Research and writing rules

- Search current public sources because the conflict is time-sensitive.
- Prefer original government, military, state-agency, carrier, regulatory, and maritime records.
- Preserve translations as derivatives linked to the original language object.
- Distinguish an official claim from an independently established physical fact.
- Distinguish absence not yet located from a bounded and adequately searched absence.
- Do not use publication date as event time.
- Do not merge events because counts, locations, or wording match.
- Record corrections as first-class receipts rather than silently overwriting earlier analysis.
- Add all meaningful new work directly to the ERL repository.

## Completion condition

This work is complete only when the incident record has:

- preserved primary objects and hashes;
- normalized and uncertainty-annotated chronology;
- event-identity resolution;
- claim-to-receipt mapping;
- contradiction review;
- passing machine validation;
- independent review receipt;
- and a bounded final determination stating exactly what is established, unresolved, contradicted, or inadmissible.

## Required response convention

Every future assistant response in this workstream must end with:

1. current repository progress lines;
2. a delta statement describing what changed;
3. a copy-ready `Next session prompt` that points directly to this handoff and all task-specific files needed for the next action.
