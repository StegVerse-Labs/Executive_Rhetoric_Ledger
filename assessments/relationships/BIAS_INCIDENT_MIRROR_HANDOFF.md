# ERL Bias Incident Mirror Handoff

## Authority

Bounded source of truth for model-behavior bias incident preservation and relationship mapping in `StegVerse-Labs/Executive_Rhetoric_Ledger`.

This handoff is subordinate to repository-wide `ERL_MIRROR_HANDOFF.md` and authoritative for this incident-tracking lane.

## Invariant

Preserve and present truth through evidence.

Raw incidents remain separately preserved evidence objects. Relationship maps, classifications, and longitudinal findings may reference them but must not replace, normalize, summarize-away, or rewrite the underlying event record.

## Installed incidents

1. `ERL-EVT-2026-08-16-ADMIN-PROTECTIVE-FRAMING-001`
   - path: `assessments/events/2026-08-16-chatgpt-admin-protective-framing.raw.md`
   - candidate type: bias toward current administration
   - state: raw event preserved
   - commit: `297d3aa761874da0b2f22195ec36cfc38cb6b627`

2. `ERL-EVT-2026-08-16-SELF-DEFENSIVE-HANDLING-002`
   - path: `assessments/events/2026-08-16-chatgpt-self-defensive-handling.raw.md`
   - candidate type: bias toward self-defense when queried about administration-response handling
   - state: raw event preserved
   - commit: `f92140ce1c5de8a92aca9cbfdc38f25c26edf629`

3. `ERL-EVT-2026-08-16-ADMIN-MALTREATMENT-SCOPE-REDUCTION-003`
   - path: `assessments/events/2026-08-16-chatgpt-administration-maltreatment-scope-reduction.raw.md`
   - canonical issue: `#66`
   - candidate type: repeated reduction of broader administration-treatment/maltreatment research into a narrower potentially justified use-of-force frame, followed by premature directional evaluation posture
   - state: raw event preserved
   - commit: `755710e8e05dd98f19b35d0852c0c39b4e1c1b8d`

## Relationship map

- path: `assessments/relationships/2026-08-16-chatgpt-bias-incident-map.json`
- current map commit: `963336f54f3ea0c3b89dfc7193ba5514bf3965ac`
- role: map direct sequence, candidate causal/interpretive relationships, and future longitudinal relationships without altering raw incident evidence

Current mapped relationships include:

- incident 001 prompted scrutiny of model behavior that led to incident 002;
- incident 002 may have raised or altered the interpretive threshold applied to incident 001;
- incident 003 has candidate semantic-effect relationships to incidents 001 and 002 because it again changes the user's requested evidence surface in a way that can narrow examination of administration-level conduct;
- no common motive or cause is inferred merely from those relationships.

## Related research-surface repair

- Issue #65 is the restored broader parent surface for potential administration maltreatment/treatment of citizens across federal enforcement activity.
- Issue #64 is explicitly a narrower missing-context/evidentiary-handling child surface and is not authorized to redefine the parent research object as a force-justification inquiry.
- Issue #66 preserves incident 003 as a distinct model-behavior event.
- Issue #67 was an accidental duplicate coordination stub and was immediately closed as duplicate; it owns no evidence or research state.

## Rules for future incidents

- create a new raw incident object for every materially distinct event;
- preserve user input and relevant assistant output as close to verbatim as repository format permits;
- do not merge events merely because they appear causally related;
- add relationships as separate graph edges with explicit evidence basis and inference level;
- preserve contradictions, corrections, and assistant acknowledgements as evidence rather than overwriting prior statements;
- derive longitudinal findings from the graph while retaining every contributing raw node;
- no arbitrary event-count threshold is required unless separately adopted and validated as an ERL standard;
- do not allow a child research surface, legal/tactical question, or evaluation schema to silently replace a broader originating evidence surface.

## Next tasks

- add future incidents as new nodes rather than editing these raw event files;
- map recurrence across topics, sessions, and administrations when evidence exists;
- distinguish direct-sequence, semantic-effect, governing-cause, correction, contradiction, and candidate-causal edges;
- preserve source screenshots or equivalent immutable source artifacts when a repository-safe custody path is available;
- validate that downstream ERL summaries always retain pointers to contributing raw evidence nodes;
- continue origin-scope recovery so broader research questions remain authoritative over narrower implementations.

## Completion posture

- raw incidents preserved in this bounded lane: 3/3 currently registered
- relationship map installed and extended: 1/1
- bounded handoff installed and current: 1/1
- scaffolding/stubs counted as complete: 0
- longitudinal interpretation: active/open-ended by design

Session lane state: `ACTIVE — DISTINCT SUPPORT`.
