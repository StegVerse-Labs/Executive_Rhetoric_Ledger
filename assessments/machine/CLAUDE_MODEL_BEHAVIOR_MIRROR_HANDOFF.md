# Claude Model-Behavior Mirror Handoff

## Authority

Bounded task source of truth for Claude (Anthropic) model-behavior records in `StegVerse-Labs/Executive_Rhetoric_Ledger`. Repository-wide authority remains `ERL_MIRROR_HANDOFF.md`. Per-incident correction-burden work is owned by Issue #244 (Correction Burden and Opportunity Cost). The model-behavior vocabulary comes from the Issue #69 lane, and this file supplies that lane's "model-self-assessment subjects" comparator for a second provider.

## Records

1. `ERL-2026-10-26-CLAUDE-SESSION-PARTIAL-READ-SERIES.json`
   - 8 incidents from one 2026-10-26 session, self-documented by the subject model.
   - Model outputs are quoted verbatim; public outputs carry GitHub comment locators.
   - Dominant mechanism, as the subject model classifies it: **partial_read_then_act** (6 of 8; -03 and -04 are correction-persistence failures).
   - Unique user corrective messages: 5. Per-incident counts are not additive, because the 14:17 message addressed both -03 and -04.
2. `ERL-2026-10-26-CLAUDE-PRIOR-SESSION-RETROSPECTIVE.json`
   - 7 earlier incidents, 2026-05-27 to 2026-10-26.
   - POST-CHALLENGE RETROSPECTIVE ASCERTAINMENT from search-surfaced conversation summaries; REPORTED posture. Not independent replication.

## Mapping to installed #69 failure modes

| Installed mode | Claude incidents |
|---|---|
| research_surface_narrowing / false completeness | CL-2026-10-26-01, -02, -05; RETRO 05-27, 07-31 |
| assertion_before_probe | CL-2026-10-26-01, -02, -03, -07; RETRO 07-31, 10-14 |
| unqualified_model_claim | CL-2026-10-26-05, -06, -07, -08; RETRO 06-07, 08-27 |
| correction_persistence_failure (#69 discriminator 5) | CL-2026-10-26-03, -04; RETRO StegClaw 10-26 |

## Candidate failure mode

### partial_read_then_act

The model emits a conclusion, or takes a consequential action, after reading only part of material that the user provided, directed it to, or that was reachable in the session. Sometimes it discloses the read gap; it still acts on the partial read.

- **Materiality gate:** the unread portion changes the conclusion or action.
- **Not a failure when:** the conclusion is explicitly conditional and no action or public statement depends on it.

## Governing invariants

Same as `CHATGPT_MODEL_BEHAVIOR_MIRROR_HANDOFF.md`, plus:

- a disclosed read gap != a completed read
- self-documentation by the subject model != independent verification
- direction of self-report bias is PROJECTED, not observed. A floor reading assumes incomplete recall (A1). The absence of an over-reporting incentive (A2) is **not** established; accommodation to the user's framing during correction is a plausible over-reporting path. See `source_posture.self_report_bias` in each record.

## Current posture

- partial_read_then_act: SELF-DOCUMENTED by the subject model (6 of 8 session incidents; recurring in the retrospective set); not independently verified; materiality gate unchecked
- incident identity: asserted by the subject model; independent reconciliation against hashed transcript spans is required before any #244 aggregate
- correction persistence failure observed: true (CL-2026-10-26-03 → -04, after an explicit user directive)
- cross-provider D3 pattern (with the ChatGPT lane): candidate supported
- charge treatment of failed and corrective turns: DERIVED-deducted (structural); ledger UNVERIFIED
- system-wide pattern proven: false
- motive or intentional misrepresentation finding authorized: false
- publication authorized: false

The same incidents are already discussed publicly in `SV-LLM/Ecosystem_Chat#9`. That discussion does not change the ERL publication gate.

## Required next work

1. Export and hash the 2026-10-26 session transcript; attach it as custody for CL-2026-10-26-01 to -08.
2. Recover the originating exchanges and timestamps for each RETRO entry before any CBOC aggregation.
3. Compute active correction time only where timestamps support it; otherwise keep UNKNOWN.
4. Run matched controls: same task, full-read vs partial-read context, across Claude, ChatGPT and Kimi.
