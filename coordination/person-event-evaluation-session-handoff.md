# Person/Event Evaluation Normalization Handoff

## Goal

Make ERL's current-state/DPOI evaluation method the canonical evaluation structure for repositories and Site clusters centered on people, institutions, events, incidents, or decisions; require append-only evidence movement after newly acquired reviewed data; and project the Fauci case publicly through a Site cluster with a visible Evidence Update Ledger.

## Canonical continuation

- ERL standard: `standards/person-event-current-state-evaluation.v1.md`
- ERL registry: `coordination/person-event-evaluation-registry.v1.json`
- ERL rollout: `docs/PERSON_EVENT_EVALUATION_ROLLOUT.v1.md`
- ERL validator/workflow: `scripts/validate_person_event_evaluation_registry_v1.py`, `.github/workflows/validate-person-event-evaluation-registry-v1.yml`
- Trumpality consumer: `contracts/executive-rhetoric-ledger-reviewed-projection.contract.yml`
- Trumpality Evidence Movement Ledger: `data/receipts/ledger_evidence_updates.jsonl`
- Trumpality current-state index: `data/receipts/ledger_current_state_evaluation.json`
- Site Fauci candidate workload: `StegVerse-Labs/Site#235`
- Fauci evidence owner: ERL Issue #47 / PR #48

## State

- ERL evaluation standard: COMPLETE.
- Machine conformance registry: COMPLETE.
- Registry validator/workflow: IMPLEMENTED; hosted run must be observed before claiming validator activation complete.
- Trumpality baseline evaluation ledger/index: COMPLETE.
- Trumpality validator/workflow: IMPLEMENTED; hosted run must be observed before claiming validator activation complete.
- Site Fauci cluster: PENDING_ADMISSION by Site repository orchestrator; no external ownership asserted.
- Other direct person-specific ERL consumers found in current connected-repository inspection: none beyond Trumpality.

## New-data requirement

Relevant newly acquired and reviewed evidence must append a proposition-relative movement (`strengthen`, `weaken`, `disambiguate`, `contextualize`, `no-update`) before or with a current-state update. Zero-result discovery remains `no-update` absent independent coverage-completeness evidence.

## Authority

ERL owns evaluation semantics. Subject repositories are governed consumers. Site is public projection. No import, candidate discovery, cluster rendering, or ledger append grants factual truth, culpability, causation, coordination, motive, publication, or execution authority by itself.

## Site release condition

Issue #235 becomes implementable only when Site's repository orchestrator admits it and assigns a repository-native owner without colliding with the active sequence. Public completion additionally requires Site validation and deployed-route verification.
