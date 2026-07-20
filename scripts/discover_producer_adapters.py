#!/usr/bin/env python3
"""Discover governed producer declarations without a hard-coded repository registry."""
import base64
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = json.loads((ROOT / "config/producer-discovery.json").read_text(encoding="utf-8"))
TOKEN = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
API = "https://api.github.com"


def request(path: str):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "executive-rhetoric-ledger-producer-discovery"}
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    req = urllib.request.Request(API + path, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def list_repositories(org: str):
    page = 1
    while True:
        rows = request(f"/orgs/{org}/repos?type=all&per_page=100&page={page}")
        if not rows:
            return
        yield from rows
        if len(rows) < 100:
            return
        page += 1


def fetch_declaration(repository: str, path: str, default_branch: str):
    encoded = urllib.parse.quote(path, safe="/")
    try:
        payload = request(f"/repos/{repository}/contents/{encoded}?ref={default_branch}")
    except urllib.error.HTTPError as error:
        if error.code == 404:
            return None
        raise
    return json.loads(base64.b64decode(payload["content"]).decode("utf-8"))


def main() -> int:
    import urllib.parse
    generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    discovered, failures = [], []
    for org in CONFIG["organization_scopes"]:
        try:
            repositories = list(list_repositories(org))
        except Exception as error:
            failures.append({"organization": org, "stage": "list", "error": type(error).__name__})
            continue
        for repo in repositories:
            if repo.get("archived"):
                continue
            repository = repo["full_name"]
            try:
                declaration = fetch_declaration(repository, CONFIG["contract_path"], repo["default_branch"])
            except Exception as error:
                failures.append({"repository": repository, "stage": "declaration", "error": type(error).__name__})
                continue
            if declaration is None:
                continue
            discovered.append({
                "repository": repository,
                "default_branch": repo["default_branch"],
                "visibility": "private" if repo.get("private") else "public",
                "declaration_path": CONFIG["contract_path"],
                "declaration": declaration,
                "discovery_status": "declared-review-required"
            })
    discovered.sort(key=lambda row: row["repository"].lower())
    output = {
        "generated_at": generated_at,
        "consumer_repository": CONFIG["consumer_repository"],
        "producers": discovered,
        "authority": {"may_discover": True, "may_register": False, "may_promote": False}
    }
    output_path = ROOT / CONFIG["output_path"]
    failure_path = ROOT / CONFIG["failure_path"]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    failure_path.write_text(json.dumps({"generated_at": generated_at, "failures": failures}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Discovered {len(discovered)} producer declaration(s); recorded {len(failures)} non-authoritative failure(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
