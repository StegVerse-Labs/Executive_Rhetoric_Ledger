# ERL Fund Governance Classification Standard v1

## Purpose

Provide a reusable, fail-closed classification model for evaluating potentially problematic use, retention, transfer, or control of pooled political, nonprofit, organizational, public, or donor-supplied funds without collapsing distinct legal, representational, governance, and strategic questions into a single `misuse` label.

## Core rule

`legal_permissibility != represented_purpose_alignment != governance_quality != deployment_strategy`

Each axis MUST be evaluated independently. Evidence supporting one axis MUST NOT automatically promote another.

## Four top-level classifications

### 1. Legal misuse

Question: Do primary records and controlling authority support a conclusion that the conduct violated applicable law, regulation, reporting requirements, restrictions on personal use, coordination rules, fiduciary duties, contractual restrictions, or other enforceable obligations?

Allowed states:
- `NOT_ASSESSED`
- `INSUFFICIENT_EVIDENCE`
- `NO_VIOLATION_SUPPORTED`
- `POTENTIAL_VIOLATION`
- `VIOLATION_SUPPORTED`

`VIOLATION_SUPPORTED` requires controlling authority plus primary factual evidence sufficient for independent reconstruction. A media allegation, delayed spending, amendment, unusual payment, or donor complaint is insufficient alone.

### 2. Represented-purpose divergence

Question: Were funds used, retained, transferred, or controlled in a way materially inconsistent with the purpose reasonably represented to contributors, stakeholders, beneficiaries, members, or the public?

Allowed states:
- `NOT_ASSESSED`
- `REPRESENTATION_NOT_RECONSTRUCTED`
- `ALIGNED`
- `PARTIAL_DIVERGENCE`
- `MATERIAL_DIVERGENCE_SUPPORTED`

This axis can be nonzero even where conduct is lawful. It requires preservation of the actual solicitation, representation, governing statement, restriction, or other purpose evidence and comparison against actual disposition of funds.

### 3. Governance / ethical misuse

Question: Does otherwise lawful conduct materially concentrate control, create self-dealing or related-party risk, defeat organizational purpose, produce an inadequately disclosed private benefit, bypass meaningful oversight, or otherwise create a governance-quality failure?

Allowed states:
- `NOT_ASSESSED`
- `INSUFFICIENT_EVIDENCE`
- `NO_GOVERNANCE_CONCERN_SUPPORTED`
- `GOVERNANCE_RISK`
- `GOVERNANCE_MISUSE_SUPPORTED`

A governance concern is not a legal violation unless separately supported on the legal axis.

### 4. Strategic nondeployment

Question: Are funds intentionally retained, delayed, reserved, redirected within lawful scope, or deployed selectively for strategic leverage, future contests, succession influence, bargaining power, contingency reserves, or other organizational strategy?

Allowed states:
- `NOT_ASSESSED`
- `STRATEGY_NOT_RECONSTRUCTED`
- `NORMAL_DEPLOYMENT`
- `DELAYED_OR_SELECTIVE_DEPLOYMENT`
- `STRATEGIC_NONDEPLOYMENT_SUPPORTED`

Strategic nondeployment is descriptive, not inherently adverse. It MUST NOT be labeled misuse absent independent support on another axis.

## Evidence state vector

Every governed fund case SHOULD maintain the following independent dimensions:

- `LEGALITY`
- `DONOR_REPRESENTATION`
- `BENEFICIAL_RECIPIENT`
- `ORGANIZATIONAL_PURPOSE`
- `DEPLOYMENT_TIMING`
- `CONTROL_CONCENTRATION`
- `DISCLOSURE_ACCURACY`

Optional dimensions MAY be added when domain-specific evidence requires them, but these seven are the default cross-case minimum.

## Required evidence classes

Before an adverse classification may be supported, the case SHOULD reconstruct as applicable:

1. controlling legal/contractual authority;
2. organization/committee formation and amendment history;
3. donor/member/public-facing representations and restrictions;
4. receipts, transfers, disbursements, refunds, debts, obligations, and retained balances;
5. beneficial recipients and related-party relationships;
6. deployment chronology and decision authority;
7. disclosure/reporting accuracy and amendment supersession;
8. alternative explanations and ordinary-course controls;
9. independent review.

## Fail-closed invariants

- `lawful != aligned_with_represented_purpose`
- `represented_purpose_divergence != legal_violation`
- `related_party_payment != self_dealing`
- `private_benefit != prohibited_personal_use`
- `large_balance != misuse`
- `delayed_spending != misuse`
- `strategic_nondeployment != misuse`
- `donor_frustration != donor_deception`
- `amended_filing != wrongdoing`
- `governance_risk != governance_misuse_supported`
- `candidate_layer_exists != finding`

## Promotion boundary

No axis may be promoted to its strongest adverse state from candidate-layer existence, secondary reporting, inference from timing, political disagreement, or an unexplained transaction alone. Strong adverse states require primary evidence, an explicit evidence-to-classification path, competing explanations, and independent review.

## Publication boundary

A public summary MUST report each material axis separately. It MUST NOT compress a mixed state such as `lawful + represented-purpose divergence + strategic nondeployment` into the single word `misuse` unless the legal or governance misuse axis itself is independently supported.
