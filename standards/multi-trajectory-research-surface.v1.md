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
7. why no local search result independently changed an ERL conclusion.
