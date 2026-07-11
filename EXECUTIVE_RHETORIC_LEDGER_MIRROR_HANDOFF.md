# Executive Rhetoric Ledger Mirror Handoff

## Current task source of truth

The validated repository foundation is green. The active goal is building an automated, evidence-backed historical compendium of politically significant rhetoric, action, institutional response, and measurable consequence.

All fourteen declared related repositories have initial native-mechanism and external-platform audits. The repository now separates:

```text
observed capability
-> machine capability record
-> native contract audit
-> verified producer or consumer boundary
-> adapter readiness
-> governed evidence intake
```

Generic adapter construction remains prohibited.

## Governing integration rule

```text
Discover and preserve the native mechanism first.
Audit external platforms that supply, alter, remove, rank, correct, or publish data.
Record observed capability separately from verified contracts.
Repair exact native defects without weakening evidence or governance boundaries.
Integrate through the smallest compatible boundary.
Do not duplicate scanners, categorizers, archives, canonical writers, or publication state machines without governed deprecation.
```

## Current integration records

- Relationship manifest: `integration/related-repositories.json`
- Relationship map: `integration/related-repositories.md`
- Native-mechanism audit: `integration/native-mechanism-audit.md`
- Per-repository audit index: `integration/audits/README.md`
- Capability registry: `integration/repository-capabilities.json`
- Capability schema: `schemas/repository-capability-registry.schema.json`
- Capability validator: `scripts/validate_repository_capabilities.py`
- Contract-audit registry: `integration/repository-contract-audits.json`
- Contract-audit schema: `schemas/repository-contract-audit.schema.json`
- Contract-audit validator: `scripts/validate_repository_contract_audits.py`
- Trumpality contract audit: `integration/contracts/Trumpality.contract-audit.md`

## Progress

```yaml
related_repositories_declared: 14
partial_mechanism_and_platform_audits: 14
machine_capability_records: 14
machine_contract_audit_records: 1
full_contract_audits_complete: 0
adapter_candidates:
  - "StegVerse-Labs/Trumpality"
adapter_ready: 0
active_repository_adapters: 0
adapter_construction: "blocked-pending-contract-output-receipt-failure-and-consumer-verification"
```

## Trumpality contract verification

The first detailed native contract audit is installed.

Verified native inputs and mechanisms include:

- Monday seed ingest from `seeds/sources.urls.txt`;
- subject and topic-cluster parameters;
- SQLite record storage at `data/processed/records.sqlite`;
- Tuesday/Friday co-occurrence processing;
- optional quarantine-table input;
- co-occurrence table and CSV report output;
- declared record, graph, and export paths;
- native repository and governance contracts.

### Exact native repairs

The implementation tree is lowercase `core/`, but multiple workflow and script references used uppercase `CORE/`. The co-occurrence implementation directory is `core/coocur/`, while the workflow referenced `cooccur/`.

The following Trumpality files were repaired without changing schedules, evidence labels, source rules, database meaning, or output posture:

- `.github/workflows/update-ingests.yml`
- `.github/workflows/cooccurrence.yml`
- `scripts/run_ingest.sh`
- `core/ingest_pipeline/url_list_ingest.py`
- `core/ingest_pipeline/base_ingest.py`
- `core/coocur/scan.py`

Repair commits:

- `13585e234d124a08a6b355b220bc97d0566143f8`
- `7648cb9c1524309ea8688aa3b3cac47d270be2dc`
- `0fe22d056084f0f6ab3e43ca24934f478e234d50`
- `bde903fd1498026516e01e606e30bdc59f6036cd`
- `db8b6f9759661ba39cd80919008cdc85f949a1ae`
- `b8689c5b9aa5c5b8e1a9c85fd2113239bb016c95`

No complete successful workflow result is attached after these repairs, so the repair is not yet claimed green.

## Trumpality remaining blockers

- Archive and monitor workflow refers to implementation files not located during the audit.
- No structured archive receipt is verified.
- No producer-export object or callback contract is verified.
- No downstream consumer acknowledgment path is verified.
- No URL-level, content-hash, or claim-level deduplication is verified.
- Fetch failures print `skip:` but do not produce structured unresolved-source receipts.
- Seed records receive the fixed category `investigative_report` before governed source-role review.
- No complete post-repair native workflow run is attached.

Trumpality therefore remains:

```yaml
contract_state: "partially-verified"
adapter_state: "candidate-blocked"
```

## Contract-audit governance

```text
A repaired path does not make a contract verified.
A declared output path is not a verified output until production and consumption are observed.
A heuristic score is not proof.
A verified contract does not authorize ledger acceptance.
```

The contract-audit validator enforces:

- repository membership in the capability registry;
- unique contract-audit records;
- existing human-readable audit references;
- verified contracts must have non-empty inputs, outputs, receipts, consumers, and failure handling;
- verified contracts cannot retain blockers;
- ready or active adapters require verified contracts;
- repaired-partial audits require concrete repair records.

## Validation integration

The existing activation chain now includes:

```text
validate_repository_capabilities.py
-> validate_repository_contract_audits.py
-> run_activation_validation.py
-> validate-ledger-schemas.yml
```

No new workflow was created.

The latest commit status queries returned no attached status checks. Do not claim the expanded validation chain or Trumpality native repairs are green until complete runs are available.

## Current next integration goal

```text
confirm Trumpality post-repair workflow execution
-> resolve archive and monitor implementation
-> define durable producer export and receipt
-> verify deduplication correction and failure queues
-> identify downstream acknowledgment consumer
-> complete Administrations contract audit
-> audit shared StegVerse-Core biography workflows
-> resolve StegSocials callback contract
-> select first low-risk federated integration
```

## Required follow-on work

Destination: `StegVerse-Labs/Executive_Rhetoric_Ledger`

- Confirm the expanded validation chain is green.
- Confirm Trumpality weekly ingest and co-occurrence workflows complete after the path repairs.
- Locate or repair Trumpality archive, link-monitor, and schema-patch implementations.
- Define and verify Trumpality producer-export, archive-receipt, unresolved-source, deduplication, correction, and acknowledgment contracts.
- Locate Administrations workflows and producer outputs.
- Audit the shared `StegVerse/StegVerse-Core` biography ingest and co-occurrence workflows or obtain durable output contracts.
- Determine StegSocials platform capture, archive, deduplication, account-authenticity, scheduled discovery, and callback contracts.
- Determine VAwatchdog and FREE-DOM_OverSight retrieval, redaction, promotion, archive, failure, and update contracts.
- Determine StegScholar and Patents downstream canonical-output consumers and correction propagation.
- Do not activate adapters until native contracts, failures, receipts, privacy boundaries, and consumers are verified.

## Release posture

The ledger foundation, relationship network, fourteen initial audits, capability registry, first detailed contract audit, contract schema, validator, and activation-chain integration are installed. Trumpality execution-path defects were repaired, but its contract remains partial and no adapter is active.

## Archive readiness

This handoff contains the validated foundation, repository audits, capability registry, first contract audit, exact Trumpality repairs, remaining blockers, validation integration, and next contract-verification work. Earlier conversation context is not required; the complete thread is ready for archiving.
