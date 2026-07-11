# Native-Mechanism and Platform Audit: StegVerse-Labs/Patents

## Audit status

```yaml
repository: "StegVerse-Labs/Patents"
audit_state: "partial-mechanism-and-platform-audit"
adapter_state: "blocked-pending-full-native-review"
repository_visibility: "public"
recurring_sync_confirmed: true
patent_watcher_declared: true
patent_watcher_workflow_path_confirmed: false
external_platform_source_role: "confirmed"
full_adapter_ready: false
```

## Declared purpose

Patents bootstraps an autonomous Patent AI Entity for StegVerse. Its README declares that it watches StegVerse repositories for patentable changes, creates invention-disclosure stubs, generates provisional-draft skeletons, produces broad-to-narrow claim tiers, tracks provisional deadlines, and maintains a central patent manifest.

It explicitly prohibits automatic filing and requires human or legal review before any external filing or publication.

## Confirmed native mechanisms

### Patent portfolio manifest

`patent_manifest.json` declares:

```yaml
manifest_signature: "patents:v1"
portfolio_epoch: 1
minimum_entity_version: "0.1.0"
allowed_organizations:
  - "StegVerse"
  - "StegVerse-Labs"
allowed_repository_globs:
  - "StegVerse/*"
  - "StegVerse-Labs/*"
excluded_repository_globs:
  - "**/Patents"
  - "**/archive/**"
templates:
  disclosure: "templates/disclosure.md"
  provisional: "templates/provisional.md"
  claims: "templates/claims.md"
  diagram: "templates/diagram.md"
deadline_policy_days:
  provisional_to_nonprovisional: 365
  pct_from_provisional: 365
```

This is already a native scope, template, and deadline contract. Executive Rhetoric Ledger must not replace it.

### Daily StegDB canonical overlay sync

Patents already runs a scheduled daily sync at `03:23 UTC`:

```yaml
workflow: ".github/workflows/sync-overlay-from-stegdb.yml"
schedule: "23 3 * * *"
source_repository: "stegverse-labs/stegdb"
source_path: "canonical/overlays/PatentsOverlay/canon"
destination_path: "canon/"
write_behavior: "rsync --delete, validate non-empty output, commit and push changes"
concurrency: "one overlay sync per repository; cancel in progress"
```

The workflow fails loudly when the source overlay is missing or the resulting canonical directory is empty.

### Declared Patent Watcher

The README instructs operators to run an action named `Patent Watcher`, initially in dry-run mode, and review generated material in `disclosures/` and `provisionals/`.

The exact current workflow path and implementation were not located in this audit pass. The declared mechanism is therefore preserved as `declared-unverified-current-path`; no replacement watcher may be installed.

## External platform and source environments

Patents interacts with or may derive evidentiary state from:

- GitHub organization and repository history;
- pull requests, commits, releases, issues, diagrams, and code changes;
- StegDB canonical overlays;
- USPTO Patent Center and public patent records;
- WIPO PATENTSCOPE and PCT records;
- Google Patents and other search surfaces;
- assignment and ownership records;
- patent prosecution histories;
- office actions, notices, filing receipts, and deadlines;
- prior-art databases, standards repositories, papers, products, and public demonstrations;
- human legal review and filing counsel systems.

These environments may change:

- invention-disclosure candidates;
- priority and public-disclosure dates;
- inventor and assignee posture;
- prior-art and novelty analysis;
- claim scope and amendment history;
- filing, abandonment, publication, grant, expiration, and maintenance status;
- deadline state;
- ownership and assignment chain;
- relationship between a repository change and an actual invention.

## Evidence and provenance boundary

```text
repository change or external patent record
-> allowlist and exclusion review
-> invention or prior-art candidate
-> disclosure, claim, diagram, deadline, or portfolio record
-> human and legal review
-> filing or non-filing decision outside automated authority
-> authoritative patent-office or assignment record
-> reviewed innovation-history or political-adjacency candidate
-> Executive Rhetoric Ledger review
```

A repository commit can establish that code or documentation changed. It does not by itself establish inventorship, novelty, reduction to practice, ownership, patentability, deployment, effectiveness, or political influence.

## Current integration posture

The smallest compatible boundaries are likely:

1. Patents supplies reviewed authoritative filing, assignment, prosecution, deadline, or public-disclosure records.
2. Patents may nominate technology-policy adjacency or historical innovation candidates.
3. Executive Rhetoric Ledger preserves patent record posture separately from claims of deployment, effectiveness, ownership beyond the record, or political influence.
4. Existing allowlists, exclusions, templates, deadline policy, and StegDB canonical sync remain authoritative within Patents.
5. No second repository watcher, deadline engine, portfolio manifest, or `canon/` writer may be added.

## Open audit gaps

- Current mirror handoff or equivalent task source of truth.
- Exact Patent Watcher workflow path, schedule, triggers, and implementation.
- Current dry-run and write-authority boundaries.
- Change-detection, fingerprint, deduplication, and candidate-ranking logic.
- Disclosure, provisional, claims, and diagram schemas or validators.
- Deadline notification and supersession behavior.
- Inventor and assignee review process.
- USPTO, WIPO, prior-art, assignment, or prosecution-data integrations.
- Archive and receipt paths.
- Output contract from `canon/`, `disclosures/`, `provisionals/`, and the central manifest.
- Handling of confidential invention material and premature public disclosure.

## Prohibited integration changes

- Do not add a duplicate repository watcher or StegDB overlay sync.
- Do not bypass the native allowlist, exclusions, templates, or deadline policy.
- Do not automatically file or publish patent material.
- Do not treat a generated disclosure or claim draft as a legal filing or granted right.
- Do not infer inventorship, ownership, novelty, deployment, effectiveness, or influence from repository proximity alone.
- Do not export confidential invention details into the public political ledger.

## Preliminary capability classification

```yaml
classification: "scheduled-canonical-sync-patent-monitoring-and-portfolio-producer-partial"
ledger_contribution_posture: "reviewed-authoritative-patent-records-and-innovation-adjacency-candidates"
shared_canonical_dependency: "StegVerse-Labs/StegDB"
patent_watcher_status: "declared-implementation-unaudited"
external_patent_platform_automation_status: "unconfirmed"
full_adapter_ready: false
```
