# Mirror: SV-LLM/Ecosystem_Chat issue #9 — AI failure-aware compute accounting research

## What this is

A 100% mirror of the research process conducted in the private issue `SV-LLM/Ecosystem_Chat#9` ("Research: AI failure-aware compute accounting, customer remediation, and independent Kimi/Claude review"), created under the owner-approved publication direction recorded in source comment `6429784312` (2026-10-26T23:28:51Z):

> "Mirror this issue's entire research process into the public Executive Rhetoric Ledger (ERL) repository. Include the issue body, full comment chronology, multi-LLM contributions, competing claims, corrections, final adversarial review, and subsequent clarifications; preserve authorship, source URLs, stable identifiers, provenance, and publicly appropriate redactions. A summary or link alone is not a 100% mirror. Protect private screenshots/account details and record authorized omissions explicitly."

## Contents

| Path | Object |
|---|---|
| `issue-body.md` | Verbatim source issue body (provenance front matter) |
| `comments/` | One Markdown file per source comment, chronological, 101 files, verbatim bodies (four logged partial redactions in the post-freeze deltas) with provenance front matter |
| `register/frozen-evidence-register.json` | Machine-readable register of the frozen evidence baseline (observations, hypotheses, evidence items, case studies, claim stack, burdens, standard, unknowns) |
| `register/authorized-omissions.json` | Explicit manifest of every authorized omission (required by the publication direction) |
| `register/redaction-log.json` | Redaction review record for all mirrored text |
| `manifest.json` | File inventory with git blob SHAs and source identifiers |

## Provenance model

Every mirrored file carries front matter with:

- `mirror_id` — stable ERL mirror identifier (`ERL-MIRROR-EC9-…`)
- `source_repo`, `source_issue`, `comment_id`, `source_url` — exact source locators (note: source repo is private; URLs are recorded for custody, not public reachability)
- `posted_by` — the GitHub account that posted the object (all source objects were posted via the `StegVerse` account)
- `attributed_author` — the author named in the object text (Kimi / Claude / ChatGPT / issue coordinator), or `not stated in comment text`
- `created_at` / `updated_at` — UTC timestamps from the source API record
- `redactions` — per-object redaction status
- `note` — optional; flags later corrections or supersessions (e.g., superseded artifact hashes) without altering the verbatim body

## Redaction and omission policy

1. **Redactions** (text altered): applied only where text would expose credentials, private account secrets, or third-party PII. Every redaction is logged in `register/redaction-log.json` with location and class. Result of the mirror review: **no redactions were required in objects 1–59**; the post-freeze deltas (0059–0101) carry four partial redactions (RD-1..RD-4) that remove collapsed blocks reproducing private-repository file content of `StegVerse-Labs/.github`, each logged with byte length and sha256.
2. **Omissions** (objects not mirrored): private screenshot image bytes, ERL-gated Case C/C-2 record contents, originating-conversation data, local manuscript binaries (all versions), and the Site candidate package. Each is explicitly recorded in `register/authorized-omissions.json` with class, reason, and authorization reference. An omission is part of the mirror, not a gap in it.
3. **Private-repo boundary:** the source issue lives in a private repository. This mirror publishes its *text record* under explicit owner direction. Nothing here grants access to, or reproduces, any other content of the source repository.

## Reading guidance

- The record is adversarial and self-correcting by design. Later comments frequently narrow or correct earlier ones (e.g., `6426819450` corrects `6426783484`; `6427594129` corrects `6427349734`; final reviews `6429425538` / `6429453316` / `6429477644` apply corrections F1–F6 / S1–S2 / N1–N3; `6432565196` supersedes the final-edition PDF hash announced in `6432435970`; `6466554826` supersedes `6429425538` and `6460969942` as Claude's operative final review). **Do not quote an early comment as the record's position without checking for later corrections.**
- Claim classes OBSERVED / DERIVED / PROJECTED / UNAVAILABLE are used throughout and are load-bearing.
- "Overcharging" in this record means *computational overcharging* as defined in source comment `6429784312`; the standalone phrase "apparently overcharging" is barred by reviewer consensus.
- The register's key structural artifacts: the four-axis failure taxonomy (delivery / side effects / attribution / charge treatment) with remedy-burden, remedy-effectiveness, and displayed-usage-availability fields; the five-layer claim stack; the three customer burdens (detection / remedy / continuation) plus correction-cost transfer; the three-zone design/significance/legal structure; the eight-requirement failure-accountability standard. See `register/frozen-evidence-register.json` for the indexed baseline.
- Manuscript version chain (all local artifacts; hashes in `register/authorized-omissions.json` OM-6): v0.6 (21 pp., reviewed) → v0.7 (7 pp. condensed brief, not a replacement) → v0.8 (25 pp.) → v0.9 (27 pp. annotated reconciliation) → v1.0 (18 pp. unified rewrite) → final 19-page publication edition.
- The frozen evidence register froze at comment 0046 (`6432565196`). Comments 0047–0058 are post-freeze; they add no evidence entries and do not alter the frozen baseline. They record the publication-coordination directive (0047), the independent Kimi and Claude publication reviews (0048, 0049 — both register-level PASS, text-level blocked on manuscript-byte custody), the Drive/KV binary-custody bridge (0050), multi-model coordination and lane assignments A–J (0051–0055, 0057), and Claude's reconciled and operative final adversarial reviews (0056, 0058). This mirror tracks the living source issue; later comments are mirrored as maintenance under owner issue #251.
- Comments 0059–0078 are the post-freeze append-only delta mirrored under owner issue #251 (2026-10-28): final-review cycle replies and ChatGPT's final disposition (0059–0060), Kimi's lane C/E receipts (0061), Lane A original-byte recovery and KV custody bridge delivery (0062–0066), Claude's independent custody receipt, final-text review and mirror readback (0067), native execution-authority and ACTIONS-BY-MANIFEST conformance analysis (0068–0069), the `.github` #3373 registration PR and Claude's local Registry apply (0070–0071), and v1.0.1 / Site #1636 coordination and reconciliation (0072–0078). They add no evidence entries.
- Comments 0079–0101 are append-only delta 2 (2026-10-28/29): lane maps and the A/B/C merge-decision record (0079–0082, 0086–0087), Site #1636/#1637 merges (0083–0084, 0092), Registry patch v2 and its transport and exact-match readbacks for `.github` #3373 (0085, 0090–0091, 0096–0099), v1.0.1/v1.0.2 artifact-identity readbacks (0088–0089, 0093–0095), and Kimi's return-cycle receipts with Claude's reply (0100–0101). They add no evidence entries.

## Custody statement

Mirrored from source API records on 2026-10-27/28. Source comment IDs and timestamps are preserved verbatim in front matter. File-level custody hashes: see `manifest.json` (git blob SHAs). A hash establishes byte identity, not the correctness of any interface accounting described in the record.