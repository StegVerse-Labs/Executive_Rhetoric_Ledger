# Political Influence Tree Standard

## Status

- **Repository:** `StegVerse-Labs/Executive_Rhetoric_Ledger`
- **Standard name:** Political Influence Tree Standard
- **Short name:** PITS
- **Document type:** Ledger standard
- **Primary function:** Structure political topic analysis as traceable influence trees with evidence posture at each branch.
- **Applies to:** Executive rhetoric, policy claims, campaign claims, administrative justifications, judicially contested claims, public-interest claims, fraud claims, national-security claims, emergency claims, and other politically active public narratives.

## Purpose

The Political Influence Tree Standard prevents modern political topics from being recorded as isolated headlines, slogans, partisan claims, or unsupported public narratives.

A political topic is not admissibly understood until its factual basis, influence lineage, authority adoption, action conversion, control comparison, institutional response, and outcome evidence are separately identified.

This standard requires political topics to be handled with the same category of factual discipline as all other StegVerse data classes.

## Core Rule

```text
No political topic is evaluated by alignment.
Every political topic is evaluated by lineage, evidence, authority, control comparison, and outcome.
```

## Fundamental Premise

Political topics often become visible only after upstream influence has already occurred.

A topic may appear to begin as a speech, executive order, agency action, lawsuit, campaign message, viral claim, or media controversy. In many cases, the more important governance origin is earlier:

```text
event / condition
→ framing
→ institutional amplification
→ public premise formation
→ political adoption
→ executive rhetoric
→ policy action
→ judicial or institutional response
→ measurable consequence
```

The ledger must therefore distinguish the surface claim from the influence structure that made the claim politically active.

## Required Tree Structure

```text
Political Topic
├── Surface Claim
│   ├── exact quote / policy statement / public framing
│   ├── speaker / office / institution
│   ├── date / venue / jurisdiction
│   └── source receipt
│
├── Claimed Justification
│   ├── fraud
│   ├── national security
│   ├── economic harm
│   ├── public safety
│   ├── constitutional authority
│   ├── emergency condition
│   ├── administrative necessity
│   ├── moral / cultural premise
│   └── other stated basis
│
├── Factual Basis
│   ├── primary evidence
│   ├── administrative data
│   ├── court record
│   ├── budget record
│   ├── enforcement record
│   ├── independent analysis
│   ├── expert testimony
│   ├── official investigation
│   ├── unsupported assertion
│   └── contradicted evidence
│
├── Influence Lineage
│   ├── think tank / policy shop
│   ├── donor / corporate interest
│   ├── media amplifier
│   ├── legal advocacy network
│   ├── academic / expert citation
│   ├── lobbying channel
│   ├── party platform / campaign document
│   ├── religious / cultural institution
│   ├── activist organization
│   ├── foreign influence indicator
│   └── executive office / agency adopter
│
├── Action Conversion
│   ├── speech only
│   ├── campaign promise
│   ├── executive order
│   ├── agency rule
│   ├── budget condition
│   ├── enforcement directive
│   ├── procurement condition
│   ├── litigation posture
│   ├── legislation
│   ├── informal pressure
│   └── no action found
│
├── Control Comparison
│   ├── comparable red jurisdiction
│   ├── comparable blue jurisdiction
│   ├── comparable prior administration
│   ├── comparable policy instrument
│   ├── comparable fraud / harm magnitude
│   ├── comparable enforcement tool
│   ├── comparable judicial posture
│   └── control unavailable / not yet established
│
├── Judicial / Institutional Response
│   ├── upheld
│   ├── enjoined
│   ├── stayed
│   ├── dismissed
│   ├── remanded
│   ├── under review
│   ├── settled
│   ├── agency reversal
│   ├── legislative override
│   └── no challenge found
│
├── Outcome Evidence
│   ├── measurable effect
│   ├── projected effect
│   ├── claimed effect
│   ├── no measurable effect yet
│   ├── contradicted by later data
│   ├── harm documented
│   ├── benefit documented
│   └── insufficient evidence
│
└── Ledger Classification
    ├── supported
    ├── partially supported
    ├── unsupported
    ├── contradicted
    ├── rhetorically amplified
    ├── institutionally seeded
    ├── legally contested
    ├── admissible with controls
    ├── inadmissible without controls
    └── pending evidence
```

## Required Fields

```yaml
topic_id: ""
topic_name: ""
jurisdiction: ""
time_window: ""
surface_claim:
  claim_text: ""
  speaker_or_institution: ""
  date: ""
  venue: ""
  source_url: ""
  source_type: ""
claimed_justification:
  category: ""
  stated_basis: ""
  quoted_basis: ""
factual_basis:
  primary_records: []
  administrative_data: []
  court_records: []
  independent_analysis: []
  unsupported_assertions: []
  contradictions: []
influence_lineage:
  known_origin_points: []
  institutional_amplifiers: []
  media_amplifiers: []
  legal_networks: []
  funding_or_donor_links: []
  policy_documents: []
action_conversion:
  action_type: ""
  instrument: ""
  date: ""
  actor: ""
  enforcement_or_implementation_status: ""
control_comparison:
  required: true
  available_controls: []
  missing_controls: []
  comparison_notes: ""
institutional_response:
  judicial_status: ""
  administrative_status: ""
  legislative_status: ""
  oversight_status: ""
outcome_evidence:
  measured_outcomes: []
  claimed_outcomes: []
  projected_outcomes: []
  contradicted_outcomes: []
ledger_classification:
  evidence_posture: ""
  influence_posture: ""
  authority_posture: ""
  admissibility_status: ""
  confidence: ""
receipts:
  sources: []
  review_notes: []
  last_reviewed: ""
```

## Evidence Posture Categories

```text
primary-record-supported
administrative-data-supported
court-record-supported
independent-analysis-supported
expert-testimony-supported
partially-supported
unsupported-assertion
contradicted-by-record
rhetorical-only
pending-verification
insufficient-control-comparison
```

## Influence Posture Categories

```text
organic-event-driven
media-amplified
think-tank-seeded
legal-network-seeded
donor-network-linked
campaign-platform-linked
agency-originated
executive-originated
grassroots-originated
foreign-influence-indicated
unknown-origin
```

These labels are descriptive, not accusatory. A topic should not be classified as seeded, linked, coordinated, or foreign-influenced unless the ledger contains admissible sources supporting that classification.

## Authority Posture Categories

```text
speech-only
campaign-commitment
executive-direction
agency-rulemaking
enforcement-directive
budgetary-condition
procurement-condition
litigation-position
legislative-proposal
judicially-tested
institutionally-rejected
no-authority-conversion-found
```

## Admissibility Status

```text
admissible
admissible-with-controls
admissible-for-structure-only
pending-evidence
inadmissible-without-controls
inadmissible-unsupported
inadmissible-contradicted
```

## Control Comparison Requirement

Control comparison is required whenever a claim is used to justify differential treatment, selective enforcement, emergency authority, funding leverage, fraud enforcement, or moralized policy action.

Examples of required control questions:

```text
Was the same standard applied to comparable red and blue jurisdictions?
Was the same enforcement tool used for comparable conduct?
Was the claimed harm magnitude similar across comparison cases?
Was the judicial posture consistent across administrations?
Was the claimed factual basis stronger, weaker, or absent in comparable cases?
Was the policy instrument proportional to the documented factual basis?
```

A claim may remain documented without a control comparison, but it should not be treated as fully admissible for comparative ledger analysis until the comparison is complete.

## Topic Example: Election Fraud

A topic such as election fraud must not be treated as one undifferentiated category.

```text
Election Fraud
├── voter impersonation
├── mail ballot fraud
├── registration fraud
├── machine manipulation claims
├── administrative error
├── ballot harvesting allegations
├── prosecution records
├── recount / audit records
├── court findings
├── media amplification
├── legislative proposals
└── executive enforcement posture
```

Each branch receives its own evidence posture.

Example:

```yaml
topic_name: "Election Fraud"
branch: "Widespread voter impersonation changed election outcomes"
surface_claim:
  claim_text: "Widespread voter impersonation changed outcomes."
factual_basis:
  primary_records: []
  court_records: []
  unsupported_assertions:
    - "No admissible record supplied in this entry."
ledger_classification:
  evidence_posture: "unsupported-assertion"
  admissibility_status: "inadmissible-unsupported"
  confidence: "low"
```

This prevents the ledger from collapsing all election-integrity issues into one political slogan.

## Powell Memorandum Linkage

The Powell Memorandum is an example of upstream institutional influence. It should be treated as a historical anchor, not as proof of causation for later claims unless a separate evidentiary chain supports that connection.

Its relevance to this standard is structural:

```text
funding
→ scholarship
→ media
→ legal theory
→ public premise
→ executive action
→ court test
```

The memo demonstrates that political action may be downstream from long-running institutional preparation.

## Non-Partisan Rule

This standard applies equally across administrations, parties, movements, agencies, courts, donors, corporations, advocacy groups, media networks, and ideological coalitions.

The ledger does not classify claims by whether they are politically favored.

It classifies claims by:

```text
source
evidence
lineage
authority
comparison
outcome
admissibility
```

## Anti-Misuse Rule

A Political Influence Tree must not be used to imply conspiracy, coordination, corruption, foreign influence, donor control, judicial capture, or institutional bad faith unless the required branch contains evidence sufficient for that classification.

Unknown lineage must remain unknown.

Unsupported claims must remain unsupported.

Structural similarity is not proof of direct causation.

## Minimal Entry Template

```yaml
topic_id: ""
topic_name: ""
summary: ""
surface_claim:
  claim_text: ""
  speaker_or_institution: ""
  date: ""
  source_url: ""
claimed_justification:
  category: ""
  stated_basis: ""
factual_basis:
  posture: ""
  primary_sources: []
  contrary_sources: []
influence_lineage:
  posture: ""
  known_nodes: []
  unknown_nodes: []
action_conversion:
  posture: ""
  instrument: ""
control_comparison:
  status: ""
  notes: ""
institutional_response:
  status: ""
  notes: ""
outcome_evidence:
  status: ""
  notes: ""
ledger_classification:
  evidence_posture: ""
  influence_posture: ""
  authority_posture: ""
  admissibility_status: ""
  confidence: ""
receipts:
  source_urls: []
  last_reviewed: ""
```

## Done Criteria for a Political Influence Tree

A topic entry is complete enough for ledger use when:

1. the surface claim is quoted or precisely summarized;
2. the speaker, institution, date, and source are identified;
3. the claimed justification is categorized;
4. the factual basis is separated from the rhetoric;
5. known influence lineage is recorded without filling unknown gaps;
6. the action conversion path is identified or marked absent;
7. control comparison is completed or marked missing;
8. judicial, administrative, legislative, or oversight response is recorded where applicable;
9. measurable outcomes are separated from claimed or projected outcomes;
10. admissibility status and confidence are assigned.

## Summary

The Political Influence Tree Standard makes political-topic analysis traceable, comparable, and evidence-bound.

It prevents modern political claims from being treated as isolated narratives and requires each topic to be mapped through factual basis, influence lineage, authority adoption, action conversion, control comparison, institutional response, and outcome evidence.

Within the Executive Rhetoric Ledger, this standard should govern how political topics are converted from public rhetoric into structured, reviewable ledger entries.
