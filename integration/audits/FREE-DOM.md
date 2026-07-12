# Native Mechanism Audit: StegVerse-Labs/FREE-DOM

## Audit posture

```yaml
repository: "StegVerse-Labs/FREE-DOM"
audit_state: "contract-partial"
classification: "daily-osint-discovery-classification-and-routing-producer"
relationship_status: "newly-discovered-pending-network-registry-migration"
adapter_state: "candidate-blocked"
reviewed_at: "2026-07-11"
```

FREE-DOM is the previously omitted upstream public-source discovery repository. It is a more likely discovery federation producer than any subject-specific repository.

## Confirmed native mechanisms

### Daily public OSINT sweep

```yaml
workflow: ".github/workflows/ai_search_agent.yml"
schedule: "30 10 * * *"
manual_trigger: true
source_scope: "whitelisted RSS and public pages only"
agent: "scripts/search_agent.py"
summary_builder: "scripts/build_ai_agent_summary.py"
```

The agent:

1. reads `data/sources/sources_whitelist.csv`;
2. finds master events whose `deep_search_event` is blank or `pending`;
3. finds verified people/events whose `deep_search_person` is blank or `pending`;
4. derives keywords from event, person, and location fields;
5. scans whitelisted feeds and pages;
6. appends discovered links non-destructively to notes fields;
7. writes raw JSONL run logs under `data/logs/ai_agent/`;
8. updates summary artifacts.

### Classification and routing

FREE-DOM maintains distinct data surfaces:

- `data/master/` — canonical or verified datasets;
- `data/pending/` — new material awaiting merge;
- `data/unverified/` — event, person, and connection leads;
- `data/logs/ai_agent/` — raw search-run logs;
- `data/summary/` — aggregated indexes and freshness state;
- `data/archive/` — processed import batches.

The merge process validates CSV shape and required fields, deduplicates by native composite keys, sorts records, routes unverified objects by `event`, `person`, or `connection`, and archives processed pending files.

## Confirmed source classes

The whitelist currently includes court dockets, official oversight releases, C-SPAN, major wire and news organizations, and public-interest broadcast feeds. Whitelisting controls where discovery occurs; it does not establish truth, neutrality, completeness, or admissibility.

## Provenance retained

The current search log retains some useful discovery provenance:

- event-versus-person search target;
- derived keywords;
- feed or page used for discovery;
- result title;
- result link;
- RSS publication string when available;
- repository base scope;
- timestamp encoded in the log filename;
- raw run log and total-hit summary.

Pending and master CSV records may retain `source_urls`, primary/secondary source fields, confidence, notes, and next-step posture depending on record class.

## Provenance gaps

The current implementation does not yet establish complete reconstructable custody for every discovered object. The audit has not verified:

- a stable discovery-object ID;
- retrieval timestamp on each hit object;
- HTTP status and response headers;
- exact captured source fragment or full snapshot;
- content hash;
- source author or issuing institution as structured fields;
- normalized publication time;
- query/rule version or code commit on each hit;
- classification-rule version and confidence;
- explicit routing receipt from discovery object to destination row;
- correction or reclassification succession;
- content-level or claim-level duplicate identity;
- proof that appended lead URLs remain linked to the exact discovery log after later edits;
- archive hashes for processed pending batches.

Exceptions during retrieval and feed parsing are generally swallowed or converted to empty results, so failed-source attempts are not fully visible as durable per-source receipts.

## Canonical-state concern

The search agent writes discovered lead links directly into notes fields of `data/master/master_timeline.csv` and `data/master/verified_people_events.csv`. Although this is non-destructive text appending, it mixes unreviewed discovery leads into files described as master or verified surfaces.

A lead URL in a canonical row must remain explicitly classified as a discovery lead, not as verification of the row or the linked claim.

## Smallest compatible ledger boundary

```text
FREE-DOM discovery hit
-> provenance sufficiency evaluation
-> immutable discovery envelope
-> classification and routing receipt
-> repository-specific candidate
-> Executive Rhetoric Ledger pending intake
-> governed source-posture and admissibility review
```

FREE-DOM should remain the primary public OSINT discovery candidate. Trumpality, Administrations, biography repositories, and the Executive Rhetoric Ledger should not add competing broad scanners where FREE-DOM already supplies discovery.

## Required contract completion

Before adapter readiness:

- create a stable discovery-envelope schema;
- add per-hit retrieval time, run ID, code commit, source identity, and query terms;
- retain content or a durable snapshot pointer and SHA-256 hash;
- emit explicit classification and routing receipts;
- preserve correction and reclassification succession;
- produce durable failed-source receipts;
- separate lead annotations from verified canonical state;
- verify one end-to-end trace from source URL through discovery, classification, routing, and downstream candidate;
- update the Executive Rhetoric Ledger relationship network and capability registry from fourteen to fifteen repositories.

## Evidence boundary

```text
Discovery != verification.
Whitelisting != neutrality.
Classification != admissibility.
Routing != factual standing.
Canonical file placement != proof.
```
