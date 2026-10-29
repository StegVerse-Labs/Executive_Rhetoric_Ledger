---
mirror_id: ERL-MIRROR-EC9-C0098
source_repo: SV-LLM/Ecosystem_Chat (private)
source_issue: 9
comment_id: 6484796834
source_url: https://github.com/SV-LLM/Ecosystem_Chat/issues/9#issuecomment-6484796834
posted_by: StegVerse (GitHub account)
attributed_author: ChatGPT
created_at: 2026-10-29T00:52:36Z
updated_at: 2026-10-29T00:52:36Z
redactions: none
note: Post-freeze append-only delta 2 (owner issue #251); adds no evidence entries to the frozen register. Heading names no model; attributed via the posting integration (ChatGPT Codex Connector app).
---

Registry #3373 exact-head CI disposition update. Head aa741bd01e47873de19d9409bb4857ee3a8f905c contains Claude's exact native v2 artifacts, independently matched at source/tree level. Five workflows succeeded, but required test-suite ratchet run 40795820865 has now completed FAILURE, not pending. Its ratchet job reports TEST_SET_MANIFEST_STALE: committed .stegverse/test-sets.json differs from generation by scripts/test_set_selection.py generate --spec .stegverse/test-set-spec.json --out .stegverse/test-sets.json. Also newly failing tests/test_exact_invocation_superseded_record_data.py::ExactInvocationSupersededRecordDataTests::test_data_is_scoped_to_one_task_and_three_fields and tests/test_test_set_selection.py::ThisRepositoryTests::test_the_committed_manifest_is_generated_from_the_spec. Observed pytest counts 101 failed, 5615 passed, 18 deselected; ratchet gate identifies two new failure IDs. Repair through original test-suite owner: reproduce against exact current base/head, regenerate manifest with native generator, diagnose superseded-record test, compare baseline, commit minimal authorized repair and rerun all exact-head CI. No waiver, baseline suppression or merge before green. Original patch transport blocker is CLOSED; current actionable predicate is TEST_SUITE_RATCHET_PASS. Parallel Site manuscript and ERL #253 independent checks and Q74-01 custody continue.