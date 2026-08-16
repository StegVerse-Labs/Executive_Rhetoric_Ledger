# ERL Research-Surface Origin-Scope Audit

Date: 2026-08-16
Status: ACTIVE / ORIGIN-SCOPE RECONCILIATION
Repository: `StegVerse-Labs/Executive_Rhetoric_Ledger`

## Purpose

Audit every active ERL research surface against the request, observation, or research question that created it and determine whether an adjacent or correlated domain was incorrectly demoted to `context`, `control`, `later analysis`, `supporting evidence`, or a separate lane even though the originating scope made that domain part of the evidence inventory required to answer the question.

## Governing invariant

**Preserve and present truth through evidence.**

A research surface must not become narrower merely because one implementation path, evidence class, adapter, or later analytical role is easier to formalize.

## Scope-admission rule

A domain is part of a surface's primary inventory when at least one of the following is true:

1. the originating user request explicitly includes the domain;
2. the originating research question expressly asks for a relationship involving the domain;
3. the domain is a necessary intermediate state in the causal, authority, physical, chronological, evidentiary, or outcome chain the request asks ERL to reconstruct;
4. excluding the domain would make a requested comparison or causal test non-reconstructable;
5. the same evidence object is directly operative in multiple research surfaces.

A domain is **not** admitted merely because it is interesting or correlated. If the origin does not include it and it is not required to reconstruct the requested relationship, preserve it as `ADJACENT_ONLY` until evidence establishes a stronger relationship.

A domain may serve as a control in later analysis **without losing its status as primary inventory evidence** when the originating request includes that domain. `CONTROL` is an analytical role, not an evidence-demotion state.

## Shared-node rule

When one raw evidence object belongs to more than one research surface, preserve the object once under its proper evidentiary authority and let each research surface reference it by immutable identity. Cross-surface membership must not duplicate, rewrite, normalize, or overwrite the source object.

## Origin-evidence grades

- `ORIGIN_EXACT`: exact originating user language recovered.
- `ORIGIN_DURABLE_PROXY`: the first durable research-candidate/issue text preserves the research question but exact initiating chat language has not yet been recovered.
- `ORIGIN_PARTIAL`: some originating language is recovered but not the entire creation sequence.
- `ORIGIN_NOT_RECOVERED`: current repository state identifies the surface, but the initiating request has not yet been recovered sufficiently to make a complete demotion determination.

## Audit findings

### 1. Environmental policy by administration — Reagan through Trump 47

Surface: `assessments/environmental-policy/**`
Origin grade: `ORIGIN_EXACT`
Demotion finding: `CONFIRMED_SCOPE_DEMOTION`

Originating scope: map federal policies by administration that cover how the environment is treated **or result in affecting the environment**, without judging them better or worse. The user subsequently made explicit that bottled/spring/purified water and company claims are included, and clarified that economic, industrial, commercial, agricultural, extractive, infrastructure, or other activity belongs in the inventory when federal policy limits or expands that activity in a way that affects the environment.

Demoted domains detected:

- commercial bottled/spring/purified-water regulation and company claims — initially omitted, subsequently restored;
- economic and industrial activity policy affecting environmental outcomes — incorrectly described as a later `control` variable;
- by the same origin rule, agricultural, extractive, infrastructure, transportation, energy, manufacturing, land-use, procurement/subsidy, permitting, and commercial-activity policy belongs in the primary inventory whenever the policy changes environmentally consequential activity.

Required inventory posture:

`federal policy -> changed activity/permission/incentive/constraint -> environmental pathway/resource/exposure`

Independent market or activity changes that are not caused or governed by the federal policy under examination may later be controls. Policy-caused activity change remains primary evidence.

Disposition: `RESTORE_TO_PRIMARY_INVENTORY`.

### 2. General causal-testing platform / reusable ERL testing system

Origin grade: `ORIGIN_EXACT`
Demotion finding: `CONFIRMED_SCOPE_DEMOTION`

Recovered originating user request, 2026-07-31: build the observed capability-discontinuity inquiry side by side with the Fauci examination and determine whether the reusable causal-testing parts should become a testing platform. The accepted design explicitly described a domain-independent causal engine applicable to executive rhetoric, infrastructure incidents, AI behavior, scientific questions, and organizational failures. The user then objected when implementation discussion focused again on LLM behavior and stated that LLM behavior was a very narrow evidence pool.

Demoted domain pattern:

- the general testing platform was repeatedly narrowed toward LLM/model behavior;
- executive-rhetoric, infrastructure, scientific, organizational, and other admissible experimental domains were treated as secondary examples despite being part of the accepted platform definition.

Required inventory posture:

The shared experimental language — observation, candidate explanations, expected signatures, experiments, observed results, likelihood/confidence updates, remaining hypothesis space, replay, and receipts — is primary platform inventory. LLM behavior is one adapter/evidence stream, not the defining research domain.

Disposition: `RESTORE_DOMAIN_NEUTRAL_PRIMARY_SCOPE`.

### 3. DOGE / Musk federal exposure

Surface: `ERL-RC-DOGE-MUSK-2026`; Issue #3
Origin grade: `ORIGIN_PARTIAL`
Demotion finding: `POSSIBLE_SCOPE_DEMOTION_REQUIRES_ORIGIN_RECONCILIATION`

Current durable candidate is concentrated on Musk's federal role, ethics/recusal/waiver state, agency enforcement matters involving Musk companies, Starlink procurement, IG removals, DOGE savings/fraud claims, federal budget measures, and control comparisons.

Adjacent/correlated domains that must be tested against the unrecovered full originating request before exclusion:

- cross-company Musk incentive structure across affected private entities;
- federal friction removed, retained, or transferred for those entities;
- procurement, contract, enforcement, regulatory, labor, safety, securities, transportation, and communications effects as one connected authority/incentive graph;
- DOGE fiscal-survivability effects versus automation/AI/infrastructure acceleration effects;
- rhetoric/narrative effects on regulators, competitors, capital allocation, and infrastructure timing when those effects were part of the initiating theory.

Disposition: `DO_NOT_DEMOTE_PENDING_EXACT_ORIGIN`; acquire the initiating transcript before closing any of these domains as context-only.

### 4. xAI Colossus 2 environmental justice / regulatory exemption

Surface: `ERL-RC-XAI-COLOSSUS2-2026`
Origin grade: `ORIGIN_DURABLE_PROXY`
Demotion finding: `NO_CURRENT_DEMOTION_DETECTED`

The durable originating question already treats as first-class evidence: turbine inventory and operation, permit coverage, federal/state applicability, emissions, cumulative airshed effects, DOJ national-security argument, temporary/portable classification, public participation, demographics/health, comparator projects, discrimination/disparate-impact hypotheses, company responses, Title VI/EJ records, enforcement posture, and economic/national-security justification.

Important cross-surface membership: energy-generation, permitting, emissions, enforcement, community exposure, and environmentally operative government policy may also be referenced by the longitudinal environmental-policy surface. That cross-membership does not make them merely contextual here.

Disposition: `PRESERVE_CURRENT_BREADTH`.

### 5. Fauci HSGAC / Operation Warp Speed causal examination

Surface: `ERL-RC-FAUCI-HSGAC-2026`; Issue #47 / PR #48; supporting Issue #56
Origin grade: `ORIGIN_PARTIAL`
Demotion finding: `NO_CURRENT_CANONICAL_DEMOTION_DETECTED; CROSS-SURFACE ORIGIN CHECK REQUIRED`

The repository-wide handoff preserves the original session goal as more than refusal counting: exact questions/responses; decision authority; first/second Trump-administration continuity; personnel lifecycle; records topology; Morens/Folkers routing; independently reconstructable documentary conflicts; funding/scientific-review/testimony/communication edges; and controls.

The wider Operation Warp Speed research associated with this surface includes authorization/development/testing timing, White House/HHS/FDA authority and pressure, pharmaceutical/funding/contract pathways, public communication and election timing, role continuity, and later testimony. These domains must not be treated as mere historical context when they are required to reconstruct the authority or event referenced by a hearing question. They may remain separate propositions or linked sub-surfaces, but their evidence nodes are in-scope when question-causally relevant.

Disposition: `PRESERVE_CANONICAL_BREADTH_AND_LINK_OWS_NODES`; recover the earliest OWS/Fauci initiating transcript before declaring the origin audit closed.

### 6. ICE temporary vehicle-stop limits after fatal shootings

Surface: `ERL-RC-ICE-VEHICLE-STOP-2026`
Origin grade: `ORIGIN_DURABLE_PROXY`
Demotion finding: `NO_CURRENT_DEMOTION_DETECTED`

The candidate itself makes the policy change inseparable from the two fatal incidents, disputed use-of-force accounts, exact directive scope/succession, operational safety, institutional response, public executive enforcement posture, internal tactical restriction, and later practice. Those domains are primary inventory, not later controls.

Disposition: `PRESERVE_CURRENT_BREADTH`.

### 7. Ruben Ray Martinez / South Padre Island force event

Surface: `ERL-RC-RRM-SPI-2025`; Issue #30
Origin grade: `ORIGIN_DURABLE_PROXY`
Demotion finding: `NO_CURRENT_DEMOTION_DETECTED`

Current durable inventory preserves separate vehicle encounter, firearm discharge, and post-shooting response events, and the active review requires the official vehicle-assault assertion, recordings and vehicle movement, commands, witnesses, agent injury, firearm necessity/proportionality/policy/constitutional standards, post-shooting restraint and medical chronology, grand-jury state, delayed disclosure, and missing primary records.

The broader federal fatal-shooting/policy-comparison surface may reference this event, but that does not convert any of these case elements to context-only.

Disposition: `PRESERVE_CURRENT_BREADTH`.

### 8. Multi-angle federal force / crossfire / AI minimization

Surface: Issue #45 / `ERL-2026-07-24-MULTIANGLE-001`
Origin grade: `ORIGIN_DURABLE_PROXY`
Demotion finding: `NO_CURRENT_DEMOTION_DETECTED; HIGH DEMOTION RISK`

The research surface intentionally joins three co-equal evidence questions: apparent excessive/civil-rights force, firearm/line-of-fire danger, and AI analytical minimization/deference. Agency records, unedited video, body/dash/dispatch, ballistics, medical and supervisory records, official statements/rhetoric, line-of-fire reconstruction, independent frame review, and controlled AI tests are all primary inventory for the combined experiment.

AI behavior must not be demoted to a meta-commentary appendix, and physical-force evidence must not be reduced to a test fixture for AI behavior.

Disposition: `PRESERVE_COEQUAL_DOMAINS`.

### 9. Iran / Jordan / FirstNet escalation

Surface: `ERL-RC-IRAN-JORDAN-FIRSTNET-2026`
Origin grade: `ORIGIN_DURABLE_PROXY`
Demotion finding: `NO_CURRENT_DEMOTION_DETECTED`

The candidate is explicitly cross-domain. Missile launch/interception, U.S./Iranian/Jordanian publication timing and rhetoric, pre-existing strike architecture, executive authorization, cyber/telecommunications/FirstNet degradation, intelligence and threat inputs, maritime activity, Jordanian sovereignty/narrative timing, and competing causation hypotheses are already first-class evidence lanes.

Disposition: `PRESERVE_CROSS_DOMAIN_INVENTORY`.

### 10. Ellis–Scavino transfer-of-power chain

Surface: `ERL-RC-ELLIS-SCAVINO-2026`
Origin grade: `ORIGIN_DURABLE_PROXY`
Demotion finding: `NO_CURRENT_DEMOTION_DETECTED`

The surface's question is evidentiary validity across a multi-node attribution chain. Proffer authenticity, Ellis statement, Scavino statement, Scavino access/knowledge, Trump state of mind/instruction, operational-plan inference, contemporaneous communications, witnesses, January 6 records, later transfer outcome, cooperation incentives, memory/perception variables, and contradictions are all represented as separate evidence propositions.

Disposition: `PRESERVE_CHAIN_NODES`.

### 11. Daniel Siad / Epstein-network death and evidence continuity

Surface: `ERL-RC-DANIEL-SIAD-2026`
Origin grade: `ORIGIN_DURABLE_PROXY`
Demotion finding: `NO_CURRENT_DEMOTION_DETECTED`

The candidate explicitly defines the research object as investigation/evidence continuity, not only cause of death. Death investigation/autopsy, DOJ file references, victim/witness testimony, devices/accounts/business records, modelling/recruitment/network links, pre-death investigative state, mutual legal assistance, cross-border custody, reconstructability without testimony, rumor correction, and public-trust effects are in-scope.

Disposition: `PRESERVE_CONTINUITY_SCOPE`.

### 12. Trump-administration oil-flow normalization claim

Surface: `ERL-RC-OIL-FLOW-2026`
Origin grade: `ORIGIN_DURABLE_PROXY`
Demotion finding: `NO_CURRENT_DEMOTION_DETECTED`

The candidate correctly refuses to collapse `oil flowing normally` into one metric and makes production, exportable supply, storage/inventory, terminal loading, bypass pipelines, vessel transits/capacity, delivered exports, LNG/gas, baseline definition, AIS uncertainty, and exact statement scope part of primary inventory.

These physical-flow and policy nodes may also participate in environmental-policy research when federal policy changes production, transport, refining, or extraction. Shared membership is permitted.

Disposition: `PRESERVE_PHYSICAL_CHAIN`.

### 13. Cassidy / Trump IRS audit-protection authority chain

Surface: `ERL-RC-CASSIDY-IRS-2026`
Origin grade: `ORIGIN_DURABLE_PROXY`
Demotion finding: `NO_CURRENT_DEMOTION_DETECTED`

The candidate already preserves the complete requested authority chain: lawsuit, settlement, collateral/order question, audit-protection instrument, actor authority, adverseness/procedural legitimacy, scope, legal effect at time T, judicial review/effect, later executive action, anti-weaponization fund as a separate instrument, congressional scrutiny, Blanche confirmation, Cassidy statement/reasoning, professional-responsibility referrals, appeal/stay/successor state, and intraparty discriminator.

Disposition: `PRESERVE_AUTHORITY_CHAIN`.

### 14. AI integration / reservation split

Surface: `ERL-RC-AI-RESERVATION-SPLIT-2026`
Origin grade: `ORIGIN_DURABLE_PROXY`
Demotion finding: `NO_CURRENT_DEMOTION_DETECTED; IMPLEMENTATION COVERAGE GAP`

The candidate's primary inventory is intentionally multi-axis: factual belief, religious/spiritual commitment, moral conviction, institutional trust, economic threat, privacy/surveillance, dignity/identity, risk tolerance, AI exposure, consequence sensitivity, authority-delegation tolerance, reversibility, consent, human review, and receipt/governance requirements across use cases.

No one axis may be treated as explanatory context for the others. The current gap is empirical implementation (survey/interview/vignette/source acquisition), not a conceptual scope demotion.

Disposition: `PRESERVE_MULTI_AXIS_SCOPE`.

### 15. UAP disclosure / documentary feedback loop

Surface: `ERL-RC-UAP-MEDIA-2026`; Issue #62
Origin grade: `ORIGIN_DURABLE_PROXY`
Demotion finding: `NO_CURRENT_DEMOTION_DETECTED`

The candidate already makes official disclosure/reporting/hearings/declassification, documentary/media production, testimony, secondary reporting, technical/scientific evidence, archival/historical evidence, claim lineage/source reuse, platform/distribution growth, audience demand, algorithmic amplification, terminology shift, general documentary controls, lag, and mutual-feedback hypotheses part of the research design. Evidence classes are intentionally physically separate but remain jointly necessary to answer the origin question.

Disposition: `PRESERVE_SEPARATE_CLASSES_WITH_SHARED_CAUSAL_GRAPH`.

### 16. Model-behavior bias / relationship mapping

Surface: `assessments/machine/**` and `assessments/relationships/**` incident lane created 2026-08-16
Origin grade: `ORIGIN_EXACT`
Demotion finding: `PRIOR_ABSTRACTION_DEMOTION_CORRECTED`

Originating requirement: preserve incidents in as raw a form as possible, actively track incidents, map relationships among them, and let mappings provide later findings. Two distinct bias-type events were required: administration-directed framing effect and defensive behavior when the model is queried about its handling of administration responses.

The earlier attempt to replace raw incident relationships with normalization/motive taxonomies was a scope error. Raw incidents, exact exchanges, corrections, temporal ordering, and relationship edges are primary inventory. Higher-order labels are derived analysis only.

Disposition: `RAW_EVENTS_FIRST / RELATIONSHIPS_SECOND / FINDINGS_DERIVED`.

## Surfaces requiring exact-origin recovery before audit closure

The activation registry includes active research surfaces whose durable candidate is sufficient to continue research but does not itself prove that every original user-requested domain survived translation. Exact-origin recovery remains mandatory before this repository-wide audit may be marked complete, especially for:

- DOGE / Musk;
- earliest Fauci / Operation Warp Speed creation sequence;
- any umbrella-owned research candidate whose candidate document was created from an external article/share without the complete preceding user reasoning preserved.

If exact origin cannot be recovered, the durable candidate remains authoritative for forward research, but the audit status must remain `ORIGIN_NOT_FULLY_RECONCILED` rather than silently assuming no demotion occurred.

## Repository-wide anti-demotion rule

For every existing and future ERL research surface:

1. preserve the originating request/observation as a raw origin object or exact quotation where possible;
2. derive a machine-readable scope inventory from that origin;
3. classify each adjacent domain as `PRIMARY_INVENTORY`, `SHARED_PRIMARY`, `CONTROL_AND_PRIMARY`, `CONTROL_ONLY`, `ADJACENT_ONLY`, `SEPARATE_SIBLING`, or `UNRESOLVED`;
4. require an evidence-backed reason before moving a domain from primary inventory to a lesser role;
5. never let implementation convenience, schema boundaries, evidence-class separation, or later analytical use silently narrow the original research question;
6. allow one evidence node to serve multiple research surfaces by reference;
7. preserve contradictory evidence and scope changes as append-only history;
8. require origin-scope reconciliation as part of any `100% complete` claim for a research surface.

## Current audit disposition

`ACTIVE / REPAIR INSTALLED; ORIGIN RECOVERY INCOMPLETE`

Confirmed demotion corrections are identified for the environmental-policy surface, general causal-testing platform, and model-behavior incident lane. DOGE/Musk has a material possible demotion that cannot be closed until exact originating language is recovered. The remaining audited active surfaces presently preserve the breadth visible in their durable originating candidate/issue records; this is not equivalent to proof that no earlier chat-level domain was lost.

No research surface may be declared 100% inventory-complete while a known origin-scope reconciliation remains unresolved.