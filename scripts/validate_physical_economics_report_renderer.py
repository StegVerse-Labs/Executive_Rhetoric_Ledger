#!/usr/bin/env python3
"""End-to-end smoke validation for deterministic Physical Economics report rendering."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    hasher = load_module(ROOT / "scripts" / "finalize_physical_economics_evidence_snapshot.py", "pe_hash")
    resolver = load_module(ROOT / "scripts" / "resolve_physical_economics_report_boundary.py", "pe_resolve")
    renderer = load_module(ROOT / "scripts" / "render_physical_economics_report.py", "pe_render")
    verifier = load_module(ROOT / "scripts" / "generate_physical_economics_report_verification_receipt.py", "pe_verify")

    cases = load(ROOT / "tests" / "physical-economics-reporting" / "boundary-resolver.cases.json")["cases"]
    case = next(item for item in cases if item["case_id"] == "price-change-complete")
    request = case["request"]
    snapshot = hasher.finalize(case["snapshot"])
    matrix = load(ROOT / "contracts" / "physical-economics-report-pertinence.matrix.v0.1.json")
    boundary, errors = resolver.resolve(request, snapshot, matrix)
    failures: list[str] = []
    if errors or boundary is None:
        failures.append(f"boundary resolution failed: {errors}")
    else:
        document = renderer.build_document("REPORT-SMOKE", request, snapshot, boundary, [], [], None)
        document_schema = load(ROOT / "schemas" / "physical-economics-report-document.schema.json")
        for error in Draft202012Validator(document_schema, format_checker=FormatChecker()).iter_errors(document):
            failures.append(f"report document schema: {error.message}")
        markdown = renderer.render_markdown(document)
        if markdown.find("## Report Boundary") < 0 or markdown.find("## Findings") < 0:
            failures.append("renderer omitted required boundary/findings sections")
        elif markdown.find("## Report Boundary") > markdown.find("## Findings"):
            failures.append("renderer placed findings before report boundary")
        if document["findings"]:
            failures.append("renderer invented findings when none were supplied")
        if "No substantive finding objects were supplied" not in markdown:
            failures.append("renderer did not disclose absent governed finding objects")

        receipt = verifier.generate(
            "REPORT-SMOKE",
            markdown.encode("utf-8"),
            request,
            snapshot,
            boundary,
            renderer.RENDERER_VERSION,
        )
        receipt_schema = load(ROOT / "schemas" / "physical-economics-report-verification-receipt.schema.json")
        for error in Draft202012Validator(receipt_schema, format_checker=FormatChecker()).iter_errors(receipt):
            failures.append(f"verification receipt schema: {error.message}")
        if receipt.get("verification_state") != "VERIFIABLE":
            failures.append(f"renderer output not portable-verifiable: {receipt.get('verification_state')}")
        if receipt.get("report_content_hash") != verifier.sha256_bytes(markdown.encode("utf-8")):
            failures.append("report content hash is not reproducible")

    if failures:
        for failure in failures:
            print(f"FAIL {failure}")
        return 1

    print("PASS deterministic report document schema")
    print("PASS boundary rendered before findings")
    print("PASS no findings invented")
    print("PASS rendered report portable verification")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
