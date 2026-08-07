# Person/Event Evaluation Rollout v1

## Canonical rule

Any StegVerse repository whose primary purpose is preserving information about a person, institution, event, incident, or decision must either conform to `standards/person-event-current-state-evaluation.v1.md` or carry an explicit reviewed exemption with equivalent controls.

## Current inventory

### StegVerse-Labs/Executive_Rhetoric_Ledger
Role: canonical evaluation authority and producer of reviewed DPOI/current-state movements.
State: CONFORMING / authority owner.
Canonical registry: `coordination/person-event-evaluation-registry.v1.json`.
Validator: `scripts/validate_person_event_evaluation_registry_v1.py`.
Hosted validation: `.github/workflows/validate-person-event-evaluation-registry-v1.yml`.

### StegVerse-Labs/Trumpality
Role: person-specific governed consumer.
State: CONFORMING.
Evidence: contract v2 plus append-only Evidence Movement Ledger, current-state index, validator, workflow, and updated handoff.

### StegVerse-Labs/Site — Fauci / July 29 2026 HSGAC cluster
Role: public human-readable projection.
State: PENDING_ADMISSION.
Candidate task: Site issue #235.
Blocker: Site orchestration currently disallows external task ownership; the workload must be admitted repository-natively.
Required public projection: Overview / Current State, Evidence, DPOIs, Chronology & Authority, Analysis, Evidence Gaps, Method, and a near-bottom Evidence Update Ledger on the cluster home page.

## Discovery of additional subject repositories

Current connected-repository inspection found Trumpality as the direct person-specific ERL consumer. No other repository was observed with the same reviewed-person projection contract at this time. Newly created or discovered person/event repositories must be added to `coordination/person-event-evaluation-registry.v1.json` before they claim an independent evaluation model.

## New-data behavior

After any relevant new data is acquired and reviewed, a proposition-relative evidence movement must be recorded as `strengthen`, `weaken`, `disambiguate`, `contextualize`, or `no-update` before or with the derived current-state update. Public subject clusters project that history through a visible Evidence Update Ledger; subject repositories preserve the same history append-only locally.

## Non-authority boundary

Conformance does not authorize publication of discovery candidates or infer guilt, motive, causation, coordination, or factual truth from import activity. Site and subject repositories remain projections/consumers; ERL remains the evaluation authority unless a separately reviewed governance decision changes that ownership.
