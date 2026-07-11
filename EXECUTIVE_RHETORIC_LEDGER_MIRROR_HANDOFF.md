# Executive Rhetoric Ledger Mirror Handoff

## Current task source of truth

The validated repository foundation is green. The active goal is building an automated, evidence-backed historical compendium of politically significant rhetoric, action, institutional response, and measurable consequence.

Fourteen related repositories are declared. Adapter construction remains blocked until each repository's native mechanisms and external platform interactions are audited.

## Governing integration rule

```text
Discover and preserve the native mechanism first.
Audit the external platforms that supply, alter, remove, rank, correct, or publish data.
Integrate through the smallest compatible boundary.
Do not install duplicate scanners, competing categorizers, parallel archives, or replacement workflows without a governed deprecation decision.
```

## Current integration records

- Relationship manifest: `integration/related-repositories.json`
- Relationship map: `integration/related-repositories.md`
- Native-mechanism audit: `integration/native-mechanism-audit.md`
- Per-repository audit index: `integration/audits/README.md`
- StegSocials audit: `integration/audits/StegSocials.md`
- VAwatchdog audit: `integration/audits/VAwatchdog.md`
- StegScholar audit: `integration/audits/StegScholar.md`
- Patents audit: `integration/audits/Patents.md`
- Network schema: `schemas/related-repository-network.schema.json`
- Network validator: `scripts/validate_related_repository_network.py`

## Expanded audit dimensions

Each related repository must be reviewed for:

- current README and purpose;
- `*_MIRROR_HANDOFF.md` or equivalent task source of truth;
- workflows and schedules;
- external platforms and institutional systems that act as data sources or publication surfaces;
- source lists, queries, APIs, feeds, browser capture, email, webhooks, and manual intake paths;
- ingest contracts and entrypoints;
- categorization, clustering, and relationship mapping;
- archive, fingerprint, deduplication, and receipt mechanisms;
- handling of edits, deletions, moderation, corrections, changed account state, amended publications, and amended records;
- privacy, review, and admissibility boundaries;
- exports and existing cross-repository relationships;
- current failures and workflow limits.

## Audit progress

```yaml
related_repositories_declared: 14
full_audits_complete: 0
partial_mechanism_and_platform_audits: 9
pending_full_audits: 5
active_repository_adapters: 0
adapter_construction: "blocked-pending-native-and-platform-capability-review"
replacement_of_existing_automation: "prohibited-without-governed-deprecation"
```

## Newly confirmed StegScholar posture

StegScholar is a scholarly-context and control producer with a daily StegDB canonical-overlay sync.

```yaml
workflow: ".github/workflows/sync-overlay-from-stegdb.yml"
schedule: "17 3 * * *"
source: "stegverse-labs/stegdb/canonical/overlays/StegScholarOverlay/canon"
destination: "canon/"
classification: "scheduled-canonical-sync-scholarly-context-producer-partial"
```

Its external source environments include scholarly submission systems, preprint servers, DOI and citation registries, journal and conference platforms, institutional repositories, publisher correction and retraction systems, and academic search engines.

Peer review, citation counts, venue prestige, and search rank are source-posture signals, not proof. Preprint, accepted manuscript, version of record, correction, and retraction states must remain distinct.

No duplicate StegDB sync or parallel `canon/` writer may be added.

## Newly confirmed Patents posture

Patents is a patent-monitoring and portfolio producer with a daily StegDB canonical-overlay sync, a native patent manifest, declared repository watcher, templates, allowlists, exclusions, and deadline policy.

```yaml
workflow: ".github/workflows/sync-overlay-from-stegdb.yml"
schedule: "23 3 * * *"
source: "stegverse-labs/stegdb/canonical/overlays/PatentsOverlay/canon"
destination: "canon/"
manifest: "patent_manifest.json"
patent_watcher: "declared; current workflow implementation unaudited"
classification: "scheduled-canonical-sync-patent-monitoring-and-portfolio-producer-partial"
```

Its external source environments include GitHub history, USPTO, WIPO, patent search systems, assignment records, prosecution histories, prior-art sources, standards repositories, papers, products, and legal filing systems.

A repository change does not establish inventorship, novelty, ownership, reduction to practice, deployment, effectiveness, patentability, or political influence. Automated filing and public export of confidential invention material remain prohibited.

No duplicate repository watcher, deadline engine, portfolio manifest, or StegDB sync may be added.

## Previously corrected platform postures

- StegSocials is both a governed publication system and a platform-source intake environment. Broad autonomous scanning remains unconfirmed.
- VAwatchdog is a platform-interacting, privacy-restricted accountability intake. Automated institutional-record retrieval remains unconfirmed.
- At least four biography or political-record repositories depend on shared reusable workflows in `StegVerse/StegVerse-Core`; that shared implementation or durable output contract remains unaudited.

## Pending audits

- `StegVerse-Labs/Talarico`
- `StegVerse-Labs/FREE-DOM_OverSight`
- `StegVerse-Labs/Randolph_Geneaology_Hub`
- `StegVerse-Labs/StegLearn`
- `StegVerse-Labs/StegBiography`

## Current next integration goal

```text
complete native-mechanism and platform-source audits
  -> identify shared engines and output contracts
  -> classify each repository capability
  -> design minimal compatible adapters
  -> discovery-cycle manifest
  -> recurring source-search federation
  -> archive and receipt exchange
  -> deduplication and clustering
  -> adjacency and historical graph generation
  -> governed review and compendium update
```

## Required follow-on work

Destination: `StegVerse-Labs/Executive_Rhetoric_Ledger`

- Complete the five remaining repository and platform audits.
- Audit the shared StegVerse-Core biography ingest and co-occurrence workflows or obtain their output contracts.
- Complete Trumpality archive, update-ingest, monitor, platform-source, and export-path review.
- Locate and review the Administrations workflow, platform sources, and producer-export paths.
- Determine StegSocials platform capture, archive, deduplication, account-authenticity, and scheduled discovery mechanisms.
- Determine VAwatchdog institutional-platform query, retrieval, FOIA, archive, redaction, and update mechanisms.
- Determine StegScholar DOI, submission, correction, retraction, bibliography, and downstream `canon/` contracts.
- Locate and audit the Patents Patent Watcher implementation, dry-run boundary, deadline outputs, filing-platform integrations, confidentiality controls, and downstream contracts.
- Build adapters only after native and external-platform boundaries are documented.

## Release posture

The ledger foundation and relationship network are validated. The automated compendium goal remains incomplete. Existing repository automation and external-platform relationships must be federated, not duplicated.

## Archive readiness

This handoff contains the current validated foundation, relationship network, nine partial audits, platform-source classifications, scheduled canonical syncs, shared-engine dependencies, integration restrictions, and remaining audit work. Earlier conversation context is not required; the complete thread is ready for archiving.
