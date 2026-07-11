# Native-Mechanism Audit: StegVerse-Labs/VAwatchdog

## Audit status

```yaml
repository: "StegVerse-Labs/VAwatchdog"
audit_state: "partial-mechanism-audit"
adapter_state: "blocked-pending-full-native-review"
repository_visibility: "private"
current_repo_status: "scaffolded"
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

## Native source tiers

| Tier | Meaning | Ledger-compatible posture |
|---|---|---|
| Tier 0 | First-person observation only | Preserve as attributed observation; do not publish as established fact without corroboration. |
| Tier 1 | Public source verifies context | Contextual support only. |
| Tier 2 | Public source verifies a specific event | Candidate factual anchor subject to receipt review. |
| Tier 3 | Internal document, FOIA, audit, or sworn record | High-confidence candidate with privacy, authenticity, and authority review. |
| Tier 4 | Court-tested or adjudicated record | Strongest external support, preserving exact scope and disposition. |

## Confirmed native boundaries

The repository already distinguishes verified anchors from non-verified claims. It also prohibits doxxing, unsupported allegations, sealed information, and protected victim data.

Its intended activation target is the ability to accept observations and evidence consistently, distinguish verified from unverified material, and produce an audit-ready timeline without manual reconstruction.

## Current mechanism posture

The README reports the repository as scaffolded and not evidentiary complete. No recurring scanner, categorizer, workflow, archive process, or export contract was confirmed during this pass.

The repository therefore must not yet be treated as an automated upstream producer.

## Likely smallest compatible boundary

When native structures are complete, the likely boundary is:

```text
VAwatchdog source-tiered record
-> privacy and corroboration review
-> Source Posture translation
-> candidate oversight incident, contradiction, institutional response, or outcome
-> Executive Rhetoric Ledger review
```

VAwatchdog should retain custody of sensitive first-person records, protected identifiers, internal documents, and detailed technical hypotheses. Executive Rhetoric Ledger should receive only reviewed, minimally necessary, source-postured candidate records or durable pointers.

## Open audit gaps

- Mirror handoff or equivalent task source of truth.
- Source-separation policy file and verification matrix.
- Observation, anomaly, and financial model schemas.
- Templates and validators.
- Any workflow or scheduled source-monitoring mechanism.
- Archive, fingerprint, deduplication, and receipt paths.
- FOIA and oversight request tracking.
- Privacy and redaction implementation.
- Existing export contract or downstream consumers.

## Prohibited integration changes

- Do not add a recurring scanner until existing workflows and source lists are fully inventoried.
- Do not export Tier 0 observations as established facts.
- Do not move protected or sealed material into the public ledger.
- Do not infer causation between technical anomalies and criminal or financial events without an evidence chain.
- Do not name individuals from unsupported internal allegations.

## Preliminary capability classification

```yaml
classification: "privacy-restricted-manual-source-only"
ledger_contribution_posture: "reviewed-source-postured-candidates-only"
full_adapter_ready: false
```
