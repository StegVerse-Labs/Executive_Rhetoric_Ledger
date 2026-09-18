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
| Senate procedural vote reported 2026-09-15 | The Senate failed to invoke cloture on the motion to proceed to H.R. 3633; Reuters reported a 50-49 vote, below the 60 votes required. | Procedural status only; does not resolve the merits or future disposition of the legislation. |

## Primary source anchors

- AI Emergency Button Act draft: https://www.kennedy.senate.gov/public/_cache/files/a/6/a6c8aed8-f68a-4ae5-b9c0-7b3fb89937da/116B6B836573706BDA71C73E35CA83A57425FCC2A681001D0E403EA13D503FA2.ai-emergency-button-act.pdf
- Kennedy Senate office, 2026-09-16: https://www.kennedy.senate.gov/public/2026/9/senate-blocks-kennedy-bill-to-require-ai-developers-to-install-an-emergency-kill-switch
- Senate final-draft CLARITY substitute: https://www.lummis.senate.gov/wp-content/uploads/EHF26724.pdf
- Lummis Senate office, 2026-09-14: https://www.lummis.senate.gov/press-releases/lummis-boozman-scott-release-final-clarity-act-text/
- Reuters procedural report, 2026-09-15: https://www.reuters.com/legal/government/us-senate-vote-advancing-landmark-crypto-bill-2026-09-15/

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

## Legislative-state preservation

As of this intake:

- the AI Emergency Button Act proposal did not pass through Kennedy's September 16 unanimous-consent attempt;
- the Senate did not invoke cloture on the motion to proceed to H.R. 3633 on September 15;
- the September 14 CLARITY language is therefore preserved here as a final Senate draft/substitute proposal, not as enacted federal law.

Later legislative changes must be appended as new evidence states rather than overwriting this snapshot.

## Required follow-up before finding promotion

1. Preserve the exact Senate floor/roll-call procedural records for both September events.
2. Reconcile any subsequently numbered or formally introduced AI Emergency Button Act text against the Kennedy-office draft.
3. Track later CLARITY substitutes, amendments, reconsideration, or reintroduction.
4. Obtain independent legal review before making any statutory-applicability or compliance statement about a specific system.
5. Perform independent ERL review before any publication or substantive finding transition.

## Nonclaims

This record does not endorse or oppose either proposal. It does not infer legislative motive, predict future passage, declare either proposal legally effective, or classify StegVerse under either proposal. It preserves a source-supported authority-boundary comparison for future longitudinal analysis.
