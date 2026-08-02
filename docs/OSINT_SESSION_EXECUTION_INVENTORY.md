# OSINT Session Execution Inventory

Canonical continuation: `docs/OSINT_SESSION_CONSOLIDATION_MIRROR_HANDOFF.md`

| Task ID | Originating goal | Destination | Exact location | Owner | Claim state | Completion | Validation | Integration | Archive dependency | Evidence | Next executable action |
|---|---|---|---|---|---|---|---|---|---|---|---|
| CHAT-RUNTIME-001 | Ecosystem Chat vertical slice | StegVerse-org/LLM-adapter | `docs/ECOSYSTEM_CHAT_MIRROR_HANDOFF.md`, Issue #18, Issue #31 | adapter workflows | BLOCKED | provider path integrated; real provider unexecuted | contract tests PASS | Site/custody bindings installed | durable provider authority state | merged adapter commits and receipts | observe authorized provider receipt; execute only when authority receipt and bindings exist |
| CHAT-CUSTODY-001 | custody and reconstruction | master-records/orchestration | `docs/ECOSYSTEM_CHAT_CUSTODY_MIRROR_HANDOFF.md` | runtime evidence workflow | COMPLETE for transition custody | authenticated custody and reconstruction PASS | hosted workflow PASS | adapter round trip integrated | provider-usage custody remains | PR #3 merge `421da84784888e3dc9bb98a7b2b47a1518f0eee0` | wait for real provider usage, then run existing custody path |
| CHAT-SITE-001 | Site activation and projection | StegVerse-Labs/Site | `docs/SITE_MIRROR_HANDOFF.md`, Issue #24 | Site orchestrator | CLAIMED_FOR_IMPLEMENTATION | portable-node and deterministic fallback verified; activation pending | handoff lists current workflow evidence | Publisher observer installed | real provider plus persistent endpoint | Site canonical handoff | obey Site orchestrator; do not duplicate active claims |
| CHAT-PUBLISHER-001 | downstream publication | GCAT-BCAT-Engine/Publisher | `docs/PUBLISHER_MIRROR_HANDOFF.md` | hourly awareness workflow | MACHINE_OWNED/BLOCKED | consumer implemented | Publisher validation PASS | waiting on Site declaration/readiness | Site packet release condition | Publisher handoff and artifact | existing hourly observer rechecks automatically |
| OSINT-DAILY-001 | daily new and old data sweep | StegVerse-Labs/Executive_Rhetoric_Ledger | `.github/workflows/run-recurring-discovery.yml` | recurring workflow | MACHINE_OWNED | live family crawl operational | run `29999867554` PASS | candidate pipeline integrated | source API/feed coverage incomplete | artifact `8560503648` | implement machine-readable source families and coverage windows |
| OSINT-LIVE-001 | Charlotte immigration incident source chain | Executive Rhetoric Ledger | `config/source-adapters.json` | source capture workflow | COMPLETE | three live source adapters installed | live capture validation PASS | review routing integrated | none | PR #38 merge `79104cbed100bb777c31721f26c6b192aa97762f` | monitor updates through daily workflow |
| OSINT-HISTORY-001 | older un-ingested records | Executive Rhetoric Ledger | discovery receipt schema, backfill queues | recurring workflow | CLAIMED_FOR_IMPLEMENTATION | backfill machinery exists; coverage accounting incomplete | deterministic backfill tests PASS | daily source families partially integrated | pagination/date windows missing | current handoff | add per-family time-window, page cursor, and gap receipts |
| PERSON-ROUTING-001 | share reviewed evidence to person repositories | Executive Rhetoric Ledger → Trumpality | `person_specific_projections/trumpality.json` | post-review generator and Trumpality consumer | CLAIMED_FOR_INTEGRATION | producer and consumer code merged | repository tests PASS | destination main receipt not fully reverified | Trumpality import evidence | ERL PRs #35-#37; Trumpality PR #4 | verify Trumpality projection on main and destination receipt |
| CLAIM-CLEANUP-001 | prevent duplicate execution | Executive Rhetoric Ledger | PRs #39, #41, #42 | this consolidation lane | SUPERSEDED | stale duplicate implementations | replacement PRs #43/#44 validated | canonical main contains final code | stale PR closure | merge commits `78755c…`, `67eafa…` | close superseded PRs with canonical references |
| PROVIDER-AUTH-001 | real model execution | LLM-adapter | provider authority receipt and receipt-triggered workflow | human authority boundary + repository workflow | BLOCKED | dormant gate built | Architecture Guard and validation PASS | runtime path integrated | explicit approval receipt, model, Master-Records bindings | adapter handoff | no execution until exact authority receipt reaches main |

## Session goal consolidation

1. Authoritative URLs and startup order — COMPLETE; preserved in Site handoff and canonical docs.
2. Ecosystem Chat machine execution — COMPLETE through fail-closed runtime and transition custody; provider activation BLOCKED and durably owned.
3. Provider protocol compatibility and authority gating — COMPLETE in source and validation; execution BLOCKED by explicit authority receipt.
4. Person-specific repository sharing — IMPLEMENTED and reviewed-only; destination verification assigned to Trumpality.
5. Daily OSINT sweep — ACTIVE and machine-owned; official machine-readable source coverage and historical coverage receipts remain.
6. Charlotte case intake — COMPLETE and monitored.
7. Duplicate PR/session consolidation — ACTIVE in this inventory and canonical handoff.
8. Site/Publisher propagation — MERGED INTO canonical Site and Publisher handoffs; no duplicate implementation permitted.

## Collision rules

- PR #48 owns only Fauci HSGAC assessment files.
- Site active claims listed in `docs/SITE_MIRROR_HANDOFF.md` remain exclusive.
- Publisher Site propagation is machine-owned by its existing hourly workflow.
- This workstream owns only ERL OSINT source coverage, historical gap accounting, Trumpality projection verification, and session consolidation.
