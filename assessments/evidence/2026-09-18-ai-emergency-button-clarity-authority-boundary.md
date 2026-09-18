# AI Emergency Button / CLARITY Authority-Boundary Comparison — 2026-09-18

**Goal Task ID:** `ERL-AI-EMERGENCY-CLARITY-AUTHORITY-BOUNDARY-001`  
**COSV:** `40000100100000`  
**Status:** `RESEARCH_INTAKE / FINDING_NOT_AUTHORIZED / PUBLICATION_NOT_AUTHORIZED`

## Purpose

Preserve the September 2026 relationship between two distinct federal legislative control concepts without treating them as equivalent:

- a proposed human-operated shutdown capability for advanced AI systems; and
- a proposed digital-asset framework that distinguishes non-controlling blockchain developers/providers from actors with unilateral transaction-control authority.

The research question is architectural and evidentiary: can a system expose a bounded emergency suspension capability while keeping user-asset transaction initiation, custody, and ledger governance outside that operator's unilateral control?

## Source-state table

| Source / date | Observed proposition | Evidence boundary |
|---|---|---|
| AI Emergency Button Act draft linked by Sen. John Kennedy's office, 2026-09-16 | A covered entity developing or operating an advanced AI system in the United States would have to ensure the system includes a technical capability for a human operator to shut it down. DHS, in consultation with relevant federal agencies, would promulgate compliance regulations after enactment. | Proposed bill text. The two-page draft uses the term `advanced artificial intelligence system` but does not separately define that phrase in the displayed text. |
| Kennedy Senate-office release, 2026-09-16 | Kennedy sought unanimous consent; Sen. Rand Paul objected, so the proposal did not pass by unanimous consent. Kennedy described the company owning the model, rather than government, as operating the switch. | Sponsor-office account of the floor effort and sponsor's explanation of intended operation. |
| Senate final-draft H.R. 3633 substitute, 2026-09-14 | Section 10604 defines a `non-controlling blockchain developer or provider` as a developer/provider that, in the regular course of operations, lacks the legal right or unilateral and independent ability to control, initiate upon demand, or effectuate transactions involving digital assets to which users are entitled without third-party approval, consent, or direction. | Proposed Senate substitute text, not enacted law. |
| Lummis Senate-office release, 2026-09-14 | The final draft included BRCA edits intended to shield developers from money-transmission registration requirements and establish a civil safe harbor. | Sponsor-office characterization; exact legal effect remains governed by the draft text and any later enacted text. |
| U.S. Senate Roll Call Vote No. 234, 2026-09-15 2:19 p.m. | On cloture on the motion to proceed to H.R. 3633, the Senate recorded 49 yeas, 50 nays, and 1 not voting; cloture was rejected. The Senate floor-activity record also records a motion to reconsider entered after the failed cloture vote. | Official Senate procedural record. This supersedes the earlier secondary-source vote-count wording while leaving the preserved September 14 draft untouched. |
| Kennedy Senate-office floor record and linked floor video, 2026-09-16 | Kennedy sought unanimous consent to pass the AI Emergency Button Act; Sen. Rand Paul objected, preventing passage by unanimous consent. The official Senate-office release links the floor remarks video. | Official Senate-office account of the floor event. No roll-call vote occurred; this record does not imply broader Senate agreement or disagreement beyond the failed unanimous-consent request. |
| U.S. Senate Daily Press floor log, 2026-09-16, 5:15 p.m. | The Senate Daily Press records that Kennedy spoke on artificial intelligence development and asked unanimous consent to pass S. 5417; Paul reserved the right to object and asked unanimous consent to modify Kennedy's request; Kennedy objected to Paul's request; Paul then objected to Kennedy's original request. | Official institutional Senate floor log. This independently establishes the numbered bill used in the unanimous-consent exchange and the sequence of competing requests/objections; it is not itself a verbatim Congressional Record transcript. |
| S. 5417 legislative metadata, 2026-09-16 | S. 5417 is identified as a bill to require entities to include human-controlled shutdown mechanisms in all artificial intelligence systems, introduced by Sen. John Kennedy and read twice and referred to the Senate Committee on Commerce, Science, and Transportation. | Numbered Senate legislative state. The currently retrieved official/official-derived metadata establishes the bill number, sponsor, title/purpose line, date, and referral, but this update does not claim an exact-byte identity between the enrolled S. 5417 text and the earlier Kennedy-office two-page draft because a primary full-text copy was not independently retrieved in this pass. |

## Primary source anchors

- AI Emergency Button Act draft: https://www.kennedy.senate.gov/public/_cache/files/a/6/a6c8aed8-f68a-4ae5-b9c0-7b3fb89937da/116B6B836573706BDA71C73E35CA83A57425FCC2A681001D0E403EA13D503FA2.ai-emergency-button-act.pdf
- Kennedy Senate office, 2026-09-16: https://www.kennedy.senate.gov/public/2026/9/senate-blocks-kennedy-bill-to-require-ai-developers-to-install-an-emergency-kill-switch
- Senate final-draft CLARITY substitute: https://www.lummis.senate.gov/wp-content/uploads/EHF26724.pdf
- Lummis Senate office, 2026-09-14: https://www.lummis.senate.gov/press-releases/lummis-boozman-scott-release-final-clarity-act-text/
- U.S. Senate Roll Call Vote No. 234, 2026-09-15: https://www.senate.gov/legislative/LIS/roll_call_votes/vote1192/vote_119_2_00234.htm
- U.S. Senate floor activity, 2026-09-15: https://www.senate.gov/legislative/LIS/floor_activity/09_15_2026_Senate_Floor.htm
- Kennedy Senate office, 2026-09-16: https://www.kennedy.senate.gov/public/2026/9/senate-blocks-kennedy-bill-to-require-ai-developers-to-install-an-emergency-kill-switch
- Kennedy floor remarks video linked by Senate office: https://www.youtube.com/watch?v=cWfavLHKkSU
- U.S. Senate Daily Press, September 16 floor log: https://www.dailypress.senate.gov/page/2/
- S. 5417 official bill locator: https://www.congress.gov/bill/119th-congress/senate-bill/5417
- GovInfo Congressional Record Index (2026), current index includes `AI EMERGENCY BUTTON ACT` and S. 5417 under computer/technology indexing: https://www.govinfo.gov/app/details/CRI-2026/CRI-2026-PAPER
- Reuters procedural report, 2026-09-15 (secondary context retained): https://www.reuters.com/legal/government/us-senate-vote-advancing-landmark-crypto-bill-2026-09-15/

## Control-plane comparison

The source texts regulate different objects and different forms of authority.

| Authority / capability | AI Emergency Button draft | CLARITY final draft / BRCA |
|---|---|---|
| Shut down an AI system | Proposed required technical capability for a human operator | Not the subject of Section 10604 |
| Initiate a user's digital-asset transaction | Not addressed by the two-page shutdown draft | Central to the non-controlling developer/provider definition |
| Effectuate a user's digital-asset transaction unilaterally | Not addressed | A developer/provider with this unilateral ability would not fit the quoted non-controlling definition on that basis |
| Hold or safeguard user assets | Not addressed | Draft includes separate software/self-custody protections and other custody provisions; custody should not be collapsed into AI shutdown authority |
| Govern or rewrite distributed-ledger state | Not addressed | Separate distributed-ledger/decentralized-governance concepts appear elsewhere in H.R. 3633; Section 10604 is specifically bounded to developer/provider transaction-control status |
| Suspend an AI execution process while leaving asset authority untouched | Technically compatible with the shutdown concept | Not expressly resolved by Section 10604; requires implementation-specific and legal analysis |

## Bounded architectural inference

The two proposals are not facially contradictory merely because one preserves a human shutdown capability and the other protects a class of non-controlling blockchain developers/providers.

A system can be designed so that:

```text
AI_EXECUTION_AUTHORITY
!= DIGITAL_ASSET_TRANSACTION_AUTHORITY
!= ASSET_CUSTODY
!= LEDGER_GOVERNANCE_AUTHORITY
!= EMERGENCY_SUSPENSION_AUTHORITY
```

For example, a narrowly scoped transition from `AI_ACTIVE` to `AI_SUSPENDED` could stop an AI execution process without granting the operator authority to originate a user's asset transaction, take custody of the user's assets, reverse a completed transaction, or rewrite ledger history. That is an architectural possibility only. Whether a concrete implementation would satisfy either proposal's legal definitions is not established by this comparison.

## StegVerse design relevance

This source set is relevant to StegVerse's existing separation among governance, execution, custody, and state-transition authority because it provides a real legislative example of why those powers should be represented separately.

The evidence does **not** establish:

- that StegVerse is a covered entity under the AI Emergency Button draft;
- that StegVerse or any component qualifies as a non-controlling blockchain developer/provider under H.R. 3633;
- that StegVerse complies with either proposal;
- that either proposal is good or bad policy;
- that a particular emergency-control mechanism should be adopted.

Any StegVerse-specific applicability or compliance analysis must be a separate, source-bounded task.

## Later-version reconciliation

- The formally introduced House `AI Kill Switch Act`, H.R. 9917, was introduced July 23, 2026 by Rep. Ted Lieu with Rep. Nathaniel Moran as cosponsor and is separately indexed by GovInfo. It is a distinct House bill and must not be silently substituted for Kennedy's later Senate-office `AI Emergency Button Act` discussion draft.
- The prior source pass recorded that no numbered Senate bill had yet been established. That historical observation is preserved. A later source pass on September 18 independently located the official Senate Daily Press floor log identifying Kennedy's unanimous-consent request as **S. 5417**. Separate legislative metadata identifies S. 5417 as introduced September 16, sponsored by Kennedy, read twice, and referred to the Senate Committee on Commerce, Science, and Transportation. The numbered state is appended here and does not erase the earlier uncertainty state.
- Exact-text reconciliation between S. 5417 and the Kennedy-office two-page draft remains open because this pass did not independently retrieve a primary full-text S. 5417 document suitable for byte-level or clause-level comparison. No identity between the two texts is inferred merely from title, sponsor, or floor usage.
- The September 14 Senate final-draft CLARITY text remains preserved as the compared draft state. The September 15 reconsideration motion remains procedurally open in the preserved Senate record. No later official substitute or amendment text was established in the September 16-18 source pass; any later substitute, amendment, reconsideration disposition, or reintroduction must be appended as a new evidence state rather than replacing it.

## Legislative-state preservation

As of this intake:

- the AI Emergency Button Act proposal did not pass through Kennedy's September 16 unanimous-consent attempt;
- the Senate did not invoke cloture on the motion to proceed to H.R. 3633 on September 15;
- the September 14 CLARITY language is therefore preserved here as a final Senate draft/substitute proposal, not as enacted federal law.

Later legislative changes must be appended as new evidence states rather than overwriting this snapshot.

## Required follow-up before finding promotion

1. Preserve any later Congressional Record transcript or Senate journal entry that gives a more granular verbatim record of the September 16 S. 5417 unanimous-consent exchange; retain both the official Senate-office record and Senate Daily Press floor log already captured.
2. Retrieve the primary full text of S. 5417 when independently available and compare it clause-by-clause against the Kennedy-office two-page draft; keep H.R. 9917 separate unless a formal relationship is established by primary sources.
3. Track later CLARITY substitutes, amendments, the disposition of the entered reconsideration motion, or reintroduction as appended evidence states.
4. Obtain independent legal review before making any statutory-applicability or compliance statement about a specific system.
5. Perform independent ERL review before any publication or substantive finding transition.

## Nonclaims

This record does not endorse or oppose either proposal. It does not infer legislative motive, predict future passage, declare either proposal legally effective, or classify StegVerse under either proposal. It preserves a source-supported authority-boundary comparison for future longitudinal analysis.
