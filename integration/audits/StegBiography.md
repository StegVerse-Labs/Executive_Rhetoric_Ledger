# Native-Mechanism and Platform Audit: StegVerse-Labs/StegBiography

## Audit status

```yaml
repository: "StegVerse-Labs/StegBiography"
audit_state: "partial-mechanism-and-platform-audit"
repository_visibility: "public"
adapter_state: "shared-engine-dependent-and-privacy-review-required"
recurring_source_scan_confirmed: false
```

## Declared purpose

StegBiography is intended for fact-based, evidence-linked reconstruction of a life rather than gossip, political framing, or unsupported narrative.

The current README is minimal and does not document schemas, workflows, schedules, source tiers, archive rules, privacy controls, or producer outputs.

## External platform and source environments

Potential source environments include:

- civil and vital records;
- court and administrative dockets;
- archives, libraries, and newspapers;
- scholarly and historical publications;
- official biographies and institutional records;
- interviews, speeches, and media platforms;
- social accounts and deleted or corrected public statements;
- genealogy and cemetery platforms;
- campaign, legislative, corporate, and nonprofit records;
- shared StegVerse biography-ingest and co-occurrence workflows.

No active platform connector or schedule was confirmed in this repository during this pass.

## Required evidence distinctions

```text
verified life event
self-reported claim
third-party account
contemporaneous primary record
later recollection
allegation
adjudicated finding
relationship claim
association
correction
retraction
```

Biography structure must not collapse association into action, allegation into fact, or narrative coherence into proof.

## Privacy and harm boundary

The system must distinguish public figures, historical persons, private persons, victims, witnesses, family members, and living minors. Sensitive identity, health, family, address, and protected records require necessity, authority, and privacy review.

## Smallest compatible boundary

```text
source-postured biographical event or relationship candidate
+ identity resolution
+ temporal scope
+ privacy posture
+ contradiction and correction state
-> Executive Rhetoric Ledger review
```

The ledger may return accepted rhetoric, action, institutional response, and outcome records for incorporation into a biography, while StegBiography retains narrative and life-chronology responsibility.

## Open gaps

- Mirror handoff.
- Shared-engine implementation and output contract.
- Source and identity schemas.
- Schedules and source lists.
- Archive, fingerprint, deduplication, and co-occurrence outputs.
- Privacy and subject-response rules.
- Correction, dispute, deprecation, and merge handling.
- Export and publication surfaces.

## Prohibited integration changes

- Do not add another biography scanner before the shared engine is audited.
- Do not export protected or private-person data without review.
- Do not infer causation or intent from co-occurrence.
- Do not allow a biography repository to self-authorize evidence into the ledger.

## Preliminary classification

```yaml
classification: "shared-engine-dependent-biographical-context-producer-partial"
platform_source_role: "confirmed-conceptually-automation-unconfirmed"
privacy_review_required: true
full_adapter_ready: false
```
