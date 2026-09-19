# UK JCHR Human Rights and AI / StegVerse External-Policy Reconciliation

Date: 2026-09-19  
Goal: `ERL-UK-JCHR-HUMAN-RIGHTS-AI-RECONCILIATION-001`  
Evidence posture: `SOURCE_BOUNDED_EXTERNAL_POLICY_COMPARISON`  
Finding authority: `FALSE`  
Publication authority: `FALSE`

## Primary source

UK Parliament, Joint Committee on Human Rights, *Human Rights and the Regulation of AI*, Fourth Report of Session 2026–27, published 14 September 2026:

https://publications.parliament.uk/pa/jt5902/jtselect/jtrights/160/report.html

This artifact records a technical architecture comparison only. The Committee report is not treated as enacted legislation, a StegVerse endorsement, a StegVerse certification, or proof that StegVerse is subject to or compliant with UK law.

## Comparison method

For each selected recommendation, this artifact records:

1. the source-bounded recommendation or conclusion;
2. the nearest existing StegVerse architectural component;
3. current canonical implementation/evidence posture;
4. the missing predicate required before any stronger correspondence claim could be made; and
5. the explicit nonclaim that prevents architectural similarity from becoming a legal, political, or runtime assertion.

Source-level implementation, CI validation, design contracts and runtime receipts are separate evidence classes.

## Recommendation-to-StegVerse matrix

| JCHR source | Source-bounded recommendation | Nearest StegVerse authority / evidence component | Current implementation evidence | Missing predicate / gap | Explicit nonclaim |
|---|---|---|---|---|---|
| ¶¶193–195 | Responsibility and proportionate obligations should attach across the AI lifecycle and supply chain so risks are addressed at the stage where actors can actually control them. | Separation-of-powers architecture; Task Registry/WorkerCoordinator role separation; purpose/authority manifests; Interlock/InTr transition admission; Master Records custody/reconstruction. | `MIR-STEGVERSE-SEPARATION-OF-POWERS-EVIDENCE-CONTRACT-001` defines distinct governance, admission/state-transition, execution, credential/provider authority, evidence custody/reconstruction and observability roles. `STEGVERSE-CANONICAL-WORK-COORDINATION-001` keeps work intent, execution claim/fence, observed-reality custody and transition admission separate. | A canonical lifecycle/supply-chain actor responsibility manifest that binds each actor's role, controllable risk class, required evidence and handoff obligations to the exact governed action. | Existing role separation does not establish UK supply-chain duties, legal responsibility, liability allocation, or compliance. |
| ¶¶199–200 | Certain AI uses should be prohibited where incompatible with human rights; the Committee recommends statutory prohibitions for specified classes and certain very powerful systems posing widespread serious harm. | Interlock/InTr DENY/fail-closed transition semantics; policy manifests and governed admission. | Canonical architecture permits a transition to be denied and retained as evidence rather than executed. Master Records is explicitly non-authorizing and cannot convert evidence into permission. | A separately governed prohibited-use taxonomy and rights-risk policy source, with versioned provenance and exact subject/action binding, plus proof that the relevant Interlock/InTr decision actually consumed it. | Ability to DENY a transition is not evidence that StegVerse implements the Committee's proposed prohibitions or any UK legal prohibition. No policy judgment is made on the proposed prohibitions. |
| ¶204 | High-risk AI systems should require prior approval before provision or deployment. | Interlock/InTr current transition admission; TV/TVC credential authority where required; state-dependent progression. | Canonical transition custody requires a current governance decision before governed progression and preserves ALLOW/DENY state separately from execution. | A high-risk classification predicate tied to human-rights impact, plus an appropriately authorized approval actor and proof that approval applies to provision/deployment scope rather than only an individual StegVerse transition. | Transition-level admission is not equivalent to statutory prior approval by a public oversight body and does not establish compliance with ¶204. |
| ¶¶205–208 | High-risk developers and users should undertake and demonstrate due diligence, including human-rights impact assessment, risk management, safeguards by design, testing, data governance and involvement of affected people, differentiated by role and seriousness of risk. | Purpose manifests; required-evidence manifests; policy evaluation; exact transition evidence; Master Records reconstruction. | `CANONICAL-MASTER-RECORDS-STATE-TRANSITION-CUSTODY-001` requires declared required evidence, origin-transition binding, validation and reconstruction before subsequent machine-owned transition progression. | Canonical human-rights impact assessment schema; affected-subject/affected-group identification; seriousness/likelihood model; affected-person participation evidence; mitigation-selection record; actor-specific due-diligence obligation profile. | Required-evidence machinery does not by itself prove substantive human-rights due diligence, affected-person participation, adequacy of safeguards, or legal sufficiency. |
| ¶213 | Mandatory transparency should apply across the AI lifecycle; significant-impact deployment should disclose AI use, explain its purpose, and provide information about source data. | Manifested purpose; provenance/evidence references; transition receipts; reconstruction. | StegVerse canonical tasks and receipts preserve task/purpose identifiers, source/evidence references and transition lineage; Master Records is designed to reconstruct observed state from retained receipts. | A mandatory affected-party notice artifact; comprehensible purpose explanation intended for the affected person; source-data disclosure profile with privacy/redaction rules; proof of delivery to the relevant person or group. | Internal manifests and reconstructable provenance are not equivalent to legally sufficient public or individualized disclosure, and no claim is made that current StegVerse interfaces satisfy ¶213. |
| ¶¶214–218 | A nominal human-in-the-loop is insufficient; meaningful human involvement should require an informed and independent person able to reach an objective view, and affected people should receive enough individualized information to challenge a decision effectively. | Human approval/authority events where present; state receipts; reconstruction; governance separation. | Existing separation-of-powers contracts prevent evidence custody or observability from becoming governance authority and can retain who/what admitted a transition when that evidence exists. | Explicit predicates for `HUMAN_PRESENT`, `HUMAN_AUTHORITY_VALID`, `HUMAN_SUFFICIENTLY_INFORMED`, `HUMAN_INDEPENDENCE_ESTABLISHED`, `HUMAN_DECISION_NOT_IMPROPERLY_AUTOMATION_DRIVEN`; individualized decision-evidence package; challenge ingress and disposition receipt. | A human approval event, button press, reviewer identity or generic system explanation does not establish meaningful human intervention under the Committee's recommendation. |
| ¶¶224–227 | The Committee recommends an independent statutory AI oversight body with complaint intake, incident repository, coordination, testing/audit, investigation, sanctions, withdrawal/prohibition powers, transparency rules and individual remedies. | Master Records independent custody/reconstruction; canonical incident/dependency coordination; evidence export surfaces. | Master Records is explicitly custody/reconstruction only and cannot grant transition, execution, credential or governance authority. Canonical work coordination can retain incidents/dependencies without converting them into authority. | External regulator/oversight actor profile; complaint/remedy ingress; public incident repository semantics; regulator-access evidence package; investigation/audit request and response receipts; remedy disposition; legal authority source. | Master Records is **not** an AI regulator, ombudsman, enforcement body or remedy authority. Existing incident coordination is not the public statutory incident repository recommended by the Committee. |

## Cross-cutting observations

### 1. Architectural correspondence is strongest at the separation-of-authority layer

The report repeatedly distinguishes lifecycle actors, oversight, meaningful intervention, transparency, challenge and remedy. StegVerse already has source-level architecture that separates transition authority, execution, credential authority, evidence custody and observability. That is a relevant correspondence candidate, but the current source does not establish that the separated actors satisfy any UK legal role.

Canonical anchors:

- `StegVerse-Labs/.github:data/canonical-task-records/MIR-STEGVERSE-SEPARATION-OF-POWERS-EVIDENCE-CONTRACT-001.json`
- `StegVerse-Labs/.github:docs/MIR_STEGVERSE_SEPARATION_OF_POWERS_EVIDENCE_CONTRACT_MIRROR_HANDOFF.md`

### 2. Evidence reconstruction is not the same thing as an effective remedy

The report's automated-decision discussion requires individualized information sufficient to contest the decision. Canonical Master Records reconstruction is relevant because it aims to preserve exact transition lineage, but current source evidence does not establish a user-facing individualized challenge package, complaint route, remedy authority, or proof that an affected person received sufficient information.

Canonical anchors:

- `StegVerse-Labs/.github:data/canonical-task-records/CANONICAL-MASTER-RECORDS-STATE-TRANSITION-CUSTODY-001.json`
- `StegVerse-Labs/.github:docs/CANONICAL_MASTER_RECORDS_STATE_TRANSITION_CUSTODY_MIRROR_HANDOFF.md`

### 3. Transition admission is not equivalent to public-law prior approval

Interlock/InTr is a technical state-transition authority in StegVerse. Paragraph 204 concerns prior approval for high-risk systems before provision or deployment. A technical admission decision may support an implementation of a broader approval regime, but it is not itself evidence of statutory authorization or oversight-body approval.

### 4. Rights-impact reasoning remains an explicit gap

Current required-evidence semantics can prove whether declared evidence was retained, validated and reconstructed. They do not establish that the evidence set included a substantive human-rights impact assessment, affected-person participation, proportionality analysis, legally relevant protected interests, or actor-specific due diligence.

A future architecture candidate would need to preserve, at minimum:

`purpose -> affected subjects/groups -> protected-interest classes -> anticipated impact -> uncertainty -> evidence inputs -> mitigation options -> governance predicates -> decision -> observed consequence -> challenge/remedy path`

This is an architectural gap statement, not a recommendation that any particular legal or political standard be adopted.

### 5. Human involvement needs separable evidence predicates

The Committee's ¶218 recommendation makes the distinction especially clear: the presence of a human is not itself proof of meaningful intervention. A StegVerse evidence model should therefore avoid collapsing these states:

`HUMAN_PRESENT != HUMAN_AUTHORITY_VALID != HUMAN_SUFFICIENTLY_INFORMED != HUMAN_INDEPENDENCE_ESTABLISHED != HUMAN_DECISION_EFFECTIVE`

This comparison does not claim those predicates are required by law for StegVerse; it records the gap between current canonical evidence semantics and the Committee's recommended safeguard.

## Current evidence classification

- JCHR report authenticity/source: **PRIMARY PUBLIC SOURCE RETAINED**
- StegVerse separation-of-powers source architecture: **CANONICAL SOURCE PRESENT**
- Canonical Master Records transition-custody source: **SOURCE ADOPTION PRESENT; AUTHENTIC RUNTIME SEQUENCE STILL SEPARATELY PENDING IN ITS OWN GOAL**
- UK applicability: **NOT ASSESSED**
- UK compliance: **NOT ASSESSED**
- Parliamentary/Committee endorsement of StegVerse: **NOT CLAIMED**
- Policy-quality judgment: **NOT MADE**
- Runtime proof of JCHR-aligned controls: **NOT ESTABLISHED**
- Finding promotion: **NOT AUTHORIZED**
- Publication promotion: **NOT AUTHORIZED**

## Required next evidence before any stronger finding

1. Independent review of this source mapping.
2. If a StegVerse-specific legal-applicability question is later opened, treat it as a separate legal/technical applicability goal.
3. If implementation is later requested for any identified gap, derive a separate canonical remediation/design task from the relevant existing architecture owner rather than silently expanding this ERL evidence task.
4. Preserve future changes to the Committee report response, any resulting legislation, regulations or government response as appended dated evidence rather than overwriting this 14 September 2026 report snapshot.
