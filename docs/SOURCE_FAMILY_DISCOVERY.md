# Governed Source-Family Discovery

The recurring discovery workflow monitors allowlisted official source indexes and converts relevant links into the repository's existing source-adapter format.

Discovery may:

- fetch configured index pages;
- extract and canonicalize links;
- enforce host and path allowlists;
- filter by configured relevance terms;
- create capture candidates;
- archive, hash, deduplicate, cluster, and route candidates for review.

Discovery may not:

- promote a candidate;
- make a factual or legal finding;
- publish unreviewed material;
- change a person-specific repository;
- claim completeness merely because an index was checked.

Initial source families are Federal Register DHS documents, DOJ press releases, ICE newsroom releases, and CBP media releases. Coverage is expected to expand through the same schema and validation contract rather than separate crawlers.
