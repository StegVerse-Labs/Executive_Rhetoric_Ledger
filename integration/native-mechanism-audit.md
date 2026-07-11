# Related Repository Native-Mechanism Audit

## Purpose

This audit must be completed before repository-specific adapters, scanners, classifiers, or archive paths are added to `Executive_Rhetoric_Ledger`.

The governing rule is:

```text
Discover and preserve the native mechanism first.
Integrate through its smallest compatible boundary.
Do not install duplicate scanners, competing categorizers, parallel archives, or replacement workflows without a governed deprecation decision.
```

## Audit dimensions

Each related repository must be reviewed for:

1. current README and declared purpose;
2. `*_MIRROR_HANDOFF.md` or equivalent task source of truth;
3. workflows and schedules;
4. source lists, queries, and providers;
5. ingestion contracts and entrypoints;
6. categorization, entity extraction, and clustering;
7. co-occurrence or relationship graphs;
8. archive, fingerprint, deduplication, and receipt behavior;
9. review, privacy, and admissibility boundaries;
10. exports and existing cross-repository relationships;
11. current failures, incomplete mechanisms, and workflow limits.

## Current audit status

| Repository | Audit state | Native mechanisms confirmed | Integration posture |
|---|---|---|---|
| `StegVerse-Labs/Trumpality` | partial-mechanism-audit | Evidence-first append-only records; weekly Monday ingest; Tuesday/Friday co-occurrence scan; native ingest contract; FREE-DOM relationship graph; explicit relationship to Administrations and Executive Rhetoric Ledger. | Reuse native ingest contract and produced records or graph outputs. Do not add a second scheduled source scanner. |
| `StegVerse-Labs/Administrations` | partial-mechanism-audit | Evidence-first append-only records by presidential term; declares reuse of the Trumpality ingest, archival, and FREE-DOM involvement engine; per-term records, seeds, and graph directories. | Treat as an institutional producer using shared biography infrastructure. Exact workflow and export paths still require discovery. |
| `StegVerse-Labs/Giuffre-ality` | partial-mechanism-audit | Biography repository; scheduled Tuesday/Friday co-occurrence scan delegated to the shared StegVerse-Core reusable workflow. | Consume or extend shared co-occurrence output only after output paths and privacy rules are identified. Do not duplicate the graph scan. |
| `StegVerse-Labs/Maxwellality` | partial-mechanism-audit | Biography repository; scheduled Monday weekly ingest delegated to the shared StegVerse-Core biography workflow. The workflow file is currently named `weekly-ingest.ym`, which must be treated as existing repository state rather than silently renamed during this audit. | Identify generated outputs and source seeds before integration. Do not install another weekly scanner. |
| `StegVerse-Labs/Epsteinality` | partial-mechanism-audit | Biography repository; scheduled Monday weekly ingest delegated to the shared StegVerse-Core biography workflow. | Identify generated outputs, source seeds, co-occurrence support, archival behavior, and privacy boundaries before integration. |
| `StegVerse-Labs/VAwatchdog` | pending-full-audit | Not yet reviewed. | Adapter construction blocked. |
| `StegVerse-Labs/StegScholar` | pending-full-audit | Not yet reviewed. | Adapter construction blocked. |
| `StegVerse-Labs/StegSocials` | pending-full-audit | Not yet reviewed. | Adapter construction blocked. |
| `StegVerse-Labs/Patents` | pending-full-audit | Not yet reviewed. | Adapter construction blocked. |
| `StegVerse-Labs/Talarico` | pending-full-audit | Not yet reviewed. | Adapter construction blocked. |
| `StegVerse-Labs/FREE-DOM_OverSight` | pending-full-audit | Not yet reviewed. | Adapter construction blocked. |
| `StegVerse-Labs/Randolph_Geneaology_Hub` | pending-full-audit | Not yet reviewed. | Adapter construction blocked. |
| `StegVerse-Labs/StegLearn` | pending-full-audit | Not yet reviewed. | Adapter construction blocked. |
| `StegVerse-Labs/StegBiography` | pending-full-audit | Not yet reviewed. | Adapter construction blocked. |

## Confirmed native mechanisms

### Trumpality

Purpose and standards:

- records verbatim statements, attributable actions, courts, and outcomes;
- requires primary sources where possible;
- secondary sources are limited to those citing primary documentation;
- records are append-only;
- uses a FREE-DOM graph for entities, events, dates, court filings, and source URLs.

Scheduled mechanisms:

```yaml
weekly_ingest:
  schedule: "0 7 * * 1"
  reusable_workflow: "StegVerse/StegVerse-Core/.github/workflows/bio-weekly-ingest.yml@main"
cooccurrence_scan:
  schedule: "15 8 * * 2,5"
  entrypoint: "CORE/cooccur/scan.py"
  output_behavior: "commits updated co-occurrence graph"
```

Native ingest contract:

```yaml
entrypoint: "CORE/ingest_pipeline/url_list_ingest.py"
subject: "Donald J. Trump"
topic_cluster_default: "general"
source_seed_glob: "seeds/sources.urls.txt"
default_cron: "0 7 * * 1"
```

### Administrations

- institutional scope by presidential term;
- declares reuse of the same ingest, archival, and FREE-DOM involvement engine as Trumpality;
- each term has its own `records/`, `seeds/`, and `freedom/` structures;
- preserves append-only corrections and primary-source standards.

The README references a weekly ingest, but the exact workflow path was not located during this first audit pass. That gap remains open rather than being filled by assumption.

### Giuffre-ality

```yaml
cooccurrence_scan:
  schedule: "15 8 * * 2,5"
  reusable_workflow: "StegVerse/StegVerse-Core/.github/workflows/bio-cooccurrence.yml@main"
```

The repository's brief README does not yet document source posture, privacy, archive, or output paths. Those must be established from current files and shared workflow behavior before integration.

### Maxwellality

```yaml
weekly_ingest:
  schedule: "0 7 * * 1"
  reusable_workflow: "StegVerse/StegVerse-Core/.github/workflows/bio-weekly-ingest.yml@main"
workflow_path_observed: ".github/workflows/weekly-ingest.ym"
```

### Epsteinality

```yaml
weekly_ingest:
  schedule: "0 7 * * 1"
  reusable_workflow: "StegVerse/StegVerse-Core/.github/workflows/bio-weekly-ingest.yml@main"
```

## Shared-mechanism implication

At least four related biography or political-record repositories use shared StegVerse-Core reusable workflows. The likely integration boundary is therefore not an independent scanner in each repository. It is one or more of:

- shared workflow output contracts;
- generated record directories;
- source seed manifests;
- co-occurrence graph outputs;
- archive receipts;
- producer exports into the ledger.

The shared `StegVerse/StegVerse-Core` workflow implementation must be audited before any adapter is activated.

## Current restrictions

Until the audit is complete:

- no related repository is classified as adapter-ready;
- no existing scheduled scan may be replaced;
- no duplicate schedule may be added;
- no current output directory may be reclassified without reading its consumers;
- no source categorization may be remapped without preserving existing labels and receipts;
- no biography, victim, witness, family, or private-person record may be exported without privacy review;
- no repository may self-authorize its evidence into the ledger.

## Next audit sequence

1. Audit the shared `StegVerse/StegVerse-Core` reusable workflows used by the biography repos.
2. Complete Trumpality output, archive, update-ingest, and monitor-path review.
3. Complete Administrations workflow and producer-export review.
4. Audit StegSocials for scheduled social-source discovery and categorization.
5. Audit the remaining oversight, scholarly, patent, public-figure, genealogy, educational, and biography repositories.
6. Only after each audit, assign one of:
   - `native-producer-ready`;
   - `publication-consumer-ready`;
   - `shared-engine-dependent`;
   - `manual-source-only`;
   - `privacy-restricted`;
   - `blocked-incomplete`.
