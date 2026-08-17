# Environmental Policy Inventory Execution Handoff

Date: 2026-08-16
Parent authority: `assessments/environmental-policy/ENVIRONMENTAL_POLICY_MIRROR_HANDOFF.md`
Goal: `ERL-ENV-POLICY-REAGAN-TRUMP47-001`
State: `ACTIVE / SOURCE ACQUISITION`

## Governing scope

The inventory includes any federal policy instrument that governs environmental treatment **or changes an activity in a way that affects the environment**. This includes policies framed primarily as energy, industrial, agricultural, extractive, commercial, infrastructure, transportation, manufacturing, land-use, procurement, subsidy, permitting, or economic policy when their operative mechanism changes environmentally consequential activity.

Policy-caused activity change is `PRIMARY_INVENTORY`; it must not be demoted to a later analytical control. Independent activity changes not caused or governed by the policy may later serve as controls.

Commercial water remains primary inventory where applicable: bottled, spring, purified, mineral, artesian, well, distilled, sparkling and other packaged drinking water; FDA quality/identity standards; FTC claims; source/purity/treatment/health/environmental claims; extraction/source links; recalls/enforcement; and raw company claims.

Invariant: **Preserve and present truth through evidence.** No administration or policy receives a better/worse score at the inventory layer.

## Installed inventory batches

### Foundation batch

`2026-08-16-reagan-ghwb-clinton-water-foundation-batch.json`

Commit: `60edf55a4c34eff7871a61cee2fb4212b7d3f6c3`

Nodes include:
- Reagan — 1986 Safe Drinking Water Act amendments;
- Reagan — SARA 1986;
- Reagan — EPCRA/SARA Title III;
- George H. W. Bush — 1990 Clean Air Act amendments;
- George H. W. Bush — Pollution Prevention Act;
- Clinton — 1995 FDA bottled-water identity/quality rule;
- Clinton — 1996 FDA bottled-water chemical-quality amendment.

### Mid-period batch

`2026-08-16-clinton-gwb-obama-policy-batch.json`

Commit: `29dd30b928f5610bcc28b622b186b1e693646751`

Nodes include:
- Clinton — Food Quality Protection Act of 1996;
- Clinton — Safe Drinking Water Act amendments of 1996;
- Clinton — microbial/disinfection-byproduct drinking-water implementation seed;
- George W. Bush — 2004 nonroad diesel engine/fuel rule;
- Obama — Mercury and Air Toxics Standards;
- Obama — Clean Power Plan;
- Obama — 2016 oil/gas methane NSPS.

### Late-period batch

`2026-08-16-trump45-biden-trump47-policy-batch.json`

Commit: `6813fdc639a0516566a701fdab6319318ab22e85`

Nodes include:
- Trump 45 — 2019 WOTUS repeal rule;
- Trump 45 — 2020 Navigable Waters Protection Rule;
- Trump 45 — Affordable Clean Energy rule;
- Biden — 2024 PFAS National Primary Drinking Water Regulation;
- Biden — 2024 PFOA/PFOS CERCLA designation;
- Biden — 2024 Steam Electric ELG;
- Biden — 2024 legacy CCR/CCRMU rule;
- Biden — 2024 Lead and Copper Rule Improvements;
- Trump 47 — EO 14154, `Unleashing American Energy`;
- Trump 47 — steam-electric reconsideration announcement;
- Trump 47 — proposed PFOA/PFOS compliance extension;
- Trump 47 — proposed rescission of other PFAS drinking-water components;
- Trump 47 — CCR management-unit deadline extension;
- Trump 47 — proposed CWA §401 rule.

### Statutory gap batch — installed 2026-08-16

`2026-08-16-water-oil-statute-gap-batch.json`

Commit: `7ee28f4ff94b3c84c31d78d422527831ec49aec9`
Validation: re-fetched from `main`; blob `326c36cb277bf1a6ca5ea8dfdc912e421e3f6536`.

New independent nodes:
- Reagan — Water Quality Act of 1987, Public Law 100-4 / 101 Stat. 7;
- George H. W. Bush — Oil Pollution Act of 1990, Public Law 101-380.

Primary evidence families include GovInfo authentic/statutory records and official EPA records for stormwater, nonpoint-source programs, State Water Pollution Control Revolving Funds, National Estuary Program, oil-spill response, liability, planning, and the Oil Spill Liability Trust Fund.

### Executive/rule gap batch — installed 2026-08-16

`2026-08-16-eo-wotus-gap-batch.json`

Commit: `3361512f66ee1736da0b12f40dd2e76fce8ec95e`
Validation: re-fetched from `main`; blob `f6b19badb6dff58befe2c88f045e0e417c63f2fe`.

New independent nodes:
- Clinton — Executive Order 12898, 59 FR 7629, `Federal Actions To Address Environmental Justice in Minority Populations and Low-Income Populations`;
- Obama — 2015 `Clean Water Rule: Definition of Waters of the United States`, 80 FR 37054 / Federal Register document 2015-13435.

The 2015 rule node records its jurisdictional role across Clean Water Act programs and leaves the exact predecessor/successor relationship to the existing 2019 repeal and 2020 replacement nodes explicitly pending rather than inferring an unvalidated edge.

## Evidence-state rules

1. A seed node is not an exhaustive administration inventory.
2. Proposed rules remain distinct from final rules.
3. Court vacatur/stay is a separate lifecycle state, not rewritten into the issuing policy node.
4. An agency announcement to reconsider is not a replacement final rule.
5. A government description of expected effects is stored as an official statement unless independently measured.
6. Company water claims remain raw claims until mapped to governing rules/evidence.
7. Economic/industrial activity policies are admitted when the policy itself changes environmentally consequential activity.
8. A later repeal/replacement relationship is not installed merely because two nodes concern the same regulatory definition; the exact edge requires source-backed lifecycle validation.
9. A policy node may record operative legal mechanisms without assigning a favorable/unfavorable or stronger/weaker label.

## Highest-priority gaps after this advancement

### Reagan
- Medical Waste Tracking Act;
- lead/gasoline and mobile-source changes in-period;
- Montreal Protocol / ozone implementation;
- public lands, extraction, energy, agriculture and industrial policy with environmental operation.

`Water Quality Act of 1987` is no longer a missing node.

### George H. W. Bush
- Great Lakes Critical Programs Act;
- wetlands/no-net-loss implementation history;
- coastal/public-lands/energy/extraction policy;
- pesticide/chemical/waste policy changes.

`Oil Pollution Act of 1990` is no longer a missing node.

### Clinton
- exact 1998 microbial and disinfectant/byproduct rules as independent nodes;
- roadless/public-land rules;
- vehicle/fuel, industrial, agricultural and extraction policy;
- additional bottled-water standards, enforcement and claim rules.

`Executive Order 12898` is no longer a missing node.

### George W. Bush
- Brownfields Act;
- highway diesel implementation lineage;
- Clean Air Interstate Rule;
- utility mercury rule;
- wetlands/CWA jurisdiction and permitting changes;
- energy/extraction/public-land policy;
- bottled-water contaminant/quality/claim rules.

### Obama
- vehicle GHG/fuel-economy standards;
- federal sustainability orders;
- power/energy/extraction/public-land changes;
- commercial-water regulatory and enforcement history.

The `2015 Clean Water Rule/WOTUS` is no longer a missing node; its lifecycle edges remain pending.

### Trump 45
- methane revisions;
- NEPA implementing-rule revisions;
- vehicle/fuel rules;
- public-land/oil/gas/mineral changes;
- pesticide/chemical actions;
- enforcement/funding changes;
- commercial-water rules/claims/enforcement;
- exact lifecycle edges linking 2015 WOTUS, the 2019 repeal, and the 2020 Navigable Waters Protection Rule.

### Biden
- 2023 WOTUS plus Sackett-conforming amendment;
- 2023/2024 oil/gas methane rules;
- 2024 fossil-power suite;
- environmental-justice orders/actions;
- IRA/IIJA funding and implementation policies affecting environmental activity;
- public-land/extraction changes;
- commercial-water PFAS and company-claim relationships.

### Trump 47
- 2025/2026 WOTUS proposal and final state if changed;
- CEQ NEPA regulatory removal and each agency's replacement procedures;
- vehicle/emissions rules;
- federal land/oil/gas/mineral actions;
- coal-ash proposed amendments beyond deadline extension;
- grant/funding terminations/reallocations affecting environmentally operative projects;
- enforcement policy changes;
- commercial-water PFAS/quality/claim effects.

## Relationship work still required

The policy-node corpus must be connected through predecessor/successor edges after node acquisition. Relationship types include enactment/implementation, amendment, repeal, replacement, restoration, delay, deadline extension, court response, funding change, jurisdiction change, delegation, enforcement change and company-claim governance.

Immediate relationship target: source-backed lifecycle reconstruction for the 2015 Clean Water Rule → 2019 repeal → 2020 Navigable Waters Protection Rule. The node corpus must preserve each instrument independently and install only the legal/operational edges established by primary sources.

Do not perform a cross-administration significance overlay until the inventory completion gate is met. The requested next phase after 100% inventory completion is to map administration periods over one another and examine significant relationships without assigning partisan value.

## Execution ownership and continuation

Current owner: this environmental-policy inventory lane under the parent environmental handoff.
Current claim state: `ACTIVE / SOURCE ACQUISITION`.
No duplicate implementation lane was found in the inspected inventory directory.

Next executable acquisitions are the remaining named nodes above, with commercial-water reconstruction retained as a first-class requirement rather than a later appendix.

## Completion posture

`NOT_COMPLETE`.

No percentage is asserted for this bounded environmental lane because an exhaustive denominator has not yet been established. The 100% gate requires origin-scope reconciliation plus primary-source-backed coverage across every applicable admitted domain for every administration, commercial-water reconstruction, and predecessor/successor mapping.

The newly installed four nodes are completed acquisitions, not evidence that four administrations are complete.
