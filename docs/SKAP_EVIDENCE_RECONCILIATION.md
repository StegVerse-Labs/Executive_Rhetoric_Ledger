# SKAP Account ↔ Evidence Reconciliation

Goal Task ID: `SS-DATA-RECLAMATION-DISCLOSURE-INGESTION-001`

This layer compares SKAP-maintained account/provider topology against independently maintained evidence mappings. It is deliberately bidirectional.

For every SKAP account, the reconciler records whether the account provider is `KNOWN_AND_MAPPED` or `KNOWN_BUT_UNMAPPED`, then retains downstream organization references and evidence references reachable from that provider. Separately, verified propagation observations whose organizations cannot be connected to a known SKAP provider or its downstream disclosure context are surfaced as `EVIDENCE_WITHOUT_KNOWN_ACCOUNT_ORIGIN`.

The reconciliation is a coverage and discovery surface, not proof of subject-specific data traversal. Provider disclosure, graph reachability, or inferred relationships do not become `OBSERVED_TRANSFER` without authentic transfer evidence. Cross-subject reconciliation fails closed.

The deterministic implementation is `scripts/reconcile_skap_evidence.py`; its schema is `schemas/skap-evidence-reconciliation.schema.json`; the canonical fixture is `fixtures/digital-data-reclamation/skap-evidence-reconciliation.sample.json`; validation is integrated into `scripts/validate_digital_data_reclamation.py`.
