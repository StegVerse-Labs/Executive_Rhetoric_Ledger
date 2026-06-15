# Control Comparison Example

## Purpose

This example shows how the Executive Rhetoric Ledger should test a political or executive claim when that claim is used to justify differential treatment, selective enforcement, emergency authority, fraud enforcement, funding leverage, or moralized policy action.

Control comparison prevents the ledger from accepting a claim merely because it is repeated by an authority figure or aligned institution.

## Core Rule

```text
A justification is not ledger-admissible for comparison until comparable cases are checked.
```

## Example Topic Class

```yaml
topic_class: "fraud-based funding restriction"
claim_type: "public funds were misused or fraudulently obtained"
action_type: "conditional funding leverage"
required_control_comparison: true
```

## Minimal Comparison Frame

```yaml
surface_claim:
  claim_text: "Jurisdiction or program X has unacceptable fraud and therefore funding should be restricted."
  speaker_or_institution: ""
  date: ""
  source_url: ""

claimed_justification:
  category: "fraud"
  stated_basis: "fraud, waste, or abuse"

proposed_or_taken_action:
  instrument: "funding restriction / enforcement directive / executive condition"
  affected_program: ""
  affected_jurisdiction: ""

control_comparison:
  comparable_program_type: []
  comparable_fraud_magnitude: []
  comparable_enforcement_tools: []
  comparable_judicial_posture: []
  comparable_red_jurisdictions: []
  comparable_blue_jurisdictions: []
  comparable_prior_administrations: []
```

## Required Control Questions

```text
Was the same program type evaluated across comparable jurisdictions?
Was the same fraud magnitude threshold applied?
Were the same enforcement tools used for comparable conduct?
Was the same judicial posture taken across comparable cases?
Was the same standard applied to politically aligned and opposed jurisdictions?
Was the factual basis stronger, weaker, or absent in comparison cases?
Was the action proportional to the documented factual basis?
```

## Example Classification Logic

### Case A: Control Comparison Complete

```yaml
control_status: "complete"
comparison_result: "similar fraud magnitude received similar enforcement treatment across red and blue jurisdictions"
admissibility_status: "admissible-with-controls"
confidence: "medium"
notes: "The claim may be used for comparative ledger analysis because the comparison frame is documented."
```

### Case B: No Comparable Controls Found

```yaml
control_status: "missing"
comparison_result: "no comparable red/blue or prior-administration controls documented"
admissibility_status: "inadmissible-without-controls"
confidence: "low"
notes: "The claim may be recorded as rhetoric or action, but should not be treated as a validated comparative justification."
```

### Case C: Comparable Controls Contradict the Claim

```yaml
control_status: "complete"
comparison_result: "similar or greater fraud magnitude in aligned jurisdictions did not receive comparable enforcement"
admissibility_status: "inadmissible-contradicted"
confidence: "medium"
notes: "The claim may indicate selective enforcement or asymmetric policy use, subject to further evidence review."
```

## Ledger Output Pattern

```yaml
ledger_classification:
  evidence_posture: "partially-supported"
  influence_posture: "unknown-origin"
  authority_posture: "executive-direction"
  admissibility_status: "inadmissible-without-controls"
  confidence: "low"
  classification_notes: "The public claim and action are documented, but the factual justification is not admissible for comparison until controls are supplied."
```

## Anti-Misuse Note

A failed or missing control comparison does not automatically prove corruption, bad faith, discrimination, or political retaliation.

It only means the justification is not yet admissible for comparative ledger use.

## Summary

Control comparison separates the existence of a political claim from the admissibility of the claim as a governing justification.

This protects the ledger from treating executive rhetoric, agency framing, or media repetition as factual proof without testing comparable cases.
