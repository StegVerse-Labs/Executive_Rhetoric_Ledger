from __future__ import annotations

import hashlib
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


def make_chain(payload_hash: str):
    roles = [
        ("EXTERNAL_SYSTEM", "STEGOS_ECOSYSTEM"),
        ("STEGOS_ECOSYSTEM", "DEVICE_SYSTEM"),
        ("DEVICE_SYSTEM", "KV"),
    ]
    receipts = []
    prior = None
    for index, (from_role, to_role) in enumerate(roles, start=1):
        body = {
            "schema": "stegverse.intr.hop_receipt/v1",
            "receipt_id": f"receipt-{index}",
            "packet_id": "packet-1",
            "hop_index": index,
            "direction": "FORWARD",
            "from_role": from_role,
            "to_role": to_role,
            "operation_hash": "sha256:" + "1" * 64,
            "payload_hash": payload_hash,
            "prior_receipt_hash": prior,
            "boundary_identity_ref": f"boundary:test:{to_role.lower()}",
            "boundary_verification": "VERIFIED",
            "transition_state": "RECEIVED" if index == len(roles) else "FORWARDED",
            "secret_plaintext_present": False,
            "authority_transfer": False,
            "recorded_at": "2026-09-10T20:00:00Z",
        }
        receipt = {**body, "receipt_hash": digest(body)}
        receipts.append(receipt)
        prior = receipt["receipt_hash"]
    return receipts


def test_consumes_complete_intr_chain_into_kv(tmp_path: Path):
    payload = tmp_path / "cern.html"
    payload.write_bytes(b"<html>cern</html>\n")
    kv = tmp_path / "kv"
    kv.mkdir()
    chain = make_chain(envelope_hash())
    result = consume(
        dispatch=make_dispatch(),
        group_id="ERL-RC-CYBER-SABOTAGE-LINEAGE-2026",
        source_id="ERL-CYBER-WEB-HISTORY-CERN",
        intr_receipts=chain,
        payload=payload,
        kv_root=kv,
        kv_instance_id="MYKV-TEST",
        captured_at="2026-09-10T20:00:00Z",
    )
    assert result["state"] == "KV_STORED_AND_READBACK_VERIFIED"
    assert result["intr_terminal_receipt_hash"] == chain[-1]["receipt_hash"]
    assert result["finding_authorized"] is False
    assert result["publication_authorized"] is False
    stored = kv / "02_Research" / "ERL" / result["artifact_id"] / "cern.html"
    assert stored.read_bytes() == payload.read_bytes()
    assert result["source_sha256"] == hashlib.sha256(payload.read_bytes()).hexdigest()


def test_rejects_single_valid_hop(tmp_path: Path):
    payload = tmp_path / "cern.html"
    payload.write_bytes(b"x")
    kv = tmp_path / "kv"
    kv.mkdir()
    with pytest.raises(ValueError, match="complete"):
        consume(
            dispatch=make_dispatch(), group_id="ERL-RC-CYBER-SABOTAGE-LINEAGE-2026",
            source_id="ERL-CYBER-WEB-HISTORY-CERN", intr_receipts=make_chain(envelope_hash())[:1],
            payload=payload, kv_root=kv, kv_instance_id="MYKV-TEST", captured_at="2026-09-10T20:00:00Z")


def test_rejects_skipped_boundary(tmp_path: Path):
    payload = tmp_path / "cern.html"
    payload.write_bytes(b"x")
    kv = tmp_path / "kv"
    kv.mkdir()
    chain = make_chain(envelope_hash())
    chain[1]["to_role"] = "KV"
    body = dict(chain[1]); body.pop("receipt_hash"); chain[1]["receipt_hash"] = digest(body)
    with pytest.raises(ValueError, match="adjacency"):
        consume(dispatch=make_dispatch(), group_id="ERL-RC-CYBER-SABOTAGE-LINEAGE-2026",
                source_id="ERL-CYBER-WEB-HISTORY-CERN", intr_receipts=chain, payload=payload,
                kv_root=kv, kv_instance_id="MYKV-TEST", captured_at="2026-09-10T20:00:00Z")


def test_rejects_broken_prior_hash(tmp_path: Path):
    payload = tmp_path / "cern.html"
    payload.write_bytes(b"x")
    kv = tmp_path / "kv"
    kv.mkdir()
    chain = make_chain(envelope_hash())
    chain[2]["prior_receipt_hash"] = "sha256:" + "0" * 64
    body = dict(chain[2]); body.pop("receipt_hash"); chain[2]["receipt_hash"] = digest(body)
    with pytest.raises(ValueError, match="prior-hash"):
        consume(dispatch=make_dispatch(), group_id="ERL-RC-CYBER-SABOTAGE-LINEAGE-2026",
                source_id="ERL-CYBER-WEB-HISTORY-CERN", intr_receipts=chain, payload=payload,
                kv_root=kv, kv_instance_id="MYKV-TEST", captured_at="2026-09-10T20:00:00Z")


def test_rejects_authority_transfer(tmp_path: Path):
    payload = tmp_path / "cern.html"
    payload.write_bytes(b"x")
    kv = tmp_path / "kv"
    kv.mkdir()
    chain = make_chain(envelope_hash())
    chain[1]["authority_transfer"] = True
    body = dict(chain[1]); body.pop("receipt_hash"); chain[1]["receipt_hash"] = digest(body)
    with pytest.raises(ValueError, match="authority"):
        consume(dispatch=make_dispatch(), group_id="ERL-RC-CYBER-SABOTAGE-LINEAGE-2026",
                source_id="ERL-CYBER-WEB-HISTORY-CERN", intr_receipts=chain, payload=payload,
                kv_root=kv, kv_instance_id="MYKV-TEST", captured_at="2026-09-10T20:00:00Z")
