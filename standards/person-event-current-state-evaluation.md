# Person / Event Current-State Evaluation Standard

## Purpose

Provide one reusable evidence-evaluation structure for any repository or public Site cluster that tracks a person, event, institution, decision, incident, or related evidence set.

ERL is the evaluation authority. Person/event repositories are governed consumers. Public Site pages are readable projections of the same evaluated state and must not create independent truth claims.

## Required current-state structure

Every evaluated subject must expose:

1. `subject_id` and subject type (`person`, `event`, `institution`, `decision`, `incident`, or `mixed`).
2. Evidence-state banner: `PARTIAL`, `REVIEW_REQUIRED`, `ASSESSABLE`, `REVIEWED`, or `SUPERSEDED`.
3. What is presently established.
4. What evidence has strengthened.
5. What evidence has weakened.
6. What remains unresolved.
7. What evidence would materially disambiguate the current state.
8. DPOI state matrix.
9. Evidence-movement ledger.
10. Chronology and authority overlay.
11. Evidence-gap register.
12. Explicit inference ceilings.
13. Source/custody references and validation state.
14. Publication and promotion authority state.

## DPOI evaluation

Each Data Point of Interest must preserve:

- proposition being tested;
- competing explanations;
- observed evidence;
- strengthening evidence;
- weakening evidence;
- disambiguating evidence;
- affected state dimensions;
- chronology;
- formal/de-facto authority nodes;
- confidence/evidence state;
- unresolved discriminator;
- next evidence needed;
- inference ceiling;
- source and custody receipts.

Directional labels are proposition-relative, never labels on a source or person. One item may strengthen one proposition while weakening an alternative.

A zero-result search has `no-update` effect unless independent coverage-completeness evidence supports a stronger inference.

## Evidence movement ledger

Every newly acquired or newly reviewed data object must append one ledger entry. It must not silently overwrite the prior state.

Minimum entry:

```json
{
  "ledger_event_id": "stable-id",
  "subject_id": "stable-subject-id",
  "observed_at": "RFC3339",
  "evidence_ref": "custody-or-source-ref",
  "dpoi_refs": ["DPOI-ID"],
  "directional_effects": [
    {
      "dpoi_id": "DPOI-ID",
      "direction": "strengthen|weaken|disambiguate|contextualize|no-update",
      "state_dimensions": ["authority", "knowledge", "timeline"],
      "basis": "why the evidence changes or does not change the present state"
    }
  ],
  "prior_state_ref": "previous-state-id",
  "resulting_state_ref": "new-state-id-or-unchanged",
  "review_state": "CANDIDATE|REVIEW_REQUIRED|REVIEWED",
  "promotion_authorized": false
}
```

No acquired evidence may automatically establish guilt, innocence, motive, culpability, causation, coordination, factual truth, or publication authority.

## Readable current-state report

Human-readable projections should use this order:

1. Current-State banner and as-of timestamp.
2. One-page state summary.
3. DPOI state matrix.
4. Evidence movement since the previous state.
5. Chronology / authority graph.
6. Detailed evidence analysis by DPOI.
7. Evidence-gap register.
8. Methodology, custody, and source appendix.

Statements should be visibly classed as `OBSERVED`, `INFERRED`, or `UNRESOLVED`.

## Public Site cluster contract

For a public cluster dedicated to one subject, the cluster home page must include a prominent **Evidence Update Ledger** near the lower portion of the primary explanatory content, using the same readable governance style as the Site child-governance explanation surfaces.

The ledger must show, for each newly acquired or newly reviewed evidence object:

- date/time;
- source class;
- concise description;
- DPOI(s) affected;
- whether it strengthens, weakens, disambiguates, contextualizes, or causes no update;
- current review state;
- link to the detailed evidence/state page;
- explicit statement when the overall state remains unchanged.

Recommended cluster pages:

- `/subject/` — current-state home and Evidence Update Ledger;
- `/subject/evidence/` — source/custody index;
- `/subject/dpoi/` — DPOI state matrix;
- `/subject/chronology/` — chronology and authority overlay;
- `/subject/analysis/` — detailed current-state evidence assessment;
- `/subject/gaps/` — unresolved discriminators and evidence gaps;
- `/subject/method/` — evaluation method and promotion boundaries.

The Site projection must derive from canonical evaluated records and must never become an independent evidence authority.

## Consumer repository contract

Person/event repositories such as Trumpality should retain append-only imports of reviewed ERL state and maintain a local current-state index plus evidence-update ledger. Native records and native verification labels must remain unchanged unless that repository has an independent governed process authorizing mutation.

Minimum consumer surfaces:

- append-only reviewed projection objects;
- current projection pointer;
- append-only evidence-update ledger;
- current-state evaluation pointer/index;
- source receipt and hash references;
- explicit supersession link to prior state.

## Promotion boundary

Discovery -> candidate routing -> custody -> review -> current-state evaluation -> reviewed projection -> public projection.

No layer may skip the preceding authority boundary.
