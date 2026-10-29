# ERL Native Research Automation — Mirror Handoff

Updated: 2026-10-28
Goal Task ID: ERL-NATIVE-RESEARCH-AUTOMATION-001 (issue #245; Registry admission not authenticated)
COSV: UNVERIFIED
Authority: StegVerse-Labs/Executive_Rhetoric_Ledger#245; repository-wide ERL_MIRROR_HANDOFF.md; related #60 (closed), #132 (closed), #223 (open), Trumpality#8 (closed).
Coordination branch: research/erl245-existing-acquisition-reconciliation-20261028
Disposition: RESEARCH/COORDINATION ONLY; no authenticated WorkerCoordinator claim/fence, manifest ALLOW, or sovereign runtime receipt.

## Verified implementation inventory (2026-10-28)
- Trumpality `.github/workflows/erl-active-research.yml`: scheduled at 05 minutes every 6 hours; runs deterministic adapter tests and `scripts/erl_research_agent.py`; persists append-only source candidates, receipts and dispositions. Workflow presence does not prove today's runtime success.
- Trumpality `scripts/erl_research_agent.py`: consumes active frontier `id` or `trajectory_id` and `required_evidence` or `acquisition_queries`, searches whitelisted sources, emits lead-only candidates and scan receipts; cannot promote findings.
- ERL `.github/workflows/trumpality-research-intake.yml`: scheduled at 35 minutes every 6 hours; resolves pinned Trumpality commit, runs `scripts/intake_trumpality_research_candidates.py`, writes readback.
- ERL `scripts/intake_trumpality_research_candidates.py`: `GROUP_ID = ERL-RC-TRUMP-FAMILY-CRYPTO-MARKET-2026`, `LANE_DOC` and `LANE_DIR` are hardcoded. Therefore successful intake in this single lane does not prove universal research-lane coverage.
- ERL #223 documents successful prior producer/intake cycles and subsequent Registry/MyKV repair evidence; reconcile exact latest owner and readback before any reimplementation.
- ERL #132 and #60 are closed; do not reopen completed architectural tasks merely because #245 is open.

## Exact bounded next source change (original owner lane only)
Extend the existing ERL consumer with an authenticated lane mapping/configuration derived from current ERL research frontier and approved Registry entries, rather than creating a new research engine. Preserve legacy crypto lane paths and historical byte-prefix receipts unchanged. Dispatch candidates by approved trajectory/group mapping; unknown/unadmitted mappings must fail closed without mutating another lane. No token or workflow permission is authority.

## Parallel independent work
A. Owner/Registry: verify task identity, COSV, native claim/fence, expected head, and authorize exact consumer paths.
B. Producer: verify most recent Trumpality six-hour execution and pin actual source commit/scan receipts.
C. Consumer: implement multi-lane routing with strict mapping and backward-compatible legacy intake; no source write before claim.
D. Tests: fixture for two independent lanes, unknown mapping, replay, cross-lane injection, duplicate candidate, stale producer commit, lost fence, and unchanged historical hashes.
E. Research: acquire source material for #252 national-election case study and separate any unrelated Butler/Crooks research intake; do not infer personal misconduct or conflate unreviewed claims with findings.
F. Custody: independent exact-head CI, sovereign KV readback, owner review and protected merge.

## Acceptance evidence
Two distinct admitted lanes produce fresh acquisition receipts, intake and independent review requests without repeated prompts; each has exact source commit, source digest, deterministic tests, non-ALLOW negative controls, authenticated manifest transition, and sovereign readback. Prior #223 evidence is reusable but does not by itself satisfy this multi-lane criterion.

## Manual action
None requested from user. Native owner must issue authentic Registry/COSV and WorkerCoordinator claim/fence before protected implementation. On absent authority preserve explicit FAIL_CLOSED, continue independent read-only evidence and tests.

## Next prompt
Authenticate #245's canonical Registry task and claim; inspect owner branch; implement scoped multi-lane intake in the existing consumer with deterministic adversarial tests and exact-head CI; reconcile #223/#252 and KV, avoiding duplicate infrastructure.
