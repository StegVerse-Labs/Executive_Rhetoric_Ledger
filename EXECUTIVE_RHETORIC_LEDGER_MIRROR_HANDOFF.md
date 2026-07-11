# Executive Rhetoric Ledger Mirror Handoff

## Current task source of truth

The validated repository foundation is green. The active goal is building an automated, evidence-backed historical compendium of politically significant rhetoric, action, institutional response, and measurable consequence.

All fourteen declared related repositories have an initial native-mechanism and external-platform audit. Generic adapter construction remains prohibited. The repository now contains a machine-readable capability and contract-audit registry that distinguishes observed capability from verified integration authority.

## Governing integration rule

```text
Discover and preserve the native mechanism first.
Audit the external platforms that supply, alter, remove, rank, correct, or publish data.
Record observed capability separately from verified contracts.
Integrate through the smallest compatible boundary.
Do not install duplicate scanners, competing categorizers, parallel archives, or replacement workflows without a governed deprecation decision.
```

## Current integration records

- Relationship manifest: `integration/related-repositories.json`
- Relationship map: `integration/related-repositories.md`
- Native-mechanism audit: `integration/native-mechanism-audit.md`
- Per-repository audit index: `integration/audits/README.md`
- Repository-specific audits under `integration/audits/`
- Capability registry: `integration/repository-capabilities.json`
- Capability registry schema: `schemas/repository-capability-registry.schema.json`
- Capability validator: `scripts/validate_repository_capabilities.py`
- Network schema: `schemas/related-repository-network.schema.json`
- Network validator: `scripts/validate_related_repository_network.py`

## Capability-registry rules

The registry records:

- repository capability classes;
- confirmed native mechanisms;
- external platform classes;
- verified inputs and outputs;
- contract state;
- privacy posture;
- adapter state;
- prohibited changes;
- audit references.

```text
Capability declaration != evidentiary standing.
Observed mechanism != verified contract.
Verified contract != adapter activation.
Adapter activation != authority to accept evidence.
```

An adapter may advance to `ready` or `active` only when its contract state is `verified`, with verified inputs and outputs. The registry validator enforces this boundary.

## Audit and registry progress

```yaml
related_repositories_declared: 14
partial_mechanism_and_platform_audits: 14
pending_initial_audits: 0
machine_capability_records: 14
full_contract_audits_complete: 0
adapter_candidates:
  - "StegVerse-Labs/Trumpality"
active_repository_adapters: 0
adapter_construction: "blocked-pending-contract-and-output-verification"
replacement_of_existing_automation: "prohibited-without-governed-deprecation"
```

`Trumpality` is marked only as an adapter candidate because its scheduled ingest, co-occurrence scan, seed input, native ingest contract, record paths, and graph output are partially verified. Candidate status does not authorize connection or acceptance.

## Capability classes represented

- scheduled producers;
- shared-engine-dependent producers;
- platform-source intake systems;
- publication consumers;
- oversight clearinghouses;
- scholarly context producers;
- patent-monitoring systems;
- historical identity and biographical contexts;
- educational surfaces;
- public-figure research;
- manual and privacy-restricted intake.

## Validation integration

The capability registry is now part of the existing activation-validation chain:

```text
scripts/validate_repository_capabilities.py
  -> scripts/run_activation_validation.py
  -> .github/workflows/validate-ledger-schemas.yml
```

No new workflow was created.

Validation checks include:

- schema conformance;
- exact membership parity with the fourteen-repository relationship network;
- duplicate repository detection;
- existence of every audit reference;
- verified-contract input and output requirements;
- prohibition on `ready` or `active` adapters without a verified contract;
- privacy-boundary declaration requirements.

## Current next integration goal

```text
verify native contracts and output paths
  -> audit shared StegVerse-Core biography workflows
  -> resolve Trumpality and Administrations producer outputs
  -> resolve StegSocials platform capture and callback contracts
  -> resolve privacy-preserving oversight exports
  -> resolve StegScholar and Patents downstream canon consumers
  -> select first low-risk producer and publication-consumer integration
  -> discovery-cycle manifest
  -> recurring source-search federation
  -> archive and receipt exchange
  -> deduplication and clustering
  -> adjacency and historical graph generation
  -> governed review and compendium update
```

## Required follow-on work

Destination: `StegVerse-Labs/Executive_Rhetoric_Ledger`

- Confirm the expanded validation chain is green.
- Audit the shared `StegVerse/StegVerse-Core` biography ingest and co-occurrence workflows or obtain their durable output contracts.
- Complete Trumpality archive, monitor, update-ingest, platform-source, failure, receipt, and producer-export review.
- Locate Administrations workflows, consumers, and producer outputs.
- Determine StegSocials platform capture, archive, deduplication, account-authenticity, scheduled discovery, and callback contracts.
- Determine VAwatchdog and FREE-DOM_OverSight retrieval, redaction, promotion, archive, failure, and update contracts.
- Determine StegScholar and Patents downstream canonical-output consumers and correction propagation.
- Define privacy-safe identity boundaries for genealogy and biography records.
- Define correction propagation into StegLearn without exporting learner data.
- Do not activate adapters until required contracts, failures, receipts, privacy boundaries, and consumers are verified.

## Release posture

The ledger foundation, relationship network, initial audits, capability-registry schema, fourteen capability records, validator, and activation-chain integration are installed. The automated compendium remains incomplete because native contracts and consumers have not been fully verified and no repository adapter is active.

## Archive readiness

This handoff contains the validated foundation, fourteen repository/platform audits, machine-readable capability registry, contract-state and adapter-state boundaries, validation integration, privacy restrictions, and next contract-verification work. Earlier conversation context is not required; the complete thread is ready for archiving.
