# Governed Source-Family Discovery

The recurring discovery workflow monitors allowlisted source indexes and converts relevant links into the repository's existing source-adapter format.

Discovery may fetch configured index pages, extract and canonicalize links, enforce host and path allowlists, filter by relevance terms, create capture candidates, and pass those candidates through the existing archive, hashing, deduplication, clustering, adjacency, historical-backfill, and governed-review pipeline.

Discovery may not promote a candidate, make a factual or legal finding, publish unreviewed material, mutate person-specific repositories, or claim complete coverage merely because an index was checked.

Initial source families are Federal Register DHS documents, DOJ press releases, ICE newsroom releases, and CBP media releases. Additional families must use the same schema, allowlist, receipt, and candidate-only authority contract rather than a separate crawler or scheduler.
