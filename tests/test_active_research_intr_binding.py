from __future__ import annotations

from pathlib import Path

import pytest

from scripts.build_active_research_intr_binding import (
    INTR_PATH,
    build_binding,
    persist_binding,
)
from scripts.consume_active_research_acquisition import digest


def make_dispatch():
    return {
        "mykv_coordination": {
            "github_storage_satisfies_persistence": False,
            "exact_byte_readback_required": True,
        },
        "lanes": [{
            "group_id": "ERL-RC-CYBER-SABOTAGE-LINEAGE-2026",
            "dispatch_state": "ELIGIBLE_FOR_AUTOMATED_ACQUISITION",
            "finding_authorized": False,
            "publication_authorized": False,
            "queues": [{
                "executable_items": [{
                    "source_id": "ERL-CYBER-CISA-IRAN-2025-JOINT-FACT-SHEET",
                    "url": "https://www.cisa.gov/news-events/cybersecurity-advisories/aa25-176a",
                    "allowed_hosts": ["www.cisa.gov", "cisa.gov"],
                    "persistence_required": True,
                    "required_storage_lane": "02_Research/ERL",
                }]
            }],
        }],
    }


def test_binding_matches_consumer_envelope_and_canonical_three_hop_path():
    binding = build_binding(
        dispatch=make_dispatch(),
        group_id="ERL-RC-CYBER-SABOTAGE-LINEAGE-2026",
        source_id="ERL-CYBER-CISA-IRAN-2025-JOINT-FACT-SHEET",
        payload_ref="kv-staging:ERL-CYBER-CISA-IRAN-2025-JOINT-FACT-SHEET/envelope.json",
    )
    envelope = binding["acquisition_envelope"]
    intent = binding["transport_intent"]
    request = binding["materialization_request"]

    assert binding["acquisition_envelope_sha256"] == digest(envelope)
    assert intent["payload_hash"] == binding["acquisition_envelope_sha256"]
    assert intent["boundary_path"] == INTR_PATH
    assert request["boundary_path"] == INTR_PATH
    assert request["payload_hash"] == intent["payload_hash"]
    assert request["packet_id"] == intent["packet_id"]
    assert binding["expected_runtime_receipt_count"] == 3
    assert binding["runtime_receipts_present"] is False
    assert binding["transport_execution_claimed"] is False


def test_binding_is_non_authorizing_and_keeps_tvtvc_credential_authority():
    binding = build_binding(
        dispatch=make_dispatch(),
        group_id="ERL-RC-CYBER-SABOTAGE-LINEAGE-2026",
        source_id="ERL-CYBER-CISA-IRAN-2025-JOINT-FACT-SHEET",
        payload_ref="staging:envelope.json",
    )
    intent = binding["transport_intent"]
    request = binding["materialization_request"]

    assert intent["authority"] == {
        "authority_transfer": False,
        "transport_grants_execution_authority": False,
        "credential_authority": "TV/TVC",
    }
    assert request["request_grants_execution_authority"] is False
    assert request["claim_or_fence_minted"] is False
    assert request["transport_grants_execution_authority"] is False
    assert request["credential_authority"] == "TV/TVC"
    assert request["github_token_runtime_authority"] == "NONE"
    assert request["authority_transfer"] is False
    assert request["authority_effect"] == "NONE_REQUEST_ONLY"


def test_binding_is_deterministic_and_idempotently_persisted(tmp_path: Path):
    kwargs = dict(
        dispatch=make_dispatch(),
        group_id="ERL-RC-CYBER-SABOTAGE-LINEAGE-2026",
        source_id="ERL-CYBER-CISA-IRAN-2025-JOINT-FACT-SHEET",
        payload_ref="staging:envelope.json",
    )
    first = build_binding(**kwargs)
    second = build_binding(**kwargs)
    assert first == second
    assert first["binding_hash"] == second["binding_hash"]

    output = tmp_path / "binding.json"
    assert persist_binding(output, first) == output.resolve()
    assert persist_binding(output, second) == output.resolve()

    changed = dict(second)
    changed["source_id"] = "different"
    with pytest.raises(ValueError, match="different bytes"):
        persist_binding(output, changed)


def test_empty_payload_reference_fails_closed():
    with pytest.raises(ValueError, match="payload_ref"):
        build_binding(
            dispatch=make_dispatch(),
            group_id="ERL-RC-CYBER-SABOTAGE-LINEAGE-2026",
            source_id="ERL-CYBER-CISA-IRAN-2025-JOINT-FACT-SHEET",
            payload_ref="   ",
        )
