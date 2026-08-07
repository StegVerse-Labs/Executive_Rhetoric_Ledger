# DPOI Directional Discovery

ERL recurring discovery may use Data Points of Interest (DPOIs) to focus searches on evidence that could strengthen, weaken, or disambiguate the current evidence state.

## Governing rule

A discovery result is a candidate signal, not a finding. Automation may identify why a result is potentially relevant to a DPOI, but it may not change the DPOI's evidentiary state without governed review and source custody.

A zero-result search has `no_result_effect: no-update`. Absence of a discovered result is not disproof unless a separate coverage-completeness contract establishes that the relevant source universe and time range were exhaustively observed.

## Category search parameters

Every enabled recurring search carries `dpoi_search_parameters`:

- `evidence_directions`: which directions the search is intended to test: `strengthen`, `weaken`, `disambiguate`.
- `strengthen_terms`: terms that may indicate corroboration, confirmation, admission, authentication, or another support-bearing record.
- `weaken_terms`: terms that may indicate contradiction, correction, dismissal, retraction, non-involvement, or another countervailing record.
- `disambiguation_terms`: terms targeting uncertainty in timeline, identity, authority, jurisdiction, scope, definition, records custody, channel purpose, or comparable state dimensions.
- `state_dimensions`: the specific parts of the current DPOI state the search may clarify.
- `no_result_effect`: fixed to `no-update`.
- `candidate_only`: fixed to `true`.

## Interpretation

Directional term matches are search and routing aids. They do not determine truth value. A single candidate can carry more than one direction after review—for example, a record can weaken one causal explanation while strengthening a narrower authority-chain explanation.

The recurring discovery-cycle manifest preserves these parameters with each planned query so downstream discovery, source capture, clustering, contradiction analysis, and review can explain why an item was collected and which unresolved state dimensions it could affect.

## Source-family integration boundary

Issue #51 / `ERL-OSINT-API-001` owns `config/source-families.json`, `schemas/source-family.schema.json`, `scripts/discover_source_family_links.py`, `scripts/validate_source_family_discovery.py`, and `.github/workflows/run-recurring-discovery.yml` through its active claim window. That lane must integrate the DPOI directional parameters into candidate receipts when it next changes those owned files, without adding promotion authority or treating zero-result coverage as negative evidence.
