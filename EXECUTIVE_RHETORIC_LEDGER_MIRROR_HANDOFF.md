# Executive Rhetoric Ledger Mirror Handoff

## Current task source of truth

The validated repository foundation is green. The active goal is building an automated, evidence-backed historical compendium of politically significant rhetoric, action, institutional response, and measurable consequence.

Fourteen related repositories are declared, but adapter construction is blocked until each repository's native mechanisms are audited.

## Governing integration rule

```text
Discover and preserve the native mechanism first.
Integrate through its smallest compatible boundary.
Do not install duplicate scanners, competing categorizers, parallel archives, or replacement workflows without a governed deprecation decision.
```

## Current integration records

- Relationship manifest: `integration/related-repositories.json`
- Relationship map: `integration/related-repositories.md`
- Native-mechanism audit: `integration/native-mechanism-audit.md`
- Network schema: `schemas/related-repository-network.schema.json`
- Network validator: `scripts/validate_related_repository_network.py`

## Audit dimensions

Each related repository must be reviewed for:

- current README and purpose;
- `*_MIRROR_HANDOFF.md` or equivalent task source of truth;
- workflows and schedules;
- source lists, queries, and providers;
- ingest contracts and entrypoints;
- categorization, clustering, and relationship mapping;
- archive, fingerprint, deduplication, and receipt mechanisms;
- privacy, review, and admissibility boundaries;
- exports and existing cross-repository relationships;
- current failures and workflow limits.

## Audit progress

```yaml
related_repositories_declared: 14
full_audits_complete: 0
partial_mechanism_audits: 5
pending_full_audits: 9
active_repository_adapters: 0
adapter_construction: "blocked-pending-native-capability-review"
replacement_of_existing_automation: "prohibited-without-governed-deprecation"
```

### Partially audited repositories

#### `StegVerse-Labs/Trumpality`

Confirmed:

- evidence-first, append-only statement/action/court/outcome records;
- primary-source preference and disconfirming-case preservation;
- Monday weekly ingest through `StegVerse/StegVerse-Core/.github/workflows/bio-weekly-ingest.yml@main`;
- Tuesday/Friday co-occurrence scan through `CORE/cooccur/scan.py`;
- native `contracts/ingest.contract.yml` using `CORE/ingest_pipeline/url_list_ingest.py`;
- seed input at `seeds/sources.urls.txt`;
- FREE-DOM entity/event/court/source graph;
- explicit relationship with Administrations and Executive Rhetoric Ledger.

Integration implication: reuse the ingest contract, generated records, archive outputs, or co-occurrence graph. Do not install a second scheduled scanner.

#### `StegVerse-Labs/Administrations`

Confirmed:

- append-only institutional records by presidential term;
- declared reuse of Trumpality's ingest, archive, and FREE-DOM engine;
- per-term `records/`, `seeds/`, and `freedom/` structures;
- primary-source and correction standards.

Open gap: README references weekly ingest, but the exact workflow path was not located in the first pass. Do not infer or add one.

#### `StegVerse-Labs/Giuffre-ality`

Confirmed:

- person-centered biography purpose;
- Tuesday/Friday co-occurrence scan through the shared `bio-cooccurrence.yml` reusable workflow.

Open gaps: source posture, output paths, archive behavior, privacy controls, and review boundaries.

#### `StegVerse-Labs/Maxwellality`

Confirmed:

- person-centered factual biography purpose;
- Monday weekly ingest through the shared `bio-weekly-ingest.yml` reusable workflow;
- observed workflow path `.github/workflows/weekly-ingest.ym`.

Open gaps: generated outputs, source seeds, archive behavior, co-occurrence support, and privacy controls. The unusual `.ym` path is preserved as current state and must not be silently renamed during audit.

#### `StegVerse-Labs/Epsteinality`

Confirmed:

- person-centered biography purpose;
- Monday weekly ingest through the shared `bio-weekly-ingest.yml` reusable workflow.

Open gaps: generated outputs, source seeds, co-occurrence support, archive behavior, and privacy controls.

## Shared-engine dependency

At least four related repositories delegate recurring ingest or co-occurrence work to reusable workflows in `StegVerse/StegVerse-Core`.

The attempted direct fetch of `.github/workflows/bio-weekly-ingest.yml` from that repository returned `Not Found` through the current connector. This does not prove the workflow is absent; it means the implementation remains unaudited from this session.

Adapter design must therefore remain blocked until the shared workflow implementation or its durable output contract is available.

## Pending full audits

- `StegVerse-Labs/VAwatchdog`
- `StegVerse-Labs/StegScholar`
- `StegVerse-Labs/StegSocials`
- `StegVerse-Labs/Patents`
- `StegVerse-Labs/Talarico`
- `StegVerse-Labs/FREE-DOM_OverSight`
- `StegVerse-Labs/Randolph_Geneaology_Hub`
- `StegVerse-Labs/StegLearn`
- `StegVerse-Labs/StegBiography`

## Current next integration goal

```text
complete native-mechanism audits
  -> identify shared engines and output contracts
  -> classify each repository capability
  -> design minimal compatible adapters
  -> discovery-cycle manifest
  -> recurring source search federation
  -> archive and receipt exchange
  -> deduplication and clustering
  -> adjacency and historical graph generation
  -> governed review and compendium update
```

## Required follow-on work

Destination: `StegVerse-Labs/Executive_Rhetoric_Ledger`

- Complete all fourteen native-mechanism audits.
- Audit the shared StegVerse-Core biography ingest and co-occurrence workflows or obtain their output contracts.
- Complete Trumpality archive, update-ingest, monitor, and export-path review.
- Locate and review the Administrations workflow and producer-export paths.
- Prioritize StegSocials because it may already perform scheduled social-source scanning and categorization.
- Classify each repo as one of:
  - `native-producer-ready`;
  - `publication-consumer-ready`;
  - `shared-engine-dependent`;
  - `manual-source-only`;
  - `privacy-restricted`;
  - `blocked-incomplete`.
- Build adapters only after classification and contract review.

## Release posture

The ledger foundation and relationship network are validated. The automated compendium goal remains incomplete. Existing repository automation must be federated, not duplicated.

## Archive readiness

This handoff contains the current validated foundation, relationship network, partial native-mechanism audit, confirmed scheduled scans, shared-engine dependency, integration restrictions, and remaining audit work. Earlier conversation context is not required; the complete thread is ready for archiving.
