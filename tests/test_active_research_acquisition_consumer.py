from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from scripts.consume_active_research_acquisition import consume, digest


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
                    "source_id": "ERL-CYBER-WEB-HISTORY-CERN",
                    "url": "https://web30.web.cern.ch/web-history.html",
                    "allowed_hosts": ["web30.web.cern.ch", "home.cern"],
                    "persistence_required": True,
                    "required_storage_lane": "02_Research/ERL",
                }]
            }],
        }],
    }


def make_receipt(payload_hash: str):
    body = {
        "schema": "stegverse.intr.hop_receipt/v1",
        "receipt_id": "receipt-1",
        "packet_id": "packet-1",
        "hop_index": 1,
        "direction": "FORWARD",
        "from_role": "ERL_DISPATCHER",
        "to_role": "ERL_ACQUISITION_EXECUTOR",
        "operation_hash": "sha256:" + "1" * 64,
        "payload_hash": payload_hash,
        "prior_receipt_hash": None,
        "boundary_identity_ref": "erl-acquisition-executor:test",
        "boundary_verification": "VERIFIED",
        "transition_state": "RECEIVED",
        "secret_plaintext_present": False,
        "authority_transfer": False,
        "recorded_at": "2026-09-10T20:00:00Z",
    }
    return {**body, "receipt_hash": digest(body)}


def envelope_hash():
    return digest({
        "schema": "stegverse.erl.active-research-acquisition-envelope/v1",
        "group_id": "ERL-RC-CYBER-SABOTAGE-LINEAGE-2026",
        "source_id": "ERL-CYBER-WEB-HISTORY-CERN",
        "source_url": "https://web30.web.cern.ch/web-history.html",
        "required_storage_lane": "02_Research/ERL",
        "finding_authorized": False,
        "publication_authorized": False,
    })


def test_consumes_admitted_payload_into_kv(tmp_path: Path):
    payload = tmp_path / "cern.html"
    payload.write_bytes(b"<html>cern</html>\n")
    kv = tmp_path / "kv"
    kv.mkdir()
    result = consume(
        dispatch=make_dispatch(),
        group_id="ERL-RC-CYBER-SABOTAGE-LINEAGE-2026",
        source_id="ERL-CYBER-WEB-HISTORY-CERN",
        intr_receipt=make_receipt(envelope_hash()),
        payload=payload,
        kv_root=kv,
        kv_instance_id="MYKV-TEST",
        captured_at="2026-09-10T20:00:00Z",
    )
    assert result["state"] == "KV_STORED_AND_READBACK_VERIFIED"
    assert result["finding_authorized"] is False
    assert result["publication_authorized"] is False
    stored = kv / "02_Research" / "ERL" / result["artifact_id"] / "cern.html"
    assert stored.read_bytes() == payload.read_bytes()
    assert result["source_sha256"] == hashlib.sha256(payload.read_bytes()).hexdigest()


def test_rejects_receipt_not_bound_to_envelope(tmp_path: Path):
    payload = tmp_path / "cern.html"
    payload.write_bytes(b"x")
    kv = tmp_path / "kv"
    kv.mkdir()
    with pytest.raises(ValueError, match="bind"):
        consume(
            dispatch=make_dispatch(),
            group_id="ERL-RC-CYBER-SABOTAGE-LINEAGE-2026",
            source_id="ERL-CYBER-WEB-HISTORY-CERN",
            intr_receipt=make_receipt("sha256:" + "0" * 64),
            payload=payload,
            kv_root=kv,
            kv_instance_id="MYKV-TEST",
            captured_at="2026-09-10T20:00:00Z",
        )


def test_rejects_authority_transfer(tmp_path: Path):
    payload = tmp_path / "cern.html"
    payload.write_bytes(b"x")
    kv = tmp_path / "kv"
    kv.mkdir()
    receipt = make_receipt(envelope_hash())
    receipt["authority_transfer"] = True
    body = dict(receipt)
    body.pop("receipt_hash")
    receipt["receipt_hash"] = digest(body)
    with pytest.raises(ValueError, match="authority"):
        consume(
            dispatch=make_dispatch(),
            group_id="ERL-RC-CYBER-SABOTAGE-LINEAGE-2026",
            source_id="ERL-CYBER-WEB-HISTORY-CERN",
            intr_receipt=receipt,
            payload=payload,
            kv_root=kv,
            kv_instance_id="MYKV-TEST",
            captured_at="2026-09-10T20:00:00Z",
        )
