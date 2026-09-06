# ERL Canonical Object Provenance Reference MIRROR_HANDOFF

Updated: 2026-09-05
Repository: `StegVerse-Labs/Executive_Rhetoric_Ledger`
Parent candidate owner: issue #63
Upstream canonical provenance owner: `StegVerse-Labs/StegOS#190`
Canonical lineage schema: `stegos.object_provenance_lineage.v1`
Authority effect: `NONE`

## Machine preflight

Resolved before functional mutation:

- repository continuity authority: `ERL_MIRROR_HANDOFF.md`;
- bounded Orli candidate authority: `docs/ORLI_SHULL_AI_GOVERNANCE_COLLAPSE_MIRROR_HANDOFF.md` / issue #63;
- research-candidate activation authority: `docs/RESEARCH_CANDIDATE_ACTIVATION_MIRROR_HANDOFF.md` and `coordination/research-candidate-activation-registry.v1.json`;
- canonical source-object provenance authority: `StegVerse-Labs/StegOS#190` / `stegos.object_provenance_lineage.v1`;
- Master Records: custody/reconstruction only;
- ERL: downstream research-candidate/assessment producer only;
- Workspace/Site/task registries: downstream references/projections only;
- TV/TVC credential authority remains unchanged.

Open-PR collision review found no active ERL PR claiming `schemas/canonical-provenance-reference.schema.json`, `scripts/validate_canonical_provenance_reference.py`, `tests/test_canonical_provenance_reference.py`, or this handoff. Existing open ERL research and automation PRs retain their own bounded surfaces.

## Purpose

Issue #190 requires downstream ERL/task/artifact producers to reference canonical receipt-bound provenance rather than prose-only source posture. ERL must not recreate the canonical provenance graph or mint competing object, edge, lineage, transition-receipt, or custody identities.

This change therefore adds a reference-only ERL boundary:

```text
canonical StegOS lineage
  -> ERL reference record
  -> research candidate / assessment producer
```

The ERL record may carry only canonical IDs and receipt references already produced by the authority-owned lineage path. It cannot contain or manufacture canonical `objects`, `edges`, `root_object_ids`, Workspace projection state, Master Records projection state, provider object identity, or content hashes.

## Implemented source surfaces

- `schemas/canonical-provenance-reference.schema.json`
- `scripts/validate_canonical_provenance_reference.py`
- `tests/test_canonical_provenance_reference.py`

The validator requires:

- schema `stegverse.erl.canonical-provenance-reference.v1`;
- canonical lineage schema exactly `stegos.object_provenance_lineage.v1`;
- canonical `svlineage:sha256:*`, `svobj:sha256:*`, and `svedge:sha256:*` identifiers;
- at least one canonical source-root object;
- at least one canonical derivation edge;
- at least one transition receipt reference;
- `authority_effect: NONE`;
- optional Master Records custody receipt reference only after such a receipt actually exists.

It fails closed on local/noncanonical IDs, missing roots or edges, duplicate receipt references, authority expansion, and attempts to reproduce canonical graph fields inside ERL.

## Historical Orli boundary

No reference record is created for `ERL-2026-09-03-ORLI-SHULL-AI-GOVERNANCE-COLLAPSE-001` yet because authentic canonical lineage for the original source screenshot/conversation event has not been observed. Creating placeholder canonical IDs would fabricate provenance.

Once authentic canonical ingress exists, ERL may persist a reference record bound to the real lineage/candidate object/roots/edges/transition receipts. If only historical source bytes are recovered without the original transition receipt, the record must preserve the bounded historical-recovery posture rather than claim original runtime provenance.

## README completeness predicate

README impact was evaluated before mutation.

**Determination: no README change is required for this change set.** The repository README already defines ERL as a lineage/evidence layer, states that repository origin is provenance rather than proof, and preserves reviewed evidence posture and uncertainty. This change does not alter existing record interpretation, publication rules, authority boundaries, runtime behavior, credential paths, or source-admissibility semantics. It adds a fail-closed internal validator for an optional future reference object and explicitly prevents ERL from becoming provenance authority.

If ERL later requires canonical provenance references for existing record admission, changes public producer interfaces, changes evidence admissibility, or begins consuming/runtime-writing lineage automatically, README must be updated in that same future change set.

## Evidence boundary

Source/schema/test success proves only that ERL can reject malformed or authority-expanding canonical-reference projections. It does not prove:

- authentic source ingress;
- authentic conversation-event identity;
- an authentic transition receipt;
- a canonical ERL candidate object;
- Master Records custody;
- reverse reconstruction from a real ERL artifact;
- Workspace projection;
- publication or finding authority.

## Next lawful transition

After merge, the next provenance transition remains external to this source adapter: obtain one authentic `stegos.object_provenance_lineage.v1` chain containing an ERL research-candidate derivation, then persist and validate only its canonical references here. The historical Orli candidate must remain unbound until exact source/runtime provenance is truthfully available.
