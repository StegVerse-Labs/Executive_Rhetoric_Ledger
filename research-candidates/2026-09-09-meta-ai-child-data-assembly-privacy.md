# ERL Research Candidate — Meta AI Child-Data Assembly / Privacy

Record ID: `ERL-2026-09-09-META-AI-CHILD-DATA-ASSEMBLY-001`

## Status

- lifecycle: `research_candidate`
- captured_at: `2026-09-09T21:14:00-05:00`
- source_class: `user-supplied LinkedIn screenshots plus user-supplied LinkedIn short link`
- publication_finding_authorized: `false`
- legal_liability_finding_authorized: `false`
- platform-retention-mechanism_proven: `false`

## Source

User-supplied source link:
`https://lnkd.in/p/gTpUgFZW`

The current session also supplied six LinkedIn screenshots showing discussion around a video/post concerning AI-assisted correlation of family photographs, identity, relationships, historical information, and location-related information. The short LinkedIn URL was not fetchable through the current public web retrieval path, so this record is bounded to what is visible in the supplied captures and does not treat unseen source material as verified.

## Observable claims in the supplied material

The screenshots visibly contain discussion asserting that:

1. removing or deleting a photograph from a social profile may not guarantee that all derived, indexed, copied, cached, or otherwise retained representations disappear;
2. AI systems can increase privacy risk by joining information from multiple posts, accounts, people, and time periods;
3. children create a distinct consent and asymmetry problem because they generally cannot meaningfully consent to long-term data profiling created for them by adults or third parties;
4. the privacy risk is not limited to possession of an individual object, but extends to relationship discovery and inference across many individually innocuous objects;
5. commenters characterize these concerns in terms of data minimization, transparency, accountability, surveillance, and ownership/control of personal data.

These are captured as source claims and observations, not accepted findings about Meta's internal systems.

## Key evidentiary distinction

The strongest defensible proposition supported by the supplied material is not that a specific platform intentionally preserved a deleted photograph. The record instead captures a narrower and more general problem:

> deletion of an originating object does not necessarily prove deletion of every copy, index, embedding, derived feature, relationship edge, cache, model-accessible representation, or independently sourced copy that can later contribute to an inference.

The specific persistence mechanism in the underlying incident remains unproven from the supplied screenshots alone.

## StegVerse relevance

This candidate is directly relevant to KnowledgeVault, governed AI access, and digital-data ownership.

StegVerse's differentiating privacy boundary is not merely whether a person can store or delete an object. It is whether another system has authority to correlate that object with other objects and derive new information from the combination.

A useful governance concept for this class of problem is `Derived Data Authority`:

`May actor/system A combine data objects X + Y + Z to derive inference Q, for purpose P, for requester R, at time T?`

Under this model, possession or technical readability of X, Y, and Z does not automatically confer authority to derive Q.

KnowledgeVault therefore has a stronger ownership role than conventional cloud storage when paired with StegVerse governance: it can preserve user-custodied source objects while Interlock/InTr or another governed transition layer can separately control access, correlation, derivation, export, and downstream use.

## Ownership model suggested by this case

A stronger digital-ownership model distinguishes at least five rights:

- custody: who physically/logically holds the source object;
- access: who may read the source object;
- correlation: who may join it with other objects;
- derivation: who may create inferred attributes or relationship graphs from it;
- propagation: who may publish, replicate, sell, train on, or otherwise distribute the source or derived artifact.

Deletion should be represented as a governed lifecycle event with receipts and downstream revocation/tombstone propagation where technically possible, rather than being treated as evidence that every external copy or inference has disappeared.

## Research questions

1. What exact source behavior did the underlying video demonstrate, and can the original video/post be independently captured and preserved?
2. Was the allegedly deleted image still present in platform storage, independently reposted, cached, indexed, embedded, or reproduced from another source?
3. What current Meta policies and technical controls apply to deletion, retention, AI personalization, face/identity inference, child data, and model training/use?
4. Which derived representations can survive deletion of a source object, and under what retention or legal basis?
5. What regulatory duties apply to deletion, access, purpose limitation, data minimization, children's data, and inferred data in relevant jurisdictions?
6. How should StegVerse express source-object deletion, derived-data revocation, and correlation authority as machine-verifiable receipts?

## Required next evidence

- original LinkedIn video/post capture or stable source URL;
- first-party platform policies and deletion/retention documentation current to the event date;
- any first-party statements addressing the incident;
- applicable regulator/court records where directly relevant;
- technical evidence sufficient to discriminate storage retention from independent reposting, indexing, caching, embeddings, or other derived representations.

## Assessment boundary

This record supports a `privacy-and-derived-data-governance research candidate` classification. It does not establish unlawful conduct, intentional retention of a specific deleted image, a particular model-training path, or a specific internal Meta architecture.
