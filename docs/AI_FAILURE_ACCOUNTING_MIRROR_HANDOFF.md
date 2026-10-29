# AI Failure-Aware Compute Accounting — Mirror Handoff

## Authority

Scoped continuity handoff for the ERL lane mirroring the multi-LLM research process conducted in `SV-LLM/Ecosystem_Chat` issue #9 ("Research: AI failure-aware compute accounting, customer remediation, and independent Kimi/Claude review"). This handoff governs only the mirror lane. Repository-wide continuity remains with `ERL_MIRROR_HANDOFF.md`.

## Lane identity

- Canonical Goal Task ID: `EC9-WHEN-AI-SERVICES-FAIL-PUBLICATION-001`
- Historical mirror-lane label: `ERL-AI-FAILURE-ACCOUNTING-MIRROR-2026-10-26` (not a separate canonical Goal Task ID)
- Lane type: research-process mirror (not a primary evidence lane)
- Source: `SV-LLM/Ecosystem_Chat` issue #9 (private repository), issue body plus 113 comments (0001–0058 frozen batch, ERL PR #249; 0059–0078 delta 1, ERL PR #253; 0079–0101 delta 2, ERL PR #254; 0102–0105 delta 3, ERL PR #256; 0106–0111 delta 4, ERL PR #257; 0112–0113 delta 5, ERL PR #258), 2026-10-26/29 UTC
- Mirror root: `mirrors/sv-llm-ecosystem-chat-issue-9/`
- Mirror authorization: owner direction recorded in source-issue comment `6429784312` ("Deferred public research publication — ERL mirror and Site pages"), which requires a 100% mirror — issue body, full comment chronology, multi-LLM contributions, competing claims, corrections, final adversarial review, and subsequent clarifications — with authorship, source URLs, stable identifiers, provenance, publicly appropriate redactions, and explicitly recorded authorized omissions. "A summary or link alone is not a 100% mirror."
- Canonical coordination owner: ERL issue #251 (research-candidate owner; append-only delta lane)
- Task Registry identity: REGISTERED as `EC9-WHEN-AI-SERVICES-FAIL-PUBLICATION-001` — StegVerse-Labs/.github PR #3373 merged at expected head `9dce84f2` → `0fff5f55`; Registry generation 322, coordination_state PROPOSED, COSV `10100000110000`, WorkerCoordinator claim/fence null (registration is not execution authority). ERL main-merge exemption `REPOSITORY_MAIN_MERGE_TRANSFER_NOT_INSTALLED` is on file in `data/organization-role-exemption-register.json`

## Governing state

- Mirror lifecycle: frozen batch 0001–0058 MERGED (ERL PR #249 at `c3116e5e` → `5b55da3c`; 58/58 bodies, 63/63 manifest blobs, two independent readbacks); delta 1 0059–0078 MERGED (ERL PR #253 at `16fe6167` → `8daf6a01`; ChatGPT review 5690446174, Kimi readback PASS 6484885831); delta 2 0079–0101 MERGED (ERL PR #254 at `8b7ffc8a` → `0e319795`; non-author readback 6486520554: 22/22 bodies, RD-4 28,433 B digest, 106/106 blobs); delta 3 0102–0105 MERGED (ERL PR #256 at `898d7086` → `3148a85b`; non-author readback 6486628476: 4/4 bodies, 110/110 blobs); delta 4 0106–0111 MERGED (ERL PR #257 at `cc012a7a` → `855c1237`; non-author readback 6489016856: 6/6 bodies, 116/116 manifest blobs); delta 5 0112–0113 MERGED (ERL PR #258 at `98610e32` → `7ac28e23`; three concurring readbacks, 118/118 manifest entries; mirror lane closed through 0113); Claude CBOC records MERGED (ERL PR #247 at `878da1b8` → `e6b2193d`)
- Case status of the underlying research: `evidence_solicitation_phase_closed` (source comment `6428361696`); provisional evidence baseline frozen; bounded custody work continuing
- Motive finding authorized: false
- Legal/culpability finding authorized: false (source issue maintains an explicit Zone 3 legal gate; independent legal review required before any cause-of-action language)
- Publication authorized for the manuscript: false. v1.0 bytes are in KV custody with two readbacks; reviewed v1.0.2 is integrated into Site PR #1633 at `a95422e0` (L2 SHA-256 by ChatGPT and Kimi, Kimi text 29/29 and L2b PASS; draft, non-ALLOW; SPPA FAIL_CLOSED pending the Q74-01 custody basis)
- Publication authorized for THIS MIRROR: true, per comment `6429784312`, subject to the redaction and omission rules below

## Content boundaries (binding on this lane)

1. The mirror preserves the research record. It creates no findings. All substantive claims remain attributed to their authors and claim classes (OBSERVED / DERIVED / PROJECTED / UNAVAILABLE) exactly as recorded in the source.
2. "Overcharging" appears in this lane only as defined by the source register: computational overcharging — consumption/retention of finite prompt, execution, token, quota, or window entitlements for failed or materially nonconforming performance beyond the applicable failure-accounting standard; no monetary debit required. The standalone phrase "apparently overcharging" is barred as a headline or finding term (source comments `6427370281`, `6427861641`, `6428361696`).
3. No claim that any provider's backend ledger charged, deducted, reversed, or restored any specific entitlement. Per-event debits are UNKNOWN across the record.
4. No legal conclusions. Class-action and enforcement references in the record are contextual only.
5. Kimi-authored text must not be cited in support of any future legal section (standing conflict-of-interest constraint, source comments `6425428564`, `6426783484`).
6. Private screenshots (IMG_4068, IMG_4070–IMG_4075, IMG_4077–IMG_4085, C1AFD2B5-AF68-4B20-BEDB-C18A1126338E) are never included as images; their textual descriptions are part of the mirrored record; see `register/authorized-omissions.json`.
7. ERL-internal Case C / C-2 source records are cited by locator only; their contents are not reproduced here or in any downstream publication until ERL's own publication gate clears them (source comments `6427349734` L1, `6427370281`, `6427861641`).

## Installed structure

- `mirrors/sv-llm-ecosystem-chat-issue-9/README.md` — mirror charter, redaction/omission policy, custody statement
- `mirrors/sv-llm-ecosystem-chat-issue-9/issue-body.md` — verbatim source issue body with provenance front matter
- `mirrors/sv-llm-ecosystem-chat-issue-9/comments/NNNN-<comment-id>-<slug>.md` — one file per source comment, chronological, provenance front matter, verbatim body
- `mirrors/sv-llm-ecosystem-chat-issue-9/register/frozen-evidence-register.json` — machine-readable register: observations O1–O11, hypotheses H1–H6, evidence items E1–E6, case studies, claim stack, burdens, standard requirements, unresolved unknowns
- `mirrors/sv-llm-ecosystem-chat-issue-9/register/authorized-omissions.json` — explicit omission manifest (required by `6429784312`)
- `mirrors/sv-llm-ecosystem-chat-issue-9/register/redaction-log.json` — redaction review record
- `mirrors/sv-llm-ecosystem-chat-issue-9/manifest.json` — file inventory with git blob SHAs (delta 5 covers 113 comments; 118 non-self entries)

## Downstream

- StegVerse-Labs/Site Research landing page must LINK this mirror (per `6429784312` step 3) once merged to main. No Site work is performed in this lane.
- No Publisher, admissibility-wiki, stegguardian-wiki, tag, release, or other propagation is authorized from this lane.

## 2026-10-29 historical preparation checkpoint

The following records the pre-merge preparation state. The current reconciliation below supersedes its pending delta-5 and Site-edition statements.

- Registry re-read: `StegVerse-Labs/.github` at `7582e93b69548a8bd831ebd89d7dd49492281bce`, generation 322, 120 tasks. The canonical row remains `PROPOSED`, COSV `10100000110000`, completion unclaimed/unvalidated, WorkerCoordinator claim/fence null. Identity registration does not establish `INGRESS_ADMITTED` or execution authority. Display status remains INACTIVE.
- Session Prompt Count: 1 in this continuation session. Goal Prompt Count: NOT RECONCILED/20; neither the canonical record nor its Registry row supplies a cumulative count. The supplied previous-session count 15 is retained as a recovery coordinate, not a cumulative total; this prompt adds one qualifying prompt and does not reset the goal count.
- Source cutoff: comment `6488385324`, 2026-10-29T05:00:18Z, 113 comments. Delta 5 adds only `6488066956` and `6488385324`. Keep coordination receipts on #251 and the maintenance PR; do not create a recursive source-comment/mirror dependency.
- Site #1633 remains OPEN/DRAFT at `a95422e0ac8d683ffa055444824ce2052e54492b`. L2/L2b/L2c reviews are recorded; the manuscript is `NOT_ALLOWED` pending original custody authority and SPPA promotion. Registry dependency `DEP-EC9-MANUSCRIPT-V1_0_1` is stale relative to those receipts and must be reconciled by the existing Registry owner without promoting the custody dependency.
- Custody owner: `ORGANIZATION-BATCH-CUSTODY-REPLAY-001`, StegVerse-Labs/.github#2810. The SPPA source still declares no authenticating custody basis; original claim/fence, InTr, TV/TVC and custody receipts plus independent sovereign readback are required before native ALLOW. Local source evaluation or test fixtures cannot supply them.
- Delta 5 next action: non-author compare both new source bodies/timestamps, preserve all 111 historical bodies and 4 redactions/7 omissions, verify 118 manifest SHA/byte entries and exact-head CI, then merge using the reviewed expected head under the existing ERL source-merge lane. Site publication is a separate transition.
- Verification this session: `python -m unittest tests.test_site_production_promotion_authorization -q` passed 25 tests at Labs `7582e93b`; these use temporary/fixture custody and are non-authorizing. A separate read-only CLI evaluation of Site head `a95422e0` with only observed repository/head/ref inputs returned exit 1, `FAIL_CLOSED`, `PROMOTION_MANIFEST_MISSING`, `receipt_appended=false`, `organization_readback=NOT_PERFORMED`, `promotion_may_proceed=false`. No authentic native request or sovereign receipt was supplied or fabricated. This diagnostic is not the original-owner custody transition.
- Maintenance validation: 109 unredacted source bodies match (accounting only for historical file-final newlines), all 113 source timestamps/positions match, four redacted-span digests reproduce, and all 111 historical comment blobs are unchanged. The two new bodies match exactly. Existing research-candidate validator passes (32 groups, 33 candidate files).
- Manual Work: None.


## 2026-10-29 current reconciliation — continuation prompt 10

- ERL mirror through 0001–0113 is complete: PR #258 merged as `7ac28e232138573761d75c7c5be0879083f4ebe`. Owner closure: https://github.com/StegVerse-Labs/Executive_Rhetoric_Ledger/issues/251#issuecomment-6492450128 . Do not repeat source-body mirroring or create recursive source comments. No mirror content, manifest, omissions or redactions changes in this maintenance update.
- Site #1633 now carries independently reviewed v1.0.3 at `822b77e186f6ff5ea86e7f35c7cb77c49358fc08`, still draft / NOT_ALLOWED. Owner integration: https://github.com/StegVerse-Labs/Site/pull/1633#issuecomment-6503989152 . PDF: 186269 bytes, SHA256 `463fce02c432dede1a5505376e1f41b67b05c81c2a34f0a2f9ab07c56373ab28`; DOCX: 55591 bytes, SHA256 `be72df87676b07f9e6cef84d5c338abe5738344a82ffefc98edc592c52dd9db7`. Historical v1.0.2 expectations are superseded for future production verification.
- TVC #559 and #560 are merged; genuine main-push run `40917305561`, job `123600841295`, emits Labs receipt `sha256:2e0ec2ddf99dd53b8a42d8bd2f1f4253871da2b3a7068ce69027b3ffdf1a5ed2` with `ledger_candidate=true`. Receipt recovery and read-only native main-source parser/seal/admission preflight succeeded. Governed Labs writer append, supplied-epoch transition and published native consumer acceptance remain separate; no append is claimed here.
- Existing source repair #3376 at `d810644d` has completed independent review and relevant 109-case CI evidence. Its required verification still needs accepted TVC ledger evidence before protected integration. No duplicate custody reader implementation is needed.
- Live EC9 shard `12337d19` remains PROPOSED, both dependencies UNRESOLVED, claim/fence null. Original owners: custody #2810, Registry #3195, ledger writer #3183, Site #1633. Authentic task-bound custody, sovereign/MR readback, admitted manuscript dependency event and exact-head native SPPA ALLOW remain required before promotion.
- Session Prompt Count: 10. Goal Prompt Count: NOT RECONCILED (+10 this session)/20; request original Registry-owner reconciliation, never reset by changing sessions or repositories.
- Next work: original writer ingest/readback; authentic custody and Registry returns; protected source integration; exact-head Site SPPA and post-promotion live-byte verification. Maintain the current reviewed edition unless a separately reviewed content change is required.
- Manual Work: None.
