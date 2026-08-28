# United States Economic Trajectory Mirror Handoff

## Authority

Bounded source of truth for the United States historical-to-present economic trajectory lane in `StegVerse-Labs/Executive_Rhetoric_Ledger`.

Canonical coordination: Issue #78.
Canonical branch: `feature/paired-national-economic-trajectories`.

This lane establishes U.S. observations, mechanisms, affected populations, controls, contradictions, and outcomes independently. Canadian evidence may appear only as an external influence or explicit control; it may not define the U.S. finding.

## Goal

Build a reconstructable U.S. trajectory across:

- total, real, per-capita, median, and distributional economic measures;
- productivity, profits, capital investment, labor, wages, and employment quality;
- housing, healthcare, insurance, food, household debt, savings, and material insecurity;
- trade dependence, domestic productive capacity, tariffs, retaliation, and foreign market loss;
- fiscal, tax, regulatory, immigration, public-service, and transfer policy;
- wealth ownership and distribution;
- AI, automation, robotics, and labor displacement;
- sectoral, state, demographic, and household effects.

## Governing rules

```text
Observation != effect.
GDP or market strength != broad household security.
Tariff revenue != foreign payment without incidence evidence.
Protected capacity != competitive capacity.
Policy timing != policy causation.
Same metric in another country != same U.S. meaning.
Missing evidence != permission to infer.
```

Every material finding must identify the measure, unit, price basis, population denominator, geography, time interval, source revision, transmission mechanism, affected groups, controls, contrary evidence, and confidence.

## Current state

```yaml
lane_id: ERL-ECON-US
status: AUTOMATED_EVIDENCE_ACQUISITION_IMPLEMENTATION
national_findings_authorized: false
comparison_promotion_authorized: false
publication_authorized: false
canonical_issue: 78
```

## Initial implementation

- national trajectory schema;
- shared measurement dictionary;
- U.S. seed registry;
- source and gap matrix;
- validator and deterministic fixtures;
- CI integration.
- weekly official-source monitoring manifest;
- deterministic source fingerprinting and revision detection;
- gap-routed review-task generation;
- governed automation candidate branch with no finding or publication authority.

## Evidence acquisition order

1. BEA national accounts, income, profits, investment, and international trade.
2. BLS labor, wages, productivity, prices, and employment quality.
3. Census income, poverty, inequality, housing, business, and population records.
4. Federal Reserve wealth distribution, credit, household finance, production, and regional evidence.
5. CBO, Treasury, USITC, USTR, federal budget, tariff, trade, and regulatory records.
6. State and sector records needed to resolve distribution and regional effects.
7. OECD, IMF, and World Bank controls with definition reconciliation.
8. Academic and independent analysis for mechanisms and alternatives.
9. Media and social claims only as labeled discovery or rhetoric objects.

## Release conditions

A U.S. trajectory finding may advance only when its national evidence chain is reconstructable and reviewable. Comparative use requires a reviewed U.S. finding ID, not an unreviewed raw observation.

## Remaining work

The automated lane now monitors declared Census, USITC, and BLS household, tariff, and labor/automation surfaces and routes changes to U.S. gaps. Historical series extraction, source-specific normalization, evidentiary admission, mechanism analysis, independent review, and findings remain pending.

Known missing durable modules and destinations:

- source-specific historical-series adapters → `scripts/economic_adapters/united_states/`;
- normalized revision-vintaged series → `economic-trajectories/united-states/series/`;
- evidentiary admission queue → `economic-trajectories/united-states/admission-queue.v1.json`;
- independent review receipts → `economic-trajectories/united-states/reviews/`.

## Session consolidation — 2026-08-26

Live repository state at consolidation:

- Issue `#78`: open canonical coordination owner;
- PR `#79`: open draft; latest research-implementation head before consolidation `35d2807077a5106edf52ee1a21f7241abaf521a9`; consolidation/evidence custody then advanced through `66585b1b3fa8806ac8fc7dc5a09400a5cad822e6` and the commit containing this handoff;
- session automation commit `5f0f0cc14a4fde6f1cfaeb4838287ce9b96b3543`: dedicated run `32900604098` passed;
- research-implementation-head dedicated run `32984047962`: queued when inspected and therefore not yet validation evidence;
- live `main` head: `9001265b6c690c077d3da70edd9a9992d5dfaf25`;
- branch/main relation: diverged, 20 commits ahead and 20 behind from merge base `2ca582ffe9297ddd452a54f90a96718660d5a033`.

The broader household-value and ownership-distribution capability on `main` is governed by `docs/ECONOMIC_DISTRIBUTION_MIRROR_HANDOFF.md`. It is complementary to this national lane, not a replacement: the distribution lane owns the cross-cutting household/distribution model, while this lane owns United States-specific observations, mechanisms, affected populations, controls, and review. Integration must reconcile shared indicator definitions and preserve the stricter boundary rather than duplicating or overwriting either lane.

Next executable boundary: reconcile PR `#79` with current `main`; resolve the shared measurement-dictionary and U.S. household/distribution overlap; rerun dedicated and repository-wide CI; then merge only if all owned checks pass. After merge, obtain the first repository-native economic research workflow run and persistent governed candidate receipt. No user credential, provider action, or iPhone step is required. No finding, comparison, publication, tag, release, deployment, or downstream propagation is authorized.

Archive state: all U.S.-lane state unique to this session is durable in this handoff, Issue `#78`, PR `#79`, and their receipts. Continuation does not require this conversation.

Trigger custody: `research-notes/2026-08-25-canada-us-economic-trajectory-linkedin-trigger.md` preserves the three user-supplied LinkedIn screenshots, hashes, session-derived research question, and the explicit limitation that the linked YouTube video was not reviewed or custodied.

Latest validation receipt: final consolidation head `e7301ed259a97c6ed882489bdac9a2f6d9c59c65` runs `33008909790` and `33008909743` failed because the marginal-dependency/substitution additions exceed the current measurement and gap-matrix schemas. This is implemented-but-not-validated work, not activation evidence. Run `33008909711` failed only on the three pre-existing unregistered candidates owned by Issue `#80`, confirming that moving the screenshot trigger manifest out of the candidate root removed the newly introduced fourth registration blocker.
