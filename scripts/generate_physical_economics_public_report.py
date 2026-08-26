#!/usr/bin/env python3
"""Execute the bounded backend transaction behind Physical Economics GENERATE_REPORT.

This orchestration does not acquire evidence from the network and does not invent
findings. It consumes a prepared evidence snapshot draft plus optional governed
finding/gate objects, finalizes the snapshot hash, resolves boundaries, renders the
report document/Markdown, and emits a portable verification receipt.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path

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


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("request", type=Path)
    parser.add_argument("snapshot_draft", type=Path)
    parser.add_argument("--report-id", required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--findings", type=Path)
    parser.add_argument("--prospective-gates", type=Path)
    parser.add_argument("--prior-delta", type=Path)
    args = parser.parse_args()

    hasher = load_module(ROOT / "scripts" / "finalize_physical_economics_evidence_snapshot.py", "pe_snapshot_hasher")
    resolver = load_module(ROOT / "scripts" / "resolve_physical_economics_report_boundary.py", "pe_boundary_resolver")
    renderer = load_module(ROOT / "scripts" / "render_physical_economics_report.py", "pe_renderer")
    verifier = load_module(ROOT / "scripts" / "generate_physical_economics_report_verification_receipt.py", "pe_verifier")

    request = load(args.request)
    snapshot = hasher.finalize(load(args.snapshot_draft))
    matrix = load(ROOT / "contracts" / "physical-economics-report-pertinence.matrix.v0.1.json")

    manifest, errors = resolver.resolve(request, snapshot, matrix)
    if errors or manifest is None:
        for error in errors:
            print(f"FAIL boundary resolution: {error}", file=sys.stderr)
        return 1

    findings = load(args.findings) if args.findings else []
    gates = load(args.prospective_gates) if args.prospective_gates else []
    prior_delta = load(args.prior_delta) if args.prior_delta else None
    document = renderer.build_document(
        args.report_id,
        request,
        snapshot,
        manifest,
        findings,
        gates,
        prior_delta,
    )
    markdown = renderer.render_markdown(document)

    out = args.output_dir
    out.mkdir(parents=True, exist_ok=True)
    snapshot_path = out / "evidence-snapshot.json"
    boundary_path = out / "boundary-manifest.json"
    document_path = out / "report-document.json"
    markdown_path = out / "report.md"
    receipt_path = out / "verification-receipt.json"

    write_json(snapshot_path, snapshot)
    write_json(boundary_path, manifest)
    write_json(document_path, document)
    markdown_path.write_text(markdown, encoding="utf-8")

    verification = verifier.generate(
        args.report_id,
        markdown.encode("utf-8"),
        request,
        snapshot,
        manifest,
        renderer.RENDERER_VERSION,
    )
    write_json(receipt_path, verification)

    if verification["verification_state"] != "VERIFIABLE":
        print(f"FAIL portable verification: {verification['verification_state']}", file=sys.stderr)
        return 1

    result = {
        "report_id": args.report_id,
        "state": "GENERATED_NOT_PUBLICLY_ACTIVATED",
        "completeness_state": manifest["completeness_state"],
        "evidence_snapshot": str(snapshot_path),
        "boundary_manifest": str(boundary_path),
        "report_document": str(document_path),
        "report_markdown": str(markdown_path),
        "verification_receipt": str(receipt_path),
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
