# Native-Mechanism Audit: StegVerse-Labs/StegSocials

## Audit status

```yaml
repository: "StegVerse-Labs/StegSocials"
audit_state: "partial-mechanism-audit"
adapter_state: "blocked-pending-full-native-review"
replacement_scanner_allowed: false
native_publication_boundary_confirmed: true
platform_source_interaction_confirmed: true
native_source_scanner_confirmed: false
```

## Declared purpose

StegSocials is a governed public-communication and social-response repository. It treats social posts as public claim surfaces and converts them through a controlled response flow:

```text
Observed Post
-> Claim Extraction
-> Governance Relevance
-> StegVerse Position
-> Evidence / Diagram / Repo Reference
-> Response Draft
-> Publication Posture
-> Receipt
```

StegSocials is therefore not only a publication surface. The external platforms it interacts with are also input environments whose posts, comments, reactions, corrections, removals, account actions, and circulation patterns may become source material affecting discovery, categorization, response posture, and later evidentiary organization.

The current repository evidence confirms platform-aware intake and publication design, but does not yet confirm a broad autonomous recurring platform scanner.

## Confirmed platform environments

The platform guide explicitly distinguishes:

- LinkedIn;
- X;
- Facebook;
- long-form publication surfaces;
- diagram-caption surfaces.

The repository preserves a common claim-extraction and governance process while changing response form by platform.

```text
platform content
-> observed public claim surface
-> claim and assumption extraction
-> governance classification
-> evidence or repository linkage
-> candidate response
-> governed publication
-> receipt and correction posture
```

Platform interaction can affect repository state in both directions:

```text
external platform -> source discovery and claim intake
StegSocials -> governed response and publication
external platform -> publication outcome, reaction, correction, removal, or account-state evidence
StegSocials -> receipt, correction, retirement, or follow-up candidate
```

## Confirmed native structures

```text
campaigns/      coordinated social response campaigns
intake/         captured social claims and intake templates
queue/          candidate response records
release_queue/  scheduled release objects without secrets
responses/      drafted and admitted public responses
receipts/       traceable publication receipts
schemas/        structured response and receipt schemas
scripts/        validation helpers
.github/        issue templates and validation workflow
```

Confirmed operational examples include response objects, receipts, drafted responses, and queue records.

## Source and evidence implications

A platform artifact can establish different things depending on its state and provenance:

| Platform artifact | What it may establish | What it does not establish by itself |
|---|---|---|
| Original post or comment | That a claim was published by an account at a recorded time, subject to account and capture verification | That the claim is true |
| Edited or deleted post | That platform state changed, if the earlier state is durably captured | Why it changed or whether the original claim was false |
| Reaction or engagement count | Circulation or public response at a specific capture time | Representativeness, truth, or genuine human origin |
| Platform moderation notice | That a platform applied a rule or action | That the platform's factual or legal conclusion is correct |
| Account suspension or restriction | That account access or visibility changed | The underlying justification without platform records |
| Publication receipt | That an attempted or completed publication occurred | That the published content was accepted as factual truth |

The platform itself is therefore both:

- a source environment;
- a publication environment;
- an intermediary that can alter visibility, ordering, availability, metadata, and context.

## Secure release boundary

StegSocials separates content governance from credential custody:

```text
StegSocials repo
-> prepares governed post objects
-> marks post admitted
-> scheduler reads admitted release queue
-> token broker retrieves platform credential at runtime
-> publisher posts
-> receipt captures result
-> token never enters repo
```

The repository must not store passwords, session cookies, recovery codes, raw OAuth tokens, API keys, browser profiles, or device-trust files.

Credential references are opaque handles only, for example:

```yaml
credential_ref: "vault://stegsocials/linkedin/company-page-publisher"
```

## Release state machine

```text
draft
-> admitted
-> scheduled
-> publishing
-> published
-> receipted

failed | cancelled | corrected | retired
```

A release object and its admission record are distinct. The release object requests future publication; the admission record determines whether that request may proceed.

## Confirmed validators

### Release queue safety

`scripts/check_release_queue.py` scans release queue YAML for secret-like keys and suspicious credential patterns. It allows opaque reference fields while blocking raw credential-like material.

### Release admission

`scripts/check_release_admissions.py` requires:

- content reviewability;
- campaign declaration;
- bounded position;
- no-overclaim posture;
- platform and account declaration;
- opaque credential reference;
- no stored password, token, cookie, recovery code, or session secret;
- declared release window;
- no blind retry;
- receipt and correction paths.

## Current integration posture

StegSocials should not receive a second release queue, publication state machine, credential path, admission validator, platform classifier, or source-capture path from Executive Rhetoric Ledger until its own platform-facing intake mechanisms are completely inventoried.

The smallest compatible boundaries are likely:

1. External platforms provide candidate public claims, reactions, corrections, and circulation evidence to StegSocials through its native intake path.
2. StegSocials preserves platform identity, account identity, capture time, artifact state, and platform-specific context.
3. Executive Rhetoric Ledger may receive reviewed source-postured claim candidates, contradiction candidates, circulation outcomes, or durable platform pointers.
4. Executive Rhetoric Ledger produces reviewed publication candidates.
5. StegSocials converts reviewed candidates into its native response, queue, admission, release, and receipt objects.
6. StegSocials retains publication authority, account boundary, release timing, and publication receipt responsibility.
7. Platform outcomes return as source-postured circulation, correction, moderation, or account-state evidence rather than truth determinations.

## Open audit gaps

- Exact workflow names and trigger schedules.
- Whether any current workflow scans external social sources automatically.
- Platform API, browser, webhook, feed, email, or manual capture mechanisms.
- Existing claim categorization schema and intake validators.
- Platform artifact fingerprinting, screenshot, archive, and durable-link behavior.
- Deduplication across reposts, screenshots, mirrors, and cross-platform copies.
- Account-authenticity and impersonation handling.
- Treatment of edits, deletions, moderation notices, and disappearing content.
- Platform-specific publisher implementations.
- Current queue population and active release status.
- Existing export or callback contract to other repositories.
- Current mirror handoff or equivalent task source of truth.

## Prohibited integration changes

- Do not install another release queue.
- Do not move credentials into Executive Rhetoric Ledger.
- Do not duplicate publication receipts.
- Do not install a second platform capture or categorization path until native intake mechanisms are fully inventoried.
- Do not classify StegSocials as a recurring autonomous source scanner until a current scheduled discovery mechanism is located.
- Do not let publication success, engagement, moderation, or platform identity convert a claim into factual truth.
- Do not discard platform metadata or content-state changes that affect provenance.

## Preliminary capability classification

```yaml
classification: "platform-interacting-publication-and-source-intake-partial"
source_discovery_status: "platform-source-role-confirmed-automation-unconfirmed"
ledger_to_stegsocials_boundary: "reviewed-publication-candidate"
stegsocials_to_ledger_boundary: "source-postured-platform-claim-circulation-correction-and-publication-outcome"
full_adapter_ready: false
```
