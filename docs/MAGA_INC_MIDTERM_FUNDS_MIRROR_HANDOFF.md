# MAGA Inc. Midterm Funds / Potential Misuse Mirror Handoff

## Authority

Bounded source of truth for `ERL-2026-09-03-MAGA-INC-MIDTERM-FUNDS-001` in `StegVerse-Labs/Executive_Rhetoric_Ledger`.

Repository-wide continuity remains governed by `ERL_MIRROR_HANDOFF.md`. Research-candidate activation remains governed by `docs/RESEARCH_CANDIDATE_ACTIVATION_MIRROR_HANDOFF.md` and `coordination/research-candidate-activation-registry.v1.json`. Issue `#120` is the durable candidate-specific coordination owner.

## Goal

Determine whether primary records support any legally, representationally, governance-wise, or strategically material proposition concerning funds raised, represented, retained, transferred, or spent by MAGA Inc. or materially related committees in the 2025-2026 cycle, without collapsing distinct axes into a single `misuse` label.

## Reusable fund-governance model

Installed and machine-enforced:

- `standards/fund-governance-classification.v1.md`
- `schemas/fund-governance-classification.schema.json`
- `scripts/validate_fund_governance_classification.py`
- `.github/workflows/validate-fund-governance-classification.yml`
- `assessments/fund-governance/2026-09-03-maga-inc-midterm-funds.classification.json`

Four independent axes:

1. `legal_misuse`
2. `represented_purpose_divergence`
3. `governance_ethical_misuse`
4. `strategic_nondeployment`

Core invariant:

`legal_permissibility != represented_purpose_alignment != governance_quality != deployment_strategy`

Dedicated fund-governance validation run `33919866860` succeeded. Repository-wide `Validate Ledger Schemas` run `33920105658` also succeeded after an unrelated educational-access intake schema repair.

## Current classification

Lifecycle: `RESEARCH_ACTIVE_NOT_ASSESSABLE`.

- legal misuse: `INSUFFICIENT_EVIDENCE`
- represented-purpose divergence: `REPRESENTATION_NOT_RECONSTRUCTED`
- governance/ethical misuse: `INSUFFICIENT_EVIDENCE`
- strategic nondeployment: `STRATEGY_NOT_RECONSTRUCTED`
- finding authorized: false
- publication authorized: false

Seven-dimension state vector:

- `LEGALITY`: partial FEC authority boundaries reconstructed; case-fact mapping pending
- `DONOR_REPRESENTATION`: solicitation/purpose custody pending
- `BENEFICIAL_RECIPIENT`: partial Schedule E only; other disbursements pending
- `ORGANIZATIONAL_PURPOSE`: Hybrid PAC account-purpose authority plus committee identity partially reconstructed; case-specific restrictions pending
- `DEPLOYMENT_TIMING`: retained balance and limited observed deployment require full chronology plus 24/48-hour IE normalization
- `CONTROL_CONCENTRATION`: not yet reconstructed
- `DISCLOSURE_ACCURACY`: filings partial; amendment supersession and FEC display-method normalization pending

## Installed case surfaces

- `research-candidates/2026-09-03-maga-inc-midterm-funds-potential-misuse.md`
- `config/maga-inc-midterm-funds-source-queue.v1.json`
- `assessments/source-posture/2026-09-03-maga-inc-midterm-funds-initial-fec-anchor.json`
- `assessments/source-posture/2026-09-04-maga-inc-fec-summary-method-boundary.json`
- `assessments/chronology/2026-09-03-maga-inc-fec-filing-chronology.partial.json`
- `assessments/evidence/2026-09-03-maga-inc-initial-independent-expenditure-anchor.json`
- `assessments/evidence/2026-09-03-maga-inc-statement-of-organization-anchor.json`
- `assessments/evidence/2026-09-04-maga-inc-fec-authority-boundaries.json`
- `assessments/fund-governance/2026-09-03-maga-inc-midterm-funds.classification.json`
- `coordination/research-candidate-activation-registry.v1.json`
- Issue `#120`

## Official FEC identity and summary anchor

Official committee page: `https://www.fec.gov/data/committee/C00892471/`.

Observed current profile:

- committee: `MAGA INC.`
- committee ID: `C00892471`
- registration date: `2024-11-07`
- type: active monthly Hybrid PAC with Non-Contribution Account, nonqualified, unauthorized
- summary coverage: `2025-01-01` through `2026-07-31`
- total receipts: `$400,684,172.17`
- total disbursements: `$21,034,141.27`
- independent expenditures: `$1,708,261.87`
- other disbursements: `$19,325,879.40`
- ending cash on hand: `$403,450,026.85`
- debts/loans owed by committee: `$0.00`

These are summary-level observations only and authorize no adverse finding.

## Critical FEC summary-method boundary

The FEC committee page states that its displayed independent-expenditure totals are drawn from quarterly, monthly, and semi-annual reports and **do not include 24-hour or 48-hour independent-expenditure reports**. The FEC also warns newly filed summary data may take up to 48 hours to appear.

Therefore:

`committee_page_IE_summary != complete_IE_transaction_population`

A reconstructed Schedule E + 24/48-hour population must be deduplicated, amendment-normalized, and reconciled against like-for-like reporting classes before any discrepancy claim is permitted.

Durable method artifact:
`assessments/source-posture/2026-09-04-maga-inc-fec-summary-method-boundary.json`

## FEC legal/authority boundary advancement

Primary FEC guidance now establishes an initial legal framework in:
`assessments/evidence/2026-09-04-maga-inc-fec-authority-boundaries.json`.

Boundaries reconstructed so far:

1. Hybrid PACs may maintain a segregated non-contribution account receiving unlimited permissible-source funds for independent expenditures, candidate-referencing ads, and generic voter drives, alongside a contribution account subject to statutory limits/source restrictions.
2. Contribution and non-contribution accounts must remain segregated; both are subject to reporting guidance and applicable expense-allocation rules.
3. Non-contribution accounts may accept unlimited funds from individuals, corporations, labor organizations, and other political committees, but not prohibited sources including foreign nationals, federal contractors, national banks, or federally chartered corporations.
4. An independent expenditure is expressly candidate-related advocacy made without coordination with the candidate/campaign/party; coordination can change its legal character.
5. Hybrid PAC non-contribution-account funds cannot be used to make candidate contributions; candidate contributions must come from the contribution account under applicable limits and source rules.

Initial cited authority includes 11 CFR 102.5(a)(1), 103.2, 106.6, 110.1(d), 100.16, 109.21, and 109.37.

These rules are authority inputs, not proof that MAGA Inc. violated any rule. Personal-use and related-party-payment authority remain separately incomplete.

## Filing / organization reconstruction

Current primary filing anchors:

1. Form 1 image `202507309764365676` — amended Statement of Organization filed 2025-07-30; Charles Gantt observed as treasurer, Bulldog Compliance address, committee email and website.
2. Form 3X image `202507319789366210` — new July 31 Mid-Year report; coverage 2025-01-01 through 2025-06-30.
3. Form 3X image `202601029793901842` — amended 30-Day Post-Special Election report for Tennessee; coverage 2025-07-01 through 2025-12-22.
4. Form 3X image `202601319808906870` — new January 31 Year-End report; coverage 2025-12-23 through 2025-12-31.
5. Form 3X image `202602209837825060` — new February 20 monthly report; coverage 2026-01-01 through 2026-01-31; opening cash `$304,395,525.76`, receipts `$6,576,796.16`, disbursements `$78,060.75`, closing cash `$310,894,261.17`.

The official profile independently confirms registration date `2024-11-07`; the original 2024 Form 1 image remains unlocated after the current machine search pass. No image number is inferred or fabricated.

Native byte hashes remain pending. Amendment existence is not wrongdoing evidence without content-level reconciliation.

## Independent-expenditure data quality

Prior duplicate repair commit: `ec5cbf3a3c5ed2f070e144cad426e92f3fbf134c`.

Distinct partial Schedule E sample:

- `SE.4694` — Designated Market Media; 2025-11-19; `$2,310.00`; production cost/digital ad; Aftyn Behn; TN-07; oppose.
- `SE.5214` — Electoral Communications Group, LLC; 2026-03-09; `$8,950.44`; text messages; Clay Fuller; GA House; support.

These are not a cycle total and support no adverse classification.

## Governing invariants

- `large_cash_balance != misuse`
- `delayed_spending != misuse`
- `strategic_nondeployment != misuse`
- `donor_frustration != donor_deception`
- `lawful != aligned_with_represented_purpose`
- `represented_purpose_divergence != legal_violation`
- `political_strategy != personal_use`
- `related_party_payment != self_dealing`
- `private_benefit != prohibited_personal_use`
- `authority_rule != case_violation`
- `secondary_reporting != transaction_level_proof`
- `committee_page_IE_summary != complete_IE_population`
- `candidate_layer_exists != finding`
- `amended_filing != wrongdoing`
- `partial_schedule_e_sample != cycle_total`

## Remaining machine-executable work

1. Locate the initial 2024 Form 1 and every later Form 1 amendment; build field-level supersession chronology.
2. Complete enumeration of all 2025-2026 regular reports and amendments.
3. Enumerate complete Schedule E plus 24/48-hour IE population; deduplicate and amendment-normalize before reconciliation.
4. Reconstruct monthly cash, receipts, disbursements, other disbursements, debts, refunds, and amendment supersession.
5. Build committee/affiliate/shared-vendor relationship graph and beneficial-recipient map.
6. Preserve donor-facing solicitations and represented purposes with provenance.
7. Extend controlling FEC authority only where case facts make additional rules/advisory/enforcement precedent material, including personal-use/related-party boundaries.
8. Reconstruct control concentration and committee decision authority separately from beneficial-recipient evidence.
9. Reconcile primary committee statements about 2026 spending strategy and deployment timing.
10. Run contradiction, alternative-explanation, and independent review before promotion on any axis.

## Completion / propagation boundary

This lane may transition only when primary-source transaction, representation, authority, control, contradiction, and independent-review evidence supports an explicit governed promotion, supersession, merge, or closure decision. Each axis retains its own evidence path.

No Site, Publisher, admissibility-wiki, stegguardian-wiki, master-records, tag, release, or publication propagation is authorized from the current state.
