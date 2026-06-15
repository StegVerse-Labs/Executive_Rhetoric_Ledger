# Source Receipt Examples

## Purpose

This file provides example receipts for common Executive Rhetoric Ledger source classes.

A receipt is not just a URL.

A receipt records what the source can prove, what it cannot prove, and how it may be used inside the ledger.

## Core Rule

```text
A receipt proves only what its posture allows it to prove.
```

## Example 1: Primary Record Receipt

Use when the source directly contains the claim, order, filing, rule, transcript, or record being analyzed.

```yaml
source_id: "SRC-PRIMARY-001"
title: "Example Executive Order"
url: "https://example.gov/executive-order"
archive_url: ""
access_date: "2026-06-15"
publication_date: "2026-01-20"
source_type: "executive-order"
institutional_proximity: "direct-origin"
evidence_role: "action-conversion-source"
verification_status: "verified-primary"
admissibility_use: "admissible-for-action-record"
confidence: "high"
red_flags: []
notes: "This source proves the executive order exists and records its text. It does not independently prove the factual claims used to justify the order."
```

## Example 2: Court Opinion Receipt

Use when the source establishes judicial posture.

```yaml
source_id: "SRC-COURT-001"
title: "Example Court Opinion"
url: "https://example.com/court-opinion"
archive_url: ""
access_date: "2026-06-15"
publication_date: "2026-03-10"
source_type: "court-opinion"
institutional_proximity: "judicial-reviewer"
evidence_role: "institutional-response-source"
verification_status: "verified-primary"
admissibility_use: "admissible-for-court-posture"
confidence: "high"
red_flags: []
notes: "This source proves the court's posture and reasoning. It should not be used alone to prove every factual allegation discussed in the litigation."
```

## Example 3: News Report Receipt

Use when a news report is used for context or as a pointer to primary records.

```yaml
source_id: "SRC-NEWS-001"
title: "Example News Report"
url: "https://example.com/news-report"
archive_url: ""
access_date: "2026-06-15"
publication_date: "2026-02-01"
source_type: "news-report"
institutional_proximity: "media-intermediary"
evidence_role: "context-only-source"
verification_status: "verified-secondary"
admissibility_use: "admissible-for-context-only"
confidence: "medium"
red_flags:
  - "no-primary-source-linked"
notes: "This source may support context and chronology. It should not be used as primary factual basis unless supported by linked records."
```

## Example 4: Social Media Receipt

Use when the source proves that a public claim was made or amplified.

```yaml
source_id: "SRC-SOCIAL-001"
title: "Example Social Media Post"
url: "https://example.com/social-post"
archive_url: ""
access_date: "2026-06-15"
publication_date: "2026-02-15"
source_type: "social-media-post"
institutional_proximity: "direct-origin"
evidence_role: "surface-claim-source"
verification_status: "partially-verified"
admissibility_use: "admissible-for-claim-text"
confidence: "medium"
red_flags:
  - "screenshot-only-source"
notes: "This source may prove the claim text if authenticated. It does not prove the factual truth of the claim. Archive or platform verification is preferred."
```

## Example 5: Think Tank Report Receipt

Use when a report may be part of influence lineage, claimed justification, or factual basis.

```yaml
source_id: "SRC-THINKTANK-001"
title: "Example Policy Report"
url: "https://example.org/policy-report"
archive_url: ""
access_date: "2026-06-15"
publication_date: "2025-11-01"
source_type: "think-tank-report"
institutional_proximity: "interested-party"
evidence_role: "influence-lineage-source"
verification_status: "verified-secondary"
admissibility_use: "admissible-for-influence-lineage"
confidence: "medium"
red_flags: []
notes: "This source may help establish influence lineage or policy framing. It requires separate primary records before being used as factual basis for executive action."
```

## Example 6: Unsupported Assertion Receipt

Use when the source proves only that an unsupported assertion was made.

```yaml
source_id: "SRC-ASSERTION-001"
title: "Example Public Statement"
url: "https://example.com/public-statement"
archive_url: ""
access_date: "2026-06-15"
publication_date: "2026-04-01"
source_type: "press-release"
institutional_proximity: "direct-origin"
evidence_role: "surface-claim-source"
verification_status: "verified-primary"
admissibility_use: "inadmissible-for-factual-basis"
confidence: "high"
red_flags:
  - "claim-without-data"
notes: "This source proves the statement was made by the issuing institution. It does not provide admissible factual support for the statement."
```

## Receipt Review Checklist

- [ ] Source type is identified.
- [ ] Institutional proximity is assigned.
- [ ] Evidence role is assigned.
- [ ] Verification status is assigned.
- [ ] Admissibility use is limited to what the source can actually prove.
- [ ] Confidence is assigned.
- [ ] Red flags are listed.
- [ ] Notes distinguish claim existence from claim truth.

## Summary

Receipts keep the ledger from treating all sources as equal.

A receipt should always explain what a source proves, what it does not prove, and whether it is admissible for claim text, action record, court posture, influence lineage, factual basis, outcome measurement, or context only.
