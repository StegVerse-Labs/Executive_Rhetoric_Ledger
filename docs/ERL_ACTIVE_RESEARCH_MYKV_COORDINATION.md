# ERL Active Research / MyKV Coordination Contract

## Purpose

Define how active ERL research lanes resume automated acquisition while using MyKV as the durable coordination substrate for acquired source data, provenance, derived research artifacts, and execution receipts.

ERL remains the research/evidence authority. MyKV remains the user-custodied storage and continuity substrate. Neither storage location nor successful acquisition promotes a claim into a finding.

## Core rule

An automated ERL acquisition cycle is not complete merely because bytes were fetched or written into a GitHub workspace.

For any lane whose acquisition policy requires durable retention, completion requires one of the following terminal acquisition-storage states:

- `KV_STORED_AND_READBACK_VERIFIED`
- `KV_ALREADY_PRESENT_AND_HASH_MATCHED`
- `KV_PERSISTENCE_PENDING`
- `KV_UNAVAILABLE`
- `SOURCE_UNAVAILABLE`
- `ACQUISITION_ERROR`

Only the first two states constitute completed durable acquisition. `KV_PERSISTENCE_PENDING` and `KV_UNAVAILABLE` preserve resumability but do not permit the lane to claim durable acquisition completion.

## Coordination sequence

```text
active research registry
  -> active research dispatcher
  -> executable acquisition item
  -> Interlock/InTr admission
  -> transient source acquisition
  -> hash + provenance + media metadata
  -> ERL KV artifact manifest
  -> MyKV 02_Research/ERL/<artifact_id>/
  -> create-only payload writes
  -> canonical manifest written last
  -> exact byte readback
  -> ERL KV write/provider-operation receipt
  -> ERL evidence/reference index
  -> lane-specific analysis / contradiction / adjacency work
  -> derived artifact manifest
  -> MyKV persistence + readback
```

GitHub Actions may carry, validate, or stage execution manifests and candidate state. GitHub storage is not the authoritative durable research-data store and cannot satisfy MyKV persistence by itself.

## Cross-lane source reuse

The same acquired source may be relevant to multiple active research lanes. ERL MUST avoid unnecessary duplicate acquisition/storage when exact bytes are already present in MyKV.

A source object is reusable when its exact-byte identity and provenance are sufficient for the new lane. The new lane records a reference to the existing MyKV artifact and adds its own lane-relative purpose, evidence class, state dimensions, and unresolved propositions.

Cross-lane reuse MUST NOT copy another lane's finding state. A source can strengthen one proposition, weaken another, and merely disambiguate a third.

## MyKV storage boundary

Canonical ERL durable storage remains:

`02_Research/ERL/<artifact_id>/`

The existing native writer `adapters/kv/erl_kv_writer.py` remains authoritative for mounted-MyKV create-only writes, manifest-last ordering, object hash/size validation, idempotent exact re-entry, credential exclusion, and byte-for-byte readback.

Provider-backed persistence MUST retain the provider-operation receipt and independent readback evidence required by the existing ERL KV storage contract.

## Active lane execution eligibility

A research lane may be automatically dispatched only when:

1. the candidate registry says the lane is active;
2. no governed terminal transition exists;
3. an executable acquisition queue/search surface exists;
4. the item is in an executable state such as `READY`, `CONTINUING`, or `REFRESH`;
5. execution authority/policy requirements are satisfied;
6. the acquisition operation cannot itself grant finding or publication authority.

The dispatcher MUST record non-executable active lanes as durable deferred states rather than silently omitting them.

## Restart semantics

The dispatcher reconstructs work from durable registry state plus the latest acquisition/MyKV receipts. Chat/session continuity is not required.

On restart:

- exact MyKV artifact + valid readback receipt -> reuse and continue downstream analysis;
- acquired bytes but no verified MyKV persistence -> resume at persistence;
- prior source failure -> retry according to lane cadence/policy;
- terminal candidate transition -> do not dispatch;
- no executable acquisition surface -> retain `RESEARCH_ACTIVE_NO_AUTOMATED_ACQUISITION`.

## Data-sharing semantics between ERL lanes

MyKV provides shared custody, not shared conclusions.

Each lane may reference common MyKV source artifacts while maintaining independent:

- proposition bindings;
- evidence-direction classification;
- attribution ceilings;
- contradiction state;
- chronology interpretation;
- authority/jurisdiction mapping;
- review status;
- finding/publication state.

Derived artifacts that materially change research state are themselves persisted as new MyKV ERL artifacts with provenance back to the source objects and prior state.

## Publication boundary

Automated acquisition and MyKV persistence authorize neither public release nor factual promotion. Reviewed publication remains governed by the existing ERL/StegSocials publication contracts.

## First test lane

`ERL-RC-CYBER-SABOTAGE-LINEAGE-2026` is the first recommended active-research dispatcher test because it already has `config/network-cyberphysical-sabotage-source-queue.v1.json` containing public HTTPS, no-credential `READY` items.

The test passes only if eligible items produce durable MyKV storage/readback receipts or explicit persistence-deferred receipts; a GitHub-only capture is insufficient.
