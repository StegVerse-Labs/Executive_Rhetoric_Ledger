# White House Press Access Precedent Mirror Handoff

Updated: 2026-09-18

## Canonical identity

- Goal Task ID: `ERL-WHITE-HOUSE-PRESS-ACCESS-PRECEDENT-001`
- Repository: `StegVerse-Labs/Executive_Rhetoric_Ledger`
- Canonical issue: `#177`
- COSV: `40000100100000`
- Task Registry generation: `48`
- Status: `ACTIVE / CHECKED_OUT / RESEARCH_ACTIVE_NOT_ASSESSABLE / FINDING_NOT_AUTHORIZED / PUBLICATION_NOT_AUTHORIZED`

## Objective

Maintain a continuing, source-bounded ERL reconstruction of executive control over White House press access, with the September 18, 2026 CNN/MS NOW/Politico exclusion announcement as the current event and with freedom-of-the-press, viewpoint-discrimination, access-surface, procedural, and cross-administration precedent questions preserved separately.

## Existing-engine binding

This task does not own or create a scheduler, crawler, dispatcher, publication system, or new authority plane.

It reuses:

- `.github/workflows/run-recurring-discovery.yml`;
- `config/recurring-searches.example.json`;
- `scripts/generate_active_research_dispatch.py`;
- `docs/ERL_ACTIVE_RESEARCH_MYKV_COORDINATION.md`;
- the existing MyKV `02_Research/ERL` persistence contract.

Active-research group: `ERL-RC-WHITE-HOUSE-PRESS-ACCESS-2026`.  
Acquisition queue: `config/white-house-press-access-source-queue.v1.json`.

## Initial legal/evidence posture

The First Amendment text is an official constitutional anchor. `Sherrill v. Knight` supplies the longstanding D.C. Circuit baseline for White House hard-pass/open-press-facility access and procedural safeguards, without creating an unlimited right to every presidential space.

The April 8, 2025 district-court order in `Associated Press v. Budowich` granted preliminary relief on a likely viewpoint-discrimination theory. The June 6, 2025 D.C. Circuit stay order partially stayed that injunction and distinguished restricted presidential workspaces from opened press facilities. Those are different procedural stages and must remain distinct; neither is to be rewritten as a final merits judgment that resolves every White House access surface.

For the September 18, 2026 event, Reuters and AP presently provide contemporaneous event locators and reported wording. Direct first-party custody of the exact presidential/White House announcement remains an active acquisition requirement.

## Cross-administration rule

The research target is institutional rather than partisan: identify the governmental-access rule that actually survives authoritative adjudication and implementation, then test the same rule symmetrically against a hypothetical later administration excluding ideologically different outlets. The lane may document consequences of a rule; it may not choose a political winner or recommend an electoral response.

## Required next evidence

1. Locate and custody the exact first-party presidential/White House statement and timestamp.
2. Determine actual implementation by access surface: hard pass, briefing room, pool, East Room/open facility, Oval Office/Air Force One/restricted workspace, and event-specific invitation.
3. Preserve any written credential denial, stated criteria, procedural notice, or appeal/reconsideration mechanism.
4. Preserve outlet, WHCA, pool, and White House responses.
5. Track any litigation and maintain TRO, preliminary-injunction, stay, merits, and appellate stages separately.
6. Track final disposition and later use of `Associated Press v. Budowich`.
7. Maintain cross-administration controls using the same legal/access categories regardless of party or outlet ideology.
8. Independent review before any finding or publication transition.

## Nonclaims

- no motive finding;
- no final constitutional judgment;
- no policy-quality or partisan finding;
- no prediction about electoral consequences;
- no assumption that announcement equals implementation;
- no assumption that one White House access surface determines all others;
- no publication authorization.

## Current source state

Candidate artifact: `research-candidates/2026-09-18-white-house-press-access-precedent.md`.  
Evidence intake: `assessments/evidence/2026-09-18-white-house-press-access-precedent-intake.md`.  
Durable issue: `#177`.  
Task Registry registration: merged at generation 48 under COSV `40000100100000`.

## Merge and validation evidence

- Task Registry registration: generation `48`, canonical Goal Task `ERL-WHITE-HOUSE-PRESS-ACCESS-PRECEDENT-001`, COSV `40000100100000`.
- Initial conflicted registry PR `#2137`: closed as superseded after concurrent main movement; no state from it is canonical.
- Replacement registry PR `StegVerse-Labs/.github#2139`: merged at `6532ce05d62ea3a0810aa77581a01591439e87ea`.
- ERL implementation PR `#178`: merged at `b775028d4ad74bc3ce790e37f7863b6edbe11920`.
- Final implementation head: `f326ee6ae25d978a701961364ae8dda51283a02e`.
- Validate research candidate activation run `35399221996`: SUCCESS.
- Validate Active Research MyKV Dispatch run `35399222046`: SUCCESS.
- Validate Active Research Acquisition Consumer run `35399221962`: SUCCESS.
- Validate Ledger Schemas run `35399222084`: SUCCESS after the recurring-discovery deterministic fixture was updated to include the new search.
- The dispatcher remains generic. The active overlay plus public no-credential READY queue places this lane on the existing automated-acquisition path; no lane-specific execution authority or promotion authority was added.
- No authentic source-acquisition-to-MyKV receipt for this new lane is claimed by registration alone.

## Next action

Continue the lane through the existing recurring-discovery and active-acquisition mechanisms: acquire the exact first-party presidential/White House statement first, then bind observed implementation by access surface, preserve outlet/WHCA responses and litigation stages, and update the cross-administration control record. Do not promote acquired material into a finding merely because acquisition succeeds.
