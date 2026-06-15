# Political Influence Tree Entry Template

## Purpose

Use this template to create a structured Political Influence Tree entry for a politically active topic, claim, policy justification, executive statement, administrative action, or judicially contested public narrative.

This template implements the Political Influence Tree Standard.

## Completion Rule

A topic entry is not complete until the surface claim, factual basis, influence lineage, authority adoption, action conversion, control comparison, institutional response, outcome evidence, and ledger classification are separately recorded.

Do not fill unknown branches with assumptions.

Unknown remains unknown.

Unsupported remains unsupported.

Structural similarity is not proof of direct causation.

---

# Political Influence Tree Entry

## Entry Metadata

```yaml
topic_id: ""
topic_name: ""
entry_status: "draft"
jurisdiction: ""
time_window: ""
created_date: ""
last_reviewed: ""
reviewer: ""
related_standard: "standards/political-influence-tree-standard.md"
```

## 1. Surface Claim

Record the visible claim as precisely as possible.

```yaml
surface_claim:
  claim_text: ""
  exact_quote_available: false
  speaker_or_institution: ""
  office_or_role: ""
  date: ""
  venue: ""
  jurisdiction: ""
  source_url: ""
  source_type: ""
  transcript_available: false
  archive_url: ""
```

### Notes

```text

```

## 2. Claimed Justification

Identify the stated basis for the claim or action.

```yaml
claimed_justification:
  category: ""
  stated_basis: ""
  quoted_basis: ""
  implied_basis: ""
  justification_type:
    - "fraud"
    - "national-security"
    - "economic-harm"
    - "public-safety"
    - "constitutional-authority"
    - "emergency-condition"
    - "administrative-necessity"
    - "moral-cultural-premise"
    - "other"
```

### Notes

```text

```

## 3. Factual Basis

Separate the factual record from rhetoric, repetition, or political framing.

```yaml
factual_basis:
  evidence_posture: "pending-verification"
  primary_records: []
  administrative_data: []
  court_records: []
  budget_records: []
  enforcement_records: []
  independent_analysis: []
  expert_testimony: []
  official_investigations: []
  unsupported_assertions: []
  contradictions: []
  missing_records: []
```

### Evidence Summary

```text

```

## 4. Influence Lineage

Record known upstream influence nodes without inventing missing links.

```yaml
influence_lineage:
  influence_posture: "unknown-origin"
  known_origin_points: []
  institutional_amplifiers: []
  media_amplifiers: []
  legal_networks: []
  funding_or_donor_links: []
  policy_documents: []
  academic_or_expert_sources: []
  lobbying_channels: []
  party_or_campaign_documents: []
  religious_or_cultural_institutions: []
  activist_organizations: []
  foreign_influence_indicators: []
  unknown_nodes: []
```

### Lineage Notes

```text

```

## 5. Action Conversion

Identify whether the claim became an institutional action.

```yaml
action_conversion:
  authority_posture: "no-authority-conversion-found"
  action_type: ""
  instrument: ""
  instrument_url: ""
  date: ""
  actor: ""
  enforcing_entity: ""
  implementation_status: ""
  affected_population_or_program: ""
```

### Conversion Notes

```text

```

## 6. Control Comparison

Control comparison is required whenever the claim is used to justify differential treatment, selective enforcement, emergency authority, funding leverage, fraud enforcement, or moralized policy action.

```yaml
control_comparison:
  required: true
  status: "missing"
  comparable_red_jurisdictions: []
  comparable_blue_jurisdictions: []
  comparable_prior_administrations: []
  comparable_policy_instruments: []
  comparable_fraud_or_harm_magnitude: []
  comparable_enforcement_tools: []
  comparable_judicial_posture: []
  missing_controls: []
  comparison_notes: ""
```

### Control Questions

```text
Was the same standard applied to comparable red and blue jurisdictions?
Was the same enforcement tool used for comparable conduct?
Was the claimed harm magnitude similar across comparison cases?
Was the judicial posture consistent across administrations?
Was the claimed factual basis stronger, weaker, or absent in comparable cases?
Was the policy instrument proportional to the documented factual basis?
```

## 7. Judicial / Institutional Response

```yaml
institutional_response:
  judicial_status: ""
  administrative_status: ""
  legislative_status: ""
  oversight_status: ""
  injunctions: []
  stays: []
  dismissals: []
  remands: []
  settlements: []
  reversals: []
  pending_reviews: []
  no_challenge_found: false
```

### Response Notes

```text

```

## 8. Outcome Evidence

Separate measured outcomes from claimed, projected, or contradicted outcomes.

```yaml
outcome_evidence:
  measured_outcomes: []
  claimed_outcomes: []
  projected_outcomes: []
  contradicted_outcomes: []
  no_measurable_effect_yet: false
  harm_documented: []
  benefit_documented: []
  insufficient_evidence: false
```

### Outcome Notes

```text

```

## 9. Ledger Classification

```yaml
ledger_classification:
  evidence_posture: "pending-verification"
  influence_posture: "unknown-origin"
  authority_posture: "no-authority-conversion-found"
  admissibility_status: "pending-evidence"
  confidence: "low"
  classification_notes: ""
```

## 10. Receipts

Every source used in the entry must be listed here.

```yaml
receipts:
  sources: []
  archive_sources: []
  review_notes: []
  unresolved_questions: []
  last_reviewed: ""
```

## Final Summary

```text
Topic:
Claim:
Factual basis:
Influence lineage:
Authority conversion:
Control comparison:
Institutional response:
Outcome evidence:
Ledger classification:
```

## Done Criteria

- [ ] Surface claim is quoted or precisely summarized.
- [ ] Speaker, institution, date, and source are identified.
- [ ] Claimed justification is categorized.
- [ ] Factual basis is separated from rhetoric.
- [ ] Known influence lineage is recorded without filling unknown gaps.
- [ ] Action conversion path is identified or marked absent.
- [ ] Control comparison is completed or marked missing.
- [ ] Judicial, administrative, legislative, or oversight response is recorded where applicable.
- [ ] Measurable outcomes are separated from claimed or projected outcomes.
- [ ] Admissibility status and confidence are assigned.
- [ ] Receipts are listed.
