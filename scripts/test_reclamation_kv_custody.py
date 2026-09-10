#!/usr/bin/env python3
from __future__ import annotations

import copy
import importlib.util
import json
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "adapters" / "kv" / "reclamation_target_set_writer.py"
FIXTURE = ROOT / "fixtures" / "digital-data-reclamation" / "reclamation-target-set.sample.json"

spec = importlib.util.spec_from_file_location("reclamation_target_set_writer", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)


def require_refusal(fn, message: str) -> None:
    try:
        fn()
    except module.ReclamationKVError:
        return
    raise AssertionError(message)


def main() -> None:
    target_set = json.loads(FIXTURE.read_text(encoding="utf-8"))
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        first = module.write_target_set(kv_root=root, target_set=target_set, kv_instance_id="test-kv-1")
        assert first["result"] == "WRITTEN"
        assert first["proof_class"] == "NATIVE_KV_WRITER_EXACT_READBACK"
        assert first["provider_deletion_success"] is False
        readback = module.readback_target_set(kv_root=root, write_receipt=first)
        assert readback["exact_byte_match"] is True
        assert readback["sha256"] == first["sha256"]
        assert readback["provider_deletion_success"] is False

        second = module.write_target_set(kv_root=root, target_set=target_set, kv_instance_id="test-kv-1")
        assert second["result"] == "NOOP"
        assert second["sha256"] == first["sha256"]

        tampered_subject = copy.deepcopy(first)
        tampered_subject["subject_ref"] = "subject:other-user"
        require_refusal(
            lambda: module.readback_target_set(kv_root=root, write_receipt=tampered_subject),
            "cross-subject receipt mutation must fail closed",
        )

        stored_path = root / first["relative_path"]
        original = stored_path.read_bytes()
        stored_path.write_bytes(original + b" ")
        require_refusal(
            lambda: module.readback_target_set(kv_root=root, write_receipt=first),
            "byte mutation must fail exact readback",
        )
        stored_path.write_bytes(original)

        conflicting = copy.deepcopy(target_set)
        conflicting["generated_at"] = "2026-09-10T04:00:00Z"
        require_refusal(
            lambda: module.write_target_set(kv_root=root, target_set=conflicting, kv_instance_id="test-kv-1"),
            "same target identity with different bytes must fail closed",
        )

    print("reclamation KV custody tests: PASS")


if __name__ == "__main__":
    main()
