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
7. `research/conformance.json` machine-readable declaration of authority, recurrence posture, adapter, transport boundary, and validation state.
8. `data/sources/sources_whitelist.csv` or an explicit governed equivalent.
9. `scripts/search_agent.py` or an equivalent executable discovery adapter.

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
- search every ACTIVE trajectory with unresolved acquisition gaps that it actually owns under the recurrence/dispatch contract;
- never rank a source higher merely because it agrees with a trajectory;
- preserve potentially supporting, contrary, contextual, and null-result candidate evidence without local conclusion promotion;
- deduplicate by normalized source identity/hash while preserving acquisition provenance;
- append receipts rather than silently rewriting history;
- fail closed when source provenance is unavailable for a requested verified capture.

A subject/domain acquisition adapter does **not** create or promote an authoritative new trajectory on its own. When a candidate appears to reveal a materially distinct explanation, the adapter preserves the candidate and relevant acquisition context. ERL review then decides whether to create a new trajectory through the reviewed evidence-movement/frontier engine. This keeps new-trajectory discovery open without transferring evaluation authority to the acquisition surface.

## Recurring-search necessity threshold

Recurring research is attached to trajectories/evidence gaps, not merely to repository identity.

A trajectory MUST be classified `REQUIRED` when any hard trigger is true:
- it is OPEN/ACTIVE and relevant evidence can emerge after the current observation time;
- the repository or ERL publishes a current-state/freshness claim dependent on new evidence;
- an existing evidence observer/monitor already owns unresolved acquisition work;
- an unresolved gap depends on a future filing, hearing, investigation, release, litigation event, policy action, public statement, or other externally observable change;
- a reviewed projection can materially change when new evidence appears.

A trajectory SHOULD normally be classified `SHOULD` when two or more soft triggers are true:
- the subject/institution remains active;
- relevant public conduct recurs;
- primary records are released irregularly;
- a trajectory depends on external events not controlled by the repository;
- the relevant source set changes over time;
- recurring external ingest already exists;
- missing new evidence would materially degrade the research state;
- multiple unresolved trajectories depend on the same changing source domain.

Allowed recurrence classifications are:
- `REQUIRED` — recurring acquisition is necessary to maintain a truthful research state;
- `SHOULD` — recurring acquisition is structurally useful but not currently mandatory;
- `NOT_REQUIRED` — evidence is closed/historical/saturated or the repository is consumer-only;
- `DELEGATED` — another named canonical acquisition surface owns recurrence.

Cadence is determined by evidence volatility, not perceived importance:
- hourly/daily for rapidly changing events;
- daily/weekly for active policy, public figures, investigations, litigation, or current-state claims;
- weekly/monthly for slowly evolving archival/biographical records;
- event-driven when an authoritative system emits a deterministic change signal.

Every recurring trajectory must declare a cadence, owner, observable trigger, stop/saturation condition, and receipt location. A repository schedule that merely reimports static seeds is transport/ingest, not automatically a recurring research monitor.

For a repository-level `DELEGATED` posture, automatic frontier recurrence MUST be suppressed unless an individual trajectory explicitly overrides delegation under the ERL contract. Explicit acquisition requests from ERL remain executable. This prevents umbrella repositories from duplicating subject-owned recurrence while preserving directed research capability.

## Machine-readable conformance profile

Every in-scope repository must keep `research/conformance.json` synchronized with its canonical handoff and the ERL registry. At minimum it records:
- repository and role;
- canonical ERL owner/issue;
- evaluation authority;
- acquisition authority;
- local adapter path;
- recurrence classification and owner;
- whether an existing scheduled ingest is `research`, `transport`, `mixed`, or `none`;
- candidate posture (`lead-only`/`context-only` until ERL review);
- native-record mutation permission (normally false for the ERL sidecar);
- GitHub-token authority (`NONE`);
- TV/TVC credential authority where applicable;
- validation state and next executable validation action.

A repository is not on the same governed research plane merely because matching files exist. Its conformance profile, handoff, and ERL registry entry must agree.

## Credential and execution authority

No GitHub token is research, evaluation, or evidentiary authority. TV/TVC governs applicable credentialing. Repository automation may transport, validate, and persist declared artifacts only within its stated authority boundary.

## ERL integration

Local repositories export discovered candidates to ERL as pending/context-only records. ERL validates custody, links candidates to graph nodes/edges, updates trajectory movement as `strengthen`, `weaken`, `disambiguate`, `contextualize`, or `no-update`, and may create additional trajectories. Only reviewed ERL projections may flow back as governed current-state evaluation material.

## Conformance target

A repository is conforming when a reviewer can reproduce:
1. which trajectories were active and which recurrence owner was responsible;
2. which acquisition requests were generated or explicitly dispatched;
3. which sources were searched and found;
4. which candidates were emitted;
5. which potentially supporting, contrary, contextual, or null-result evidence was preserved without local conclusion promotion;
6. how candidate evidence reaches ERL review and, when warranted, creates a new trajectory only through the reviewed ERL movement/frontier path;
7. why no local search result independently changed an ERL conclusion;
8. who owns recurrence and whether scheduled ingest is research or transport.
