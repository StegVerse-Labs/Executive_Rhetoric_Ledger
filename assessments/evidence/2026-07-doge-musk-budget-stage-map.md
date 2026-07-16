# DOGE/Musk Assessment — Budget Evidence Stage Map

```yaml
topic_id: "PIT-MODERN-2026-DOGE-MUSK-EXPOSURE"
status: "active-partial"
last_reviewed: "2026-07-16"
final_budget_finding: false
```

## Purpose

Prevent the assessment from comparing unlike fiscal objects or treating a proposal, appropriation, obligation, outlay, projection, or claimed saving as interchangeable.

## Installed official sources

| Receipt | Fiscal object | Permitted use | Prohibited use |
|---|---|---|---|
| `SRC-GOVINFO-BUDGET-2026` | President's FY2026 budget proposal collection | Proposed priorities, requested levels, and administration policy posture | Enacted appropriations, obligations, actual outlays, or realized savings |
| `SRC-TREASURY-MTS-COLLECTION-001` | Treasury Monthly Treasury Statement collection | Official modified-cash accounting categories and source system for receipts, outlays, and deficit or surplus | Exact June 2026 values until the corresponding machine-readable period data or archived statement is installed |
| `SRC-GAO-24-105833` | Government-wide fraud-loss estimate for FY2018–FY2022 | Scale control with GAO's uncertainty and scope limitations | Agency attribution, program attribution, prediction, or proof of DOGE performance |

## Required fiscal stages

```text
presidential request
-> congressional authorization where applicable
-> enacted appropriation
-> apportionment and allotment
-> obligation
-> outlay or expenditure
-> Treasury period result
-> final fiscal-year actual
```

A claimed saving may enter the comparison only after it is classified as one or more of:

- announced;
- estimated;
- gross;
- net;
- duplicated;
- corrected;
- cancelled authority;
- deobligated amount;
- avoided future spending;
- realized cash outlay reduction.

## Current evidence posture

The repository can presently establish:

1. an official FY2026 presidential proposal collection exists;
2. Treasury's Monthly Treasury Statement is the official modified-cash source for monthly receipts, outlays, and deficit or surplus;
3. GAO estimated a broad government-wide fraud-loss range but imposed limitations that prevent agency-level or predictive use.

The repository cannot yet establish from installed primary receipts:

- final FY2025 outlays on the selected comparison basis;
- exact FY2026 receipts, outlays, and cumulative deficit through June 2026;
- final FY2026 outlays;
- a net fiscal effect attributable to DOGE;
- whether any claimed saving reduced cash outlays rather than future authority, contracts, leases, staffing, or planned spending;
- whether budget reallocations were caused by DOGE rather than enacted policy choices by other authorities.

## Next required objects

1. June 2026 Monthly Treasury Statement period data in JSON, CSV, XML, PDF, or archived form.
2. Final FY2025 Monthly Treasury Statement or Financial Report values on the same accounting basis.
3. CBO June 2026 Monthly Budget Review and its timing adjustments.
4. Enacted FY2026 appropriations and continuing-resolution instruments.
5. DOGE ledger versions and correction history mapped to affected Treasury or agency accounts.
6. Claim-level reconciliation showing whether each claimed saving became an actual outlay reduction.

## Promotion boundary

```text
proposal evidence
+ official period actuals
+ comparable prior-year actuals
+ enacted authority
+ claim-level DOGE reconciliation
!= proof of motive or conflict
```

Even a validated fiscal reallocation or lack of aggregate budget reduction would not independently establish that a specific enforcement or oversight action was taken to benefit Musk.
