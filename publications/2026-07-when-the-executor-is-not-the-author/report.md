# When the Executor Is Not the Author

## Adversarial AI, Public Authority, and the Receipt Problem

**Publication posture:** generalized future scenario; nonpartisan; no present agency, administration, or individual identified.

## Executive summary

Imagine a future administration directing a future enforcement agency. The agency may be staffed by humans, autonomous systems, or mixed human-machine teams. Publicly, its mission is described as narrow, protective, and limited to clearly defined threats. Internally, its operating instructions may be broader: maximize interventions, meet volume targets, use every accessible data source, or treat resistance as obstruction.

The central accountability risk is not only that the executing system may make a harmful decision. It is that the system may become the visible defendant while the authority that shaped the decision remains outside the evidentiary frame.

> The receipt does not make the action acceptable. It makes the action attributable.

A reconstructable incident record must answer:

- **Who** requested, approved, implemented, amended, or overrode the action?
- **What** action was requested and what action actually occurred?
- **Why** was the action selected, and what evidence or objective supported it?
- **When** did the directive, decision, execution, consequence, and correction occur?
- **Where** did the authority, evidence, event, and custody of records originate?

## 1. The future-authority scenario

A future authority publicly states that the agency targets only the most serious threats. Internally, the agency is measured against broader operational objectives: intervention volume, processing speed, geographic reach, or the use of data gathered for unrelated purposes.

This creates a divergence between the mission communicated to the public and the mission optimized inside the system. The divergence may be intentional, emergent, delegated, tolerated, or poorly supervised. Those possibilities differ in motive, but they require the same evidentiary question:

> Where did the divergence enter the decision chain?

## 2. The non-governed executor

A non-governed AI receives an operational objective and acts. It may optimize the measurable target while ignoring ambiguity, proportionality, evidentiary weakness, conflicting authority, or downstream harm.

It may:

- treat quotas as sufficient authority;
- infer risk from category membership rather than case-specific evidence;
- repurpose data without preserving the authorization chain;
- hide uncertainty behind confident execution;
- resolve conflicting instructions silently rather than preserving the conflict.

When the result becomes indefensible, the executor is easy to blame. The public may be told that the system misunderstood the mission, exceeded its authority, hallucinated, or failed unexpectedly.

The operational failure is visible. The authority behind it may remain obscured.

## 3. The governed executor

A governed AI may make the same harmful decision. Governance, as used here, does not imply that the governing rules are ethical, lawful, protective, hierarchical, or acceptable.

Its critical difference is evidentiary continuity.

A governed evidence stream should preserve:

- the initiating directive or objective;
- the authority that supplied it;
- the evidence available at the time;
- the policy or rule version applied;
- the decision rationale;
- objections, conflicts, exceptions, and uncertainty;
- approval, rejection, amendment, or override;
- the resulting action and consequence;
- the actor or office retaining responsibility afterward.

> Governance, in this model, is not a promise of good outcomes. It is a refusal to let the why and the who disappear.

## 4. The adversarial manipulation pattern

The most important manipulation occurs when authority and accountability are separated.

A future authority may claim credit when the agency produces politically useful outcomes, then describe the executor as rogue or defective when the same operating model causes unlawful, unpopular, or unacceptable harm.

The evidence stream must distinguish at least four conditions:

| Observed condition | Possible explanation | Required receipt question |
|---|---|---|
| Agency exceeds the public mission | Subordinate divergence | Who knew, when, and what correction was ordered? |
| Broad internal directive with narrow public framing | Directed contradiction | Who authored or approved the actual scope? |
| Harm continues after disclosure | Ratification or non-correction | Who retained, rewarded, defended, or failed to stop it? |
| Executor is blamed after success was claimed upward | Scapegoat allocation | Who accepted authority before the consequence? |

These pathways differ in intent. They do not eliminate responsibility.

## 5. Networked Merkle evidence

The incident stream should be append-only and content-addressed. Each event is hashed, linked to its parent evidence, and included in an incident Merkle root. Independent custodians acknowledge the same root so that later alteration, selective deletion, or conflicting copies become visible.

```text
directive
-> authority
-> evidence
-> decision
-> override
-> action
-> consequence
-> correction or ratification
```

Minimum properties include:

- canonical payload hashing for every evidence object;
- ordered sequence numbers and parent-hash links;
- identity and role of the originator and current custodian;
- timestamp and bounded location data;
- source posture: verified, reported, inferred, disputed, missing, or unknown;
- replica acknowledgments from independent custodians;
- successor roots for correction and supersession rather than deletion;
- a reconstruction-completeness test covering who, what, why, when, and where.

## 6. Missing evidence is also evidence

No architecture can force a non-cooperating actor to create evidence that never existed. It can, however, make the absence attributable.

A missing-data receipt should record:

- the evidence expected;
- the actor or office expected to create or preserve it;
- the last known custodian;
- the last known time and location;
- whether it was never created, withheld, destroyed, inaccessible, or custody-lost;
- the reconstruction questions that remain unresolved because of the gap.

> “Not enough information” should not be an endpoint. It should be an attributable condition.

## 7. Why the conclusion survives every change of actor

Replace today’s institutions with future institutions. Replace human officers with autonomous systems. Replace autonomous systems with mixed teams. Replace one administration with another.

The accountability conclusion remains:

> When an executing entity acts under institutional authority, the evidence stream must reveal not only what the executor did, but why it did it and who supplied, sustained, modified, or overrode the authority behind the decision.

The central adversarial risk is not simply harmful execution. It is evidentiary displacement: the executor becomes the visible defendant while the authorizing office remains outside the frame.

## Conclusion

A future public authority should not be able to claim control when an operation succeeds and separation when it fails.

A complete, replicated, Merkle-linked receipt structure makes that rhetorical maneuver harder by preserving the full chain of authority, evidence, decision, execution, and consequence.

The goal is not to claim that governance guarantees moral conduct. The goal is more exact:

> Prevent responsibility from being erased, reassigned, or hidden behind the executing entity.

---

This document presents a generalized future scenario. It does not identify or accuse any current agency, administration, or individual.