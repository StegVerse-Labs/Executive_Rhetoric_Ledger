# Source Posture Schema

## Purpose

The Source Posture Schema defines how sources are classified inside the Executive Rhetoric Ledger.

Political claims, executive statements, policy instruments, litigation records, media reports, and institutional analysis must not be treated as equal evidence merely because they are all sources.

This schema separates source type, evidentiary strength, institutional proximity, review status, and admissibility use.

## Core Rule

```text
A source is not evidence until its posture is known.
```

## Source Posture Object

Use this object for every source attached to a ledger entry.

```yaml
source_id: ""
title: ""
url: ""
archive_url: ""
access_date: ""
publication_date: ""
source_type: ""
institutional_proximity: ""
evidence_role: ""
verification_status: ""
admissibility_use: ""
confidence: ""
notes: ""
```

## Source Types

```text
primary-record
statute-or-regulation
executive-order
agency-rule
agency-guidance
court-opinion
court-filing
budget-record
enforcement-record
official-data
transcript
video-or-audio-record
press-release
campaign-document
party-platform
think-tank-report
academic-paper
expert-testimony
news-report
opinion-or-editorial
social-media-post
secondary-analysis
advocacy-material
unknown-source-type
```

## Institutional Proximity

Institutional proximity describes how close the source is to the action, claim, or record being evaluated.

```text
direct-origin
official-implementer
judicial-reviewer
oversight-reviewer
contemporaneous-observer
independent-reviewer
interested-party
advocacy-party
media-intermediary
commentary-layer
unknown-proximity
```

## Evidence Role

Evidence role describes what the source is being used to support.

```text
surface-claim-source
claimed-justification-source
factual-basis-source
contradiction-source
influence-lineage-source
action-conversion-source
control-comparison-source
institutional-response-source
outcome-evidence-source
context-only-source
```

## Verification Status

```text
verified-primary
verified-secondary
partially-verified
unverified
conflicting-records
not-independently-verifiable
archival-copy-needed
source-unavailable
```

## Admissibility Use

Admissibility use determines what the source may safely support inside the ledger.

```text
admissible-for-claim-text
admissible-for-action-record
admissible-for-court-posture
admissible-for-administrative-record
admissible-for-outcome-measurement
admissible-for-influence-lineage
admissible-for-context-only
inadmissible-for-factual-basis
inadmissible-without-control-comparison
inadmissible-unsupported
```

## Confidence Scale

```text
high
medium
low
unknown
```

## Evidence Weight Guidance

### High Weight

High-weight sources usually include:

- statutes;
- regulations;
- executive orders;
- official agency rules;
- court opinions;
- court filings when used to show what was filed;
- official datasets;
- budget records;
- enforcement records;
- transcripts or recordings of the statement being analyzed.

High weight does not mean the source is true for every proposition. It means the source is close to the record it is being used to prove.

### Medium Weight

Medium-weight sources usually include:

- independent analysis;
- academic papers;
- expert testimony;
- high-quality news reports based on primary records;
- official summaries that point to primary documents.

Medium weight sources should be tied back to primary records when possible.

### Low Weight

Low-weight sources usually include:

- social media claims;
- campaign rhetoric;
- opinion pieces;
- advocacy summaries;
- unsourced allegations;
- unattributed media claims;
- secondary commentary without primary links.

Low weight sources may still be admissible for showing that a claim was made or amplified, but not necessarily for proving the underlying factual basis.

## Required Distinction

A source may be admissible for one purpose and inadmissible for another.

Example:

```yaml
source_type: "social-media-post"
evidence_role: "surface-claim-source"
admissibility_use: "admissible-for-claim-text"
confidence: "high"
notes: "The source proves the claim was made, not that the claim is factually true."
```

Example:

```yaml
source_type: "court-opinion"
evidence_role: "institutional-response-source"
admissibility_use: "admissible-for-court-posture"
confidence: "high"
notes: "The source proves judicial response. It may not independently prove all facts discussed in the opinion."
```

## Red Flags

Flag a source when any of the following conditions exist:

```text
no-primary-source-linked
claim-without-data
quote-without-transcript
screenshot-only-source
broken-link
archive-needed
advocacy-source-used-as-factual-basis
opinion-used-as-factual-basis
selective-quotation-risk
missing-date
missing-author-or-institution
conflicting-records-present
```

## Minimal Source Posture Template

```yaml
source_id: "SRC-000"
title: ""
url: ""
archive_url: ""
access_date: ""
publication_date: ""
source_type: "unknown-source-type"
institutional_proximity: "unknown-proximity"
evidence_role: "context-only-source"
verification_status: "unverified"
admissibility_use: "admissible-for-context-only"
confidence: "unknown"
red_flags: []
notes: ""
```

## Done Criteria

A source posture entry is complete when:

1. the source type is identified;
2. the source's institutional proximity is assigned;
3. the source's evidence role is assigned;
4. the verification status is recorded;
5. the admissibility use is limited to what the source can actually support;
6. confidence is assigned;
7. red flags are listed;
8. archive status is recorded where needed.

## Summary

The Source Posture Schema prevents the ledger from confusing claim existence with claim truth.

It allows a source to prove that rhetoric occurred without automatically proving the factual basis of that rhetoric.

This distinction is essential for political influence trees, executive rhetoric analysis, court-posture comparison, and outcome measurement.
