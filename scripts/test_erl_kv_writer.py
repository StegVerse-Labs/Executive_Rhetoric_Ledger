#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from adapters.kv.erl_kv_writer import ERLKVWriteError, validate_manifest, write_bundle


class ERLKVWriterTests(unittest.TestCase):
    def build(self, directory: Path) -> tuple[dict, dict[str, Path]]:
        payload = directory / "source.txt"
        payload.write_text("ERL source fixture\n", encoding="utf-8")
        data = payload.read_bytes()
        manifest = {
            "schema": "stegverse.erl.kv-artifact/v1",
            "artifact_id": "ERL-2026-09-09-FIXTURE-001",
            "artifact_class": "SOURCE_CAPTURE",
            "captured_at": "2026-09-09T03:30:00Z",
            "source": {
                "title": "Fixture",
                "publisher": "Fixture Publisher",
                "primary_url": "https://example.test/source",
            },
            "storage": {
                "kv_instance_id": "kvi_fixture_001",
                "lane": "02_Research/ERL",
                "credential_material_present": False,
            },
            "objects": [{
                "filename": "source.txt",
                "role": "SOURCE_TEXT",
                "media_type": "text/plain",
                "size_bytes": len(data),
                "sha256": hashlib.sha256(data).hexdigest(),
            }],
            "relationships": [],
        }
        return manifest, {"source.txt": payload}

    def test_schema_and_idempotent_write(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            manifest, payloads = self.build(base)
            kv_root = base / "kv"
            kv_root.mkdir()
            first = write_bundle(kv_root=kv_root, manifest=manifest, payloads=payloads)
            second = write_bundle(kv_root=kv_root, manifest=manifest, payloads=payloads)
            self.assertEqual("WRITTEN", first["result"])
            self.assertEqual("NOOP", second["result"])
            self.assertTrue(first["readback_verified"])
            self.assertFalse(first["credential_material_present"])

    def test_hash_mismatch_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            manifest, payloads = self.build(base)
            manifest["objects"][0]["sha256"] = "0" * 64
            kv_root = base / "kv"
            kv_root.mkdir()
            with self.assertRaisesRegex(ERLKVWriteError, "hash mismatch"):
                write_bundle(kv_root=kv_root, manifest=manifest, payloads=payloads)

    def test_conflicting_rewrite_is_refused(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            manifest, payloads = self.build(base)
            kv_root = base / "kv"
            kv_root.mkdir()
            write_bundle(kv_root=kv_root, manifest=manifest, payloads=payloads)
            destination = kv_root / "02_Research/ERL/ERL-2026-09-09-FIXTURE-001/source.txt"
            destination.write_text("different\n", encoding="utf-8")
            with self.assertRaisesRegex(ERLKVWriteError, "conflicting artifact"):
                write_bundle(kv_root=kv_root, manifest=manifest, payloads=payloads)

    def test_path_and_credential_fields_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            manifest, _ = self.build(base)
            manifest["objects"][0]["filename"] = "../escape.txt"
            with self.assertRaisesRegex(ERLKVWriteError, "safe path component"):
                validate_manifest(manifest)
            manifest, _ = self.build(base)
            manifest["storage"]["credential_material_present"] = True
            with self.assertRaisesRegex(ERLKVWriteError, "credential material"):
                validate_manifest(manifest)


if __name__ == "__main__":
    unittest.main()
