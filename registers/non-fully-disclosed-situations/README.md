# Non-Fully-Disclosed Situations Register

## Purpose

This register preserves politically significant situations that became publicly observable through external reporting, litigation, whistleblowers, local officials, affected persons, leaked or internal records, or downstream operational effects before DHS or a component agency fully disclosed the relevant event, directive, implementation detail, data practice, institutional change, or recurring application.

It is separate from final ledger assessments.

```text
registration != verification
external report != final fact
agency denial != automatic exclusion
repetition != a new directive
partial disclosure != full disclosure
```

## Inclusion boundary

The register includes five categories that are intentionally broader than the strict policy-and-practice count:

1. individual raids reported before completion or before meaningful official disclosure;
2. specific shootings, deaths, injuries, or detention events where the hidden item was an event rather than a policy;
3. announced executive orders whose implementation details were later uncovered externally;
4. allegations that DHS unequivocally denies but that have sufficient independent reporting to warrant preservation as disputed, unresolved situations;
5. multiple applications of the same underlying directive, preserved as separate event instances linked to one parent directive.

## Required posture fields

Every entry must state:

- what was not fully disclosed;
- who first made it publicly observable;
- whether DHS later confirmed, partially confirmed, denied, declined comment, or remained silent;
- whether the entry concerns a directive, implementation detail, event, data practice, institutional change, allegation, or repeated application;
- current evidentiary posture;
- parent directive or related situation, when applicable;
- what remains unknown;
- whether the entry is safe for promotion beyond this register.

## Status vocabulary

```yaml
disclosure_status:
  - "not-announced-before-external-reporting"
  - "partially-disclosed"
  - "implementation-details-not-disclosed"
  - "event-not-fully-disclosed"
  - "agency-denied-disputed"
  - "later-confirmed"
  - "still-unresolved"

verification_status:
  - "multi-source-reported"
  - "primary-record-supported"
  - "court-record-supported"
  - "whistleblower-supported"
  - "officially-confirmed-after-reporting"
  - "disputed-with-independent-support"
  - "insufficient-for-promotion"
```

## Initial register scope: January 2025 forward

The machine-readable register is maintained in:

- `register.json`

The initial register includes the fourteen strict policy-and-practice contexts already identified and opens separate event-instance tracking for raids, shootings, deaths, implementation discoveries, disputed allegations, and repeated applications.

## Initial contexts

1. Alien Enemies Act removal process signed or activated before public release.
2. Living immigrants placed in Social Security death records to induce self-deportation.
3. IRS taxpayer-address access for immigration enforcement.
4. Medicaid enrollee data transferred to DHS.
5. Escalating ICE daily arrest quotas disclosed through external reporting and internal records.
6. Forced residential entry using administrative rather than judicial warrants.
7. Broad denial of bond-hearing eligibility through internal ICE guidance.
8. ICE participation in reunification interviews with parents of unaccompanied children.
9. ICE access to state driver information through Nlets.
10. Coordinated ICE public-affairs viral-content and influencer operations.
11. Reduction of internal oversight capacity and curtailment of body-camera expansion.
12. Expanded authority to detain previously admitted refugees during reinspection.
13. Use of TSA Secure Flight records for routine immigration arrests.
14. Temporary suspension of immigration-related vehicle stops after fatal shootings.

## Event-instance rule

Repeated operations under one directive must not be collapsed into a single undifferentiated record.

```text
parent directive
-> event instance
-> affected persons or place
-> source posture
-> agency response
-> outcome
-> correction or supersession
```

Examples include:

- individual raids conducted under an arrest-quota or targeting directive;
- each fatal shooting or death associated with a recurring enforcement tactic;
- each residential entry conducted under the same administrative-warrant interpretation;
- each data disclosure or query batch made under one data-sharing arrangement;
- each reunification interview where ICE questioning or arrest activity occurred;
- each vehicle stop conducted, suspended, resumed, or excepted under the same operational instruction.

## Disputed allegation rule

A DHS denial does not erase a situation from this register when independent reporting, records, witnesses, litigation, or official downstream actions provide enough support to justify preservation.

Such entries must remain labeled:

```yaml
disclosure_status: "agency-denied-disputed"
promotion_state: "register-only"
final_factual_finding: null
```

## Promotion boundary

An entry may leave this register only after governed review determines that the available evidence supports promotion into a research candidate, event packet, source-posture receipt, influence tree, assessment, or control comparison.

Until then, the register records incomplete disclosure and evidence posture—not guilt, legality, intent, causation, or final historical interpretation.
