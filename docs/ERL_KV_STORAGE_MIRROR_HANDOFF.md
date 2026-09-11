# ERL KnowledgeVault Storage Mirror Handoff

Updated: 2026-09-10

## Goal Task ID

SS-EVIDENCE-COMPARISON-001

Canonical task record:
StegVerse-Labs/.github/data/canonical-task-records/SS-EVIDENCE-COMPARISON-001.json

COSV: 40000100100000

## Purpose

Make KnowledgeVault the durable storage medium for ERL research and evidence artifacts as the ledger grows. ERL continues to define research, evidence, review, and assessment semantics; KV persists the resulting artifacts under the canonical `02_Research/ERL` lane.

## Storage contract

    ERL acquisition or analysis
    -> ERL artifact manifest
    -> object hash and size verification
    -> native writer validation/materialization
    -> mounted KV root OR authenticated provider upload
    -> 02_Research/ERL/<artifact_id>/
    -> create-only object writes
    -> canonical manifest written last
    -> byte-for-byte local and provider readback
    -> native receipt + retained provider-operation receipt

KV is storage, continuity, and user-custodied persistence. It does not replace ERL classification, comparison, review, or assessment semantics. Provider credentials and reusable secrets are not ERL artifacts and must not be written into the KV research lane.

## Installed repository surfaces

- `schemas/erl-kv-artifact.schema.json`
- `schemas/erl-kv-write-receipt.schema.json`
- `schemas/erl-kv-provider-write-observation.schema.json`
- `schemas/erl-kv-provider-operation-receipt.schema.json`
- `adapters/kv/erl_kv_writer.py`
- `scripts/validate_erl_kv_storage.py`
- `scripts/validate_erl_kv_provider_operation.py`
- `scripts/test_erl_kv_writer.py`
- `scripts/generate_active_research_dispatch.py`
- `scripts/consume_active_research_acquisition.py`
- `scripts/build_active_research_intr_binding.py`
- `tests/test_active_research_dispatch.py`
- `tests/test_active_research_acquisition_consumer.py`
- `tests/test_active_research_intr_binding.py`
- `docs/ACTIVE_RESEARCH_MYKV_COORDINATION.md`
- `docs/ACTIVE_RESEARCH_MYKV_DISPATCH_MIRROR_HANDOFF.md`
- `.github/workflows/validate-active-research-dispatch.yml`
- `.github/workflows/validate-active-research-acquisition-consumer.yml`
- `README.md`

## Implemented storage behavior

- requires explicit existing mounted KV root;
- fixes the ERL destination to `02_Research/ERL`;
- verifies artifact ID, object filenames, media metadata, byte size, and SHA-256;
- rejects traversal, symlink payloads, missing objects, extra objects, hash mismatch, credential material, and conflicting overwrite;
- allows identical idempotent re-entry as NOOP;
- writes a canonical `manifest.json` after payloads;
- performs byte-for-byte readback;
- returns an ERL KV write receipt without opening a provider session;
- accepts a separate retained provider-operation receipt only when provider writes, manifest-last ordering, provider resource identities, native receipt binding, and independent provider byte readback are all proven.

## Completed ERL-to-MyKV proof

On 2026-09-09, the OpenAI "An Alien Mind" intake was organized in the live MyKV lane at `02_Research/ERL/ERL-2026-09-06-OPENAI-AN-ALIEN-MIND`. Google Drive metadata readback verified provider storage without overstating native writer execution; the observation remains `PROVIDER_METADATA_ONLY`.

`ERL-2026-09-08-NSA-AI-DISTILLATION` then completed the native-materialization and live Google Drive path. Google Drive accepted the two validated Markdown payloads, canonical manifest last, native writer receipt, and retained provider-operation receipt. Independent downloads matched expected bytes and SHA-256 for all five files. Composite receipt hash: `bb74904fcd8169829c78bdc1c0d64905b33243c2c22852565c13e614abcd1fa8`.

Master Records pinned the ERL KV schemas, custodied the authentic native/provider receipts, reproduced imports, and reconstructed the combined chain. `master-records/orchestration` PR #89 merged at `1c565c160d1a25b408e130402b5da52e855a8169` after all nine workflows passed.

The separate propagation task `SS-ERL-KV-PROPAGATION-VERIFICATION-001` completed and retired. Site and Publisher consumed the proof; Admissibility Wiki and `StegVerse-002/stegguardian-wiki` were verified not applicable because they have no ERL/KV consumer path.

## Active research / MyKV continuation

PR #154 merged at `51ebf09e2412be858243e4925a8dd48f624cf467`, adding restartable ACTIVE research dispatch. The dispatcher retains non-automatable active lanes as explicit deferred states, discovers executable public HTTPS queue items, requires `02_Research/ERL` persistence and exact-byte readback, rejects GitHub storage as durable MyKV persistence, permits exact-byte source reuse without finding-state reuse, and carries no finding or publication authority.

PR #155 merged at `e3c75c8671609f154b9e8742b873971f425e9205` after both exact-head workflows passed. It added the repository-side acquisition consumer, binding dispatched source identity to an InTr receipt and delegating create-only persistence/readback to the existing ERL KV writer.

Review against the canonical StegOS Universal InTr implementation exposed that #155 accepted one valid hop even though external-source delivery into KV must traverse the complete adjacent boundary path:

    EXTERNAL_SYSTEM
    -> STEGOS_ECOSYSTEM
    -> DEVICE_SYSTEM
    -> KV

PR #156 merged at `2e5d972895177484cabf07bacfcd51e098b90bc1` after exact-head validation. The consumer now requires exactly three canonical `stegverse.intr.hop_receipt/v1` receipts with:

- one packet identity and one operation identity across all hops;
- exact acquisition-envelope payload hash binding at every hop;
- canonical adjacent `from_role`/`to_role` transitions with no skipped boundary;
- prior-receipt hash continuity;
- `FORWARDED` on intermediate hops and terminal `RECEIVED` at KV;
- `boundary_verification=VERIFIED` at each hop;
- no secret plaintext;
- no authority transfer.

Regression coverage rejects a single otherwise-valid hop, skipped boundary, broken prior-hash lineage, and attempted authority transfer.

The current continuation branch `ss-evidence-comparison-erl-intr-binding` adds a reusable non-authorizing runtime binding. `scripts/build_active_research_intr_binding.py` derives the exact admitted acquisition envelope from the ACTIVE dispatch item, produces a deterministic canonical Universal InTr intent for the full external-to-KV path, and produces a deterministic event-ephemeral materialization request bound to the same packet and envelope hash. It never produces hop receipts and explicitly records that runtime transport has not yet executed.

The binding preserves `TV/TVC` credential authority, sets GitHub runtime authority to `NONE`, mints no claim/fence, transfers no authority, and grants no execution authority. The validation workflow now couples binding tests with the acquisition-consumer tests so the exact envelope hash and three-hop contract cannot drift apart.

## Live active-research provider proof

The first live provider operation for this continuation uses a bounded capture from the CISA/FBI/DC3/NSA Iran-related joint fact sheet. The capture remains explicitly bounded to a public-web extraction rather than original PDF octets, and it carries `finding_authority: NONE` and `publication_authority: NONE`.

Live MyKV provider destination:

- ERL parent folder: `google-drive:folder:147zp4--w_dnf_cOJzC0nKGZrWtwB2M6n`
- artifact folder: `google-drive:folder:1osZ9dvIHmYI58t7PoopRVI6UbrPLxxIG`
- capture file: `google-drive:file:1KKBS1drUFVh-czLpmg5koRgDs4YMf-gG`
- filename: `ERL-CYBER-CISA-IRAN-2025-JOINT-FACT-SHEET.capture.txt`
- size: `1015` bytes
- SHA-256 before upload and after independent raw provider download: `94470c58db24e544c3edfcd390cca395375a348879ec3c53451ba517ff917763`

This proves an authentic live provider write plus exact-byte provider readback for the active-research source capture. It does **not** prove that the source traversed Universal InTr. Provider success and InTr transport are separate proof classes.

## Current authentic runtime boundary

The reusable runtime-binding request surface is now implemented on the continuation branch. The remaining runtime predicate is still one real active-research acquisition whose exact acquisition envelope traverses the authentic Universal InTr chain `EXTERNAL_SYSTEM -> STEGOS_ECOSYSTEM -> DEVICE_SYSTEM -> KV`, producing the three chained canonical receipts required by PR #156 and then binding those receipts to the live MyKV/provider persistence result.

A repository fixture, GitHub workflow, locally constructed receipt, generated binding, or provider write without authentic InTr traversal may validate code but cannot satisfy this runtime predicate.

## Research posture

The Iran-linked cyber-sabotage lineage remains a research candidate. The bounded CISA/FBI/DC3/NSA capture supports broad public warning/capability posture but does not itself establish a specific incident, attribution, concealment, or legal/political accountability finding. The unresolved question remains the specificity and timing of known attempted/suspected/confirmed compromises and public/private warning relative to escalation. The current capture carries no finding or publication authority.

## Remaining work

1. Validate the reusable runtime-binding branch at exact head and merge only if applicable workflows pass.
2. Submit the deterministic materialization request for the admitted CISA/Iran acquisition envelope to the authentic Universal InTr runtime owner.
3. Preserve all three authentic chained receipts and verify them with the merged consumer.
4. Bind the terminal KV receipt to the real provider-write/readback proof rather than synthesizing transport evidence.
5. Update this handoff and `docs/ACTIVE_RESEARCH_MYKV_DISPATCH_MIRROR_HANDOFF.md` with exact runtime receipt hashes and final proof class.
6. Only after authentic runtime evidence exists, determine whether a new bounded propagation-verification task is applicable for this active-research runtime capability; do not reuse the retired storage-propagation task merely to reset coordination state.

## Current state

`ERL_KV_INTEGRATION_AND_PROPAGATION_COMPLETE / ACTIVE_RESEARCH_DISPATCH_AND_CONSUMER_MERGED / PR_156_FULL_INTR_CHAIN_ADMISSION_MERGED_AND_VALIDATED / LIVE_ACTIVE_RESEARCH_PROVIDER_WRITE_READBACK_VERIFIED / REUSABLE_INTR_RUNTIME_BINDING_IMPLEMENTED_ON_BRANCH / AUTHENTIC_FULL_INTR_RUNTIME_CHAIN_NOT_YET_OBSERVED`
