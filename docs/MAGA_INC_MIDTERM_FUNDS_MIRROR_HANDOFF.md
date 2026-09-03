# MAGA Inc. Midterm Funds / Potential Misuse Mirror Handoff

## Authority

Bounded source of truth for `ERL-2026-09-03-MAGA-INC-MIDTERM-FUNDS-001` in `StegVerse-Labs/Executive_Rhetoric_Ledger`.

Repository-wide continuity remains governed by `ERL_MIRROR_HANDOFF.md`. Research-candidate activation remains governed by `docs/RESEARCH_CANDIDATE_ACTIVATION_MIRROR_HANDOFF.md` and `coordination/research-candidate-activation-registry.v1.json`. Issue `#120` is the durable candidate-specific coordination owner.

## Goal

Determine whether primary records support any misuse proposition concerning funds raised, represented, retained, transferred, or spent by MAGA Inc. or materially related committees in the 2025-2026 cycle, while preserving the distinction between political strategy, donor expectation, legal restriction, and actual misuse.

## Current state

- lifecycle: `RESEARCH_ACTIVE_NOT_ASSESSABLE`
- committee official anchor: `MAGA INC.` / FEC `C00892471`
- initiating media lead: discovery only
- FEC committee identity/current summary: verified
- research-candidate activation registry: registered / hosted validation success
- filing-level reconstruction: partial
- transaction-level reconstruction: pending
- solicitation/represented-purpose reconstruction: pending
- related-party/vendor review: pending
- legal-authority mapping: pending
- contradiction review: pending
- independent review: pending
- actual misuse finding: not made
- legal violation finding: not made
- donor-intent violation finding: not made
- motive finding: not authorized
- publication finding: not authorized

## Installed surfaces

- `research-candidates/2026-09-03-maga-inc-midterm-funds-potential-misuse.md`
- `config/maga-inc-midterm-funds-source-queue.v1.json`
- `assessments/source-posture/2026-09-03-maga-inc-midterm-funds-initial-fec-anchor.json`
- `assessments/chronology/2026-09-03-maga-inc-fec-filing-chronology.partial.json`
- `coordination/research-candidate-activation-registry.v1.json`
- Issue `#120`

## Initial official FEC anchor

Official FEC committee page: `https://www.fec.gov/data/committee/C00892471/`.

Current summary coverage: 2025-01-01 through 2026-07-31.

- total receipts: `$400,684,172.17`
- total disbursements: `$21,034,141.27`
- independent expenditures: `$1,708,261.87`
- other disbursements: `$19,325,879.40`
- ending cash on hand: `$403,450,026.85`
- debts/loans owed by committee: `$0.00`

These are summary-level observations only. FEC warns newly filed summary data may lag. No transaction purpose, beneficial-recipient, donor-intent, coordination, personal-use, or misuse conclusion is authorized from the summary.

## Filing chronology advancement

Partial official filing chronology now preserves three FEC filing anchors:

1. Image `202507319789366210` — new FEC Form 3X July 31 Mid-Year report; coverage 2025-01-01 through 2025-06-30.
2. Image `202601029793901842` — amended FEC Form 3X 30-Day Post-Special Election report for Tennessee; coverage 2025-07-01 through 2025-12-22.
3. Image `202602209837825060` — FEC Form 3X monthly report covering 2026-01-01 through 2026-01-31; summary page reports opening 2026 cash of `$304,395,525.76`, January receipts of `$6,576,796.16`, January disbursements of `$78,060.75`, and closing cash of `$310,894,261.17`.

Native byte hashes remain pending. Amendment existence is not treated as evidence of wrongdoing without content-level reconciliation.

## Activation validation evidence

Research-candidate activation registration commit: `46d5339bc57f16493eaa3f50f5d31883398887d9`.

Hosted workflow `Validate research candidate activation`, run `33819845470`, completed successfully on `main` for that commit. This proves the candidate is represented in the machine-enforced activation registry with durable ownership and a next executable task; it does not prove any substantive misuse proposition.

## Governing invariants

- `large_cash_balance != misuse`
- `delayed_spending != misuse`
- `donor_frustration != donor_deception`
- `political_strategy != personal_use`
- `stated_political_objective != legally_restricted_use`
- `secondary_reporting != transaction_level_proof`
- `candidate_layer_exists != finding`
- `amended_filing != wrongdoing`

## Next executable boundary

1. Acquire FEC Statement of Organization and amendments for `C00892471`.
2. Complete enumeration of all 2025-2026 regular reports and amendments.
3. Reconstruct monthly cash, receipts, disbursements, independent expenditures, other disbursements, debts, refunds, and amendment supersession.
4. Build committee/affiliate/shared-vendor relationship graph.
5. Preserve donor-facing solicitations and represented purposes with provenance.
6. Map controlling FEC legal restrictions and relevant advisory/enforcement precedent.
7. Reconcile primary committee statements about 2026 spending strategy.
8. Run contradiction, alternative-explanation, and independent review before any promotion.

## Completion condition

This lane may transition only when primary-source transaction, representation, authority, contradiction, and independent-review evidence supports an explicit governed promotion, supersession, merge, or closure decision.

No Site, Publisher, admissibility-wiki, stegguardian-wiki, master-records, tag, release, or publication propagation is authorized from the current state.
