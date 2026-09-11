# ERL Active Research MyKV Dispatch Mirror Handoff

Updated: 2026-09-10

## Parent Goal Task ID

SS-EVIDENCE-COMPARISON-001

Canonical parent handoff: `docs/ERL_KV_STORAGE_MIRROR_HANDOFF.md`

## Objective

Make ACTIVE ERL research lanes restartable when acquisition is machine-capable, while making MyKV the durable coordination substrate for acquired sources, provenance, derived research artifacts, and execution receipts.

## Implemented on PR #154

- `docs/ACTIVE_RESEARCH_MYKV_COORDINATION.md` defines the coordination and restart contract.
- `scripts/generate_active_research_dispatch.py` reads the canonical research-candidate activation registry plus additive overlays.
- Active groups are retained even when no machine acquisition surface exists; they receive an explicit deferred dispatch state instead of disappearing.
- Queue-like registered artifacts are inspected for executable HTTP(S) items in `READY`, `CONTINUING`, or `REFRESH` state.
- Every executable item carries `persistence_required=true` and `required_storage_lane=02_Research/ERL`.
- The dispatcher declares that GitHub storage cannot satisfy MyKV persistence.
- Exact-byte MyKV readback is required.
- Cross-lane source reuse is allowed by exact-byte identity/provenance; finding-state reuse is prohibited.
- Candidate finding and publication authority remain false.
- `tests/test_active_research_dispatch.py` covers executable and deferred active-lane behavior.
- `.github/workflows/validate-active-research-dispatch.yml` validates the real registry and requires `ERL-RC-CYBER-SABOTAGE-LINEAGE-2026` to be eligible for automated acquisition with MyKV persistence required.

## Restart rule

An ACTIVE lane is eligible for automated continuation when it has a machine-capable acquisition surface and its execution policy is satisfied. Durable acquisition completes only with `KV_STORED_AND_READBACK_VERIFIED` or `KV_ALREADY_PRESENT_AND_HASH_MATCHED`. Acquired-but-not-persisted work remains resumable as `KV_PERSISTENCE_PENDING` or `KV_UNAVAILABLE`.

## Execution boundary

GitHub Actions may validate and transport dispatch/candidate state. They are not MyKV execution authority and GitHub-hosted artifacts do not satisfy durable ERL research persistence.

The remaining runtime work is a MyKV-capable executor path that consumes the dispatch manifest, performs source acquisition under Interlock/InTr admission, emits ERL KV manifests, invokes the existing ERL KV writer/provider-operation path, verifies exact-byte readback, and returns durable receipts for restart reconstruction.

## First test lane

`ERL-RC-CYBER-SABOTAGE-LINEAGE-2026` using `config/network-cyberphysical-sabotage-source-queue.v1.json`.

## Current state

DISPATCH_IMPLEMENTED_ON_OPEN_PR / HOSTED_VALIDATION_PENDING / MYKV_EXECUTOR_CONSUMPTION_NOT_YET_PROVEN
