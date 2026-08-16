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

## Relationship map

- path: `assessments/relationships/2026-08-16-chatgpt-bias-incident-map.json`
- commit: `c71df49c45309c447a0e59211cd67912a747872a`
- role: map direct sequence, candidate causal/interpretive relationships, and future longitudinal relationships without altering raw incident evidence

Current mapped relationship:

- incident 001 prompted scrutiny of model behavior that led to incident 002;
- incident 002 may have raised or altered the interpretive threshold applied to incident 001;
- the first relationship is direct sequence; the second remains a candidate relationship requiring further evidence.

## Rules for future incidents

- create a new raw incident object for every materially distinct event;
- preserve user input and relevant assistant output as close to verbatim as repository format permits;
- do not merge events merely because they appear causally related;
- add relationships as separate graph edges with explicit evidence basis and inference level;
- preserve contradictions, corrections, and assistant acknowledgements as evidence rather than overwriting prior statements;
- derive longitudinal findings from the graph while retaining every contributing raw node;
- no arbitrary event-count threshold is required unless separately adopted and validated as an ERL standard.

## Next tasks

- add future incidents as new nodes rather than editing these raw event files;
- map recurrence across topics, sessions, and administrations when evidence exists;
- distinguish direct-sequence, semantic-effect, governing-cause, correction, contradiction, and candidate-causal edges;
- preserve source screenshots or equivalent immutable source artifacts when a repository-safe custody path is available;
- validate that downstream ERL summaries always retain pointers to contributing raw evidence nodes.

## Completion posture

- raw incidents preserved: 2/2 currently identified
- relationship map installed: 1/1
- bounded handoff installed: 1/1
- scaffolding/stubs: 0
- longitudinal interpretation: active/open-ended by design

Session lane state: `ACTIVE — DISTINCT SUPPORT`.
