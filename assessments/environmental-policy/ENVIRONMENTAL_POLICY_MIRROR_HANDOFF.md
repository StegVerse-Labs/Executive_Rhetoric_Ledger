# ERL Environmental Policy Mirror Handoff

## Authority and purpose

This handoff governs the longitudinal federal environmental-policy research lane in `StegVerse-Labs/Executive_Rhetoric_Ledger`.

Goal ID: `ERL-ENV-POLICY-REAGAN-TRUMP47-001`

Purpose: preserve and map exact federal policy instruments from the Reagan administration through Trump 47 that govern, constrain, permit, fund, monitor, remediate, disclose, or otherwise affect treatment of the environment and resulting exposure/risk to people in the United States.

## Invariant

Preserve and present truth through evidence.

No policy is to be classified as better/worse, pro-/anti-environment, stronger/weaker, protective/harmful, or favorable/unfavorable as a research-layer conclusion. The lane records what the policy instrument does, what it replaces/amends/revokes, what environmental medium or exposure pathway it governs, what authority implements it, and what later instrument changes it.

Policy effects may be described factually when directly established by authoritative text, technical analysis, implementation records, or measured outcomes. Evaluative labels are not part of the canonical policy map.

## Administration range

1. Ronald Reagan (1981-1989)
2. George H. W. Bush (1989-1993)
3. Bill Clinton (1993-2001)
4. George W. Bush (2001-2009)
5. Barack Obama (2009-2017)
6. Donald Trump, 45th administration (2017-2021)
7. Joe Biden (2021-2025)
8. Donald Trump, 47th administration (2025-present)

## Policy domains

- drinking water and public water systems
- groundwater and aquifers
- surface water, wetlands, watersheds, oceans, estuaries
- wastewater and industrial discharges
- air quality and hazardous air pollutants
- climate and greenhouse-gas regulation where environmental treatment is affected
- hazardous waste, solid waste, coal ash, medical waste
- contaminated-site cleanup and Superfund/CERCLA
- toxic chemicals, pesticides, PFAS, lead, mercury, asbestos and other exposure controls
- emergency planning, release reporting, right-to-know and monitoring
- environmental review and permitting (NEPA, CWA, ESA-related implementation when environmentally operative)
- fuels, vehicles, power plants, oil/gas and industrial source standards
- public lands, forests, habitat and ecological protection where federal policy changes environmental treatment
- environmental infrastructure funding
- federal-state-tribal delegation and enforcement structure
- international environmental commitments implemented through federal policy

## Evidence model

Each policy remains a distinct evidence node. Do not replace raw policy nodes with a normalized summary.

Minimum fields per policy node:
- administration
- president
- date
- instrument_type
- exact_title
- public_law / executive_order / CFR / Federal_Register / agency_action identifier where applicable
- issuing authority
- statutory authority
- environmental domain
- regulated actor or target
- operative mechanism
- contaminants / resources / pathways affected
- geographic scope
- status at issuance: proposed/final/signed/enacted/guidance/enforcement/appropriation/treaty
- predecessor instrument or baseline
- explicit amendments/revocations/replacements
- later successor instrument(s)
- implementation dates/deadlines
- primary authoritative source(s)
- technical/implementation source(s)
- observed outcome evidence, if separately established
- relationship edges

## Relationship graph

Policy nodes may be linked by edges such as:
- AMENDS
- REPEALS
- REVOKES
- REPLACES
- RESTORES
- IMPLEMENTS
- DELAYS
- EXTENDS_DEADLINE
- NARROWS_SCOPE
- EXPANDS_SCOPE
- CHANGES_ENFORCEMENT
- CHANGES_FUNDING
- DELEGATES_TO_STATE
- FEDERALIZES
- RESPONDS_TO_COURT_DECISION
- RESPONDS_TO_CONTAMINATION_EVENT
- SUPERSEDED_BY

The edge describes the legal/operational relationship only. It does not assign normative value.

## Source hierarchy

1. Statute / Public Law / United States Code
2. Executive Order / Presidential Memorandum / Proclamation
3. Federal Register final/proposed rule and codified CFR
4. EPA/Army/Interior/CEQ/DOE/DOT/USDA/NOAA or other administering agency primary material
5. Presidential archives for contemporaneous policy records
6. Court decisions where they change or constrain operative policy
7. GAO/CRS/agency technical records for implementation and outcome reconstruction
8. Secondary sources only as discovery aids, not as final authority when a primary source is available

## Seed inventory status

Initial authoritative-source discovery has begun. Current seed anchors include:

### Reagan
- Safe Drinking Water Act Amendments of 1986
- Superfund Amendments and Reauthorization Act of 1986, including EPCRA/TRI
- Clean Water Act amendments of 1987 / Clean Water State Revolving Fund transition
- Medical Waste Tracking Act of 1988

### George H. W. Bush
- Clean Air Act Amendments of 1990
- Pollution Prevention Act of 1990
- Great Lakes Critical Programs Act of 1990

### Clinton
- Executive Order 12898 on Federal Actions to Address Environmental Justice in Minority Populations and Low-Income Populations
- Food Quality Protection Act of 1996
- Safe Drinking Water Act Amendments of 1996
- consumer confidence / microbial and disinfection-byproduct drinking-water implementation
- roadless-area and related federal-land policy instruments

### George W. Bush
- Small Business Liability Relief and Brownfields Revitalization Act of 2002
- heavy-duty highway diesel rule implementation
- nonroad diesel rule
- Clean Air Interstate Rule
- mercury regulation for electric utilities
- wetlands policy / federal permitting changes and related water rules

### Obama
- greenhouse-gas vehicle standards
- Mercury and Air Toxics Standards
- Clean Power Plan
- 2015 Clean Water Rule / WOTUS
- methane standards for oil and gas
- federal sustainability executive orders

### Trump 45
- Executive Order 13788 and WOTUS review
- repeal of 2015 Clean Water Rule
- 2020 Navigable Waters Protection Rule
- Affordable Clean Energy rule
- methane-rule revisions
- NEPA implementing-rule revisions
- vehicle/fuel-economy and power-sector regulatory changes

### Biden
- Executive Order 13990 and environmental-policy review/restoration program
- 2023 WOTUS rule and 2023 Sackett-conforming amendment
- 2023/2024 oil-and-gas methane standards
- 2024 PFAS National Primary Drinking Water Regulation
- 2024 PFOA/PFOS CERCLA hazardous-substance designation
- 2024 Steam Electric Effluent Limitation Guidelines
- 2024 coal-combustion-residual legacy/management-unit rule
- 2024 Lead and Copper Rule Improvements
- 2024 fossil-fuel power-plant rule suite

### Trump 47
- Executive Order `Unleashing American Energy`, including revocation of EO 13990 and NEPA-related direction
- CEQ NEPA regulatory removal and agency-specific procedure replacements
- proposed revised WOTUS definition
- CWA Section 401 revision proposal
- coal-ash regulatory revisions/deadline changes
- steam-electric effluent-rule reconsideration/deadline changes
- PFAS drinking-water retention/revision actions and PFAS destruction/disposal guidance
- Tijuana-San Diego wastewater and other federal environmental implementation actions

## Current state

State: ACTIVE / SOURCE ACQUISITION

The seed list is not exhaustive and is not yet a completed policy ledger. Next work is administration-by-administration primary-source acquisition and exact instrument identification, followed by legal relationship mapping across administrations.

## Completion conditions

This lane is complete only when:
1. each administration has a primary-source-backed inventory across all applicable policy domains;
2. each inventory item is an independent policy node;
3. predecessor/successor relationships are explicitly mapped;
4. proposed actions are separated from final/enacted actions;
5. statutory acts are separated from presidential proposals and agency implementation;
6. court-driven changes are identified independently from presidential policy choices;
7. raw source references remain preserved;
8. a reviewer can reconstruct the longitudinal policy history without relying on evaluative summaries.

Session state: ACTIVE — UNIQUE WORK.
