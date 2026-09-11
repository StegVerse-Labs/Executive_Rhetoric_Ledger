# ERL Active Research MyKV Dispatch Mirror Handoff

Updated: 2026-09-10

## Parent Goal Task ID

SS-EVIDENCE-COMPARISON-001

Canonical parent handoff: `docs/ERL_KV_STORAGE_MIRROR_HANDOFF.md`

COSV: `40000100100000`

## Objective

Make ACTIVE ERL research lanes restartable when acquisition is machine-capable, while making MyKV the durable coordination substrate for acquired sources, provenance, derived research artifacts, and execution receipts.

## Merged dispatcher and consumer

PR #154 merged at `51ebf09e2412be858243e4925a8dd48f624cf467` after both hosted checks passed. It installs the ACTIVE research dispatcher and requires `02_Research/ERL` persistence, exact-byte readback, and no finding/publication promotion.

PR #155 merged at `e3c75c8671609f154b9e8742b873971f425e9205` after `Validate Active Research Acquisition Consumer` and `Validate Ledger Schemas` both passed at exact head `2eb89b57e26d64d6ef14fe4629684ce6a45b4128`. It installs the repository-side acquisition-to-ERL-KV consumer.

PR #156 merged at `2e5d972895177484cabf07bacfcd51e098b90bc1` after exact-head validation. It requires exactly three chained canonical `stegverse.intr.hop_receipt/v1` receipts before durable active-research MyKV admission.

## Live provider observation

A bounded official CISA/FBI/DC3/NSA Iran-critical-infrastructure fact-sheet capture was materialized for the active cyber-sabotage lane. This is an extracted capture, explicitly **not** the original PDF octets, with `finding_authority: NONE` and `publication_authority: NONE`.

Live MyKV target:

- canonical ERL parent folder: `google-drive:folder:147zp4--w_dnf_cOJzC0nKGZrWtwB2M6n`;
- artifact folder: `google-drive:folder:1osZ9dvIHmYI58t7PoopRVI6UbrPLxxIG`;
- source capture: `google-drive:file:1KKBS1drUFVh-czLpmg5koRgDs4YMf-gG`;
- file name: `ERL-CYBER-CISA-IRAN-2025-JOINT-FACT-SHEET.capture.txt`;
- exact size before upload and after independent provider download: `1015` bytes;
- SHA-256 before upload and after independent raw provider download: `94470c58db24e544c3edfcd390cca395375a348879ec3c53451ba517ff917763`.

This proves a real MyKV provider write and exact-byte provider readback of the bounded capture. It does not by itself prove Universal InTr admission.

## Universal InTr boundary

Canonical transport from an external acquisition source to KV is the adjacent path:

`EXTERNAL_SYSTEM -> STEGOS_ECOSYSTEM -> DEVICE_SYSTEM -> KV`

Durable admission requires:

- canonical adjacent boundary roles in order;
- one packet ID and operation hash across the chain;
- exact acquisition-envelope payload hash at every hop;
- prior-receipt hash continuity;
- `FORWARDED` for intermediate hops and terminal `RECEIVED` at KV;
- `boundary_verification=VERIFIED` at every hop;
- no secret plaintext and no authority transfer;
- terminal receipt hash retained separately from the full receipt chain.

Regression coverage rejects a single valid hop, a skipped boundary, broken prior-hash lineage, and authority transfer.

## Reusable runtime binding continuation

The current continuation branch `ss-evidence-comparison-erl-intr-binding` adds `scripts/build_active_research_intr_binding.py` and `tests/test_active_research_intr_binding.py`.

The builder reuses the admitted ACTIVE research dispatch item to create the exact canonical acquisition envelope consumed by `scripts/consume_active_research_acquisition.py`, then creates:

1. a deterministic canonical Universal InTr transport intent for `EXTERNAL_SYSTEM -> STEGOS_ECOSYSTEM -> DEVICE_SYSTEM -> KV`;
2. an event-ephemeral `stegverse.universal-intr-materialization-request/v1` bound to the same packet ID and acquisition-envelope hash; and
3. a deterministic `stegverse.erl.active-research-intr-binding/v1` wrapper that records the expected three runtime receipts without fabricating any receipt.

The binding preserves `TV/TVC` as credential authority, sets GitHub runtime authority to `NONE`, grants no execution authority, mints no claim/fence, transfers no authority, and explicitly records `runtime_receipts_present=false` and `transport_execution_claimed=false` until the authentic runtime returns receipts.

The validation workflow now runs the existing acquisition-consumer tests together with the new binding tests so the envelope hash, canonical three-hop path, non-authorizing semantics, deterministic identity, and idempotent persistence remain coupled.

## Restart rule

An ACTIVE lane is eligible for automated continuation when it has a machine-capable acquisition surface and its execution policy is satisfied. Durable acquisition completes only with `KV_STORED_AND_READBACK_VERIFIED` or `KV_ALREADY_PRESENT_AND_HASH_MATCHED`. Acquired-but-not-persisted work remains resumable as `KV_PERSISTENCE_PENDING` or `KV_UNAVAILABLE`.

## Execution boundary

GitHub Actions may validate and transport dispatch/candidate state. They are not MyKV execution authority and GitHub-hosted artifacts do not satisfy durable ERL research persistence.

The live provider observation proves real MyKV byte persistence/readback. The runtime binding now provides the reusable exact request surface needed to hand the admitted acquisition envelope to canonical Universal InTr. It still does **not** prove transport execution. Authentic completion requires the actual transport implementation to return all three receipts and those receipts to be bound to the live provider operation.

Canonical-library, fixture, repository-generated, or locally constructed receipts must remain classified separately from authentic runtime observation.

## First test lane

`ERL-RC-CYBER-SABOTAGE-LINEAGE-2026`.

## Next exact steps

1. Validate the runtime-binding branch at exact head.
2. Merge the binding PR only if the applicable workflows pass.
3. Submit the deterministic materialization request for `ERL-CYBER-CISA-IRAN-2025-JOINT-FACT-SHEET` to the authentic Universal InTr runtime owner using the exact canonical acquisition-envelope bytes referenced by the binding.
4. Preserve the three authentic chained receipts and verify them with the merged consumer.
5. Bind the terminal KV receipt to the existing live provider-write/readback evidence without synthesizing transport proof.
6. Update this handoff and the canonical parent handoff with exact receipt hashes and final proof classification; do not promote finding or publication authority.

## Current state

`DISPATCH_MERGED / PR_155_CONSUMER_MERGED_AND_VALIDATED / PR_156_FULL_CHAIN_ADMISSION_MERGED_AND_VALIDATED / LIVE_MYKV_PROVIDER_WRITE_AND_EXACT_READBACK_OBSERVED / REUSABLE_INTR_RUNTIME_BINDING_IMPLEMENTED_ON_BRANCH / AUTHENTIC_FULL_INTR_CHAIN_BOUND_TO_LIVE_PROVIDER_OPERATION_PENDING`
