# Canada Economic Trajectory Mirror Handoff

## Authority

Bounded source of truth for the Canada historical-to-present economic trajectory lane in `StegVerse-Labs/Executive_Rhetoric_Ledger`.

Canonical coordination: Issue #78.
Canonical branch: `feature/paired-national-economic-trajectories`.

This lane establishes Canadian observations, mechanisms, affected populations, controls, contradictions, and outcomes independently. United States evidence may appear only as an external influence or explicit control; it may not define the Canadian finding.

## Goal

Build a reconstructable Canadian trajectory across:

- total, real, per-capita, median, and distributional economic measures;
- productivity, capital investment, labor, wages, and employment quality;
- housing, household debt, savings, affordability, and material insecurity;
- trade concentration, diversification, infrastructure, domestic processing, and market substitution;
- tariffs, retaliation, fiscal policy, regulation, public services, taxation, and transfers;
- wealth ownership and distribution;
- AI, automation, robotics, and labor displacement;
- sectoral, regional, demographic, and household effects.

## Governing rules

```text
Observation != effect.
Aggregate growth != household improvement.
Trade diversification != completed independence.
Policy timing != policy causation.
Same metric in another country != same Canadian meaning.
Missing evidence != permission to infer.
```

Every material finding must identify the measure, unit, price basis, population denominator, geography, time interval, source revision, transmission mechanism, affected groups, controls, contrary evidence, and confidence.

## Current state

```yaml
lane_id: ERL-ECON-CA
status: AUTOMATED_EVIDENCE_ACQUISITION_IMPLEMENTATION
national_findings_authorized: false
comparison_promotion_authorized: false
publication_authorized: false
canonical_issue: 78
```

## Initial implementation

- national trajectory schema;
- shared measurement dictionary;
- Canadian seed registry;
- source and gap matrix;
- validator and deterministic fixtures;
- CI integration.
- weekly official-source monitoring manifest;
- deterministic source fingerprinting and revision detection;
- gap-routed review-task generation;
- governed automation candidate branch with no finding or publication authority.

## Evidence acquisition order

1. Statistics Canada national accounts, household income, labor, prices, housing, wealth, debt, population, trade, and productivity.
2. Bank of Canada monetary, financial-stability, productivity, potential-output, trade, and household-debt records.
3. Global Affairs Canada and Finance Canada trade agreements, tariff actions, diversification, and sector records.
4. Parliamentary, provincial, regulatory, port, pipeline, rail, industrial, and budget records.
5. OECD, IMF, and World Bank controls with definition reconciliation.
6. Academic and independent analysis for mechanisms and alternative explanations.
7. Media and social claims only as labeled discovery or rhetoric objects.

## Release conditions

A Canadian trajectory finding may advance only when its national evidence chain is reconstructable and reviewable. Comparative use requires a reviewed Canadian finding ID, not an unreviewed raw observation.

## Remaining work

The automated lane now monitors declared Statistics Canada household, trade, and labor/automation surfaces and routes changes to Canadian gaps. Historical series extraction, source-specific normalization, evidentiary admission, mechanism analysis, independent review, and findings remain pending.

Known missing durable modules and destinations:

- source-specific historical-series adapters → `scripts/economic_adapters/canada/`;
- normalized revision-vintaged series → `economic-trajectories/canada/series/`;
- evidentiary admission queue → `economic-trajectories/canada/admission-queue.v1.json`;
- independent review receipts → `economic-trajectories/canada/reviews/`.

## Session consolidation — 2026-08-26

Live repository state at consolidation:

- Issue `#78`: open canonical coordination owner;
- PR `#79`: open draft, head `35d2807077a5106edf52ee1a21f7241abaf521a9`, currently reported mergeable by GitHub but materially diverged from `main`;
- session automation commit `5f0f0cc14a4fde6f1cfaeb4838287ce9b96b3543`: dedicated run `32900604098` passed;
- current-head dedicated run `32984047962`: queued when inspected and therefore not yet validation evidence;
- live `main` head: `9001265b6c690c077d3da70edd9a9992d5dfaf25`;
- branch/main relation: diverged, 20 commits ahead and 20 behind from merge base `2ca582ffe9297ddd452a54f90a96718660d5a033`.

The broader household-value and ownership-distribution capability on `main` is governed by `docs/ECONOMIC_DISTRIBUTION_MIRROR_HANDOFF.md`. It is complementary to this national lane, not a replacement: the distribution lane owns the cross-cutting household/distribution model, while this lane owns Canada-specific observations, mechanisms, affected populations, controls, and review. Integration must reconcile shared indicator definitions and preserve the stricter boundary rather than duplicating or overwriting either lane.

Next executable boundary: reconcile PR `#79` with current `main`; resolve the shared measurement-dictionary and Canada household/distribution overlap; rerun dedicated and repository-wide CI; then merge only if all owned checks pass. After merge, obtain the first repository-native economic research workflow run and persistent governed candidate receipt. No user credential, provider action, or iPhone step is required. No finding, comparison, publication, tag, release, deployment, or downstream propagation is authorized.

Archive state: all Canada-lane state unique to this session is durable in this handoff, Issue `#78`, PR `#79`, and their receipts. Continuation does not require this conversation.

Trigger custody: `research-candidates/2026-08-25-canada-us-economic-trajectory-linkedin-trigger.md` preserves the three user-supplied LinkedIn screenshots, hashes, session-derived research question, and the explicit limitation that the linked YouTube video was not reviewed or custodied.
