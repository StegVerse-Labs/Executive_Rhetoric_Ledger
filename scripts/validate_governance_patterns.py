#!/usr/bin/env python3
"""Validate governance-pattern Markdown entries.

This checker gives governance-pattern records a repository-managed validation path
without treating them as political influence trees or activation evidence.
"""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
PATTERN_DIR = ROOT / "governance-patterns"
README_PATH = ROOT / "README.md"

REQUIRED_SECTIONS = {
    "# Governance Pattern:",
    "## Pattern Metadata",
    "## Purpose",
    "## Core Distinction",
    "## Surface Claim",
    "## Factual Basis",
    "## Governance Conversion",
    "## Control Comparison",
    "## Institutional Response",
    "## Outcome Evidence",
    "## Ledger Classification",
    "## Non-Claims",
    "## Receipts",
    "## Final Summary",
    "## Done Criteria",
}

REQUIRED_BOUNDARY_TERMS = {
    "governance-pattern",
    "not activation evidence",
    "authority_posture",
    "admissibility_status",
    "receipts:",
    "Non-Claims",
}

FORBIDDEN_TERMS = {
    "Activation state: activated",
    "activation_state: activated",
    "admissibility_status: activated",
    "evidence_posture: activated",
}


class GovernancePatternError(Exception):
    """Raised when governance-pattern validation fails."""


def _read(path: Path) -> str:
    if not path.exists():
        raise GovernancePatternError(f"Missing required path: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def _markdown_files() -> list[Path]:
    if not PATTERN_DIR.exists():
        raise GovernancePatternError("Missing governance-patterns directory")
    files = sorted(PATTERN_DIR.glob("*.md"))
    if not files:
        raise GovernancePatternError("No governance-pattern Markdown entries found")
    return files


def _missing_terms(text: str, terms: set[str]) -> list[str]:
    return sorted(term for term in terms if term not in text)


def _present_forbidden_terms(text: str, terms: set[str]) -> list[str]:
    return sorted(term for term in terms if term in text)


def validate_pattern(path: Path) -> list[str]:
    text = _read(path)
    errors: list[str] = []

    missing_sections = _missing_terms(text, REQUIRED_SECTIONS)
    if missing_sections:
        errors.append(
            f"{path.relative_to(ROOT)} missing required sections: "
            + ", ".join(missing_sections)
        )

    missing_boundary_terms = _missing_terms(text, REQUIRED_BOUNDARY_TERMS)
    if missing_boundary_terms:
        errors.append(
            f"{path.relative_to(ROOT)} missing required boundary terms: "
            + ", ".join(missing_boundary_terms)
        )

    forbidden_terms = _present_forbidden_terms(text, FORBIDDEN_TERMS)
    if forbidden_terms:
        errors.append(
            f"{path.relative_to(ROOT)} contains forbidden activation-overclaim terms: "
            + ", ".join(forbidden_terms)
        )

    return errors


def main() -> int:
    try:
        readme = _read(README_PATH)
        files = _markdown_files()

        errors: list[str] = []
        for path in files:
            errors.extend(validate_pattern(path))
            repo_relative = str(path.relative_to(ROOT))
            if repo_relative not in readme:
                errors.append(f"README.md does not reference governance-pattern entry: {repo_relative}")

        if "## Governance patterns" not in readme:
            errors.append("README.md is missing Governance patterns section")

        if errors:
            for error in errors:
                print(f"governance pattern validation failed: {error}", file=sys.stderr)
            return 1

        print(f"Validated {len(files)} governance-pattern entry/entries.")
        print("Governance patterns are repository-visible and non-activation-boundary preserving.")
        return 0
    except GovernancePatternError as exc:
        print(f"governance pattern validation failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
