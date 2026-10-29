# AI Failure-Aware Compute Accounting — Mirror Handoff

## Authority

Scoped continuity handoff for the ERL lane mirroring the multi-LLM research process conducted in `SV-LLM/Ecosystem_Chat` issue #9 ("Research: AI failure-aware compute accounting, customer remediation, and independent Kimi/Claude review"). This handoff governs only the mirror lane. Repository-wide continuity remains with `ERL_MIRROR_HANDOFF.md`.

## Lane identity

- Goal ID: `ERL-AI-FAILURE-ACCOUNTING-MIRROR-2026-10-26`
- Lane type: research-process mirror (not a primary evidence lane)
- Source: `SV-LLM/Ecosystem_Chat` issue #9 (private repository), issue body plus 78 comments (0001–0058 frozen batch, ERL PR #249; 0059–0078 append-only delta), 2026-10-26/28 UTC
- Mirror root: `mirrors/sv-llm-ecosystem-chat-issue-9/`
- Mirror authorization: owner direction recorded in source-issue comment `6429784312` ("Deferred public research publication — ERL mirror and Site pages"), which requires a 100% mirror — issue body, full comment chronology, multi-LLM contributions, competing claims, corrections, final adversarial review, and subsequent clarifications — with authorship, source URLs, stable identifiers, provenance, publicly appropriate redactions, and explicitly recorded authorized omissions. "A summary or link alone is not a 100% mirror."
- Canonical coordination owner: ERL issue #251 (research-candidate owner; append-only delta lane)
- Task Registry registration: PROPOSED as `EC9-WHEN-AI-SERVICES-FAIL-PUBLICATION-001` in StegVerse-Labs/.github PR #3373 (registration plan/apply ALLOW locally, COSV `10100000110000`, generation 321→322); not merged at this revision, so registration is not yet admitted

## Governing state

- Mirror lifecycle: frozen batch 0001–0058 verified (ERL PR #249, exact head `c3116e5e`: 58/58 bodies, 63/63 manifest blobs, two independent readbacks); append-only delta 0059–0078 installed under #251
- Case status of the underlying research: `evidence_solicitation_phase_closed` (source comment `6428361696`); provisional evidence baseline frozen; bounded custody work continuing
- Motive finding authorized: false
- Legal/culpability finding authorized: false (source issue maintains an explicit Zone 3 legal gate; independent legal review required before any cause-of-action language)
- Publication authorized for the manuscript: false. v1.0 bytes are in KV custody with two readbacks; v1.0.1 is committed to Site PR #1633 (draft, non-ALLOW; SPPA FAIL_CLOSED pending the Q74-01 custody basis)
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
- `mirrors/sv-llm-ecosystem-chat-issue-9/manifest.json` — file inventory with git blob SHAs (v5 covers the delta)

## Downstream

- StegVerse-Labs/Site Research landing page must LINK this mirror (per `6429784312` step 3) once merged to main. No Site work is performed in this lane.
- No Publisher, admissibility-wiki, stegguardian-wiki, tag, release, or other propagation is authorized from this lane.
