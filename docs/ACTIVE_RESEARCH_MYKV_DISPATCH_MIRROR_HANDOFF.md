# ERL Active Research MyKV Dispatch Mirror Handoff

Updated: 2026-09-10

## Parent Goal Task ID

SS-EVIDENCE-COMPARISON-001

Canonical parent handoff: `docs/ERL_KV_STORAGE_MIRROR_HANDOFF.md`

COSV: `40000100100000`

## Objective

Make ACTIVE ERL research lanes restartable when acquisition is machine-capable, while making MyKV the durable coordination substrate for acquired sources, provenance, derived research artifacts, and execution receipts.

## Dispatcher completion

PR #154 merged at `51ebf09e2412be858243e4925a8dd48f624cf467` after both hosted checks passed on head `d21d48442f9c61456e0d73c7155e9de85084e963`.

The merged dispatcher:

- reads the canonical research-candidate activation registry plus overlays;
- retains active groups even when no machine acquisition surface exists;
- exposes executable HTTPS items in `READY`, `CONTINUING`, or `REFRESH` state;
- requires MyKV persistence under `02_Research/ERL`;
- rejects GitHub artifact storage as durable MyKV persistence;
- requires exact-byte MyKV readback;
- permits exact-byte source reuse across lanes without reusing finding state;
- carries no finding or publication authority.

## InTr-bound consumer continuation

Branch `erl-active-research-intr-mykv-consumer-2026-09-10` adds the next bounded execution unit:

- `scripts/consume_active_research_acquisition.py` consumes one dispatched acquisition only after a canonical `stegverse.intr.hop_receipt/v1` binds the exact acquisition envelope;
- the consumer verifies HTTPS source identity against the dispatch allowlist;
- verified transport receipt may not contain secret plaintext or transfer authority;
- the consumer emits the existing `stegverse.erl.kv-artifact/v1` source-capture manifest;
- it delegates create-only materialization and exact-byte readback to `adapters/kv/erl_kv_writer.py`;
- durable completion becomes `KV_STORED_AND_READBACK_VERIFIED` or `KV_ALREADY_PRESENT_AND_HASH_MATCHED` only after writer readback succeeds;
- finding and publication authority remain false;
- regression tests reject an unbound InTr receipt and an attempted authority transfer;
- `.github/workflows/validate-active-research-acquisition-consumer.yml` provides hosted validation without claiming GitHub is MyKV execution authority.

## Restart rule

An ACTIVE lane is eligible for automated continuation when it has a machine-capable acquisition surface and its execution policy is satisfied. Durable acquisition completes only with `KV_STORED_AND_READBACK_VERIFIED` or `KV_ALREADY_PRESENT_AND_HASH_MATCHED`. Acquired-but-not-persisted work remains resumable as `KV_PERSISTENCE_PENDING` or `KV_UNAVAILABLE`.

## Execution boundary

GitHub Actions may validate and transport dispatch/candidate state. They are not MyKV execution authority and GitHub-hosted artifacts do not satisfy durable ERL research persistence.

The new consumer proves the repository-side admission-to-writer boundary deterministically. Authentic runtime completion still requires a real acquisition to traverse an actual Interlock/InTr admission surface and a real MyKV/provider target to return exact-byte storage/readback evidence.

## First test lane

`ERL-RC-CYBER-SABOTAGE-LINEAGE-2026` using `config/network-cyberphysical-sabotage-source-queue.v1.json`.

## Current state

DISPATCH_MERGED / INTR_BOUND_MYKV_CONSUMER_IMPLEMENTED_ON_BRANCH / HOSTED_VALIDATION_PENDING / AUTHENTIC_INTERLOCK_INTR_ACQUISITION_TO_MYKV_RECEIPT_NOT_YET_OBSERVED
