# SKAP-Seeded Account Disclosure Graph

StegVerse Digital Data Reclamation must not discover personal exposure only by checking known data-harvesting sites. It must also begin from the user's own known account topology.

For every authorized SKAP account, the reclamation system should identify the account provider and maintain an evidence-bounded graph of organizations to which that provider is known, reported, observed, or suspected to disclose, sell, share, process, subprocess, affiliate, index, or otherwise expose customer data.

The discovery expansion becomes:

`SKAP account -> account provider -> declared/observed downstream organizations -> additional downstream recipients -> public/search/broker surfaces`

This graph is a discovery-priority graph, not proof that a particular user's records were transferred on every edge. Edge evidence state is therefore mandatory. `DECLARED_BY_PROVIDER`, `OBSERVED_TRANSFER`, and `REGULATORY_OR_COURT_RECORD` can support stronger follow-up than `INFERRED_UNVERIFIED` or `UNKNOWN`.

A provider privacy policy, subprocessor list, sale/share disclosure, regulator record, court record, user export, or authentic network/provider receipt can establish a candidate downstream relationship. It cannot by itself prove that a specific datum for a specific user traversed that edge unless evidence supports that narrower claim.

This prevents two opposite failures: missing likely downstream copies because StegVerse only searches known brokers, and overclaiming that every listed provider relationship contains the user's data.

KnowledgeVault should retain the subject's SKAP-linked account inventory, the disclosure graph, evidence references, verification timestamps, and reclamation state. Interlock/InTr remains the transition authority for governed execution; graph membership is discovery context, not permission to act.
