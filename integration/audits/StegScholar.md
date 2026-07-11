# Native-Mechanism and Platform Audit: StegVerse-Labs/StegScholar

## Audit status

```yaml
repository: "StegVerse-Labs/StegScholar"
audit_state: "partial-mechanism-and-platform-audit"
adapter_state: "blocked-pending-full-native-review"
repository_visibility: "public"
recurring_sync_confirmed: true
external_platform_source_role: "confirmed"
full_adapter_ready: false
```

## Declared purpose

StegScholar is the scholarly research repository for StegVerse. It tracks peer-reviewed research papers, submission history and outcomes, figures and diagrams, reading lists and prior work, and evolving research primitives and terminology.

Its declared design principles require papers to remain standalone and composable, avoid dependency on StegVerse as a platform, use StegVerse only as an existence proof, and preserve stable, versioned, reusable terminology.

## Confirmed native mechanisms

### Scholarly artifact classes

```text
papers and paper source
submission checklists
venue tracking
bibliography and prior work
formal models
figures and diagrams
research terminology
roadmaps
submission outcomes
```

Recent repository history confirms paper, LaTeX, bibliography, venue, submission-checklist, formal-model, and roadmap artifacts.

### Daily StegDB canonical overlay sync

StegScholar already runs a scheduled daily sync at `03:17 UTC`:

```yaml
workflow: ".github/workflows/sync-overlay-from-stegdb.yml"
schedule: "17 3 * * *"
source_repository: "stegverse-labs/stegdb"
source_path: "canonical/overlays/StegScholarOverlay/canon"
destination_path: "canon/"
write_behavior: "rsync --delete, validate non-empty output, commit and push changes"
concurrency: "one overlay sync per repository; cancel in progress"
```

The workflow is fail-loud when the overlay path is absent or the synchronized canonical directory is empty.

## External platform and source environments

StegScholar is not only a repository of authored papers. Its evidentiary and organizational state may be affected by external scholarly platforms and institutional systems, including:

- journal and conference submission systems;
- peer-review portals;
- preprint repositories;
- DOI and bibliographic registries;
- citation indexes;
- institutional repositories;
- academic search engines;
- publisher correction, retraction, and versioning systems;
- research venue pages and calls for papers;
- author profiles and affiliation records;
- StegDB as the current canonical overlay source.

These platforms may alter:

- paper version and publication state;
- submission, acceptance, rejection, withdrawal, or revision status;
- DOI, venue, issue, page, and citation metadata;
- correction, expression-of-concern, or retraction posture;
- author identity, affiliation, and contribution records;
- discoverability and citation counts;
- availability of supplemental material;
- classification of prior work and controls.

## Evidence and provenance boundary

```text
external scholarly platform or primary publication record
-> captured bibliographic or submission state
-> source, version, venue, and correction review
-> StegScholar paper, bibliography, venue, or submission record
-> optional StegDB canonical overlay synchronization
-> reviewed scholarly-context or control candidate
-> Executive Rhetoric Ledger review
```

A citation count, search rank, abstract, or publisher metadata page does not independently establish the truth of a paper's claims. Peer review is a material source-posture signal but not a substitute for examining methods, evidence, corrections, and later replication.

## Current integration posture

The smallest compatible boundaries are likely:

1. StegScholar supplies reviewed literature, primary-paper pointers, terminology, formal models, historical context, and control candidates.
2. Executive Rhetoric Ledger preserves the exact evidentiary role of each scholarly source.
3. The ledger does not import academic conclusions as event-specific fact without an applicable evidence chain.
4. StegDB remains the canonical overlay source where the current workflow already declares that relationship.
5. No second daily canonical sync or parallel `canon/` writer may be added.

## Open audit gaps

- Current mirror handoff or equivalent task source of truth.
- Exact paper and submission directory structure.
- Current bibliography schema and validation.
- Venue and submission-state vocabularies.
- DOI, preprint, citation-index, or publisher API integrations.
- Retraction, correction, and version-supersession handling.
- Archive, fingerprint, deduplication, and receipt behavior.
- Relationship between authored papers and externally discovered literature.
- Output contract from `canon/` to downstream repositories.
- Current baseline workflow and smoke-test scope.

## Prohibited integration changes

- Do not add a duplicate StegDB overlay sync.
- Do not overwrite `canon/` from another source without a governed canonical-source change.
- Do not treat peer review, citation count, venue prestige, or search rank as proof of a claim.
- Do not collapse preprint, accepted manuscript, version of record, correction, and retraction states.
- Do not import a scholarly generalization as proof of a specific political incident without a separate evidence chain.

## Preliminary capability classification

```yaml
classification: "scheduled-canonical-sync-scholarly-context-producer-partial"
ledger_contribution_posture: "reviewed-literature-context-controls-and-primary-paper-pointers"
shared_canonical_dependency: "StegVerse-Labs/StegDB"
external_platform_automation_status: "unconfirmed-beyond-stegdb-sync"
full_adapter_ready: false
```
