# Trumpality segmented receipt intake mirror handoff

Goal Task ID: `ERL-RC-TRUMP-FAMILY-CRYPTO-MARKET-2026`  
COSV: `10100000110012`  
Canonical Registry observed: generation 326, ACTIVE / UNCLAIMED  
Updated: 2026-11-18 America/Chicago  
State: SOURCE_PREPARATION / AUTHORIZED_INTEGRATION_AND_RUNTIME_PENDING

## Current truth and scope

The canonical goal remains registered in StegVerse-Labs/.github; its parent
handoff is `docs/ERL_RC_TRUMP_FAMILY_CRYPTO_MARKET_TASK_REGISTRY_REGISTRATION_MIRROR_HANDOFF.md`
there. This bounded ERL handoff inherits that record, repository-wide
`ERL_MIRROR_HANDOFF.md`, ERL issue #223 and the existing Trumpality issue #22.
It creates no new remediation identity or execution authority. The storage
incident's successor admission remains with the existing Registry owner at
StegVerse-Labs/.github #3444 comment 6873219647. The historical closed
StegHealth #98 identity must not be borrowed.

Trumpality PR #23 at `898ba47d9033f67a5e2c2ced0a7fe9c6d7775f4d` moves the
single receipt ledger to numbered segments. At ERL baseline
`9ece8074c43d3a05ca39ef000d3c8f2aec632456`, intake requests only the removed
`research/research_receipts.jsonl`. A segmented-only fixture reproduces
FileNotFoundError before this preparation. Producer-only integration would
break ERL intake; do not describe the producer PR alone as an integrated fix.

## Prepared behavior

- Accept either the legacy single file or contiguous six-digit numbered
  segments beginning at 000000. Refuse mixed layouts, gaps, duplicate paths,
  malformed names, symlinks, oversized entries and incomplete interior records.
- Remote discovery uses the complete, non-truncated Git tree at the supplied
  full producer commit. Fetch only canonical raw paths at that same commit.
  Recompute every receipt blob's Git identity and length before intake.
- Concatenate exact bytes in numeric filename order. Preserve the logical
  `producer_files_sha256.receipts` meaning across layouts. Retain per-part
  path, bytes, row count, Git blob SHA-1 and SHA-256 in new intake provenance.
  The commit-pinned tree supplies the native manifest; no new service or
  dependency is introduced. Local `--source-dir` remains an offline fixture
  route and does not claim native Git authenticity.
- Parse complete object records and reject missing/duplicate receipt IDs
  before writing pending candidates, scan records, quarantine or intake
  receipts. Failures append only the existing actionable FAIL_CLOSED
  disposition. Existing candidate validation, PENDING_REVIEW/no-update,
  append-only readback and idempotency boundaries remain.
- Close all remote response handles. No source acquisition is rerun.

## Validation

Eight stdlib unittest methods pass, including 16 malformed-layout/remote-tree
subcases, legacy-to-segment migration, retry idempotency, complete native
blob validation, response closure and no-intake-effects failures.

Twelve captured-data replay checks also pass: predecessor 188,445 scans,
successor 190,270 scans and 865 candidates, delta 1,825 scans and 27 candidates,
exact logical receipt SHA-256
`cd78fc3724b5ead5bfe08b7171ec609df3c81595cdbd454390459d5d8782933c`,
retry with no new scans/candidates, byte-prefix conservation and append-only
readback with no authority promotion.

The preserved failed-cycle artifact 14486216257 (run 44430113790,
SHA-256 `5b80f397b13df1f1c2f6d437e92f5651da1f29c9fff030a83f6c3f629920fcf6`)
supports this replay. Its 104,429,829-byte committed prefix and 1,022,911-byte
delta match native producer segment blobs
`ff07e3cfe28a580454df4665de31a2deaddccff1` and
`4236ef740756d65cc79d8ee5e286abf68ffb9e95`. Transport is mocked from those
captured bytes; production intake and readback code execute unchanged in a
temporary fixture repository. This is not a hosted producer/consumer run.

Local results and the companion PR's exact head/CI must be filed on ERL #223,
Trumpality #22, the producer PR #23 and the registry-resolved home/pairing
surfaces. Source preparation by CODEX is not independent non-author acceptance.

## Remaining work and integration order

1. Review this companion consumer source and producer PR #23 together, including
   producer-side manifest/rotation/concurrency requirements still owed by #22.
   This consumer does not supply a producer writer transaction or adopt a
   completed whole-incident format by itself.
2. The native owner resolves incident admission and expected-head protection.
   Land consumer compatibility before exposing the segmented producer on main;
   it retains legacy support. Central handoff PR #3473 must name both sides.
3. Run an authorized producer cycle and ERL intake at exact recorded heads;
   independently verify logical counts, retained prefixes, receipt hashes and
   destination readback. No blind scan replay to recreate preserved output.
4. Only the native owner may disposition completion from retained transition
   evidence. No merge, release, runtime activation, ledger propagation or
   completion is claimed here.

Manual Work: None. The remaining acts have existing repository/Registry owners.
