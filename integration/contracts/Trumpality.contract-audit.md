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
workflow: ".github/workflows/weekly-ingest.yml"
authority: "shared StegVerse-Core reusable workflow"
subject: "Donald J. Trump"
topic_cluster: "general"
seed_file: "seeds/sources.urls.txt"
database: "data/processed/records.sqlite"
```

The separate native ingest workflow is now manual-only to avoid duplicate Monday scans. It remains available for governed recovery and testing.

The native ingest pipeline:

1. reads non-comment URLs from the seed file;
2. retrieves HTML with a declared user agent and timeout;
3. extracts page title and description;
4. records source domain, source confidence, verification label, and seed tag;
5. uses URL-level identity reuse to refresh an existing record rather than create a new UUID for the same URL;
6. emits append-only JSONL success or failure receipts;
7. marks source role and category as pending governed review rather than presuming `investigative_report`.

## Verified archive and link-health mechanism

```yaml
schedule: "0 8 * * 2,5"
workflow: ".github/workflows/archive-and-monitor.yml"
archiver: "core/archival/archiver.py"
link_monitor: "core/archival/monitor_links.py"
local_snapshot_path: "data/archive/html"
archive_receipts: "data/receipts/archive_receipts.jsonl"
link_health_receipts: "data/receipts/link_health_receipts.jsonl"
```

The archiver retrieves source content, writes a local HTML snapshot, computes SHA-256, updates archive metadata, optionally submits a save request to the Internet Archive, and emits a durable receipt. Internet Archive submission is recorded as a request posture rather than proof of completed archival custody.

The link monitor records URL availability, status code, check time, and error state. Link health changes availability posture only; it does not change whether the underlying claim is true.

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

## Verified producer-export boundary

```yaml
contract: "contracts/executive-rhetoric-ledger-export.contract.yml"
exporter: "core/exports/export_ledger_candidates.py"
output_path: "datasets/exports/executive-rhetoric-ledger"
export_receipts: "data/receipts/export_receipts.jsonl"
consumer: "StegVerse-Labs/Executive_Rhetoric_Ledger"
consumer_acknowledgment_path: "producer_exports/acknowledgments/Trumpality"
```

Every emitted object is deliberately bounded as:

```yaml
object_class: "source_receipt"
claimed_use: "context-only"
admissibility_request: "context-only"
review_status: "pending"
evidence_effect: "none-until-ledger-review"
```

The export preserves native record identity, source URL, title, attribution, timestamps, archive reference when available, verification label, confidence, producer path, and producer commit. Unknown source type and institutional proximity remain unknown until ledger review.

## Exact repairs and additions

Executable-path repairs:

- `13585e234d124a08a6b355b220bc97d0566143f8`
- `7648cb9c1524309ea8688aa3b3cac47d270be2dc`
- `0fe22d056084f0f6ab3e43ca24934f478e234d50`
- `bde903fd1498026516e01e606e30bdc59f6036cd`
- `db8b6f9759661ba39cd80919008cdc85f949a1ae`
- `b8689c5b9aa5c5b8e1a9c85fd2113239bb016c95`

Archive, receipt, deduplication, export, and duplicate-schedule repairs:

- `e4616b0ac5f67c439ba5c8b4123c9816c2a5e5ce` — archive implementation and receipts
- `825268edf6ed866cf2554cfe7b6e1da0112141f3` — link-health monitoring and receipts
- `c7421cd18a510a44b92a8c7562d14459196365f5` — URL-level identity reuse
- `24e2574483a5f7a988eb5d087c2cc50220974d05` — durable ingest receipts and deferred classification
- `e4e5862b656ab5a223b8b8575c78468dff14582a` — archive workflow activation
- `2bdd14154d05ad011be321cab48a7b791bae1d0c` — ledger export contract
- `8840c02effec9af49420741c821e009c0df29244` — conservative producer exporter
- `fc39c22984c752c6bcc2186c6d4c80f0eba82ff9` — duplicate schedule removed; manual fallback retained
- `49e4609fb6f1b250a29a4550ae806cc61bee1944` — archive-stage export integration

## Remaining contract blockers

Trumpality remains `candidate-blocked` because:

- no complete successful native workflow run has been attached after the repairs;
- no real producer export has yet been validated against the ledger schema from an observed run;
- no downstream ledger acknowledgment object has yet been produced and returned;
- correction and supersession behavior across producer exports and acknowledgments remains untested;
- URL-level deduplication is verified, but content-hash and claim-level deduplication remain unresolved;
- privacy and sensitive-record filtering is declared but not yet tested against representative records;
- shared StegVerse-Core weekly ingest behavior and output compatibility remain only partially visible.

## Smallest compatible ledger boundary

```text
Trumpality native record
-> local archive and health receipts
-> pending context-only producer export
-> Executive Rhetoric Ledger schema validation
-> Source Posture and duplicate review
-> governed acceptance, correction request, or rejection
-> acknowledgment returned to Trumpality
```

The ledger must not read the SQLite database as an accepted-fact store or treat archive success, confidence score, repository origin, or co-occurrence strength as proof.

## Adapter activation requirements

The adapter may not advance from `candidate-blocked` until all of the following are observed and verified:

- a complete successful shared weekly ingest and archive/monitor run;
- at least one real producer export passing ledger validation;
- a durable ledger acknowledgment returned to the producer;
- correction and supersession round-trip behavior;
- content-hash or claim-level duplicate handling at the ledger boundary;
- privacy filtering tests;
- no unresolved workflow path or shared-engine compatibility failure.
