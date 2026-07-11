#!/usr/bin/env python3
"""Validate the Executive Rhetoric Ledger related-repository network."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "related-repository-network.schema.json"
MANIFEST_PATH = ROOT / "integration" / "related-repositories.json"
DOC_PATH = ROOT / "integration" / "related-repositories.md"
README_PATH = ROOT / "README.md"

REQUIRED_REPOSITORIES = {
    "StegVerse-Labs/VAwatchdog",
    "StegVerse-Labs/StegScholar",
    "StegVerse-Labs/StegSocials",
    "StegVerse-Labs/Patents",
    "StegVerse-Labs/Administrations",
    "StegVerse-Labs/Trumpality",
    "StegVerse-Labs/Giuffre-ality",
    "StegVerse-Labs/Maxwellality",
    "StegVerse-Labs/Epsteinality",
    "StegVerse-Labs/Talarico",
    "StegVerse-Labs/FREE-DOM_OverSight",
    "StegVerse-Labs/Randolph_Geneaology_Hub",
    "StegVerse-Labs/StegLearn",
    "StegVerse-Labs/StegBiography",
}


def load_json(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Unable to load {path.relative_to(ROOT)}: {exc}") from exc


def main() -> int:
    failures: list[str] = []

    try:
        schema = load_json(SCHEMA_PATH)
        manifest = load_json(MANIFEST_PATH)
    except ValueError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1

    validator = Draft202012Validator(schema)
    for error in sorted(validator.iter_errors(manifest), key=lambda item: list(item.path)):
        location = ".".join(str(part) for part in error.path) or "<root>"
        failures.append(f"{MANIFEST_PATH.relative_to(ROOT)}:{location}: {error.message}")

    if isinstance(manifest, dict):
        repositories = manifest.get("repositories", [])
        names = [
            str(item.get("repository", ""))
            for item in repositories
            if isinstance(item, dict)
        ]
        duplicate_names = sorted({name for name in names if names.count(name) > 1})
        for name in duplicate_names:
            failures.append(f"duplicate repository relationship: {name}")

        missing = sorted(REQUIRED_REPOSITORIES - set(names))
        unexpected = sorted(set(names) - REQUIRED_REPOSITORIES)
        for name in missing:
            failures.append(f"required related repository missing: {name}")
        for name in unexpected:
            failures.append(f"unexpected repository requires governed review before inclusion: {name}")

        doc_text = DOC_PATH.read_text(encoding="utf-8") if DOC_PATH.exists() else ""
        readme_text = README_PATH.read_text(encoding="utf-8") if README_PATH.exists() else ""
        for name in names:
            if name not in doc_text:
                failures.append(f"{DOC_PATH.relative_to(ROOT)} does not mention {name}")
        if "integration/related-repositories.md" not in readme_text:
            failures.append("README.md must link integration/related-repositories.md")
        if "integration/related-repositories.json" not in readme_text:
            failures.append("README.md must link integration/related-repositories.json")

        for item in repositories:
            if not isinstance(item, dict):
                continue
            direction = item.get("ingestion_direction")
            contributions = set(item.get("allowed_contributions", []))
            if direction == "ledger-to-publication-surface" and contributions != {"educational-summaries"}:
                failures.append(
                    f"{item.get('repository')}: publication-only surface may accept only educational-summaries"
                )

    if failures:
        print("Related repository network validation failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    print(f"Validated {len(REQUIRED_REPOSITORIES)} governed related-repository relationships.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
