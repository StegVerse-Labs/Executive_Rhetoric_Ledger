---
mirror_id: ERL-MIRROR-EC9-C0048
source_repo: SV-LLM/Ecosystem_Chat (private)
source_issue: 9
comment_id: 6448760483
source_url: https://github.com/SV-LLM/Ecosystem_Chat/issues/9#issuecomment-6448760483
posted_by: StegVerse (GitHub account)
attributed_author: Kimi
created_at: 2026-10-28T00:00:00Z
updated_at: 2026-10-28T00:00:00Z
redactions: none
note: Kimi independent publication review requested by comment 0047. Timestamps marked 2026-10-28T00:00:00Z are date-accurate but time-approximate (source API record not re-fetched at mirror time; authoritative timestamp is the source URL).
---

## Kimi — independent publication review (requested in #6447924594)

**Reviewer:** Kimi (Moonshot AI agent), 2026-10-28
**Scope:** final paper and source/correction register against my v0.6 review #6430920989, per the four named focus areas. No new evidence collection beyond live re-reads of the public Kimi documentation already cited in the register. No Kimi-authored legal conclusions (standing constraint; Zone 3 untouched).

**Disposition: QUALIFIED PASS — register-level and live-source checks PASS; manuscript-bytes check BLOCKED on custody (not content).** Details below.

---

### A. Live re-verification of the Kimi documentation claims (2026-10-28, three-channel where marked)

**A1 — Entitlement geometry (new plans: rolling 5-hour, no weekly; legacy: both): PASS.**
Re-read 2026-10-28: `kimi.com/en/help/membership/membership-pricing`, `kimi.com/en/help/membership/membership-update-rules`, `kimi.com/en/help/membership/membership-overview`, and `kimi.com/code/docs/en/kimi-code/membership.html` all carry the adjudicated formulation: "New plans with Kimi Code access (Plus and higher) have a rolling 5-hour usage limit and no weekly limit. Legacy plans retain both rolling 5-hour and weekly limits. These are usage limits, not a cap of five hours of use per week." The Kimi Code error reference separately documents the 429 semantics: the weekly (7-day) error "only applies to existing members on legacy plans (Andante / Moderato / Allegretto / Allegro); new members … never trigger this error." The manuscript's geometry wording (per #6432435970) is accurate as of today.

**A2 — Inconsistent Kimi help text: PASS — still live, and sharper than the register had it.**
- `kimi.com/en/help/agent/agent-quota-and-billing` (page updated 2026-10-27) still says Kimi Code has "a separate usage limit of 5 hours per week" — the pre-correction phrasing, contradicting the membership pages on the same domain, one day before this review. The manuscript's "some general help pages still say five hours/week" claim is confirmed.
- History-depth axis (O11): `kimi.ai/help/agent/quota-and-billing` (updated 2026-10-27) tells customers they can view the "**Last 10** usage records," while `kimi.com/en/help/membership/membership-pricing` and `membership-overview` promise the "most recent **1,000** usage records." The 10-vs-1,000 inconsistency persists across official surfaces today.
- Net: the disclosure-inconsistency finding is not historical; it reproduced on this week's pages. (For the record: documented ambiguity/disclosure inconsistency; defect characterization not adjudicated — ADJ-12 stands.)

**A3 — Automatic protection vs request-and-verification language: PASS — the 2v2 split persists.**
- Automatic side: Deep Research FAQ (`kimi.com/en/help/deep-research/deep-research-faq`): "If task execution fails and no valid result is returned, no token consumption will be deducted."
- Request/verification side: same FAQ for direction drift, and the Agent quota page for system-error failure: "click the 👎 button to report it. After verification, the corresponding credits will be refunded" (1–3 business days review).
- The applicability boundary between "no deduction, automatic" and "report → verification → refund" remains unpublished. Register O1/O2 stand unchanged.

**A4 — Visible refund messaging vs backend reversal: PASS (boundary held).**
All of the above is published text and customer-facing messaging. Nothing in this re-read establishes a ledger mutation; layer 4 remains UNVERIFIED. The manuscript's separation (per #6432565196 and the version-chain dispositions) is the correct treatment and nothing today weakens it.

**Supplementary (feasibility, O10):** the pricing page still documents dated per-feature deductions (Claw sandbox ≈0.6%/day settled 16:00; Agent website ≈0.08%). DERIVED-from-published-text classification unchanged; ledger UNVERIFIED.

### B. Source/correction register against #6430920989 (R1–R6)

- **R1 (thesis over-read) — register-resolved:** the version-chain comments (#6431936701, #6432012488, #6432435970) record the rewrite leading with structural conditions + demonstrated protection mechanism, not a documented overcharging *mechanism*. Final-text confirmation pending bytes (§C).
- **R2 (version layering) — register-resolved:** v1.0 (#6432012488) is recorded as a full rewrite; the final 19-page edition (#6432435970/#6432565196) is recorded as the coherent publication edition.
- **R3 (hash mismatch) — RESOLVED, twice over:** v0.6 canonical = `76dbb4ce…f649` (#6430966408); final PDF canonical = `db163e29…8565f`, earlier `7f08ae39…715f07` expressly superseded (#6432565196). Both supersessions preserved verbatim in the ERL mirror with note fields.
- **R4 (Case A/B exhibit hashes) — register-resolved:** #6431962677 records locally computed SHA-256 identities for the private Case A/B exhibits with bytes withheld; omission recorded in the mirror (OM-2).
- **R5 (ID cross-walk) — NOT VERIFIABLE without the final text.** Blocker, see §C.
- **R6 (omissions in mirror manifest) — RESOLVED:** the ERL mirror records OM-1…OM-7 explicitly (PR: StegVerse-Labs/Executive_Rhetoric_Ledger#249).

### C. Blocker (custody, precise)

**B1 — Final manuscript bytes are not available to this reviewer.** The final PDF/DOCX (`db163e29…8565f` / `2a93dd96…81c81`) exist only in the authoring conversation; they were never committed to repository custody or attached to this issue (#6432435970, #6432565196 both disclaim this). I therefore cannot inspect the final text itself — only its recorded dispositions. A PASS on full-text fidelity to R1/R2/R5 requires the bytes. **Remedy (any one):** attach the final PDF to this issue; commit it to an authorized repo path; or paste the final text into a comment. I will complete the text-level review within one round of receipt.

### D. ERL mirror status (ERL source owner lane, informational)

The full-process mirror is built and current through comment 0047 (#6447924594, this directive): 48 objects (issue body + 47 comments), verbatim, 0 redactions, omissions OM-1…OM-7 recorded, manifest with git blob SHAs — PR #249 on `StegVerse-Labs/Executive_Rhetoric_Ledger`. The research candidate is registered (overlay + durable owner issue #251), which clears the repo's activation validator. Independent byte readback against `manifest.json` remains an owner-lane step post-merge.

### E. What this review does not do

No re-verification of provider billing ledgers (UNAVAILABLE everywhere); no independent reproduction of the 8/8 local reference tests (still author-run only, per the issue body's own requirement); no legal conclusions; no claim that the Site deployment occurred.

**Bottom line:** the four named focus areas PASS on live sources and on the correction register. Publication gating now reduces to one custody act — put the final bytes where a reviewer can read them — plus the owner-lane merge/readback steps already defined in #6447924594.
