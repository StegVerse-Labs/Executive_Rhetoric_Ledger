#!/usr/bin/env python3
import json, pathlib, sys

ROOT=pathlib.Path(__file__).resolve().parents[1]
FIXTURES=ROOT/"assessments"/"linguistic-provenance"/"fixtures"

def validate_record(d):
    errors=[]
    for k in ("id","status","observed_features","enregisterment_claims","provenance_evidence","authorship_finding"):
        if k not in d: errors.append(f"missing:{k}")
    af=d.get("authorship_finding",{})
    state=af.get("state")
    source=af.get("source_class")
    if state=="supported":
        qualifying=[e for e in d.get("provenance_evidence",[]) if e.get("strength") in ("independent","strong")]
        if not qualifying:
            errors.append("supported_authorship_requires_independent_or_strong_provenance")
        if source=="unknown":
            errors.append("supported_authorship_requires_non_unknown_source_class")
    if state!="supported" and source in ("ai","human","mixed"):
        errors.append("non_supported_authorship_must_keep_source_unknown")
    # Social association can never be treated as provenance evidence.
    for e in d.get("provenance_evidence",[]):
        if e.get("type")=="other" and "style" in e.get("description","").lower():
            errors.append("style_association_is_not_provenance")
    return errors

def main():
    pos=json.loads((FIXTURES/"positive.json").read_text())
    neg=json.loads((FIXTURES/"negative-unsupported-ai-authorship.json").read_text())
    pe=validate_record(pos)
    ne=validate_record(neg)
    if pe:
        print("positive fixture failed:",pe); return 1
    if not ne:
        print("negative fixture unexpectedly passed"); return 1
    expected="supported_authorship_requires_independent_or_strong_provenance"
    if expected not in ne:
        print("negative fixture failed for wrong reason:",ne); return 1
    review_path=ROOT/"assessments"/"linguistic-provenance"/"downstream-propagation-review.json"
    review=json.loads(review_path.read_text())
    if review.get("disposition")!="NO_DOWNSTREAM_PROPAGATION_AUTHORIZED":
        print("downstream review disposition invalid"); return 1
    if review.get("raw_research_candidate_propagation_authorized") is not False:
        print("raw research-candidate propagation must remain false"); return 1
    destinations=review.get("destinations",[])
    if len(destinations)!=4:
        print("downstream review must cover four destinations"); return 1
    if any(d.get("authorized") is not False for d in destinations):
        print("destination propagation unexpectedly authorized"); return 1
    completion=review.get("completion",{})
    if completion.get("lp_008_review_complete") is not True:
        print("LP-008 review not complete"); return 1
    if completion.get("propagation_performed") is not False:
        print("LP-008 review must not claim propagation performed"); return 1
    print("PASS linguistic provenance governance")
    print("negative rejection:", expected)
    print("downstream disposition: NO_DOWNSTREAM_PROPAGATION_AUTHORIZED")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
