# Network and Cyber-Physical Sabotage Lineage — Research Candidate

```yaml
record_id: "ERL-CYBER-SABOTAGE-LINEAGE-001"
status: "research_candidate"
date_opened: "2026-09-02"
historical_reconstruction_complete: false
current_attack_monitor_active: false
state_attribution_finding_authorized: false
causal_finding_authorized: false
publication_authorized: false
```

## Research purpose

Build a source-custodied, continuously reviewable history of network and cyber-physical sabotage from early computer-network incidents through current attacks. The workstream must distinguish external network entry from internal execution, espionage from sabotage, intended damage from accidental propagation, and public attribution from independently established state responsibility.

This candidate preserves an initial research structure and source-acquisition queue. It is not a completed incident catalogue or a finding that any named government conducted an operation.

## Governing distinctions

The research must keep the following event classes separate:

- `espionage`: unauthorized collection or access whose established objective is information acquisition;
- `disruption`: loss or degradation of availability without established destructive intent;
- `sabotage`: intentional impairment, destruction, or manipulation of a system or dependent process;
- `cyber_physical_sabotage`: sabotage in which digital action changes or damages a physical process or object;
- `accidental_spillover`: harmful propagation or effect beyond the intended target or without an established sabotage objective;
- `influence_or_coercion`: digital disruption used to create political, military, economic, or public-pressure effects;
- `unresolved`: the available evidence does not yet discriminate among the preceding classes.

`Internal` and `external` describe where a transition occurs, not who is trustworthy. A single operation may begin through an external supplier or public network, enter a private or air-gapped environment, propagate internally, and terminate in a physical controller.

## Seed chronology requiring source reconstruction

| Period | Incident | Initial candidate class | Evidentiary boundary |
|---|---|---|---|
| 1982 | Alleged CIA-compromised Soviet pipeline-control software | disputed supply-chain cyber-physical sabotage | The software-sabotage and explosion account is contested and must not be presented as established without corroborating primary records. |
| 1986–1987 | Hanover Hacker / Cuckoo's Egg intrusions | espionage control case | Establishes early cross-border network espionage; it is not itself an industrial-sabotage event. KGB direction, payment, and formal relationship require claim-specific sourcing. |
| 1988 | Morris worm | accidental or recklessly propagated network disruption | Widespread Internet impairment does not by itself establish an intent to sabotage physical systems. |
| 2000 | Maroochy Shire sewage-control incident | insider-enabled cyber-physical sabotage | Confirm the actor, access path, command mechanism, environmental release, and judicial record independently. |
| 2003 | Davis-Besse SQL Slammer intrusion | accidental external-to-internal spillover | Private-network and safety-monitor disruption are relevant even though targeted destructive intent and physical damage were not established. |
| 2007 | Estonia distributed denial-of-service attacks | national-scale external disruption/coercion candidate | Preserve effects and government responses separately from individual, proxy, and state-attribution claims. |
| 2007–2010 | Stuxnet / Operation Olympic Games | targeted cyber-physical sabotage candidate | Separate earliest recovered code, alleged delivery, Natanz execution, physical effects, telemetry deception, spillover, and U.S./Israeli attribution. Official acknowledgment remains distinct from journalistic or technical attribution. |
| Current | Newly reported state and non-state operations | rolling intake only | No current incident enters the chronology as sabotage or state-attributed merely because an alert, vendor, government, or media source uses that label. |

The chronology is deliberately non-exhaustive. Each seed is a research target, not a promoted ERL finding.

## Required incident model

Every incident record should preserve, when available:

1. event time, discovery time, disclosure time, and attribution time;
2. initiating actor, operator, sponsor, beneficiary, and alleged state relationship as separate fields;
3. external entry path, trust-boundary crossings, internal propagation, and terminal execution point;
4. exploited identity, credential, supplier, software, protocol, removable-media, or physical-access path;
5. human-directed versus autonomous actions;
6. intended target, affected systems, spillover population, and dependent physical processes;
7. commanded state, observed state, independently measured state, and any telemetry deception;
8. confidentiality, integrity, availability, safety, environmental, economic, military, and physical effects;
9. source class, native custody, hash, provenance, corrections, contradictions, and missing evidence;
10. attribution confidence by proposition rather than a single incident-wide confidence label.

## Core research questions

1. Which incident is the earliest independently reconstructable case in each governed class?
2. When did attacks move from information theft or network denial into autonomous manipulation of physical state?
3. Which operations crossed from public or supplier networks into private, segmented, or air-gapped systems?
4. Which attacks depended on valid internal credentials or technically valid commands that lacked legitimate transition authority?
5. Which incidents manipulated monitoring or operator perception in addition to execution?
6. How often did destructive effects result from deliberate targeting versus uncontrolled propagation?
7. How have state actors used contractors, criminal proxies, insiders, suppliers, or compromised third parties?
8. Which public attributions were later confirmed, narrowed, contradicted, withdrawn, or left unresolved?
9. What present attack patterns reproduce the transition structure of earlier incidents even when tooling and targets differ?
10. Which controls would have detected or denied the illegitimate transition, and which claims about prevention remain untested?

## Historical-to-current comparison dimensions

The comparative output must not rank incidents using a single severity score. It should produce proposition-relative comparisons across:

- reach: local, organizational, sectoral, national, or transnational;
- boundary: external-only, internal-only, supply-chain, hybrid, or air-gap crossing;
- action: observe, collect, deny, alter, destroy, deceive, or coerce;
- autonomy: operator-at-keyboard, scripted, self-propagating, target-selective, or process-autonomous;
- consequence: data loss, service interruption, environmental release, equipment degradation, injury risk, or strategic effect;
- observability: overt, delayed, covert, false-normal, or independently observable;
- attribution posture: unknown, alleged, technically associated, officially attributed, judicially established, or acknowledged;
- evidence posture: primary-custodied, authoritative-secondary, technical reconstruction, contested, or missing.

## Current-attack intake

Current monitoring should begin with official and authoritative advisory streams, then acquire the underlying incident-specific records. Advisories are discovery leads and threat-context sources; they do not independently establish that a particular intrusion caused sabotage or that the named state controlled every observed action.

The initial machine-readable acquisition queue is:

`config/network-cyberphysical-sabotage-source-queue.v1.json`

Priority current lanes:

- industrial-control and operational-technology advisories;
- destructive malware and wiper operations;
- critical-infrastructure intrusions with credible process effects;
- telecommunications, satellite, positioning, maritime, energy, water, transportation, healthcare, and nuclear-system incidents;
- supply-chain compromises capable of crossing organizational trust boundaries;
- attacks that falsify telemetry, provenance, logs, safety state, or operator-visible status;
- state, proxy, contractor, insider, and criminal-role separation;
- corrections to earlier public attribution or impact claims.

## Source and custody policy

Evidence should be physically separated into future namespaces for official records, technical analyses, judicial records, contemporaneous reporting, retrospective reporting, contested accounts, and derived comparisons. A secondary account may locate a primary object but may not inherit primary-source status.

Minimum preferred source order:

1. native government, court, regulator, operator, or incident-response records;
2. contemporaneous technical artifacts and reproducible reverse engineering;
3. named, attributable reporting based on direct participants or documents;
4. scholarly historical reconstruction;
5. retrospective summaries used only as discovery leads.

Current web content must be captured with retrieval time, native bytes or a governed immutable receipt, source identity, and later correction checks. Publication date and event date must remain separate.

## StegVerse governance relevance

This lane may test whether an incident exploited one or more of these separations:

```text
network admission != execution authority
internal presence != trusted identity
valid command syntax != legitimate state transition
commanded state != independently observed state
successful delivery != authorized receipt
single-channel telemetry != reconstructable evidence
```

The research may compare incident structures with Interlock/InTr, transition-table, receipt, independent-observation, and reconstruction controls. It must not claim that a StegVerse control would have prevented an incident until the historical transition path is reconstructed and the proposed control is tested against that path.

## First executable research slice

1. Acquire and hash the authoritative seed sources in the configured queue.
2. Create one proposition-level incident packet for each historical seed.
3. Mark disputed, accidental, espionage-only, and sabotage cases distinctly.
4. Normalize boundary crossings and commanded/observed/physical states.
5. Add current incidents only through dated candidate packets with explicit attribution and effect ceilings.
6. Perform an independent chronology and classification review before any public comparison.

## Promotion boundary

This candidate does not authorize claims that:

- the alleged 1982 Soviet pipeline event was caused by CIA-modified software;
- every harmful worm or outage was sabotage;
- network intrusion proves physical-process access;
- technical association proves state direction;
- Stuxnet attribution has been formally acknowledged by the alleged states;
- an advisory proves a current attack occurred as initially described;
- a proposed governance control would necessarily have prevented a historical operation.

Promotion requires source custody, incident-level contradiction review, proposition-relative attribution, explicit separation of observed effects from inferred objectives, current-event correction monitoring, and independent reconstruction.
