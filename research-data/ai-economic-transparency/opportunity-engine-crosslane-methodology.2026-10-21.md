# Cross-lane research input — AI Governance Opportunity Engine evidence methodology

Date: 2026-10-21  
ERL lane: `ERL-AI-ECON-TRANSPARENCY-001`  
Source task: `AI-GOVERNANCE-OPPORTUNITY-ENGINE-001`  
Source repositories: `StegVerse-Labs/StegBusiness-Ops`, `StegVerse-Labs/.github`

## Purpose

This artifact preserves research-methodology and longitudinal evidence insights from the completed AI Governance Opportunity Engine for possible use by the ERL AI Economic Transparency program.

It is a **cross-lane research input only**.

It does not:
- transfer Opportunity Engine company rankings into ERL;
- alter ERL provider findings, ratings, review state, activation state, publication state, or authority;
- reopen `AI-GOVERNANCE-OPPORTUNITY-ENGINE-001`;
- create outreach, proposal, purchasing, contracting, provider-operation, or execution authority.

ERL remains analytically independent.

## Canonical source-task status

Current canonical readback establishes:

- Goal Task ID: `AI-GOVERNANCE-OPPORTUNITY-ENGINE-001`
- COSV: `40000100100001`
- parent/root: `STEGVERSE-BUSINESS-OPPORTUNITY-ENGINE-PILOT-001`
- coordination state: `RETIRED`
- checkout state: `COMPLETED`
- completion disposition: `COMPLETE_WITH_EXPLICIT_UNKNOWNS`
- completion claimed: true
- completion validated: true
- archive ready: true
- successor Goal created: false
- future stronger evidence requires a separate task: true
- outreach hard disabled: true

The implementation is therefore **completed and retired, not superseded**.

This distinction matters. Retirement here means the bounded evidence cycle satisfied its completion contract. It does not mean a replacement engine displaced the historical implementation or evidence lineage.

Allowed next transitions are:
- `NO_FURTHER_EXECUTION_UNDER_THIS_GOAL`
- continuation only under a separately scoped future evidence-update task

Source closure:
- StegBusiness-Ops PR #51
- exact head `a9fd167a6fadd63a8eaef6bb5b10ac9416748ed4`
- validation run `35602471735`
- merged `0f22edcf245ca4ef94921afebb3c173e0b037b4a`

Canonical registry retirement:
- .github PR #2461
- exact head `4b449a9e74ddadc916fedee8a9385ffaa60177d9`
- cross-task validation run `35602896052`
- merged `268777161efecb0cde60bb47fc8db96c098226b5`

## Original evidence model

The Opportunity Engine separated the underlying opportunity model from evidence confidence.

Raw opportunity score:

```text
raw =
  0.25 * economic_scale
+ 0.25 * usage
+ 0.25 * transition_exposure
+ 0.15 * governance_gap
+ 0.10 * commercial_accessibility
```

Confidence-adjusted score:

```text
confidence_adjusted =
  raw * (0.50 + 0.50 * evidence_confidence/100)
```

Later evidence calibration used:

```text
evidence_confidence_score =
  ROUND_HALF_UP(
    100 * (
      0.35 * revenue_factor
    + 0.45 * usage_factor
    + 0.20 * product_factor
    )
  )
```

Revenue factors:
- `1.00`: A-class directly attributable absolute revenue/ARR
- `0.95`: mixed strong A/B or highly AI-exposed A-class segment
- `0.90`: A-class company/parent revenue where the ranked AI lane is not isolated
- `0.85`: B-class absolute revenue/run-rate
- `0.65`: A-class quantitative revenue-growth-only evidence
- `0.00`: no retained admissible quantitative revenue observation

Usage factors:
- `1.00`: retained A-class quantitative usage/adoption
- `0.50`: official first-party product/adoption evidence without a comparable quantitative aggregate
- `0.00`: no admissible usage evidence

Product/workflow factor:
- `1.00`: A-class official
- `0.85`: B-only
- `0.00`: no admissible evidence

## Provenance contract

The source program used explicit provenance classes:

- **A** — first-party filing, official metric, official product/adoption disclosure, API metric, or equivalent authoritative source
- **B** — strongly attributable, high-quality reporting or executive/company statement not meeting A-class requirements
- **C** — deterministic derivation from A/B evidence
- **UNKNOWN** — no admissible observation

Important controls:
- UNKNOWN observations may not contain fabricated measured numeric values.
- C-class observations require an explicit derivation.
- Future targets are not observed revenue.
- Valuation, funding, acquisition price, employee counts, web traffic, social followers, parent-segment revenue, or unrelated proxy measurements do not silently satisfy a missing revenue or usage lane.
- A stronger source may improve confidence without changing the underlying raw opportunity score.

## Immutable evidence lineage

The implementation moved from mutable enrichment toward an immutable evidence overlay model.

Historical evidence remained preserved:
- detailed top-10 evidence packet;
- four non-overlapping full-50 shards;
- deterministic baseline 50-company identity set.

Later evidence was added under:

`ai-governance-opportunity-engine/evidence/upgrades/upgrade_*.json`

The validator:
1. loads historical evidence;
2. verifies exactly 50 unique baseline companies;
3. applies upgrade overlays in lexical filename order;
4. allows a later observation to supersede the current evidence state for an existing company;
5. refuses additions/removals to the company identity set;
6. refuses frozen raw-score drift;
7. recomputes evidence confidence;
8. recomputes confidence-adjusted ranking;
9. validates deterministic ordering and tie-breaking;
10. fails if outreach is enabled.

This is a useful research pattern for ERL because later observations can update the current interpretation without rewriting the historical record.

## Longitudinal evidence program

The program ultimately completed **13 validated evidence upgrades**, followed by a bounded unresolved-lane sweep that found no factor-changing evidence.

The session covered the earlier progression in detail:

### Initial top-10 repair
The top-10 evidence repair established:
- deterministic `ROUND_HALF_UP`;
- JSON/CSV parity;
- strict A/B/C/UNKNOWN checks;
- explicit UNKNOWN behavior;
- hard outreach false;
- deterministic descending ranking.

A notable correction was AWS:
- B-class revenue factor `0.85`, not A-class;
- usage `1.00`;
- product `1.00`;
- confidence `95`;
- raw `93.50`;
- adjusted `91.16`.

The correction demonstrated that source class matters independently from the apparent quality of the economic number.

### Full-50 common-method calibration
The same evidence-confidence method was extended across the original 50-company baseline.

“Fully evidence-calibrated” was deliberately defined as:
- every baseline company is processed under the same evidence method;
- every identity appears exactly once;
- quantitative completeness is **not** implied;
- unsupported quantitative revenue or usage remains UNKNOWN.

Many lower-evidence rows initially remained at a conservative confidence of 43:
- revenue `0.00`;
- usage `0.50`;
- product `1.00`.

That state meant “evidence incomplete,” not “company weak.”

### Rank-sensitive evidence upgrades
Successive passes upgraded the most rank-sensitive missing lanes when stronger evidence became available.

Examples preserved in the session include:
- ServiceNow
- Cursor / Anysphere
- UiPath
- Palantir
- Snowflake
- Meta
- xAI
- Anduril
- Replit
- Databricks
- Moveworks
- ElevenLabs
- Tempus AI
- Glean
- CoreWeave
- NVIDIA
- Sierra
- Perplexity
- Shield AI
- Hugging Face
- Cognition
- Figure AI
- OpenEvidence
- Automation Anywhere
- Scale AI
- Abridge
- Hippocratic AI
- Harvey
- Writer
- Recursion
- Skild AI
- Groq
- Together AI
- Runway
- Physical Intelligence
- Mistral AI
- Insilico Medicine
- Cerebras
- Cohere

Later canonical work continued beyond the early session checkpoints and added further factor-changing observations.

The final canonical handoff records, among others:
- Waymo B-class annual revenue run-rate above $350M while retaining A-class ride-volume usage;
- Together AI B-class annualized revenue above $100M;
- Writer B-class company-wide ARR around $40M;
- Groq B-class approximate historical annual revenue around $100M;
- xAI A-class aggregate Grok usage around 117M MAUs;
- Mistral B-class annualized revenue run-rate above $400M;
- Abridge B-class contracted ARR around $117M.

The key methodological point is not the exact ranking. It is that the ordering moved materially as evidence quality changed **without changing frozen raw opportunity scores**.

## Final current ordering

The final merged deterministic ranking recorded in the canonical handoff is:

1. OpenAI
2. Tesla
3. Microsoft
4. Salesforce
5. Anthropic
6. Google DeepMind
7. NVIDIA
8. Amazon AWS
9. ServiceNow
10. Waymo
11. Meta
12. Anysphere (Cursor)
13. UiPath
14. GitHub
15. xAI
16. Palantir
17. Anduril
18. Moveworks
19. ElevenLabs
20. Databricks
21. Tempus AI
22. Glean
23. Replit
24. Sierra
25. Snowflake
26. Cognition
27. CoreWeave
28. Harvey
29. Hugging Face
30. Abridge
31. Recursion
32. Shield AI
33. Writer
34. Automation Anywhere
35. Skild AI
36. Groq
37. Insilico Medicine
38. Together AI
39. Cerebras
40. Mistral AI
41. Runway
42. Perplexity
43. OpenEvidence
44. Scale AI
45. Figure AI
46. Hippocratic AI
47. Cohere
48. Physical Intelligence
49. Lambda
50. Adept

This ordering must not be imported as an ERL provider ranking.

## Terminal UNKNOWN state

After the thirteenth evidence upgrade, a bounded unresolved sweep re-observed the remaining missing lanes.

No stronger factor-changing A/B/C evidence cleared the contract.

No `upgrade_015` was created.

Final unresolved terminal UNKNOWN lanes:
- Adept aggregate/revenue
- Figure AI standalone revenue
- Hippocratic AI standalone revenue
- Physical Intelligence standalone revenue

The canonical completion contract expressly permitted these to remain UNKNOWN.

Therefore:

**research completion != complete factual omniscience**

and:

**terminal UNKNOWN != blocker**

This is strongly analogous to ERL's `UNBOUNDED_UNKNOWN` treatment of non-reconstructable literal cost.

## Validation as research integrity

The Opportunity Engine repeatedly treated exact-head CI as evidence integrity rather than ordinary build hygiene.

Observed examples in the session:
- stale/diverged branches were closed or rebuilt on current main rather than merged over concurrent parent work;
- one full-50 pass detected a deterministic OpenEvidence rounding mismatch (`71.17` vs `71.16`) and refused merge until corrected;
- exact-head validation was required before expected-head merge;
- handoff closeouts were separately validated so canonical documentation reflected actual merge/run evidence rather than pending state.

This suggests an ERL research control:

> A research artifact whose deterministic reconstruction fails is not merely “documentation with a typo”; it is an evidence-integrity failure until reconciled.

## Reusable ERL methodological insights

### 1. Separate magnitude from confidence

Do not fold evidence quality directly into the underlying phenomenon.

For ERL:
- literal/request-attributable cost is one variable;
- reconstructability/disclosure confidence is another.

A provider may have:
- a known rate card;
- unknown literal request cost;
- strong product documentation;
- weak reconstructability.

Those states should remain distinct.

### 2. Do not estimate the missing quantity from confidence

Evidence confidence should not become a hidden estimator.

If literal cost is unobserved, a confidence score must not be multiplied by a hypothetical midpoint to manufacture cost.

This supports ERL's current `UNBOUNDED_UNKNOWN` treatment at 1K/100K/1M workloads.

### 3. Prefer equivalent evidence over convenient proxies

The Opportunity Engine rejected:
- valuation for revenue;
- financing for revenue;
- acquisition price for revenue;
- parent-segment revenue for standalone company revenue;
- production targets for realized revenue;
- qualitative popularity for aggregate usage.

ERL analog:
- published API price is not necessarily literal request cost;
- provider-wide revenue is not per-request economic attribution;
- plan price is not exact marginal request cost;
- unrelated usage aggregates are not request-bound consumption.

### 4. Preserve historical absence

If a metric was previously unavailable, later discovery of a stronger observation should not erase the prior state.

Use:
- dated observation;
- immutable predecessor;
- explicit supersession of the current interpretation.

This enables longitudinal study of changing transparency itself.

### 5. Confidence-driven rank movement is not phenomenon movement

A company/provider can move in an evidence-adjusted ranking because better evidence arrived.

That does not prove:
- governance improved;
- governance worsened;
- cost changed;
- provider behavior changed;
- product strength changed.

ERL should distinguish:
- changed provider surface;
- changed evidence availability;
- changed interpretation;
- changed underlying quantity.

### 6. Completion can preserve explicit unknowns

A research protocol may terminate successfully when:
- all bounded acquisition procedures were attempted;
- missing evidence is explicitly named;
- prohibited proxy substitutions are documented;
- reopen conditions are defined.

This is preferable to indefinite “active” state or fabricated closure values.

### 7. Retired is not superseded

A completed research lane may remain the canonical historical implementation.

Use “superseded” only when:
- a successor/replacement is actually admitted; and
- the lineage explicitly establishes replacement semantics.

Otherwise:
- COMPLETED/RETIRED = bounded cycle closed;
- future evidence event = separate update/research task.

### 8. No-change sweeps are evidence

A bounded search that finds no stronger admissible observation is itself meaningful if:
- scope is explicit;
- excluded proxies are listed;
- no-change disposition is preserved;
- no fake overlay/update is created merely to show activity.

### 9. Hard authority boundaries should survive research ranking

The Opportunity Engine kept `outreach_enabled=false` across all 50 rows and all overlays.

A ranking did not authorize:
- contact;
- proposals;
- publication;
- purchasing;
- contracting;
- provider operation.

For ERL, research findings likewise must not silently become publication, enforcement, commercial, or execution authority.

## Specific cross-lane comparison to ERL AI Economic Transparency

The ERL lane currently distinguishes consumer and API/enterprise surfaces and preserves `UNBOUNDED_UNKNOWN` when literal request-attributable cost cannot be reconstructed.

The Opportunity Engine methodology strengthens that model:

- consumer/API surface separation is analogous to company/segment/AI-lane separation;
- request-cost UNKNOWN is analogous to standalone revenue UNKNOWN;
- rate-card evidence is analogous to parent/company-wide economic evidence: informative, but not equivalent to the missing target quantity;
- a provider's stronger API documentation does not erase consumer-surface opacity;
- similarly, stronger parent/company disclosures do not automatically resolve a standalone AI-lane metric;
- later evidence should become a dated update, not mutate the original observation;
- protocol closure may retain UNKNOWN without converting it into a score-implied estimate.

## Research hypotheses suggested by the combined lanes

These are research candidates, not findings:

1. **Evidence-availability bias hypothesis**  
   Public rankings may systematically favor firms/providers with better disclosure even when the underlying economic or governance phenomenon is unchanged.

2. **Transparency-induced ordering volatility hypothesis**  
   Evidence-adjusted rankings may move more from disclosure events than from underlying operational changes.

3. **Surface-specific transparency hypothesis**  
   Transparency is not provider-global; it varies materially by consumer, API, enterprise, regulatory, filing, and investor surfaces.

4. **Proxy contamination hypothesis**  
   Research systems that do not enforce metric equivalence will drift toward valuation, rate-card, financing, traffic, or parent-segment proxies and create false precision.

5. **Terminal-unknown discipline hypothesis**  
   Explicit terminal UNKNOWN states improve longitudinal reproducibility compared with forced imputation.

6. **Immutable-overlay reproducibility hypothesis**  
   Dated overlay models permit more faithful reconstruction of how an assessment changed as evidence changed.

7. **Evidence confidence / economic magnitude decoupling hypothesis**  
   An observed change in confidence-adjusted score may be statistically separable from a change in the underlying economic magnitude.

## Suggested ERL use

This artifact may inform:
- scale-sensitivity methodology;
- unknown-state semantics;
- contradiction review;
- independent review criteria;
- longitudinal transparency studies;
- future research schemas for evidence confidence.

It should not be used to:
- copy Opportunity Engine ranks into ERL;
- claim provider-wide findings;
- convert absent literal cost into an estimate;
- reopen completed ERL work without a material new evidence event;
- create any external action authority.

## Canonical source references

- `StegVerse-Labs/.github/data/canonical-task-records/AI-GOVERNANCE-OPPORTUNITY-ENGINE-001.json`
- `StegVerse-Labs/.github/AI_GOVERNANCE_OPPORTUNITY_ENGINE_MIRROR_HANDOFF.md`
- `StegVerse-Labs/StegBusiness-Ops/AI_GOVERNANCE_OPPORTUNITY_ENGINE_MIRROR_HANDOFF.md`
- `StegVerse-Labs/StegBusiness-Ops/ai-governance-opportunity-engine/`
- `StegVerse-Labs/StegBusiness-Ops/ai-governance-opportunity-engine/evidence/upgrades/`

## Disposition

`CROSS_LANE_RESEARCH_INPUT_RECORDED`

No ERL conclusion is changed by this artifact alone.
