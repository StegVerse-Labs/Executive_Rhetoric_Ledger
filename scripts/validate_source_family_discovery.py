#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    schema = load(ROOT / "schemas/source-family.schema.json")
    config = load(ROOT / "config/source-families.json")
    for family in config["families"]:
        errors = list(Draft202012Validator(schema).iter_errors(family))
        if errors:
            raise SystemExit(f"Source family invalid: {family['family_id']}: {errors[0].message}")
        if family["review_boundary"]["automation_may_promote"] is not False:
            raise SystemExit("Source-family discovery may not promote")

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        fixture_config = root / "families.json"
        base_config = root / "base.json"
        output = root / "runtime.json"
        receipt = root / "receipt.json"
        fixture_config.write_text(json.dumps({
            "families": [{
                "family_id": "VALIDATION_FAMILY",
                "enabled": True,
                "index_type": "local-html-index",
                "index_url": "source_fixtures/source-family-index.html",
                "source_class": "official-government",
                "allowed_hosts": ["example.gov"],
                "allowed_path_prefixes": ["/news/"],
                "relevance_terms": ["immigration", "civil rights"],
                "max_links": 10,
                "review_boundary": {
                    "automation_may_discover": True,
                    "automation_may_capture": True,
                    "automation_may_promote": False
                }
            }]
        }), encoding="utf-8")
        base_config.write_text(json.dumps({"adapters": []}), encoding="utf-8")
        subprocess.run([
            "python", str(ROOT / "scripts/discover_source_family_links.py"),
            "--config", str(fixture_config),
            "--base-config", str(base_config),
            "--output", str(output),
            "--receipt", str(receipt),
            "--discovered-at", "2026-07-22T12:00:00Z"
        ], cwd=ROOT, check=True)
        runtime = load(output)
        endpoints = [item["endpoint"] for item in runtime["adapters"]]
        expected = [
            "https://example.gov/news/immigration-enforcement-update",
            "https://example.gov/news/civil-rights-investigation"
        ]
        if endpoints != expected:
            raise SystemExit(f"Unexpected discovered endpoints: {endpoints}")
        for adapter in runtime["adapters"]:
            if adapter["review_boundary"]["automation_may_promote"] is not False:
                raise SystemExit("Discovered adapter gained promotion authority")
        result = load(receipt)
        if result["new_adapter_count"] != 2 or result["authority"]["may_promote"]:
            raise SystemExit("Discovery receipt authority/count mismatch")
    print("Validated source-family discovery and candidate-only authority.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
