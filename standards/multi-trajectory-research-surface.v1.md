# ERL Multi-Trajectory Research Surface Standard v1

Status: active implementation standard
Authority: StegVerse-Labs/Executive_Rhetoric_Ledger
Canonical task: Issue #60

## Purpose

Define the common research structure for repositories that preserve information about a person, institution, administration, event, incident, decision, or closely related evidence domain under ERL evaluation authority.

The structure is not binary. Research must explore **all currently plausible trajectories** and must add new trajectories when incoming evidence reveals them.

## Authority split

ERL owns:
- research-frontier definition;
- trajectory enumeration and expansion;
- proposition and edge identifiers;
- evidence posture and custody requirements;
- graph enrichment;
- contradiction review;
- hypothesis movement;
- final reviewed projection/evaluation authority.

Subject/domain repositories may own:
- public-source discovery;
- source whitelists;
- native ingest;
- source lead preservation;
- domain-specific graph context;
- acquisition receipts;
- candidate export to ERL.

A subject/domain repository MUST NOT independently promote factual truth, culpability, causation, coordination, motive, or legal conclusions merely because its search finds a source.

## Required local research surface

Every conforming repository must contain:
1. `RESEARCH_MIRROR_HANDOFF.md` or another canonical `*_MIRROR_HANDOFF.md` that explicitly owns the research surface.
2. `research/README.md` describing scope and ERL authority boundary.
3. `research/frontier.json` containing active trajectories and acquisition gaps.
4. `research/acquisition_requests.jsonl` append-only ERL/domain acquisition requests.
5. `research/source_candidates.jsonl` append-only discovered source candidates.
6. `research/research_receipts.jsonl` append-only acquisition/search receipts.
7. `data/sources/sources_whitelist.csv` or an explicit governed equivalent.
8. `scripts/search_agent.py` or an equivalent executable discovery adapter.

## Frontier semantics

Each frontier trajectory must support:
- trajectory_id;
- title;
- state: OPEN, ACTIVE, BLOCKED, SATURATED, SUPERSEDED, MERGED;
- known_nodes;
- known_edges;
- unsupported_edges;
- expected_signatures;
- disconfirmers;
- source_classes;
- priority;
- acquisition_queries;
- expansion_conditions;
- stop_conditions;
- parent_trajectory_id when derived from incoming evidence.

Research must include causal, institutional, temporal, rhetorical, legal, scientific, logistical, null, mixed, and newly discovered trajectories where relevant. There is no privileged originating hypothesis.

## Candidate packet minimum

Every discovered candidate must preserve:
- candidate_id;
- repository;
- trajectory_ids;
- acquisition_request_id;
- query or discovery terms;
- source URL;
- source title if known;
- retrieval timestamp;
- source class;
- authority/proximity if known, otherwise `unknown`;
- content hash when bytes are captured;
- custody pointer or local path when available;
- verification state;
- evidence role: `lead-only` or `context-only` until ERL review;
- discovered_by;
- notes.

## Search behavior

A research adapter must:
- search every ACTIVE trajectory with unresolved acquisition gaps;
- never rank a source higher merely because it agrees with a trajectory;
- preserve contradictory and null-result evidence;
- create new trajectory candidates when evidence reveals a materially distinct explanation;
- deduplicate by normalized source identity/hash;
- append receipts rather than silently rewriting history;
- fail closed when source provenance is unavailable for a requested verified capture.

## Recurring-search necessity threshold

A repository does **not** require recurring OSINT merely because it is a research repository. Recurring acquisition becomes a required part of the research surface when the subject is materially dynamic and a one-time search cannot preserve current evidentiary state.

### Hard triggers

Recurring search is REQUIRED when **any one** of the following is true:
1. The repository tracks an ACTIVE/OPEN trajectory whose expected evidence can appear after the current research run (for example hearings, filings, appointments, statements, investigations, releases, litigation, agency actions, deaths, records disclosures, or policy changes).
2. The repository has an explicit freshness/current-state claim that would become misleading without periodic source checking.
3. The repository has a machine-owned observer, monitor, watch, scheduled ingest/search, or dependency-release condition whose purpose is source/evidence discovery rather than merely CI validation.
4. The research frontier contains a time-dependent gap with a defined future source class or event trigger.
5. The repository publishes or exports a current-state projection consumed by ERL or another governed surface and new public evidence could materially change that projection.

### Soft triggers

Recurring search SHOULD be installed when **two or more** of the following are true:
- the subject is a living person or active institution/administration;
- the subject has repeated public acts or statements relevant to the repository scope;
- new primary records are released irregularly;
- unresolved trajectories depend on external developments;
- the source set changes materially over time;
- the repository already performs recurring ingest of external source records;
- the cost of missing a new record is greater than the cost/noise of periodic checking;
- the repository has more than one ACTIVE trajectory with unresolved acquisition requests.

### Recurrence not required

Recurring search is normally NOT required when all evidence is closed/historical, all trajectories are SATURATED/SUPERSEDED/MERGED, the repository is only a reviewed publication/consumer surface, or its inputs are entirely supplied by another canonical acquisition owner.

### Cadence selection

Cadence must follow evidence volatility rather than repository importance:
- **hourly/daily:** rapidly changing active events, hearings, litigation actions, crisis/public-safety events, official announcement streams, or explicit condition watches;
- **daily/weekly:** active public figures, administrations, policy programs, recurring releases, investigations, or unresolved current-state propositions;
- **weekly/monthly:** slowly changing biography/institutional histories where new records appear irregularly;
- **event-driven only:** when an authoritative upstream system emits deterministic source-change signals.

The recurrence decision must be stored in the repository handoff or research registry as one of `REQUIRED`, `SHOULD`, `NOT_REQUIRED`, or `DELEGATED`, together with the trigger(s), cadence, owner, and release condition.

## Credential and execution authority

No GitHub token is research, evaluation, or evidentiary authority. TV/TVC governs applicable credentialing. Repository automation may transport, validate, and persist declared artifacts only within its stated authority boundary.

## ERL integration

Local repositories export discovered candidates to ERL as pending/context-only records. ERL validates custody, links candidates to graph nodes/edges, updates trajectory movement as `strengthen`, `weaken`, `disambiguate`, `contextualize`, or `no-update`, and may create additional trajectories. Only reviewed ERL projections may flow back as governed current-state evaluation material.

## Conformance target

A repository is conforming when a reviewer can reproduce:
1. which trajectories were active;
2. which acquisition requests were generated;
3. which sources were searched and found;
4. which candidates were emitted;
5. which evidence was contradictory or null;
6. which new trajectories were created;
7. why no local search result independently changed an ERL conclusion;
8. why recurring search is or is not required, and who owns it if delegated.
