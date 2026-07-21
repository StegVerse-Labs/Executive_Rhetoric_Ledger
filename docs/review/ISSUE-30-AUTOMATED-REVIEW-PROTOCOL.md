# Issue #30 automated governed-review protocol

Issue #30 is the sole human evidentiary authority surface for case `RRM-SPI-2025-03-15`.

Each reviewer records one independently authored comment using this exact structure:

```text
ERL-REVIEW-V1
disposition: accepted-with-limitations
authority: evidence-reviewer
finding: <the reviewer's bounded finding>
evidence-limit: <records or conclusions that remain unavailable or unresolved>
```

Allowed dispositions:

- `accepted-with-limitations`
- `needs-more-evidence`
- `disputed`
- `rejected-unsupported`
- `rejected-out-of-scope`

Allowed authorities:

- `evidence-reviewer`
- `civil-rights-reviewer`
- `legal-reviewer`
- `medical-evidence-reviewer`

The workflow automatically reads every Issue #30 comment after creation or editing. A receipt is created only when at least two distinct GitHub reviewers, representing at least two distinct reviewer authorities, submit the same disposition. The latest valid comment from each login controls that reviewer's vote.

When quorum exists, automation:

1. copies reviewer-authored findings and evidence limits without expansion;
2. creates a schema-valid reviewed receipt;
3. creates or updates branch `governed/issue-30-review-receipt`;
4. opens a governed integration pull request;
5. leaves publication, compendium inclusion, propagation, and closure to the repository's existing reviewed-only validation chain.

Automation may not choose a disposition, manufacture quorum, infer reviewer authority, add findings, resolve evidentiary conflicts, determine liability, or find a constitutional violation.

No manual file creation, branch creation, commit, pull request, receipt formatting, or workflow dispatch is required after reviewers post their comments.
