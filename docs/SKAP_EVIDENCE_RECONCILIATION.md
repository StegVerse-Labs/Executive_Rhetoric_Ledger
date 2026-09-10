# SKAP Account ↔ Evidence Reconciliation

Goal Task ID: `SS-DATA-RECLAMATION-DISCLOSURE-INGESTION-001`

This layer compares a non-secret SKAP-maintained account/provider projection against independently maintained evidence mappings. It is deliberately bidirectional.

SKAP supplies only the account inventory projection needed for reconciliation: stable account reference, provider organization reference, account class, and account status. The projection contract explicitly requires `contains_secret_material=false`; passwords, tokens, credential payloads, and sealed SKAP object contents are not reconciliation inputs.

For every projected SKAP account, the reconciler records whether the account provider is `KNOWN_AND_MAPPED` or `KNOWN_BUT_UNMAPPED`, then retains downstream organization references and evidence references reachable from that provider. Separately, verified propagation observations whose organizations cannot be connected to a known SKAP provider or its downstream disclosure context are surfaced as `EVIDENCE_WITHOUT_KNOWN_ACCOUNT_ORIGIN`.

The reconciliation is a coverage and discovery surface, not proof of subject-specific data traversal. Provider disclosure, graph reachability, or inferred relationships do not become `OBSERVED_TRANSFER` without authentic transfer evidence. Cross-subject reconciliation fails closed.

The non-secret SKAP projection contract is `schemas/skap-account-inventory-projection.schema.json`. The deterministic reconciler is `scripts/reconcile_skap_evidence.py`; its output schema is `schemas/skap-evidence-reconciliation.schema.json`; canonical fixtures live under `fixtures/digital-data-reclamation/`; validation is integrated into `scripts/validate_digital_data_reclamation.py`.

A producer that emits the projection from real SKAP-maintained accounts remains a separate integration surface. Until such a producer exists and emits authentic account metadata, fixture reconciliation proves the contract and classification semantics but does not claim that the user's real SKAP account inventory has been enumerated.
