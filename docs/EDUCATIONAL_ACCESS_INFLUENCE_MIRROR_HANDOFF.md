# Educational Access Influence Network MIRROR_HANDOFF

## Authority

Bounded source of truth for the 2026-09-03/04 ERL research lane examining possible cross-front influence across:

1. youth-AI restriction / cognitive-harm messaging;
2. data-center opposition / infrastructure-access restriction;
3. public-education restructuring / voucher, curriculum/book, staffing, and institutional-capacity policy.

Repository-wide continuity remains governed by `ERL_MIRROR_HANDOFF.md`.
Research-candidate activation remains governed by `docs/RESEARCH_CANDIDATE_ACTIVATION_MIRROR_HANDOFF.md`.

Canonical owner: Issue `#121`.
Goal ID: `ERL-EDUCATIONAL-ACCESS-INFLUENCE-001`.
Branch: `main`.

## Current posture

State: `RESEARCH_ACTIVE / SOURCE_ACQUISITION_PENDING`.

This handoff does not authorize a factual finding that the three fronts are coordinated, share a common ultimate motive, or intentionally reduce education. It does preserve the stronger, testable proposition that each front contains organized actors attempting to influence policy and that cross-front overlap in funders, people, lobbyists, consultants, political recipients, or messaging infrastructure should be reconstructed from primary records.

Candidate-layer finding authorized: `false`.
Publication authorized: `false`.
Motive finding authorized: `false`.

## Research graph

Required provenance path:

`person -> wealth/company -> foundation/DAF/PAC -> advocacy organization -> lobbyist/consultant -> candidate/lawmaker -> bill/order/moratorium -> policy outcome`

Each edge must preserve:

- source URL or primary-record locator;
- source class;
- date;
- amount where financial;
- direct vs intermediary relationship;
- stated grant/lobbying/campaign purpose;
- disclosure status;
- confidence/state: observed, inferred, disputed, unresolved;
- correction/contradiction records.

## Workstreams

### WS-A — Youth AI

Acquire and normalize:

- organizations advocating bans, moratoria, age restrictions, controlled-access regimes, or child-AI regulation;
- funders, corporate participants, lobbyists, PR firms, coalition membership, and political recipients;
- social-media and advertising provenance for child-cognition messaging;
- cited scientific evidence for cognitive offloading, cognitive degradation, dependency, learning outcomes, and developmental claims;
- contrary or corrective evidence and whether campaigners had access to it.

Required discriminator: distinguish ordinary information/cognitive offloading from demonstrated developmental impairment.

### WS-B — Data centers

Acquire and normalize:

- national and local organizations supplying towns/residents with toolkits, legal aid, lobbying, candidate endorsements, model ordinances, or moratorium language;
- funders and donor-advised/community-foundation intermediaries;
- originating donors where publicly traceable;
- consultant, law-firm, PR, polling, and political-campaign relationships;
- claims about water, power, pollution, tax treatment, employment, grid cost, and public benefit;
- resulting ordinances, utility proceedings, litigation, state bills, and federal legislation.

Required discriminator: separate technically supportable impact claims from categorical, materially incomplete, or misleading claims.

### WS-C — Public education restructuring

Acquire and normalize:

- voucher/private-school funding networks;
- PACs, lobbyists, model-legislation organizations, and political donors;
- Department of Education restructuring/closure advocacy;
- curriculum and book restriction campaigns;
- religious-display/education policy;
- teacher/staff qualification changes and institutional-capacity reductions;
- public-fund transfers to private institutions and the accountability rules attached to those funds.

Required discriminator: distinguish parental-choice arguments from actual changes in public accountability, access, staffing, curriculum, and public-system capacity.

## Cross-front hypotheses

The research must test, not assume:

1. independent convergence;
2. narrative propagation without formal coordination;
3. aligned but independent interests;
4. common funders/intermediaries;
5. common lobbyists/consultants/PR/polling firms;
6. coordinated advocacy;
7. deliberate youth-first sequencing;
8. downstream organic repetition of institutionally seeded claims;
9. coordinated educational/epistemic access restriction.

## Evidence-integrity rules

- Paid lobbying or explicit campaign activity is evidence of intent to influence the named policy outcome; it is not by itself proof of an unstated ultimate motive.
- Deliberate omission of material facts, misrepresentation, or knowingly misleading use of facts is dishonest when knowledge/deliberateness is supported by evidence.
- Public-money/private-education analysis must separately measure regulation, auditability, admissions, curriculum, staffing, reporting, civil-rights obligations, and public accountability.
- Historical civil-rights comparisons may be used only as structural access-control analogies unless stronger evidence warrants more.
- Secondary-source claims do not establish donor origin, coordination, or motive without primary/official corroboration.

## Installed in this session

- Durable owner: `StegVerse-Labs/Executive_Rhetoric_Ledger#121`.
- This bounded mirror handoff: `docs/EDUCATIONAL_ACCESS_INFLUENCE_MIRROR_HANDOFF.md`.

## Remaining files/modules to install

Destination: `StegVerse-Labs/Executive_Rhetoric_Ledger`

1. `research-candidates/2026-09-04-educational-access-influence-network.md`
   - Must be created in the same repository change that adds its activation-registry entry.
2. `coordination/research-candidate-activation-registry.v1.json`
   - Add `ERL-RC-EDUCATIONAL-ACCESS-INFLUENCE-2026`, durable owner `issue:121`, next executable task, terminal condition, and candidate/publication authorization false.
3. `assessments/intake/2026-09-04-educational-access-influence-primary-record-intake.json`
   - Three-lane source queue with provenance state.
4. `assessments/evidence/2026-09-04-educational-access-influence-money-graph.json`
   - Person/funder/intermediary/recipient/political-recipient edges.
5. `assessments/evidence/2026-09-04-educational-access-influence-claim-provenance.json`
   - Claim -> source -> cited evidence -> correction/contradiction -> campaign use.
6. `assessments/contradictions/2026-09-04-educational-access-influence.matrix.md`
   - Supporting, contrary, null, and unresolved evidence by proposition.
7. `assessments/reviews/2026-09-04-educational-access-influence.review.md`
   - Independent review before any publication or coordination/motive finding.

## Next executable machine task

Create the candidate and activation-registry entry atomically, then install the three-lane primary-record intake queue. Do not create an unregistered `research-candidates/` file because repository validation fails closed on missing activation coverage.

## Release / propagation

No raw candidate propagation is authorized to `StegVerse-Labs/Site`, `GCAT-BCAT-Engine/Publisher`, `admissibility-wiki`, or `stegguardian-wiki`.

If the lane later reaches reviewed publication state, create a separate verification task to ensure any pertinent released information is updated/applied to those destinations.

## Completion accounting

- durable ownership: 1/1 = 100%
- bounded handoff: 1/1 = 100%
- candidate + registry admission: 0/1 = 0%
- primary-record intake: 0/1 = 0%
- money/person influence graph: 0/1 = 0%
- claim-provenance graph: 0/1 = 0%
- contradiction matrix: 0/1 = 0%
- independent review: 0/1 = 0%

Developed deliverables: 2/7 conceptual deliverable groups installed if counting owner + handoff; no research finding is activated or publication-authorized.

## Archive condition

Not yet satisfied for this bounded research lane. Issue #121 and this handoff preserve all unique session requirements needed to continue without chat-history dependence, but the candidate/registry admission and evidence artifacts remain machine-execution work.
