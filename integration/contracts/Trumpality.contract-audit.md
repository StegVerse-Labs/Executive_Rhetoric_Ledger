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

## Verified native producer mechanisms

### Weekly ingest

```yaml
schedule: "0 7 * * 1"
workflow: ".github/workflows/weekly-ingest.yml"
authority: "shared StegVerse-Core reusable workflow"
seed_file: "seeds/sources.urls.txt"
database: "data/processed/records.sqlite"
```

The separate native ingest workflow is manual-only to avoid duplicate Monday scans. The native pipeline uses URL-level identity reuse, emits append-only success and failure receipts, and defers source-role classification to governed review.

### Archive and link health

```yaml
schedule: "0 8 * * 2,5"
workflow: ".github/workflows/archive-and-monitor.yml"
archiver: "core/archival/archiver.py"
link_monitor: "core/archival/monitor_links.py"
local_snapshot_path: "data/archive/html"
archive_receipts: "data/receipts/archive_receipts.jsonl"
link_health_receipts: "data/receipts/link_health_receipts.jsonl"
```

The archiver writes local snapshots and SHA-256 hashes and records optional Internet Archive submission only as a request posture. Link health changes availability posture only; it does not determine whether a claim is true.

### Co-occurrence

```yaml
schedule: "15 8 * * 2,5"
input_database: "data/processed/records.sqlite"
optional_input: "quarantine table"
output_database_table: "cooccurrence"
report: "data/processed/cooccurrence_report.csv"
window_hours: 6
```

The bounded score is a research-priority signal. It does not establish causation, coordination, participation, or truth.

## Verified producer-export boundary

```yaml
contract: "contracts/executive-rhetoric-ledger-export.contract.yml"
exporter: "core/exports/export_ledger_candidates.py"
output_path: "datasets/exports/executive-rhetoric-ledger"
export_receipts: "data/receipts/export_receipts.jsonl"
consumer: "StegVerse-Labs/Executive_Rhetoric_Ledger"
```

Every emitted object is bounded as a pending, context-only candidate with no evidence effect until ledger review. Unknown source type, institutional proximity, claim role, and factual use remain unknown until review.

## Verified acknowledgment return boundary

Ledger-side files:

- `schemas/producer-acknowledgment.schema.json`
- `scripts/validate_producer_acknowledgments.py`
- `producer_acknowledgments/example/trumpality-context-initial.json`
- `producer_acknowledgments/example/trumpality-context-correction.json`

Producer-side files:

- `contracts/executive-rhetoric-ledger-acknowledgment.contract.yml`
- `core/exports/import_ledger_acknowledgment.py`
- `data/receipts/ledger_acknowledgments/`
- `data/receipts/ledger_acknowledgments.jsonl`
- `data/receipts/ledger_acknowledgment_current.json`

The return importer:

1. verifies producer and ledger identity;
2. preserves every acknowledgment object;
3. appends a receipt rather than rewriting history;
4. enforces correction and supersession against the current acknowledgment;
5. permits only one current acknowledgment per `ingestion_id`;
6. never mutates native source records or verification labels.

The example round trip proves schema and succession mechanics only. It is not evidence that a live cross-repository transfer has occurred.

## Exact repairs and additions

Trumpality execution and producer commits include:

- `13585e234d124a08a6b355b220bc97d0566143f8` through `b8689c5b9aa5c5b8e1a9c85fd2113239bb016c95` — executable path repairs
- `e4616b0ac5f67c439ba5c8b4123c9816c2a5e5ce` — archive implementation and receipts
- `825268edf6ed866cf2554cfe7b6e1da0112141f3` — link-health monitoring and receipts
- `c7421cd18a510a44b92a8c7562d14459196365f5` — URL-level identity reuse
- `24e2574483a5f7a988eb5d087c2cc50220974d05` — durable ingest receipts and deferred classification
- `fc39c22984c752c6bcc2186c6d4c80f0eba82ff9` — duplicate schedule removed
- `49e4609fb6f1b250a29a4550ae806cc61bee1944` — archive-stage export integration
- `10a84c5552d7b4e1487ecd99ff3a3171f26698e1` — acknowledgment return contract
- `068e5de80b2c53b98d1383f74374d77f4093a6ad` — append-only acknowledgment importer

Ledger acknowledgment commits include:

- `a1463de5af99e4410da4bc218f1c85aa1e4eece5` — acknowledgment schema
- `ea6bd9a449c199e27e5fdf1fcd3fa927601881c4` — initial decision example
- `e53d31b1ffe4cd78c4a719e7e06164ff06c1ca5b` — correction example
- `f587ed0cbb2bc34eeb5f2cc3daf5f3523ab9628c` — succession validator
- `8f903d707f144f00ba28bc4841cd4263f35edea3` and `a5c506fece9e871276dbb1343a767d71b3dda144` — activation-chain integration

## Remaining contract blockers

Trumpality remains `candidate-blocked` because:

- no complete successful shared weekly ingest and archive/monitor run is attached after the repairs;
- no producer export from an observed native run has passed ledger validation;
- no live acknowledgment has crossed repositories and been recorded by the producer importer;
- the correction example validates succession mechanics, but a live correction/supersession round trip remains unobserved;
- URL-level deduplication exists, while content-hash and claim-level duplicate handling remain unresolved;
- privacy and sensitive-record filtering has not been tested against representative records;
- shared StegVerse-Core weekly ingest behavior remains partially unaudited.

## Smallest compatible boundary

```text
Trumpality native record
-> archive and health receipts
-> pending context-only producer export
-> ledger validation and governed review
-> acknowledgment or correction
-> append-only producer receipt
```

The SQLite database, archive status, confidence score, repository origin, and co-occurrence strength must never be treated as accepted-fact stores or independent proof.
