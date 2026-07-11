# Primary-Record Intake Queue: Delaney Hall Assessment

## Purpose

This queue converts missing evidence into governed collection tasks. Each item identifies the record owner, the assessment branches affected, the admissibility effect, and the boundary against overclaiming.

## Intake states

```text
requested
located
received-unverified
verified-primary
verified-secondary
conflicting-records
restricted-or-sealed
unavailable
superseded
```

## Queue

| ID | Record or source | Likely custodian | Affected branches | Current state | Activation effect |
|---|---|---|---|---|---|
| DH-INTAKE-001 | Original TRT World post, caption, posting time, durable URL, and underlying camera file | TRT World or original videographer | factual basis, chronology, source posture | requested | Blocks complete media provenance and continuous-event reconstruction. |
| DH-INTAKE-002 | Full unedited footage before and after each visible restraint, baton, and chemical-agent event | Media, witnesses, federal or state agencies | factual basis, force-event packets | requested | Blocks individualized necessity and proportionality findings. |
| DH-INTAKE-003 | Audio, dispatch, radio, warning, and dispersal-order records | ICE, ERO, DHS, Newark, New Jersey State Police | action conversion, protest restriction, force | requested | Blocks findings about notice, compliance opportunity, command authority, and de-escalation. |
| DH-INTAKE-004 | Arrest affidavits, charging records, probable-cause statements, and disposition records for each arrested protester | Federal, state, municipal, and court custodians | factual basis, institutional response, outcomes | requested | Blocks individualized arrest-legitimacy findings. |
| DH-INTAKE-005 | Body-worn camera, facility surveillance, vehicle-camera, and perimeter-camera footage | ICE, ERO, GEO Group, Newark, New Jersey State Police | factual basis, chronology, use of force | requested | Blocks independent reconstruction of each event. |
| DH-INTAKE-006 | Exact DHS, ICE, or ERO use-of-force, chemical-agent, baton, crowd-control, reporting, intervention, and medical-aid policies in effect on May 26, 2026 | DHS and ICE | action conversion, authority posture | requested | Blocks policy-compliance analysis; DOJ policy remains only a benchmark. |
| DH-INTAKE-007 | Incident reports and force reports identifying personnel, force type, justification, duration, injuries, intervention, and medical response | ICE, ERO, DHS oversight offices | factual basis, force, accountability | requested | Blocks event-specific official reconstruction and contradiction testing. |
| DH-INTAKE-008 | Facility access, inspection, food, sanitation, temperature, grievance, and medical records | GEO Group, ICE, DHS, New Jersey agencies | detention conditions, hunger strike, oversight | requested | Blocks resolution of conflicting conditions claims. |
| DH-INTAKE-009 | Hunger and labor strike declarations, participant lists where safely and lawfully available, demands, dates, medical monitoring, and facility responses | Detainees, counsel, advocates, GEO Group, ICE | factual basis, outcome evidence | requested | Blocks measurement of strike scope, duration, and consequences. |
| DH-INTAKE-010 | Transfer order, destination, reason, notice, legal-continuity records, medical-continuity records, and retaliation review for the reported organizer transfer | ICE, ERO, detention contractor, counsel | action conversion, authority map T4 | requested | Blocks determination whether the transfer was ordinary custody administration, lawful necessity, or retaliation. |
| DH-INTAKE-011 | Individual detention, custody-review, removal-order, stay, appeal, habeas, counsel-access, and identity records for persons materially implicated by the protest | Immigration courts, federal courts, DHS, counsel | authority map T1-T5 | restricted-or-sealed | Blocks person-specific due-process conclusions; collection must protect privacy and legal restrictions. |
| DH-INTAKE-012 | Medical treatment and injury records for protesters, officers, observers, journalists, elected officials, and detainees, with lawful consent or de-identified summaries | Hospitals, EMS, agencies, individuals | outcome evidence, force proportionality | restricted-or-sealed | Blocks measured-harm comparison; privacy protections apply. |
| DH-INTAKE-013 | Complaints, internal investigations, inspector-general referrals, civil-rights reviews, and disciplinary outcomes | DHS OIG, ICE OPR, DOJ, state and local oversight bodies | institutional response, accountability | requested | Blocks post-event accountability assessment. |
| DH-INTAKE-014 | Federal exterior operations plan and command structure | DHS, ICE, ERO | action conversion, authority chain | requested | Blocks identification of who authorized escalation, force tools, transfer protection, and withdrawal. |
| DH-INTAKE-015 | New Jersey State Police exterior operations plan, protest-zone maps, checkpoint rules, warnings, arrests, force, injuries, and complaints | New Jersey State Police and state government | control comparison | requested | Blocks completion of the federal-to-state operational control. |
| DH-INTAKE-016 | Comparable federal detention-protest incidents under prior administrations | DHS, DOJ, courts, archives, press | control comparison, selective-enforcement review | requested | Blocks administration-wide and cross-administration conclusions. |
| DH-INTAKE-017 | Press and observer declarations, original images, credentials, location data, and arrest or force records | Journalists, press organizations, legal observers, agencies | First Amendment, contradiction evidence | requested | Blocks individualized findings concerning press, observer, or mediator treatment. |
| DH-INTAKE-018 | Statements, recordings, or records from Senator Andy Kim and other elected officials present | Congressional offices, media, agencies | oversight, contradiction evidence | requested | Blocks full reconstruction of mediation, oversight, warning, and chemical-exposure claims. |

## Intake rules

1. A record is not `verified-primary` merely because it is supplied by a government agency. Authenticity and completeness must be checked.
2. A public statement proves that a claim was made; it does not automatically prove the underlying event.
3. Restricted personal records must be represented by lawful, privacy-preserving receipts or de-identified findings.
4. Missing government-controlled records must not be treated as evidence favoring the government.
5. Missing protester-controlled records must not be treated as evidence favoring protesters.
6. Contradictions remain visible until resolved or explicitly classified as unresolved.
7. No intake item may silently change `use_of_force_legitimacy: not established` into justified or unlawful.
8. Every received record must be assigned a Source Posture receipt before use.

## Promotion map

| Branch | Minimum records required before promotion |
|---|---|
| Media provenance | DH-INTAKE-001 and at least one corroborating original source |
| Continuous chronology | DH-INTAKE-002, DH-INTAKE-003, and DH-INTAKE-005 |
| Arrest legitimacy | DH-INTAKE-003 and DH-INTAKE-004, individualized by person |
| Force necessity and proportionality | DH-INTAKE-002, DH-INTAKE-005, DH-INTAKE-006, DH-INTAKE-007, and DH-INTAKE-012 |
| Hunger-strike factual posture | DH-INTAKE-008 and DH-INTAKE-009, with contradictory records preserved |
| Transfer authority and retaliation review | DH-INTAKE-010 and relevant lawful portions of DH-INTAKE-011 |
| Federal-to-state control completion | DH-INTAKE-014 and DH-INTAKE-015 with comparable measures |
| Administration-wide comparison | DH-INTAKE-016 plus completed same-event control |
| Press and observer treatment | DH-INTAKE-002, DH-INTAKE-005, DH-INTAKE-017, and DH-INTAKE-018 |
| Accountability | DH-INTAKE-007, DH-INTAKE-012, and DH-INTAKE-013 |

## Current posture

```yaml
queue_status: "active"
total_items: 18
verified_primary_items: 0
verified_secondary_items: 0
restricted_or_sealed_items: 2
activation_blocking_items: 18
next_priority:
  - "DH-INTAKE-001"
  - "DH-INTAKE-002"
  - "DH-INTAKE-006"
  - "DH-INTAKE-007"
  - "DH-INTAKE-010"
  - "DH-INTAKE-015"
```
