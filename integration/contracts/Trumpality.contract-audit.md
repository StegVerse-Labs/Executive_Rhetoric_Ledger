# Native Contract Audit: StegVerse-Labs/Trumpality

## Audit posture

```yaml
repository: "StegVerse-Labs/Trumpality"
audit_state: "contract-partial-repaired"
contract_state: "partially-verified"
adapter_state: "candidate-blocked"
reviewed_at: "2026-07-11"
```

This audit verifies the current native producer boundary without granting evidentiary standing or adapter activation.

## Declared repository contract

The native repository contract declares:

```yaml
repo_id: "stegverse.trumpality"
repo_type: "subject_audit"
subject: "Donald J. Trump"
modes:
  biography: true
  rhetoric_action_ledger: true
outputs:
  primary_records_path: "records"
  graph_path: "freedom"
  exports_path: "datasets/exports"
```

The governance contract requires reputable sourcing, permits secondary sources only when they cite primary material, requires verbatim statements, preserves append-only records, prohibits private-person doxxing, and requires confirmed-versus-alleged labels.

## Verified scheduled inputs

### Weekly ingest

```yaml
schedule: "0 7 * * 1"
subject: "Donald J. Trump"
topic_cluster: "general"
seed_file: "seeds/sources.urls.txt"
database: "data/processed/records.sqlite"
```

The ingest pipeline:

1. reads non-comment URLs from the seed file;
2. retrieves HTML with a declared user agent and timeout;
3. extracts page title and description;
4. records source domain, source confidence, verification label, and seed tag;
5. writes records into the SQLite records table.

## Verified co-occurrence mechanism

```yaml
schedule: "15 8 * * 2,5"
input_database: "data/processed/records.sqlite"
optional_input: "quarantine table"
output_database_table: "cooccurrence"
report: "data/processed/cooccurrence_report.csv"
window_hours: 6
```

The mechanism groups recent records and optional quarantine items into overlapping time/place windows. It calculates a bounded heuristic from unique source domains and verification labels. This score is a research-priority signal only; it does not establish causation, coordination, participation, or truth.

## Exact executable-path repairs

The repository stores its implementation under lowercase `core/`, but multiple workflows and scripts referenced uppercase `CORE/`. The co-occurrence implementation directory is currently `core/coocur/`, while the workflow referenced `CORE/cooccur/`.

The following references were repaired without changing cadence, evidence policy, schema meaning, or outputs:

- `.github/workflows/update-ingests.yml`
- `.github/workflows/cooccurrence.yml`
- `scripts/run_ingest.sh`
- `core/ingest_pipeline/url_list_ingest.py`
- `core/ingest_pipeline/base_ingest.py`
- `core/coocur/scan.py`

Repair commits in Trumpality:

- `13585e234d124a08a6b355b220bc97d0566143f8`
- `7648cb9c1524309ea8688aa3b3cac47d270be2dc`
- `0fe22d056084f0f6ab3e43ca24934f478e234d50`
- `bde903fd1498026516e01e606e30bdc59f6036cd`
- `db8b6f9759661ba39cd80919008cdc85f949a1ae`
- `b8689c5b9aa5c5b8e1a9c85fd2113239bb016c95`

## Remaining contract blockers

### Archive and monitor implementation unresolved

The scheduled workflow declares:

```yaml
schedule: "0 8 * * 2,5"
archiver: "CORE/archival/archiver.py"
link_monitor: "CORE/archival/monitor_links.py"
schema_patch: "CORE/schema_patch.sql"
```

The corresponding implementation files were not located during this audit. The workflow must not be treated as operational until the files, outputs, failure behavior, and archive receipts are verified.

### Export contract unresolved

The repository contract declares `datasets/exports`, but no producer-export object, receipt format, callback, or downstream consumer was verified during this pass.

### Record identity and deduplication limitation

The ingest pipeline generates a new UUID by default and uses `INSERT OR REPLACE` by record ID. The audit did not verify URL-level, content-hash, or claim-level deduplication. Repeated ingestion may therefore create semantically duplicate records unless another unobserved layer prevents it.

### Retrieval failure visibility

Individual fetch failures are printed as `skip:` and ingestion continues. No structured failure receipt, retry posture, or unresolved-source queue was verified.

### Source categorization limitation

Seed URL inputs are currently assigned the fixed category `investigative_report`. This is an ingestion label, not a verified source-type or claim-role determination.

## Smallest compatible ledger boundary

```text
Trumpality native record or graph candidate
-> producer export preserving source URL, record ID, verification label, timestamps, and native path
-> Executive Rhetoric Ledger candidate intake
-> Source Posture translation and deduplication
-> governed review
```

The ledger must not read the SQLite database as an accepted-fact store or treat the co-occurrence strength score as evidence of causation.

## Adapter activation requirements

The adapter may not advance from `candidate-blocked` until all of the following are verified:

- a durable producer-export format;
- stable record identity and deduplication behavior;
- archive and link-monitor outputs;
- structured failure and unresolved-source receipts;
- correction and supersession behavior;
- downstream consumer and acknowledgment path;
- privacy and sensitive-record filtering;
- a complete successful native workflow run after the path repairs.
