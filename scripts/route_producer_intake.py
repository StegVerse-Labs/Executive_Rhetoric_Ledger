#!/usr/bin/env python3
"""Convert intake results into producer-specific acknowledgments and governed review packets."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "producer_intake/results"
ACKS = ROOT / "producer_intake/acknowledgments"
REVIEW = ROOT / "producer_intake/review-queue"


def write(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    generated_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    routed = 0
    for path in sorted(RESULTS.glob("ERL-INTAKE-*.json")):
        result = json.loads(path.read_text(encoding="utf-8"))
        repo = result["producer_repository"]
        token = hashlib.sha256(f'{repo}|{result["intake_id"]}|{result["export_sha256"]}'.encode()).hexdigest()[:20]
        acknowledgment = {
            "acknowledgment_id": f"ERL-ACK-{token.upper()}",
            "generated_at": generated_at,
            "producer_repository": repo,
            "intake_id": result["intake_id"],
            "export_path": result["export_path"],
            "export_sha256": result["export_sha256"],
            "state": "received" if result["status"] == "review-required" else result["status"],
            "review_required": result["authority"]["requires_review"],
            "authority": {
                "may_acknowledge_receipt": True,
                "may_classify_final": False,
                "may_promote": False,
                "may_publish": False
            }
        }
        repo_dir = repo.replace("/", "__")
        write(ACKS / repo_dir / f'{result["intake_id"]}.json', acknowledgment)
        if result["status"] == "review-required":
            packet = {
                "review_packet_id": f"ERL-PRODUCER-REVIEW-{token.upper()}",
                "generated_at": generated_at,
                "source": "producer-intake",
                "producer_repository": repo,
                "intake_result": path.relative_to(ROOT).as_posix(),
                "acknowledgment": (ACKS / repo_dir / f'{result["intake_id"]}.json').relative_to(ROOT).as_posix(),
                "export_sha256": result["export_sha256"],
                "review_status": "pending",
                "authority": {
                    "automation_may_assign": True,
                    "automation_may_approve": False,
                    "automation_may_promote": False,
                    "automation_may_publish": False
                }
            }
            write(REVIEW / f'{packet["review_packet_id"]}.json', packet)
        routed += 1
    print(f"Routed producer intake results: {routed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
