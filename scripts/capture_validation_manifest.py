#!/usr/bin/env python3
"""Execute a governed validator manifest and emit durable evidence before enforcement."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def github_environment() -> dict[str, Any]:
    server = os.getenv("GITHUB_SERVER_URL", "https://github.com")
    repository = os.getenv("GITHUB_REPOSITORY", "")
    run_id = os.getenv("GITHUB_RUN_ID", "")
    attempt = os.getenv("GITHUB_RUN_ATTEMPT", "")
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
        "run_attempt": attempt,
        "job_id_environment": os.getenv("GITHUB_JOB", ""),
        "actor": os.getenv("GITHUB_ACTOR", ""),
        "runner_name": os.getenv("RUNNER_NAME", ""),
        "runner_os": os.getenv("RUNNER_OS", ""),
        "run_url": f"{server}/{repository}/actions/runs/{run_id}" if repository and run_id else "",
        "attempt_url": f"{server}/{repository}/actions/runs/{run_id}/attempts/{attempt}" if repository and run_id and attempt else "",
    }


def run_entry(entry: dict[str, Any], output_dir: Path) -> dict[str, Any]:
    started = utc_now()
    command = entry["command"]
    timeout = entry.get("timeout_seconds")
    cwd = entry.get("working_directory", ".")
    try:
        process = subprocess.run(
            command,
            cwd=cwd,
            text=True,
            capture_output=True,
            check=False,
            timeout=timeout,
        )
        exit_code = process.returncode
        stdout = process.stdout
        stderr = process.stderr
        conclusion = "success" if exit_code == 0 else "failure"
    except subprocess.TimeoutExpired as exc:
        exit_code = 124
        stdout = exc.stdout or ""
        stderr = (exc.stderr or "") + "\nvalidator timed out"
        conclusion = "error"

    completed = utc_now()
    log_name = f"{entry['id']}.log"
    log_path = output_dir / log_name
    log_path.write_text(
        f"command: {' '.join(command)}\n"
        f"exit_code: {exit_code}\n"
        f"--- stdout ---\n{stdout}\n"
        f"--- stderr ---\n{stderr}",
        encoding="utf-8",
    )
    return {
        "name": entry["id"],
        "command": command,
        "started_at": started,
        "completed_at": completed,
        "exit_code": exit_code,
        "conclusion": conclusion,
        "stdout": stdout,
        "stderr": stderr,
        "log_path": log_name,
        "log_sha256": digest(log_path),
        "log_byte_size": log_path.stat().st_size,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--output", default="validation_evidence/current")
    parser.add_argument("--subject-id", default="")
    args = parser.parse_args()

    manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    started = utc_now()
    results = [run_entry(entry, output_dir) for entry in manifest["validators"]]
    completed = utc_now()
    required_failures = {
        entry["id"] for entry in manifest["validators"] if entry.get("required", True)
    } & {result["name"] for result in results if result["exit_code"] != 0}
    success = not required_failures

    receipt = {
        "schema_version": "1.0.0",
        "receipt_type": "governed-validator-execution-evidence",
        "manifest_id": manifest["manifest_id"],
        "subject_id": args.subject_id,
        "capture_started_at": started,
        "capture_completed_at": completed,
        "execution_environment": github_environment(),
        "validators": results,
        "first_failed_validator": next(
            (result["name"] for result in results if result["exit_code"] != 0),
            None,
        ),
        "overall_conclusion": "success" if success else "failure",
        "activation_effect": "validator-layer-passed" if success else "activation-blocked",
        "authority": {
            "may_promote_publication": False,
            "may_assert_primary_source_completion": False,
            "may_change_chain_node_confidence": False,
        },
        "notes": "Validator success proves only recorded execution for the identified manifest, commit, and run.",
    }
    receipt_path = output_dir / "validation-execution-receipt.json"
    receipt_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")

    files = []
    for path in sorted(output_dir.iterdir()):
        if path.is_file():
            files.append(
                {
                    "path": path.name,
                    "sha256": digest(path),
                    "byte_size": path.stat().st_size,
                }
            )
    manifest_path = output_dir / "artifact-manifest.json"
    manifest_path.write_text(
        json.dumps(
            {
                "generated_at": completed,
                "manifest_id": manifest["manifest_id"],
                "files": files,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    print(
        json.dumps(
            {
                "overall_conclusion": receipt["overall_conclusion"],
                "receipt_path": str(receipt_path),
                "manifest_path": str(manifest_path),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
