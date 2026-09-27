#!/usr/bin/env python3
"""Execute ERL's summit queue as source custody + proposition-bound research intake.

Existing safe_request transport is reused; GitHub receives candidate snapshots only.
Neither an HTTP response nor an LLM summary proves a diplomatic claim or MyKV custody.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

from process_uap_source_queue import safe_request

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "config/us-china-ai-summit-source-queue.v1.json"
CAPTURE_ROOT = Path("assessments/us-china-ai-summit/source-captures")
CYCLE_ROOT = Path("assessments/us-china-ai-summit/research-cycles")
GROUP = "ERL-RC-US-CN-AI-SUMMIT-2026"

# Candidate patterns detect that a source contains a statement, NOT that its
# underlying assertion is accurate or that a proposal has been implemented.
PROPOSITIONS = {
    "EVENT-US-VISIT": (r"September 24,? 2026|September 24 local time|September 24", {"STATEMENTS"}),
    "OFFICIAL-AI-DIALOGUE": (r"(?:super intelligence|artificial intelligence|\bSI\b).{0,130}(?:dialogue|exchange|talks)|(?:dialogue|exchange).{0,130}(?:super intelligence|artificial intelligence)", {"INCIDENT"}),
    "OFFICIAL-INCIDENT-CHANNEL": (r"(?:communication channel|notification|incident).{0,130}(?:incident|super intelligence|\bSI\b)|(?:incident).{0,130}(?:communication channel|notification)", {"INCIDENT"}),
    "EXPORT-LICENSING-BASELINE": (r"(?:H200|MI325X|semiconductor).{0,130}(?:license|China|export)|(?:license|export).{0,130}(?:H200|MI325X|semiconductor)", {"CHIPS"}),
    "DINNER-ATTENDANCE": (r"(?:state dinner|State Dinner).{0,130}(?:Xi Jinping|President Xi|delegations|business leaders)", {"CHIPS"}),
}
SENTENCE = re.compile(r"(?<=[.!?。！？])\s+")


class ExtractText(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self.skip = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() in {"script", "style", "noscript", "svg"}:
            self.skip += 1

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() in {"script", "style", "noscript", "svg"} and self.skip:
            self.skip -= 1

    def handle_data(self, data: str) -> None:
        if not self.skip:
            self.parts.append(data)


def plain_text(payload: bytes) -> str:
    parser = ExtractText()
    parser.feed(payload.decode("utf-8", errors="replace"))
    return re.sub(r"\s+", " ", " ".join(parser.parts)).strip()


def evaluate(text: str, lane: str) -> list[dict]:
    findings: list[dict] = []
    for name, (expression, lanes) in PROPOSITIONS.items():
        if lane not in lanes:
            continue
        match = re.search(expression, text, re.IGNORECASE)
        if match:
            excerpt = text[max(0, match.start() - 90):min(len(text), match.end() + 90)]
            findings.append({
                "proposition_id": name,
                "state": "SOURCE_TEXT_MATCH_REVIEW_REQUIRED",
                "verbatim_source_context": excerpt,
                "interpretation_authorized": False,
            })
        else:
            findings.append({
                "proposition_id": name,
                "state": "NO_MATCH_IN_CAPTURED_TEXT",
                "verbatim_source_context": None,
                "interpretation_authorized": False,
            })
    return findings


def run(root: Path, queue: dict, timestamp: str, fetch=safe_request) -> dict:
    if queue.get("enabled") is not True or queue.get("credential_requirement") != "NONE":
        raise ValueError("candidate queue must be enabled without credentials")
    if queue.get("network_policy") != "PUBLIC_HTTPS_ONLY_NO_AUTH":
        raise ValueError("only public HTTPS source intake is allowed")
    if queue.get("finding_authority") != "NONE" or queue.get("publication_authority") != "NONE":
        raise ValueError("source intake cannot grant finding or publication authority")
    if queue.get("lane_id") != GROUP:
        raise ValueError("wrong registry lane")
    os.environ.pop("GITHUB_TOKEN", None)
    os.environ.pop("GH_TOKEN", None)
    outputs = []
    ids: set[str] = set()
    for item in queue["items"]:
        if item.get("state") not in {"READY", "REFRESH", "CONTINUING"}:
            continue
        url = item["url"]
        host = urlparse(url).hostname
        source_id = item["source_id"]
        if source_id in ids or not host or not url.startswith("https://") or host not in item.get("allowed_hosts", []):
            raise ValueError("invalid or duplicate HTTPS source in queue")
        ids.add(source_id)
        outcome = {
            "source_id": source_id, "lane": item["lane"], "url": url,
            "source_posture": item["evidence_class"], "retrieved_at": timestamp,
            "authority_effect": "NONE", "mykv_persistence": "NOT_CLAIMED",
        }
        try:
            payload, final_url, content_type = fetch(url, item["allowed_hosts"], 35)
            if urlparse(final_url).hostname not in item["allowed_hosts"]:
                raise ValueError("redirect escaped allowlist")
            if not payload or len(payload) > 10_000_000:
                raise ValueError("source empty or oversized")
            sha = hashlib.sha256(payload).hexdigest()
            archive = root / CAPTURE_ROOT / f"{source_id}.{sha}.native"
            archive.parent.mkdir(parents=True, exist_ok=True)
            if not archive.exists():
                archive.write_bytes(payload)
            elif hashlib.sha256(archive.read_bytes()).hexdigest() != sha:
                raise ValueError("existing capture hash mismatch")
            text = plain_text(payload) if ("html" in (content_type or "").lower() or payload.lstrip().startswith(b"<")) else payload.decode("utf-8", errors="replace")
            outcome.update({
                "acquisition_state": "SOURCE_CAPTURED",
                "source_sha256": sha, "source_size_bytes": len(payload),
                "content_type": content_type, "final_url": final_url,
                "source_capture_path": archive.relative_to(root).as_posix(),
                "text_extraction": "HTML_PLAIN_TEXT" if "html" in (content_type or "").lower() else "TEXT_FALLBACK",
                "proposition_candidates": evaluate(text, item["lane"]),
            })
        except (OSError, ValueError, RuntimeError) as exc:
            outcome.update({
                "acquisition_state": "SOURCE_UNAVAILABLE",
                "failure_class": type(exc).__name__, "error": str(exc)[:500],
                "proposition_candidates": [], "retry_eligible": True,
            })
        outputs.append(outcome)
    return {
        "schema": "stegverse.erl.us-china-ai-summit-cycle/v1",
        "group_id": GROUP, "generated_at": timestamp,
        "execution_state": "ACQUISITION_CYCLE_COMPLETED_WITH_SOURCE_FAILURES" if any(x["acquisition_state"] != "SOURCE_CAPTURED" for x in outputs) else "SOURCE_ACQUISITION_COMPLETE_REVIEW_REQUIRED",
        "items": outputs,
        "source_captured_count": sum(x["acquisition_state"] == "SOURCE_CAPTURED" for x in outputs),
        "source_unavailable_count": sum(x["acquisition_state"] != "SOURCE_CAPTURED" for x in outputs),
        "finding_authorized": False, "publication_authorized": False,
        "original_intr_receipts_observed": False, "mykv_persistence_verified": False,
        "review_state": "PRIMARY_SOURCE_CANDIDATES_REQUIRE_INDEPENDENT_REVIEW",
        "nonclaims": [
            "No claim that a source statement is independently true",
            "No inferred international incident channel deployment",
            "No inferred motive or predicted geopolitical leadership",
            "No MyKV custody or runtime admission inferred from GitHub capture"
        ]
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--queue", type=Path, default=QUEUE)
    parser.add_argument("--timestamp", default=None)
    parser.add_argument("--report", type=Path, default=None)
    args = parser.parse_args()
    root = args.root.resolve()
    queue_path = args.queue if args.queue.is_absolute() else root / args.queue
    queue = json.loads(queue_path.read_text(encoding="utf-8"))
    timestamp = args.timestamp or datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    result = run(root, queue, timestamp)
    report = args.report or (CYCLE_ROOT / (timestamp[:10] + ".json"))
    report = report if report.is_absolute() else root / report
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"report": report.relative_to(root).as_posix(), "execution_state": result["execution_state"], "captured": result["source_captured_count"], "unavailable": result["source_unavailable_count"]}))
    if result["source_captured_count"] == 0:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
