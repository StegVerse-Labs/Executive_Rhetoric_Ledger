# Research Candidate: AI Integration Reservation Split

## Candidate Metadata

```yaml
candidate_id: "RC-2026-AI-INTEGRATION-RESERVATION-SPLIT"
topic_name: "AI Integration Reservation Split Across Fact, Religion, Conviction, Trust, and Risk Tolerance"
entry_status: "draft-research-candidate"
created_date: "2026-06-17"
last_reviewed: "2026-06-17"
reviewer: "StegVerse-Labs"
related_entry: "trees/modern-topics/2026-ai-human-dignity-warning-language.md"
related_standard: "standards/political-influence-tree-standard.md"
classification: "population-attitude-research-candidate"
```

## Purpose

This research candidate establishes a structured inquiry into how deeply the general population is divided on AI integration.

The candidate is intended to determine where the split exists between people with little reservation about AI integration and people with significant reservation.

The inquiry must separate:

- factual beliefs
- religious commitments
- moral conviction
- institutional trust
- personal risk tolerance
- perceived loss of human authority
- perceived economic threat
- perceived spiritual or identity threat
- perceived governance adequacy
- practical exposure to AI tools

This candidate does not assume that reservations about AI are irrational, religious, anti-technology, or uninformed.

This candidate also does not assume that low-reservation adoption is rational, secular, informed, or safe.

## Core Research Question

```text
Where is the split among the general population between low-reservation and high-reservation positions on AI integration, and which parts of that split are best explained by fact claims, religious belief, moral conviction, institutional trust, risk tolerance, lived experience, or perceived consequence exposure?
```

## Secondary Questions

```text
1. What proportion of the population expresses little reservation, moderate reservation, significant reservation, or refusal toward AI integration?
2. Which AI use cases produce the largest shift from acceptance to reservation?
3. Which objections are factual, religious, moral, economic, privacy-based, authority-based, safety-based, or dignity-based?
4. Which factual beliefs are accurate, mistaken, unsupported, or unverified?
5. Which reservations remain even after factual correction?
6. Which reservations increase when AI moves from advisory use to consequential execution?
7. Which populations distinguish between AI assistance, AI delegation, AI replacement, and AI authority?
8. Which populations require human review, consent, reversibility, auditability, or receipt-backed governance before accepting AI integration?
9. Which factors predict low-reservation adoption despite weak governance safeguards?
10. Which factors predict high-reservation refusal even when governance safeguards are present?
```

## Population Segmentation Hypothesis

The likely split is not binary.

A useful starting segmentation is:

```yaml
reservation_segments:
  low_reservation_integrators:
    description: "People who are broadly comfortable with AI integration across many personal, professional, and institutional contexts."
    possible_drivers:
      - productivity benefit
      - technological optimism
      - low perceived spiritual threat
      - high trust in institutions or markets
      - high trust in personal ability to adapt
      - low consequence sensitivity
      - direct positive exposure to AI tools

  conditional_integrators:
    description: "People who accept AI assistance but require human review, consent, auditability, or reversibility before consequential use."
    possible_drivers:
      - practical benefit recognition
      - moderate institutional trust
      - concern about authority delegation
      - desire for evidence and receipts
      - distinction between advice and execution

  domain_specific_resisters:
    description: "People who accept AI in low-stakes contexts but resist AI in care, education, employment, warfare, governance, identity, religion, or family contexts."
    possible_drivers:
      - domain-specific dignity concerns
      - fear of dehumanization
      - profession-specific displacement risk
      - religious or moral boundaries
      - concern over irreversible decisions

  high_reservation_resisters:
    description: "People who view AI integration as dangerous unless strong human, legal, moral, or institutional limits exist first."
    possible_drivers:
      - low institutional trust
      - moral conviction
      - spiritual concern
      - observed technology harms
      - economic vulnerability
      - privacy and surveillance concern
      - fear of human replacement
      - concern over autonomous consequence

  refusal_or_prohibition_position:
    description: "People who reject certain forms of AI integration categorically, regardless of safeguards."
    possible_drivers:
      - theological prohibition
      - non-negotiable human dignity boundary
      - existential-risk belief
      - labor or social-order defense
      - trauma or direct harm from automated systems
```

## Axis Model

The research should not classify people by simple pro-AI or anti-AI labels.

Each respondent or source should be mapped across these axes:

```yaml
axes:
  factual_belief:
    scale: "accurate | partially accurate | unsupported | false | unknown"
    question: "What does the person believe AI can or cannot do?"

  religious_or_spiritual_basis:
    scale: "none | implicit | explicit | primary"
    question: "Is the reservation grounded in religious or spiritual belief?"

  moral_conviction:
    scale: "low | moderate | high | categorical"
    question: "Is the position held as a non-negotiable moral boundary?"

  institutional_trust:
    scale: "low | moderate | high | fragmented"
    question: "Does the person trust companies, governments, churches, schools, courts, or regulators to govern AI?"

  consequence_sensitivity:
    scale: "low | moderate | high | irreversible-boundary"
    question: "How much does the person distinguish between low-stakes assistance and high-stakes execution?"

  authority_delegation_tolerance:
    scale: "none | advisory-only | supervised-delegation | autonomous-delegation"
    question: "What level of decision authority may AI hold?"

  reversibility_requirement:
    scale: "none | preferred | required | categorical"
    question: "Must AI-mediated decisions be reversible?"

  receipt_requirement:
    scale: "none | preferred | required | categorical"
    question: "Must AI-mediated consequence produce audit receipts?"

  identity_or_dignity_threat:
    scale: "none | low | moderate | high | existential"
    question: "Does the person see AI integration as threatening personhood, dignity, work identity, family role, or spiritual meaning?"

  exposure_level:
    scale: "none | indirect | casual | professional | dependent"
    question: "How much has the person actually used or been affected by AI?"
```

## Fact / Religion / Conviction Separation

The core separation rule:

```text
A reservation must not be treated as factual merely because it is sincerely held.
A religious objection must not be treated as irrational merely because it is religious.
A moral conviction must not be treated as a fact claim merely because it is expressed in factual language.
A factual error must not be treated as the entire cause of reservation if a deeper dignity or authority concern remains after correction.
```

## Example Coding Table

```yaml
example_codes:
  claim_ai_will_replace_all_human_workers:
    category: "factual_belief"
    verification_needed: true
    possible_posture: "overbroad-or-unsupported-with-real-sector-specific-risk"

  claim_ai_should_not_make_life_or_death_decisions:
    category: "moral_conviction / authority_delegation_boundary"
    verification_needed: false
    governance_relevance: "high"

  claim_ai_is_spiritually_dangerous:
    category: "religious_or_spiritual_basis"
    verification_needed: "not fact-verifiable as stated"
    governance_relevance: "important for consent, adoption, refusal boundaries, and institutional trust"

  claim_ai_companies_cannot_be_trusted:
    category: "institutional_trust"
    verification_needed: true
    governance_relevance: "high"

  claim_ai_is_useful_for drafting low-stakes text:
    category: "use-case-specific-acceptance"
    verification_needed: "contextual"
    governance_relevance: "moderate"

  claim_ai_should_not bind legal, medical, employment, military, or family consequence without human review:
    category: "consequence_sensitivity / commit-time-governance"
    verification_needed: false
    governance_relevance: "very-high"
```

## Research Design Candidate

A complete research program should include:

```yaml
research_methods:
  survey:
    purpose: "Estimate population distribution across reservation segments and axis scores."
    sample_requirement: "Demographically representative sample by age, geography, education, income, religion, occupation, political identity, AI exposure, and employment displacement risk."

  structured_interviews:
    purpose: "Distinguish factual belief from religious basis, conviction, trust, and consequence sensitivity."
    sample_requirement: "Oversample high-reservation, low-reservation, religious, technical, caregiver, educator, military, medical, legal, and low-income participants."

  vignette_testing:
    purpose: "Measure how acceptance changes by use case and consequence level."
    examples:
      - "AI drafts a grocery list."
      - "AI tutors a child."
      - "AI recommends medical triage."
      - "AI denies benefits."
      - "AI screens job candidates."
      - "AI predicts criminal risk."
      - "AI authorizes a weapons action."
      - "AI generates a pastoral, legal, medical, or therapeutic response."

  factual_correction_test:
    purpose: "Determine which reservations change after factual clarification and which remain as conviction or authority boundaries."

  governance_safeguard_test:
    purpose: "Determine whether consent, human review, audit receipts, reversibility, liability, and commit-time admissibility reduce reservation."
```

## StegVerse Relevance

This candidate directly supports StegVerse because it tests whether public AI reservation is primarily about:

- misunderstanding AI capability
- distrust of institutions
- fear of displacement
- religious objection
- moral conviction
- unwillingness to delegate human authority
- lack of consent
- lack of receipts
- lack of reversibility
- lack of admissibility at the moment of consequence

The most important StegVerse distinction is likely this:

```text
Many people may accept AI assistance while rejecting AI authority.
```

That split matters because StegVerse does not need to prove that everyone wants or rejects AI.

It needs to determine where people require an admissibility boundary before AI-mediated consequence can bind.

## Relation to AI Human Dignity Warning Language Entry

The related entry records the public-warning convergence around AI, human dignity, and moral authority.

This research candidate converts that rhetorical marker into a measurable research question:

```text
How many people hear AI warning language as fact, religion, conviction, distrust, risk management, dignity defense, or governance demand?
```

## Non-Claims

This research candidate does not claim:

- that the general population is already split in a known proportion
- that religious objections are inherently anti-AI
- that low-reservation users are more rational or better informed
- that high-reservation users are more moral or more informed
- that factual correction will resolve AI reservations
- that governance safeguards will satisfy all objections
- that AI integration should proceed in every domain
- that AI integration should be blocked in every domain

## Initial Done Criteria

This research candidate is minimally established when:

- [x] the population split question is stated
- [x] fact, religion, conviction, trust, risk, and consequence sensitivity are separated
- [x] low-reservation and high-reservation segments are not treated as simplistic pro/anti groups
- [x] a measurement axis model exists
- [x] a research design candidate exists
- [x] the relationship to the AI human dignity warning-language entry is explicit
- [x] non-claims prevent overreach

## Next Build Steps

- Add a survey instrument draft.
- Add a structured interview guide.
- Add a vignette battery for consequence-level testing.
- Add a coding schema for responses.
- Add a machine-readable candidate manifest.
- Add source receipts from current polling, survey literature, and public AI-attitude research.
