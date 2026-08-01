#!/usr/bin/env python3
"""Run governed validators and emit a machine-readable GitHub Actions evidence packet.

The capture process intentionally writes its receipt before enforcement so failed
validator output remains available as an uploaded diagnostic artifact.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

VALIDATORS = [
    ("assessment_trees", ["python", "scripts/validate_assessment_trees.py"]),
    ("primary_record_intake", ["python", "scripts/validate_primary_record_intake.py"]),
    ("activation_validation", ["python", "scripts/run_activation_validation.py"]),
]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def github_environment() -> dict[str, Any]:
    server = os.getenv("GITHUB_SERVER_URL", "https://github.com")
    repository = os.getenv("GITHUB_REPOSITORY", "")
    run_id = os.getenv("GITHUB_RUN_ID", "")
    run_attempt = os.getenv("GITHUB_RUN_ATTEMPT", "")
    job = os.getenv("GITHUB_JOB", "")
    return {
        "repository": repository,
        "workflow": os.getenv("GITHUB_WORKFLOW", ""),
        "workflow_ref": os.getenv("GITHUB_WORKFLOW_REF", ""),
        "event_name": os.getenv("GITHUB_EVENT_NAME", ""),
        "head_branch": os.getenv("GITHUB_REF_NAME", ""),
        "head_ref": os.getenv("GITHUB_REF", ""),
        "head_commit": os.getenv("GITHUB_SHA", ""),
        "run_id": run_id,
        "run_number": os.getenv("GITHUB_RUN_NUMBER", ""),
        "run_attempt": run_attempt,
        "job_id_environment": job,
        "actor": os.getenv("GITHUB_ACTOR", ""),
        "runner_name": os.getenv("RUNNER_NAME", ""),
        "runner_os": os.getenv("RUNNER_OS", ""),
        "run_url": f"{server}/{repository}/actions/runs/{run_id}" if repository and run_id else "",
        "attempt_url": (
            f"{server}/{repository}/actions/runs/{run_id}/attempts/{run_attempt}"
            if repository and run_id and run_attempt
            else ""
        ),
    }


def run_validator(name: str, command: list[str], output_dir: Path) -> dict[str, Any]:
    started_at = utc_now()
    completed = subprocess.run(command, text=True, capture_output=True, check=False)
    completed_at = utc_now()
    log_path = output_dir / f"{name}.log"
    log_text = (
        f"command: {' '.join(command)}\n"
        f"exit_code: {completed.returncode}\n"
        "--- stdout ---\n"
        f"{completed.stdout}"
        "\n--- stderr ---\n"
        f"{completed.stderr}"
    )
    log_path.write_text(log_text, encoding="utf-8")
    return {
        "name": name,
        "command": command,
        "command_text": " ".join(command),
        "started_at": started_at,
        "completed_at": completed_at,
        "exit_code": completed.returncode,
        "conclusion": "success" if completed.returncode == 0 else "failure",
        "stdout": completed.stdout,
        "stderr": completed.stderr,
        "log_path": str(log_path),
        "log_sha256": sha256(log_path),
        "log_byte_size": log_path.stat().st_size,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="validation_evidence/current")
    parser.add_argument("--topic-id", default="PIT-MODERN-2026-ELLIS-SCAVINO-TRANSFER")
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    started_at = utc_now()
    results = [run_validator(name, command, output_dir) for name, command in VALIDATORS]
    completed_at = utc_now()
    overall_success = all(item["exit_code"] == 0 for item in results)

    receipt = {
        "schema_version": "1.0.0",
        "receipt_type": "governed-validator-execution-evidence",
        "topic_id": args.topic_id,
        "capture_started_at": started_at,
        "capture_completed_at": completed_at,
        "execution_environment": github_environment(),
        "validators": results,
        "first_failed_validator": next(
            (item["name"] for item in results if item["exit_code"] != 0), None
        ),
        "overall_conclusion": "success" if overall_success else "failure",
        "activation_effect": "validator-layer-passed" if overall_success else "activation-blocked",
        "authority": {
            "may_promote_publication": False,
            "may_assert_primary_source_completion": False,
            "may_change_chain_node_confidence": False,
        },
        "notes": (
            "This receipt proves only the recorded validator executions for the identified commit and run. "
            "It does not establish primary-source completeness, independent corroboration, admissibility, "
            "or publication authority."
        ),
    }

    receipt_path = output_dir / "validation-execution-receipt.json"
    receipt_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    manifest = {
        "generated_at": completed_at,
        "files": [
            {
                "path": str(path),
                "sha256": sha256(path),
                "byte_size": path.stat().st_size,
            }
            for path in sorted(output_dir.iterdir())
            if path.is_file()
        ],
    }
    manifest_path = output_dir / "artifact-manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({
        "overall_conclusion": receipt["overall_conclusion"],
        "first_failed_validator": receipt["first_failed_validator"],
        "receipt_path": str(receipt_path),
        "manifest_path": str(manifest_path),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
