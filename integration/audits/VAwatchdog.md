# Native-Mechanism Audit: StegVerse-Labs/VAwatchdog

## Audit status

```yaml
repository: "StegVerse-Labs/VAwatchdog"
audit_state: "partial-mechanism-audit"
adapter_state: "blocked-pending-full-native-review"
repository_visibility: "private"
current_repo_status: "scaffolded"
platform_source_interaction_confirmed: true
recurring_source_scan_confirmed: false
```

## Declared purpose

VAwatchdog is a controlled accountability intake for Department of Veterans Affairs and Veterans Benefits Administration observations, technical anomalies, disability-payment disruption patterns, public-source evidence, financial estimates, and questions suitable for FOIA, oversight, audit, or legal review.

It explicitly separates:

1. first-person observations;
2. publicly verifiable facts;
3. material but unverified claims;
4. technical hypotheses;
5. financial scale estimates;
6. open oversight questions.

VAwatchdog is therefore not isolated from external systems. The VA, VBA, public contact systems, benefit and identity platforms, DOJ, VA OIG, courts, FOIA channels, oversight bodies, and other public-record systems are potential source environments whose records can change the repository's organization, corroboration posture, timelines, technical hypotheses, and outcome assessments.

## Native source tiers

| Tier | Meaning | Ledger-compatible posture |
|---|---|---|
| Tier 0 | First-person observation only | Preserve as attributed observation; do not publish as established fact without corroboration. |
| Tier 1 | Public source verifies context | Contextual support only. |
| Tier 2 | Public source verifies a specific event | Candidate factual anchor subject to receipt review. |
| Tier 3 | Internal document, FOIA, audit, or sworn record | High-confidence candidate with privacy, authenticity, and authority review. |
| Tier 4 | Court-tested or adjudicated record | Strongest external support, preserving exact scope and disposition. |

## Confirmed platform and institutional source environments

The current README identifies or implies interaction with:

- Department of Veterans Affairs public information systems;
- Veterans Benefits Administration service and payment systems;
- VA public contact and regional-office information;
- federal identity and access environments involving PIV or CAC concepts;
- DOJ public case records and announcements;
- VA OIG public oversight and enforcement records;
- FOIA channels;
- audit and congressional or administrative oversight channels;
- court-tested or adjudicated records;
- first-person operational observations from call-center and IT environments.

These systems are not interchangeable sources. Each carries a different authority, completeness, latency, correction, and access posture.

## Platform-to-repository effects

External platforms may alter repository state through:

```text
new public record
-> corroborates context or a specific event
-> raises or lowers source tier
-> updates the verification matrix
-> changes timeline confidence
-> narrows or expands a technical hypothesis
-> creates a FOIA, oversight, audit, or legal-review task
```

They may also create contradictions:

```text
first-person observation
<-> agency public statement
<-> audit or OIG finding
<-> court record
<-> benefits or payment record
<-> later correction or disposition
```

The repository must preserve those differences rather than flattening them into a single narrative.

## Source-environment boundaries

| Source environment | What it may establish | Required caution |
|---|---|---|
| VA or VBA public webpage | Published agency position, office existence, public procedure, or contact information at capture time | Does not establish internal implementation or individual case handling |
| Benefits or payment platform record | Transaction, status, notice, or account event for an authorized subject | Privacy, account authority, completeness, and later correction must be preserved |
| Call-center or IT operational observation | Attributed first-person observation of system or process behavior | Requires corroboration before broader institutional claims |
| DOJ announcement or filing | That an enforcement action, allegation, plea, or disposition was publicly recorded | Exact procedural posture and scope must be preserved |
| VA OIG or audit record | Official oversight finding within its stated scope | Finding date, methodology, limitations, and response must remain attached |
| FOIA response | Records produced, withheld, referred, or declared unavailable under a particular request | Absence in a response does not prove nonexistence; exemptions and search scope matter |
| Court record | Filed allegation, order, finding, judgment, or disposition according to document type | Filing is not the same as adjudicated fact |
| News or advocacy platform | Lead, context, quotation, or public claim | Requires source-posture review and primary-record follow-up |

## Confirmed native boundaries

The repository already distinguishes verified anchors from non-verified claims. It also prohibits doxxing, unsupported allegations, sealed information, and protected victim data.

Its intended activation target is the ability to accept observations and evidence consistently, distinguish verified from unverified material, and produce an audit-ready timeline without manual reconstruction.

## Current mechanism posture

The README reports the repository as scaffolded and not evidentiary complete. No recurring scanner, categorizer, workflow, archive process, or export contract was confirmed during this pass.

That does not mean the repository is manual-source-only in purpose. It means the repository's external platform and institutional source relationships are confirmed, while their current automated retrieval and update mechanisms remain unaudited or absent from the inspected files.

The repository therefore must not yet be treated as an automated upstream producer.

## Likely smallest compatible boundary

When native structures are complete, the likely boundary is:

```text
external institutional or public platform record
-> VAwatchdog native capture and source-tier classification
-> privacy, authority, authenticity, and corroboration review
-> timeline, verification matrix, anomaly model, or oversight task update
-> Source Posture translation
-> candidate oversight incident, contradiction, institutional response, or outcome
-> Executive Rhetoric Ledger review
```

VAwatchdog should retain custody of sensitive first-person records, protected identifiers, account-specific platform records, internal documents, and detailed technical hypotheses. Executive Rhetoric Ledger should receive only reviewed, minimally necessary, source-postured candidate records or durable pointers.

## Open audit gaps

- Mirror handoff or equivalent task source of truth.
- Source-separation policy file and verification matrix.
- Observation, anomaly, and financial model schemas.
- Templates and validators.
- Exact VA, VBA, DOJ, OIG, court, FOIA, or oversight source lists and query methods.
- Any workflow, API, email, feed, browser, or scheduled source-monitoring mechanism.
- Platform authentication and account-authority boundaries.
- Archive, fingerprint, deduplication, and receipt paths.
- FOIA and oversight request tracking.
- Handling of amended agency pages, corrected notices, updated case dockets, and changed benefit statuses.
- Privacy and redaction implementation.
- Existing export contract or downstream consumers.

## Prohibited integration changes

- Do not add a recurring scanner until existing workflows, platform interactions, and source lists are fully inventoried.
- Do not export Tier 0 observations as established facts.
- Do not move protected, account-specific, medical, financial, or sealed material into the public ledger.
- Do not infer causation between technical anomalies and criminal or financial events without an evidence chain.
- Do not name individuals from unsupported internal allegations.
- Do not treat an agency platform, court filing, news source, or oversight body as infallible.
- Do not let missing FOIA production, inaccessible platform data, or unavailable internal records silently resolve a disputed claim.

## Preliminary capability classification

```yaml
classification: "platform-interacting-privacy-restricted-evidence-intake-partial"
platform_source_role: "confirmed"
automated_retrieval_status: "unconfirmed"
ledger_contribution_posture: "reviewed-source-postured-candidates-only"
full_adapter_ready: false
```
