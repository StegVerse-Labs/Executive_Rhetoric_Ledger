#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MEDIA = ROOT / "config" / "uap-media-corpus-inclusion.json"
CONTROL = ROOT / "config" / "uap-control-corpus-inclusion.json"
CLASS = ROOT / "config" / "uap-evidence-classes.json"
QUEUE = ROOT / "config" / "uap-media-source-queue.json"


def load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: root must be object")
    return value


def require_authority(doc: dict[str, Any], label: str, errors: list[str]) -> None:
    authority = doc.get("authority")
    if not isinstance(authority, dict):
        errors.append(f"{label}: authority missing")
        return
    expected = {
        "credential_authority": "TV/TVC",
        "credential_requirement": "NONE",
        "github_token_runtime_authority": "NONE",
        "publication_authority": False,
        "causal_finding_authority": False,
    }
    for key, value in expected.items():
        if authority.get(key) != value:
            errors.append(f"{label}: {key} must be {value!r}")


def valid_window(doc: dict[str, Any], label: str, errors: list[str]) -> tuple[str, str] | None:
    window = doc.get("date_window")
    if not isinstance(window, dict):
        errors.append(f"{label}: date_window missing")
        return None
    start, end = window.get("start"), window.get("end")
    try:
        start_date = date.fromisoformat(start)
        end_date = date.fromisoformat(end)
    except Exception:
        errors.append(f"{label}: invalid ISO date window")
        return None
    if start_date > end_date:
        errors.append(f"{label}: start after end")
    return start, end


def main() -> int:
    errors: list[str] = []
    media = load(MEDIA)
    control = load(CONTROL)
    classes = load(CLASS)
    queue = load(QUEUE)

    if media.get("contract_version") != "stegverse.erl.uap-media-corpus/v1":
        errors.append("media: contract_version mismatch")
    if media.get("goal_id") != "UAP-MEDIA-001":
        errors.append("media: wrong goal_id")
    if media.get("evidence_class") != "media-primary":
        errors.append("media: evidence_class must be media-primary")
    if media.get("evidence_class") not in classes.get("evidence_classes", {}):
        errors.append("media: evidence class absent from physical class contract")
    if media.get("long_form_threshold_minutes") != 20:
        errors.append("media: long-form threshold must remain explicit at 20 minutes for v1")
    freeze = media.get("freeze_policy") or {}
    for key in ("criteria_freeze_before_outcome_analysis", "criteria_change_requires_version_increment", "criteria_change_requires_reason_receipt", "retroactive_reclassification_must_preserve_prior_decision"):
        if freeze.get(key) is not True:
            errors.append(f"media: freeze policy {key} must be true")
    boundaries = media.get("classification_boundaries") or {}
    for key in ("publisher_metadata_is_evidence_of_release_metadata_only", "documentary_claims_are_not_facts_by_publication", "official_record_shown_in_media_must_be_independently_custodied", "testimony_extracted_from_media_remains_testimony", "analysis_may_not_reside_in_media_primary"):
        if boundaries.get(key) is not True:
            errors.append(f"media: classification boundary {key} must be true")
    require_authority(media, "media", errors)

    if control.get("contract_version") != "stegverse.erl.uap-control-corpus/v1":
        errors.append("control: contract_version mismatch")
    if control.get("goal_id") != "UAP-MEDIA-001":
        errors.append("control: wrong goal_id")
    if control.get("derived_class") != "control":
        errors.append("control: derived_class must be control")
    if control.get("derived_class") not in classes.get("derived_classes", {}):
        errors.append("control: derived class absent from physical class contract")
    policy = control.get("selection_policy") or {}
    for key in ("pre_analysis_freeze_required", "document_missing_cells", "never_impute_missing_release_counts_as_zero_without_evidence", "retain_all_exclusions_with_reason"):
        if policy.get(key) is not True:
            errors.append(f"control: selection policy {key} must be true")
    constraints = control.get("analysis_constraints") or {}
    for key in ("control_corpus_is_not_evidence_of_uap_claim_truth", "control_results_may_adjust_media_growth_inference_only", "platform_growth_and_topic_growth_must_be_reported_separately", "post_hoc_control_replacement_requires_versioned_receipt"):
        if constraints.get(key) is not True:
            errors.append(f"control: analysis constraint {key} must be true")
    require_authority(control, "control", errors)

    media_window = valid_window(media, "media", errors)
    control_window = valid_window(control, "control", errors)
    if media_window and control_window and media_window != control_window:
        errors.append("control and media date windows must match exactly")

    media_required = set(media.get("required_fields") or [])
    for field in ("media_id", "title", "publisher_or_platform", "release_date", "format", "inclusion_decision", "inclusion_reason"):
        if field not in media_required:
            errors.append(f"media: required field missing: {field}")
    control_required = set(control.get("required_fields") or [])
    for field in ("control_media_id", "topic_family", "title", "publisher_or_platform", "release_date", "inclusion_decision", "inclusion_reason"):
        if field not in control_required:
            errors.append(f"control: required field missing: {field}")

    # Any media-primary acquisition seed must remain physically in the media-primary namespace.
    expected_media_prefix = f"{classes['root'].rstrip('/')}/{classes['evidence_classes']['media-primary'].strip('/')}/"
    for item in queue.get("items", []):
        if isinstance(item, dict) and item.get("evidence_class") == "media-primary":
            dest = item.get("destination")
            if not isinstance(dest, str) or not dest.startswith(expected_media_prefix):
                errors.append(f"queue: media-primary item {item.get('source_id')} escapes canonical namespace")

    if errors:
        for error in errors:
            print(f"UAP_RESEARCH_CONTRACT_INVALID:{error}", file=sys.stderr)
        return 1
    print("UAP_RESEARCH_CONTRACTS_PASS media=1 control=1 windows_aligned=true authority=TV/TVC credential_requirement=NONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
