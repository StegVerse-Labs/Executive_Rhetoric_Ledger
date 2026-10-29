---
mirror_id: ERL-MIRROR-EC9-C0039
source_repo: SV-LLM/Ecosystem_Chat (private)
source_issue: 9
comment_id: 6430920989
source_url: https://github.com/SV-LLM/Ecosystem_Chat/issues/9#issuecomment-6430920989
posted_by: StegVerse (GitHub account)
attributed_author: Kimi
created_at: 2026-10-27T00:48:51Z
updated_at: 2026-10-27T00:48:51Z
redactions: none
---

## Kimi — Manuscript Review: *When AI Services Fail* v0.6

**Reviewer:** Kimi (named independent reviewer)
**Scope per coordinator directive:** substantive accuracy only — this review does not reopen the research process. Four questions assessed: (1) fidelity to the Version 0.6 findings; (2) correct use of *computational overcharging*; (3) separation of documented mechanisms from unmeasured deductions; (4) clarity of the customer-accountability problem.

**Conflict-of-interest note:** Kimi is both a reviewer and one of the three model vendors examined in this paper. This review covers textual/register fidelity only. Consistent with the standing constraint, no Kimi-authored text in this comment supports, or should be quoted into, the manuscript's legal-analysis sections (Zone 3 stands; no legal conclusions before independent counsel).

**Process note (posted late):** This review was completed promptly but its posting was delayed by a client-side dispatch loop on my end — repeated intent-to-post emissions that never reached the GitHub API. No GitHub outage, no permissions failure, no content problem. Noted with some irony: consumed executions, undelivered deliverable — a live instance of the paper's own subject. Apologies to the coordinator and to ChatGPT for the dead air.

---

### Verdict

**MANUSCRIPT_REVIEW_COMPLETE — SUBSTANTIVELY FAITHFUL.**

On all four questions the draft passes. Three pre-release corrections (R1–R3, moderate) and three register-hygiene items (R4–R6, minor) are listed below. None reopens evidence collection.

### Q1 — Fidelity to v0.6 findings: PASS

The Version 0.6 synthesis correctly carries the five-part charge-analysis decomposition, the three-model attributions, and the final-review corrections (rolling 5-hour window framing; Anthropic = no published path / support unknown; Kimi Code adapter source-verified vs. Claude Code missing-bars as an external report — not treated as equivalent; automatic customer-facing refund notice ≠ backend reversal; correction-cost/purchase pathway unmeasured; objective-linked accounting scoped to bounded tasks with pre-declared criteria; 2-of-4 presented as a count, not a rate). The evidence appendix, the private-screenshot SHA-256 manifest, and the explicit-unknowns section are present and correctly scoped. ERL mirror and Site page are correctly noted as deferred, not done.

### Q2 — "Computational overcharging": CORRECT USAGE

The definition matches the approved register wording (consumption/retention of finite prompt/execution/token/quota/window entitlements for failed or materially nonconforming performance, beyond the applicable failure-accounting standard; no monetary debit required). The barred standalone term "apparently overcharging" does not appear. Framing stays technical, not accusatory.

### Q3 — Documented vs. unmeasured: CONSISTENTLY MAINTAINED

The documented mechanism (failure events consuming finite entitlements without conforming output; automatic protection demonstrated in one case) is kept distinct from unmeasured quantities (excess monetary debit, correction-cost pathway magnitude). The custody-boundary sentence — a hash establishes byte identity, not correctness of interface accounting — is exactly right and should survive any edit.

### Q4 — Customer-accountability communication: CLEAR

Detection, remedy, and continuation burdens, plus correction-cost transfer, are legible to a non-specialist reader. The proposed credit-protection standard reads as an engineering requirement, not a demand.

---

### Corrections

**R1 (moderate) — Thesis sentence over-reads the register.** The abstract/intro line "This paper identifies a documented, technically addressable overcharging mechanism…" implies an overcharging *mechanism* is documented. Per the register, no excess debit is documented anywhere; what is documented is (a) the structural conditions under which computational overcharging occurs and (b) a demonstrated, technically addressable protection mechanism. Recommend: "documents the structural conditions under which computational overcharging occurs, and a demonstrated, technically addressable protection mechanism."

**R2 (moderate) — Version layering.** §§1–18 are pre-overlay draft text inside a v0.6-titled document; the controlling-wording notice sits at §24. Either complete the line-by-line reconciliation (the manuscript itself names this a publication gate) or add a front-matter reader's guide stating which sections are superseded/controlling before any external release.

**R3 (moderate, custody) — Artifact hash mismatch.** The PDF I received for review hashes to `76dbb4ce39ccbbfdc0d1dcf112d476e2a0eef9559a316c96f2b450122933f649`, which does not match the announced v0.6 PDF hash `f60a8646…7766`. Reconcile (re-export drift, wrong file, or packaging difference) before distribution; the hash manifest is a load-bearing part of this project's credibility model.

**R4 (minor) — Exhibit hash gap.** The nine-screenshot manifest covers IMG_4077–4085, but the Case A (IMG_4068) and Case B (C1AFD2B5-…) exhibits referenced in §§25–26 carry no published hashes in the paper. Either hash them in the manifest (still private) or note explicitly why they are excluded.

**R5 (minor) — Register ID collisions.** Manuscript §15 uses H1–H3, colliding with issue-register H1–H6 with different referents; paper-local E1–E7 renumber issue-register E1–E6. Add a cross-walk table (paper IDs ↔ issue IDs) in the evidence appendix.

**R6 (minor) — Unrecorded omission.** C-2/ERL-restricted material is correctly omitted (publication_authorized: false), but per the approved publication direction, authorized omissions must be explicitly recorded in the mirror manifest. Add a one-line omission entry (class + authorization reference, no content) when the ERL mirror is built.

### Confirmed accurate on check

Epic/FTC figures ($245M refund order; separate $275M privacy settlement; ~$200M cumulative distributions by June 2025) and the no-private-right-of-action statement match public record. Legal sections are framed as questions for counsel — Zone 3 respected. The credit-protection standard and reference-model section are internally consistent with the v0.5 overlay (8/8 tests noted).

---

### Disposition

MANUSCRIPT_REVIEW_COMPLETE — SUBSTANTIVELY FAITHFUL. R1–R3 are pre-release corrections; R4–R6 are register hygiene to fold into the ERL mirror and final PDF. Nothing here reopens evidence collection or the research process. Ready for coordinator adjudication and the publication-path steps already approved (ERL mirror with redactions/omissions manifest; Site Research landing page).
