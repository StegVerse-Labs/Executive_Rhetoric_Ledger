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
status: FRAMEWORK_IMPLEMENTATION
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

## Release conditions

No comparative conclusion may advance until both referenced national findings are reviewed, definitions are reconciled, material gaps are bounded, and independent review reproduces the comparison.

## Remaining work

All real comparison results remain pending national evidence population and review.
