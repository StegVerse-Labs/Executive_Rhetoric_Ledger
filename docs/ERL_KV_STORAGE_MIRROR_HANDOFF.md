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
    -> mounted KV root
    -> 02_Research/ERL/<artifact_id>/
    -> create-only object writes
    -> canonical manifest written last
    -> byte-for-byte readback
    -> idempotent write receipt

KV is storage, continuity, and user-custodied persistence. It does not replace ERL classification, comparison, review, or assessment semantics. Provider credentials and reusable secrets are not ERL artifacts and must not be written into the KV research lane.

## Installed repository surfaces

- schemas/erl-kv-artifact.schema.json
- schemas/erl-kv-write-receipt.schema.json
- schemas/erl-kv-provider-write-observation.schema.json
- adapters/kv/erl_kv_writer.py
- scripts/validate_erl_kv_storage.py
- scripts/test_erl_kv_writer.py
- fixtures/erl-kv/sample-manifest.json
- fixtures/erl-kv/sample-write-receipt.json
- fixtures/erl-kv/sample-provider-write-observation.json
- fixtures/erl-kv/invalid-provider-observation-overclaims.json
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
- returns an ERL KV write receipt without opening a provider session.

## Current proof boundary

Deterministic local and hosted tests prove the schema and mounted-filesystem writer behavior.

On 2026-09-09, the OpenAI "An Alien Mind" intake was organized in the live MyKV lane at `02_Research/ERL/ERL-2026-09-06-OPENAI-AN-ALIEN-MIND`. The folder contains the preserved PDF, plain-text capture, ERL research record, canonical `manifest.json`, and `provider-write-observation.json`.

Google Drive metadata readback verified the destination folder, stable file IDs, filenames, media types, and byte sizes. The observation explicitly records `byte_for_byte_provider_readback_verified=false` and `adapter_execution_proven=false`; therefore it proves live provider storage and metadata readback without overstating execution of the mounted-filesystem adapter or completion of the canonical receipt proof.

The canonical writer receipt and provisional provider observation now have separate JSON Schemas. The provider-observation schema requires both byte-for-byte verification and adapter execution to remain false, preventing metadata-only evidence from being promoted into a canonical writer receipt.

Master Records now mirrors the two ERL KV schemas with immutable upstream commit and blob pins, imports qualifying receipts into append-only custody, and reconstructs their custody chain deterministically. `master-records/orchestration` PR #86 merged at `94fa52a61363494e248859181403c59d03b34980`; PR #87 then custodied the live OpenAI provider observation and merged at `cad9c97deb06e897a72c5fa56ba0ada28edc3e05`. All nine hosted workflows passed for both changes. The live observation remains classified `PROVIDER_METADATA_ONLY` with `native_writer_proof=false`; custody preserves the evidence without elevating its proof class.

StegSocials now references the stable artifact ID, the exact-byte Level 1 evidence, and the Master Records provider-observation custody chain in its active evidence and ERL-assisted drafting handoffs. PR #22 merged at `a0b049730d16df8febafcb85cf5190974c19f15d` after both hosted workflows passed. These consumer references preserve the same non-promotion rule.

## Remaining work

1. Run one real ERL source intake through `adapters/kv/erl_kv_writer.py` against an authorized mounted KnowledgeVault root.
2. Preserve the authentic canonical write receipt, independently verify provider bytes, and bind both to the source acquisition record.
3. Import and reconstruct the authentic native-writer receipt through the installed Master Records custody path alongside the already-custodied provider observation.
4. Verify any pertinent public/index propagation in StegVerse-Labs/Site, GCAT-BCAT-Engine/Publisher, admissibility-wiki, and stegguardian-wiki only when this lane reaches release readiness.

## Current state

LIVE_PROVIDER_STORAGE_MASTER_RECORDS_CUSTODY_AND_STEGSOCIALS_REFERENCES_OBSERVED_PENDING_NATIVE_WRITER_RECEIPT
