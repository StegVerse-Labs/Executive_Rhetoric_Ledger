# ERL KnowledgeVault Storage Mirror Handoff

Updated: 2026-09-09

## Goal Task ID

SS-EVIDENCE-COMPARISON-001

Canonical task record:
StegVerse-Labs/.github/data/canonical-task-records/SS-EVIDENCE-COMPARISON-001.json

COSV: 40000100100000

## Purpose

Make KnowledgeVault the durable storage medium for ERL research and evidence artifacts as the ledger grows. ERL continues to define research, evidence, review, and assessment semantics; KV persists the resulting artifacts under the canonical 02_Research/ERL lane.

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

- schemas/erl-kv-artifact.schema.json
- schemas/erl-kv-write-receipt.schema.json
- schemas/erl-kv-provider-write-observation.schema.json
- schemas/erl-kv-provider-operation-receipt.schema.json
- adapters/kv/erl_kv_writer.py
- scripts/validate_erl_kv_storage.py
- scripts/validate_erl_kv_provider_operation.py
- scripts/test_erl_kv_writer.py
- fixtures/erl-kv/sample-manifest.json
- fixtures/erl-kv/sample-write-receipt.json
- fixtures/erl-kv/sample-provider-write-observation.json
- fixtures/erl-kv/invalid-provider-observation-overclaims.json
- fixtures/erl-kv/invalid-provider-operation-overclaims.json
- evidence/kv-provider-operations/2026-09-09-google-drive-nsa-distillation.*.json
- fixtures/erl-kv/source.txt
- docs/ERL_KV_STORAGE_MIRROR_HANDOFF.md
- .github/workflows/validate-ledger-schemas.yml
- README.md

## Implemented behavior

- requires explicit existing mounted KV root;
- fixes the ERL destination to 02_Research/ERL;
- verifies artifact ID, object filenames, media metadata, byte size, and SHA-256;
- rejects traversal, symlink payloads, missing objects, extra objects, hash mismatch, credential material, and conflicting overwrite;
- allows identical idempotent re-entry as NOOP;
- writes a canonical manifest.json after payloads;
- performs byte-for-byte readback;
- returns an ERL KV write receipt without opening a provider session;
- accepts a separate retained provider-operation receipt only when provider writes, manifest-last ordering, provider resource identities, native receipt binding, and independent provider byte readback are all proven.

## Current proof boundary

Deterministic local and hosted tests prove the schema and mounted-filesystem writer behavior.

On 2026-09-09, the OpenAI "An Alien Mind" intake was organized in the live MyKV lane at `02_Research/ERL/ERL-2026-09-06-OPENAI-AN-ALIEN-MIND`. The folder contains the preserved PDF, plain-text capture, ERL research record, canonical `manifest.json`, and `provider-write-observation.json`.

Google Drive metadata readback verified the destination folder, stable file IDs, filenames, media types, and byte sizes. The observation explicitly records `byte_for_byte_provider_readback_verified=false` and `adapter_execution_proven=false`; therefore it proves live provider storage and metadata readback without overstating execution of the mounted-filesystem adapter or completion of the canonical receipt proof.

The canonical writer receipt and provisional provider observation now have separate JSON Schemas. The provider-observation schema requires both byte-for-byte verification and adapter execution to remain false, preventing metadata-only evidence from being promoted into a canonical writer receipt.

Master Records now mirrors the two ERL KV schemas with immutable upstream commit and blob pins, imports qualifying receipts into append-only custody, and reconstructs their custody chain deterministically. `master-records/orchestration` PR #86 merged at `94fa52a61363494e248859181403c59d03b34980`; PR #87 then custodied the live OpenAI provider observation and merged at `cad9c97deb06e897a72c5fa56ba0ada28edc3e05`. All nine hosted workflows passed for both changes. The live observation remains classified `PROVIDER_METADATA_ONLY` with `native_writer_proof=false`; custody preserves the evidence without elevating its proof class.

StegSocials now references the stable artifact ID, the exact-byte Level 1 evidence, and the Master Records provider-observation custody chain in its active evidence and ERL-assisted drafting handoffs. PR #22 merged at `a0b049730d16df8febafcb85cf5190974c19f15d` after both hosted workflows passed. These consumer references preserve the same non-promotion rule.

## Authentic provider-operation proof

On 2026-09-09, `ERL-2026-09-08-NSA-AI-DISTILLATION` completed the native-materialization and live Google Drive path. The provider folder is `google-drive:folder:1esoETwRd5A2YgdVTMskCSgzTOpuRyIV5`. Google Drive accepted the two validated Markdown payloads, the canonical manifest last, the native writer receipt, and the retained provider-operation receipt. Independent provider downloads matched the expected bytes and SHA-256 values for all five files. The composite receipt hash is `bb74904fcd8169829c78bdc1c0d64905b33243c2c22852565c13e614abcd1fa8`.

## Master Records completion

Master Records pinned the three ERL KV schemas at exact source commit/blob coordinates, custodied the native writer and provider-operation receipts, reproduced all three live imports, and reconstructed the combined chain. All nine workflows passed; PR #89 merged at `1c565c160d1a25b408e130402b5da52e855a8169`.

## Remaining work

1. Execute the separate propagation-verification task for applicable Site, Publisher, admissibility-wiki, and stegguardian-wiki surfaces.

## Current state

ERL_KV_INTEGRATION_COMPLETE_PROPAGATION_SEPARATE
