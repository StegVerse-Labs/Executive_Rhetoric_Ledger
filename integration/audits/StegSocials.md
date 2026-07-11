# Native-Mechanism Audit: StegVerse-Labs/StegSocials

## Audit status

```yaml
repository: "StegVerse-Labs/StegSocials"
audit_state: "partial-mechanism-audit"
adapter_state: "blocked-pending-full-native-review"
replacement_scanner_allowed: false
native_publication_boundary_confirmed: true
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

This makes StegSocials primarily a governed social-intake, response, release, and receipt layer. The current README does not establish that it already performs broad autonomous recurring source discovery or classification.

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

StegSocials should not receive a second release queue, publication state machine, credential path, or admission validator from Executive Rhetoric Ledger.

The smallest compatible boundaries are likely:

1. Executive Rhetoric Ledger produces reviewed publication candidates.
2. StegSocials converts reviewed candidates into its native intake, response, queue, and release objects.
3. StegSocials retains publication authority, account boundary, release timing, and publication receipt responsibility.
4. Publication receipts may return to the ledger only as outcome or circulation evidence.

## Open audit gaps

- Exact workflow names and trigger schedules.
- Whether any current workflow scans external social sources automatically.
- Existing claim categorization schema and intake validators.
- Deduplication and source fingerprint behavior.
- Platform-specific publisher implementations.
- Current queue population and active release status.
- Existing export or callback contract to other repositories.
- Current mirror handoff or equivalent task source of truth.

## Prohibited integration changes

- Do not install another release queue.
- Do not move credentials into Executive Rhetoric Ledger.
- Do not duplicate publication receipts.
- Do not classify StegSocials as a recurring source scanner until a current scheduled discovery mechanism is located.
- Do not let publication success convert a claim into factual truth.

## Preliminary capability classification

```yaml
classification: "publication-consumer-ready-partial"
source_discovery_status: "unconfirmed"
ledger_to_stegsocials_boundary: "reviewed-publication-candidate"
stegsocials_to_ledger_boundary: "publication-receipt-and-circulation-outcome"
full_adapter_ready: false
```
