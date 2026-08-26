# Comparative Economic Trajectories Mirror Handoff

## Authority

Bounded source of truth for comparing reviewed Canada and United States economic trajectory findings in `StegVerse-Labs/Executive_Rhetoric_Ledger`.

Canonical coordination: Issue #78.
Canonical branch: `feature/paired-national-economic-trajectories`.

This lane consumes national findings. It does not author, overwrite, or repair them.

## Goal

Determine where independently established Canadian and U.S. trajectories show significant similarity, divergence, structural breaks, sequencing, or temporal lag.

## Governing rules

```text
National evidence first.
Comparison second.
Same observation != same effect.
Same effect != same mechanism.
Temporal ordering != causation.
Visual similarity != statistical significance.
Country ranking != household welfare.
Comparison may identify gaps; it may not fill them by inference.
```

## Current state

```yaml
lane_id: ERL-ECON-CA-US-OVERLAY
status: REVIEWED_INPUT_GATE_IMPLEMENTATION
comparison_findings_authorized: false
lag_finding_authorized: false
causal_finding_authorized: false
publication_authorized: false
canonical_issue: 78
```

## Comparison contract

Each comparison must reference at least one reviewed Canadian finding and one reviewed U.S. finding. It must record:

- aligned and non-aligned definitions;
- comparable time windows and revisions;
- mechanism equivalence or difference;
- population and distribution compatibility;
- controls and alternative explanations;
- observed lead or lag by indicator;
- sensitivity to the selected baseline;
- evidence gaps and targeted next acquisition;
- confidence and review state.

The proposition that Canada is approximately six years ahead of the United States is registered only as an unassessed hypothesis. Indicator-level evidence may support different leads, no lead, reversal, or non-comparability.

## Initial implementation

- comparison-overlay schema;
- hypothesis registry;
- deterministic positive and negative fixtures;
- validator and CI integration;
- explicit failure when raw observations or unreviewed national findings are compared.
- explicit prohibition on external-source adapters in the comparison lane;
- manual-only comparison cadence pending reviewed national inputs.

## Release conditions

No comparative conclusion may advance until both referenced national findings are reviewed, definitions are reconciled, material gaps are bounded, and independent review reproduces the comparison.

## Remaining work

All real comparison results remain pending national evidence population and review. Automated national acquisition may create comparison-relevant gaps, but it cannot populate or promote this lane.

Known missing durable modules and destinations:

- definition-reconciliation packets → `economic-trajectories/comparison/reconciliation/`;
- structural-break and lag-analysis code → `scripts/economic_comparison/`;
- independent comparison-review receipts → `economic-trajectories/comparison/reviews/`.

## Session consolidation — 2026-08-26

PR `#79` remains open draft. The latest research-implementation head before consolidation was `35d2807077a5106edf52ee1a21f7241abaf521a9`; consolidation/evidence custody then advanced through `66585b1b3fa8806ac8fc7dc5a09400a5cad822e6` and the commit containing this handoff. At live inspection GitHub reported the PR mergeable, but `main` was `9001265b6c690c077d3da70edd9a9992d5dfaf25` and the histories had materially diverged by 20 commits on each side from merge base `2ca582ffe9297ddd452a54f90a96718660d5a033`. The session automation increment at `5f0f0cc14a4fde6f1cfaeb4838287ce9b96b3543` passed dedicated run `32900604098`; research-implementation-head run `32984047962` was queued when inspected and was not yet a passed receipt.

`docs/ECONOMIC_DISTRIBUTION_MIRROR_HANDOFF.md` now governs a complementary cross-cutting household/distribution capability on `main`. It explicitly requires Canada and U.S. national trajectories to be independently reconstructed before comparison, matching this overlay's contract. Integration may share reconciled indicator definitions, but the distribution lane may not populate a national effect and this overlay may not consume raw distribution observations or unreviewed national findings.

Next executable boundary: reconcile PR `#79` with `main`, resolve shared definitions without weakening either evidence gate, rerun all owned validation, merge, and observe the first repository-native national automation receipt. Comparative population remains blocked until independently reviewed Canadian and U.S. findings exist. No user action or credential step is required. No comparison, lag conclusion, causal finding, publication, tag, release, deployment, or propagation is authorized.

Archive state: all comparison-overlay state unique to this session is durable in this handoff, Issue `#78`, PR `#79`, and their receipts. Continuation does not require this conversation.

Trigger custody: `research-candidates/2026-08-25-canada-us-economic-trajectory-linkedin-trigger.md` preserves the original rhetoric screenshots and the user's bounded comparison question. It is discovery-only and cannot serve as a national or comparative finding endpoint.
