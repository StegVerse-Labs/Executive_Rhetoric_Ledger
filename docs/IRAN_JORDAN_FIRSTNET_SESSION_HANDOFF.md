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
- `research-candidates/2026-07-30-iran-war-24h-qualified-addendum.md`
- `assessments/pit/PIT-MODERN-2026-IRAN-JORDAN-FIRSTNET.assessment.json`
- `assessments/chronology/2026-07-28-30-iran-jordan-firstnet.normalized.json`
- `assessments/contradictions/2026-07-iran-jordan-firstnet.matrix.md`
- `assessments/intake/2026-07-iran-jordan-firstnet-primary-record-intake.json`
- `assessments/source-posture/2026-07-iran-jordan-firstnet-initial-source-receipts.json`
- `assessments/receipts/2026-07-iran-jordan-firstnet.receipt-manifest.json`
- `assessments/reviews/PIT-MODERN-2026-IRAN-JORDAN-FIRSTNET.review.md`
- `assessments/reviews/PIT-MODERN-2026-IRAN-JORDAN-FIRSTNET.independent-review.json`
- `scripts/validate_iran_jordan_firstnet_assessment.py`
- `.github/workflows/validate-iran-jordan-firstnet.yml`

## Important conclusions already reached

1. Iran publicly claimed an IRGC missile operation through an official Sepah News communiqué, not merely through an English journalistic article.
2. The Persian original described the missile quantity only as "several" and did not supply an exact count.
3. Jordan's reported count of five intercepted missiles cannot be converted into five missiles launched.
4. Iran did not publish a located after-action assessment explaining success, failure, Jordan's political posture, or anticipated U.S. retaliation.
5. The broad U.S. strike operation necessarily relied on prior contingency planning and target development, but this does not prove prior knowledge, inducement, or preauthorization.
6. The FirstNet and Astound degradation is preserved as a firsthand cross-domain antecedent; cause and attribution remain unresolved.
7. Event time, announcement time, publication time, confirmation time, and analytical publication time must remain separate.
8. Reports of five Jordanian interceptions on adjacent dates may represent separate episodes. Same count plus same jurisdiction plus adjacent date does not prove event identity.

## Session update — 2026-07-30 primary capture cycle

### Repository changes completed

1. Captured the official Petra English carrier object for the July 29 Jordanian five-missile interception claim:
   - `sources/2026-07/2026-07-29-petra-jordan-five-missiles.md`
   - original URL: `https://petra.gov.jo/en/news/jordanian-air-defenses-intercept-five-missiles-fired-from-iran`
   - issuing authority: Jordanian Armed Forces-Arab Army, carried by Petra
   - source-local publication: `2026-07-29T07:48:26+03:00`
   - normalized publication: `2026-07-29T04:48:26Z`
   - repository-capture SHA-256: `a5d6b84f754946afea370f327e85c1444c441461f35a6ba0570fdfc17452409f`
   - custody limitation: textual source-visible capture, not a byte-for-byte WARC or native platform export.
2. Updated receipt `R-002` to `captured` with authority, retrieval, timestamp, language, derivative, content-path, hash, supported-claim, and limitation fields.
3. Added `assessments/event-identity/2026-07-jordan-five-interception-disambiguation.md`.
4. Preserved `EV-004` and `EV-010` as separate nodes with identity unresolved and merge prohibited pending the second primary object.

### Current evidence consequence

The July 29 Petra object establishes Jordan's official claim that five missiles fired from Iran toward Jordan were intercepted and destroyed. It does not establish the total launched, successful impacts, U.S. control of publication timing, or identity with any adjacent report. The second five-interception report remains uncaptured; therefore the record cannot yet determine whether two physical attacks occurred, but it also cannot merge the reports.

### Commits in this cycle

- `0d931784bf722076affbdd51351fb9ce33f7063a` — Petra source capture.
- `c61c1f37b80cd963ea5d88efa770ada6f15ed14d` — receipt manifest update.
- `2a661fada16e403b2125db3e46e5ecfca7037301` — event-identity disambiguation record.

## Immediate next goals

Proceed in this order:

1. Acquire and preserve the exact CENTCOM original post and metadata for status `2082231500318114110`; the object is located but the accessible retrieval returned no source text.
2. Acquire the exact Sepah News Notice No. 52 item page, not merely the section URL.
3. Preserve IRNA Persian `86222422` and English `86222477` as linked derivatives, with the Persian object controlling quantity and target-language interpretation.
4. Acquire the original White House, pool, or presidential recording/transcript for the retaliation remarks.
5. Acquire the official CENTCOM release or native object describing the reported two-hour strike wave and target classes.
6. Locate and preserve the second original Jordanian five-interception statement. Do not merge it with the July 29 object.
7. Populate the normalized chronology only with source-supported time dimensions. The July 29 Petra timestamp is publication time, not physical-event time or prior statement-issuance time.
8. Inspect the GitHub Actions result triggered by the receipt-manifest change and preserve the validation run/job result.
9. Keep independent review unassigned and the assessment at `research_candidate` until all promotion requirements are satisfied.
10. Update this handoff after every substantial repository change.

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

This work is complete only when the incident record has preserved primary objects and hashes, normalized and uncertainty-annotated chronology, event-identity resolution, claim-to-receipt mapping, contradiction review, passing machine validation, independent review receipt, and a bounded final determination stating exactly what is established, unresolved, contradicted, or inadmissible.

## Required response convention

Every future assistant response in this workstream must end with current repository progress lines, a delta statement describing what changed, and a copy-ready next-session prompt pointing directly to this handoff and all task-specific files needed for the next action.
