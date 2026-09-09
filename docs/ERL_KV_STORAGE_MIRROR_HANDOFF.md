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
- adapters/kv/erl_kv_writer.py
- scripts/validate_erl_kv_storage.py
- scripts/test_erl_kv_writer.py
- fixtures/erl-kv/sample-manifest.json
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

Deterministic local and hosted tests prove the schema and mounted-filesystem writer behavior. Authentic activation additionally requires running the writer against the user's mounted KV root and preserving the returned receipt for a real ERL intake.

The OpenAI An Alien Mind artifact currently present in MyKV demonstrates the intended storage layout, but its manual placement is not retroactively claimed as execution by this adapter.

## Remaining work

1. Run one real ERL source intake through adapters/kv/erl_kv_writer.py against an authorized mounted KnowledgeVault root.
2. Preserve the authentic write receipt and bind it to the source acquisition record.
3. Add Master Records custody/reconstruction for the authentic ERL KV receipt if the shared custody schema does not already accept it.
4. Update StegVerse-Labs/StegSocials to reference the stable ERL artifact ID and KV receipt where an ERL-backed publication is created.
5. Verify any pertinent public/index propagation in StegVerse-Labs/Site, GCAT-BCAT-Engine/Publisher, admissibility-wiki, and stegguardian-wiki only when this lane reaches release readiness.

## Current state

SOURCE_IMPLEMENTED_PENDING_AUTHENTIC_KV_WRITE_PROOF
