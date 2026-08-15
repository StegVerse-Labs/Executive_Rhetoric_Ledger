#!/usr/bin/env python3
"""Fail closed when UAP evidence or derived artifacts are stored in the wrong namespace."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config" / "uap-evidence-classes.json"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def main() -> int:
    cfg = load_json(CONFIG)
    work_root = ROOT / cfg["root"]
    errors: list[str] = []

    evidence_map = cfg["evidence_classes"]
    derived_map = cfg["derived_classes"]

    # Contract integrity: no two classes may share one canonical namespace.
    locations = list(evidence_map.values()) + list(derived_map.values())
    if len(locations) != len(set(locations)):
        errors.append("evidence/derived classes share a canonical namespace")

    # Evidence namespaces are physically distinct and JSON objects self-identify.
    evidence_root = work_root / "evidence"
    if evidence_root.exists():
        for path in evidence_root.rglob("*"):
            if not path.is_file() or path.name.lower() == "readme.md":
                continue
            relative = path.relative_to(evidence_root)
            if len(relative.parts) < 2:
                errors.append(f"evidence object is not inside a class directory: {rel(path)}")
                continue
            class_dir = relative.parts[0]
            expected = None
            for class_name, configured in evidence_map.items():
                if configured == f"evidence/{class_dir}":
                    expected = class_name
                    break
            if expected is None:
                errors.append(f"unknown evidence class directory: {rel(path)}")
                continue
            if path.suffix.lower() == ".json":
                try:
                    obj = load_json(path)
                except Exception as exc:
                    errors.append(f"invalid JSON {rel(path)}: {exc}")
                    continue
                if not isinstance(obj, dict):
                    errors.append(f"evidence JSON must be an object: {rel(path)}")
                    continue
                if obj.get("evidence_class") != expected:
                    errors.append(
                        f"evidence_class mismatch at {rel(path)}: "
                        f"expected {expected!r}, got {obj.get('evidence_class')!r}"
                    )
                forbidden = {"analysis", "confidence", "hypothesis_ranking", "causal_finding"}
                present = forbidden.intersection(obj.keys())
                if present:
                    errors.append(f"analysis fields {sorted(present)} forbidden in evidence object: {rel(path)}")

    # Derived namespaces must never masquerade as evidence.
    for derived_class, namespace in derived_map.items():
        base = work_root / namespace
        if not base.exists():
            continue
        for path in base.rglob("*.json"):
            try:
                obj = load_json(path)
            except Exception as exc:
                errors.append(f"invalid JSON {rel(path)}: {exc}")
                continue
            if not isinstance(obj, dict):
                errors.append(f"derived JSON must be an object: {rel(path)}")
                continue
            if obj.get("derived_class") != derived_class:
                errors.append(
                    f"derived_class mismatch at {rel(path)}: "
                    f"expected {derived_class!r}, got {obj.get('derived_class')!r}"
                )
            if "evidence_class" in obj:
                errors.append(f"derived object may not declare evidence_class: {rel(path)}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("VALID: UAP evidence classes are physically separated and class-consistent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
