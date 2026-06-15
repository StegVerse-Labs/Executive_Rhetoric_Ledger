# Cross-Repo Ingestion Notes

## Purpose

These notes define how other StegVerse-Labs repositories should feed records into the Executive Rhetoric Ledger without collapsing rhetoric, source existence, factual basis, authority conversion, and outcome evidence into one undifferentiated claim.

The ledger should receive structured evidence objects, not loose political narratives.

## Core Rule

```text
Ingest claim text as claim text.
Ingest evidence as evidence.
Do not convert one into the other without source posture.
```

## Expected Producer Repositories

Producer repositories may include, but are not limited to:

```text
Trumpality
Administrations
StegSocial
StegVerse policy archives
public-record collection repos
litigation or court-posture repos
agency-action tracking repos
```

A producer repo does not decide final ledger admissibility. It supplies records, receipts, and source posture for later ledger review.

## Accepted Ingestion Object Classes

```yaml
ingestion_object_classes:
  surface_claim:
    description: "A quote, statement, post, transcript segment, public framing, or campaign/executive claim."
  source_receipt:
    description: "A source posture object describing what a source can and cannot prove."
  action_record:
    description: "Executive order, agency action, rule, guidance, enforcement directive, litigation position, or legislation."
  court_posture:
    description: "Court opinion, order, injunction, stay, dismissal, remand, settlement, or pending litigation status."
  control_candidate:
    description: "Comparable case, jurisdiction, administration, policy instrument, enforcement tool, or harm magnitude."
  outcome_record:
    description: "Measured, claimed, projected, contradicted, or absent outcome evidence."
  influence_node:
    description: "Think tank, donor, legal network, media amplifier, academic source, advocacy group, or institutional origin point."
```

## Minimal Ingestion Envelope

Every cross-repo record should use this envelope before being converted into a Political Influence Tree.

```yaml
ingestion_id: ""
producer_repo: ""
producer_path: ""
producer_commit: ""
ingestion_date: ""
object_class: ""
related_topic_id: ""
related_topic_name: ""
source_receipts: []
content_summary: ""
ledger_relevance: ""
claimed_use: ""
admissibility_request: "context-only"
review_status: "pending"
notes: ""
```

## Required Source Posture

Every ingestion object must include at least one source posture entry unless the object is an internal routing note.

```yaml
source_posture_required: true
source_schema: "schemas/source-posture.schema.json"
```

A source receipt must identify:

- source type;
- institutional proximity;
- evidence role;
- verification status;
- admissibility use;
- confidence;
- red flags;
- what the source can and cannot prove.

## Admissibility Request Types

Producer repos may request a proposed admissibility use, but the ledger makes the final classification.

```text
context-only
claim-text
factual-basis
action-record
court-posture
influence-lineage
control-comparison
outcome-measurement
```

## Ingestion Guardrails

### 1. Claim Existence Is Not Claim Truth

A speech, post, press release, or media quote may prove that a claim was made.

It does not prove that the claim is true.

### 2. Media Repetition Is Not Independent Evidence

Multiple reports repeating the same unsupported claim should be treated as amplification unless they link to independent primary records.

### 3. Influence Is Not Causation

A think tank report, donor statement, legal brief, or policy memo may establish lineage.

It does not prove that a later executive action was caused by that source unless the chain is separately documented.

### 4. Action Conversion Must Be Identified

If a claim becomes an executive order, agency rule, enforcement directive, funding condition, litigation posture, or legislation, the conversion instrument must be recorded separately.

### 5. Control Comparison Cannot Be Assumed

Comparable jurisdictions, administrations, programs, harms, and enforcement tools must be documented before a claim becomes admissible for comparative analysis.

## Ingestion-to-Tree Mapping

```text
surface_claim object
→ Political Influence Tree / Surface Claim

source_receipt object
→ Political Influence Tree / Receipts

action_record object
→ Political Influence Tree / Action Conversion

court_posture object
→ Political Influence Tree / Judicial or Institutional Response

control_candidate object
→ Political Influence Tree / Control Comparison

outcome_record object
→ Political Influence Tree / Outcome Evidence

influence_node object
→ Political Influence Tree / Influence Lineage
```

## Review States

```text
pending
accepted-for-context
accepted-for-claim-text
accepted-for-action-record
accepted-for-court-posture
accepted-for-influence-lineage
accepted-for-control-comparison
accepted-for-outcome-measurement
rejected-unsupported
rejected-duplicate
rejected-out-of-scope
needs-primary-source
needs-control-comparison
needs-archive
```

## File Placement Recommendation

Producer repos should export ingestion-ready objects into a stable directory such as:

```text
ledger_exports/executive_rhetoric_ledger/
```

Each exported object should use a deterministic filename:

```text
<topic-id>__<object-class>__<date>__<short-source-id>.json
```

Example:

```text
PIT-EXAMPLE-001__surface_claim__2026-06-15__SRC-001.json
```

## Minimal Producer Checklist

- [ ] Object class is identified.
- [ ] Source receipt is attached.
- [ ] Claim text is separated from factual basis.
- [ ] Producer repo and commit are recorded.
- [ ] Proposed admissibility use is declared.
- [ ] Unknowns are left unknown.
- [ ] Unsupported claims are not upgraded.
- [ ] Control comparison requirement is noted if applicable.

## Summary

Cross-repo ingestion lets StegVerse-Labs repositories contribute records to the Executive Rhetoric Ledger while preserving evidentiary discipline.

The goal is not to move political claims faster.

The goal is to keep each claim, source, action, comparison, review, and outcome traceable enough to become admissible or explicitly remain inadmissible.
