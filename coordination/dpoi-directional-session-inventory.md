# DPOI Directional Discovery Execution Inventory

| Task ID | Originating goal | Destination | Branch | Surface | Owner | Claim state | Completion | Validation | Integration | Archival dependency | Evidence | Next executable action |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ERL-DPOI-DIRECTIONAL-001 | Make category searches seek data that can strengthen, weaken, or disambiguate a DPOI | StegVerse-Labs/Executive_Rhetoric_Ledger | main | recurring-search config/schema, discovery-cycle schema/generator/fixture, DPOI contract | recurring-discovery category-search contract | COMPLETE | COMPLETE | main run 31188450324 PASS all 40 stages | INTEGRATED | false | PR #55 / merge 5a513639798dc55b8166f0489c325b117d4bf5fa | machine-owned recurring discovery uses the parameters |
| ERL-DPOI-CRAWLER-001 | Preserve directional evidence basis in source-family candidates | StegVerse-Labs/Executive_Rhetoric_Ledger | Issue #51 implementation lane | config/source-families.json; schemas/source-family.schema.json; scripts/discover_source_family_links.py; scripts/validate_source_family_discovery.py; .github/workflows/run-recurring-discovery.yml | ERL-OSINT-API-001 / Issue #51 | MERGED_INTO_CANONICAL_WORKSTREAM | PARTIAL | live smoke currently PASS_WITH_BLOCKERS | PENDING_CRAWLER_RECEIPT_ENRICHMENT | false for this session | Issue #51; coordination/osint-session-tasks.json | implement Federal Register machine-readable adapter and directional candidate metadata before claim release |
| ERL-DPOI-ZERO-RESULT-001 | Prevent absent search hits from falsely weakening a DPOI | StegVerse-Labs/Executive_Rhetoric_Ledger | main | docs/DPOI_DIRECTIONAL_DISCOVERY.md; recurring search schemas/config | recurring-discovery category-search contract | COMPLETE | COMPLETE | validated by run 31188450324 | INTEGRATED | false | PR #55 | preserve `no-update` unless independent coverage-completeness evidence exists |
| ERL-DPOI-SESSION-CONSOLIDATION | Remove chat-only DPOI state and authority | StegVerse-Labs/Executive_Rhetoric_Ledger | main | docs/OSINT_SESSION_CONSOLIDATION_MIRROR_HANDOFF.md; coordination/osint-session-tasks.json; coordination/dpoi-directional-session-receipt.json | repository continuity surfaces | COMPLETE | COMPLETE | pending validation of consolidation-only commits | INTEGRATED | true until validation completes | commits ac1ea2a65e02dc3234cdb1c9007def12362b7691, 7df127a92886f26f98b10ac807c1199a5dd4f7f6, d944e15303199eee13a9e7a2ebc9480ef0a08637 | inspect triggered workflows and release session if green |

## Canonical continuation

MERGED INTO: `StegVerse-Labs/Executive_Rhetoric_Ledger` → `docs/OSINT_SESSION_CONSOLIDATION_MIRROR_HANDOFF.md` → `coordination/osint-session-tasks.json` → Issue #51.

## Session-specific completion rule

This session is archive-ready when the consolidation surfaces validate and no unique implementation or validation responsibility remains here. Issue #51's active claim is not a reason to retain this session because its remaining work is fully assigned, collision-bounded, finite, and machine-observable.
