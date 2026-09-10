#!/usr/bin/env python3
import importlib.util
import json
import tempfile
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker
from build_reclamation_target_set import build as build_target_set
from reconcile_skap_evidence import reconcile as reconcile_skap_evidence

ROOT = Path(__file__).resolve().parents[1]
FIX = ROOT / "fixtures" / "digital-data-reclamation"
SCHEMAS = {
    "inventory": ROOT / "schemas" / "personal-data-inventory.schema.json",
    "graph": ROOT / "schemas" / "data-propagation-graph.schema.json",
    "authority": ROOT / "schemas" / "derived-data-authority-receipt.schema.json",
    "skap_disclosure": ROOT / "schemas" / "skap-account-disclosure-graph.schema.json",
    "target_set": ROOT / "schemas" / "reclamation-target-set.schema.json",
    "skap_evidence_reconciliation": ROOT / "schemas" / "skap-evidence-reconciliation.schema.json",
}
SAMPLES = {
    "inventory": FIX / "personal-data-inventory.sample.json",
    "graph": FIX / "data-propagation-graph.sample.json",
    "authority": FIX / "derived-data-authority-receipt.sample.json",
    "skap_disclosure": FIX / "skap-account-disclosure-graph.sample.json",
    "target_set": FIX / "reclamation-target-set.sample.json",
    "skap_evidence_reconciliation": FIX / "skap-evidence-reconciliation.sample.json",
}


def load(path):
    return json.loads(path.read_text())


def validate(name, path):
    schema = load(SCHEMAS[name])
    doc = load(path)
    errors = sorted(
        Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(doc),
        key=lambda e: list(e.absolute_path),
    )
    if errors:
        raise SystemExit(f"{path}: " + "; ".join(e.message for e in errors))
    return doc


def check_cross_refs(inventory, graph):
    object_ids = {item["object_id"] for item in inventory["objects"]}
    for appearance in inventory["external_appearances"]:
        if appearance["object_ref"] not in object_ids:
            raise SystemExit("external appearance references unknown inventory object")

    node_ids = {node["node_id"] for node in graph["nodes"]}
    if len(node_ids) != len(graph["nodes"]):
        raise SystemExit("graph node_id values must be unique")
    edge_ids = set()
    for edge in graph["edges"]:
        if edge["edge_id"] in edge_ids:
            raise SystemExit("graph edge_id values must be unique")
        edge_ids.add(edge["edge_id"])
        if edge["from"] not in node_ids or edge["to"] not in node_ids:
            raise SystemExit("graph edge references unknown node")


def check_skap_disclosure_refs(doc):
    account_refs = {item["skap_account_ref"] for item in doc["accounts"]}
    if len(account_refs) != len(doc["accounts"]):
        raise SystemExit("SKAP disclosure graph account refs must be unique")
    org_refs = {item["org_ref"] for item in doc["organizations"]}
    if len(org_refs) != len(doc["organizations"]):
        raise SystemExit("SKAP disclosure graph organization refs must be unique")
    if not {item["provider_org_ref"] for item in doc["accounts"]}.issubset(org_refs):
        raise SystemExit("SKAP account references unknown provider organization")
    edge_ids = set()
    for edge in doc["disclosure_edges"]:
        if edge["edge_id"] in edge_ids:
            raise SystemExit("SKAP disclosure graph edge ids must be unique")
        edge_ids.add(edge["edge_id"])
        if edge["from_org_ref"] not in org_refs or edge["to_org_ref"] not in org_refs:
            raise SystemExit("SKAP disclosure edge references unknown organization")
        if not set(edge.get("skap_account_refs", [])).issubset(account_refs):
            raise SystemExit("SKAP disclosure edge references unknown SKAP account")
        if edge["evidence_state"] in {"DECLARED_BY_PROVIDER", "OBSERVED_TRANSFER", "REGULATORY_OR_COURT_RECORD", "CREDIBLE_THIRD_PARTY_REPORT"} and not edge["evidence_refs"]:
            raise SystemExit("evidence-backed SKAP disclosure edge must retain evidence refs")
        if edge["evidence_state"] in {"INFERRED_UNVERIFIED", "UNKNOWN"} and edge["reclamation_priority"] == "PRIMARY":
            raise SystemExit("unverified SKAP disclosure edge cannot become PRIMARY reclamation target")


def check_authority_fail_closed():
    invalid = FIX / "invalid-no-authority-allows-derivation.json"
    schema = load(SCHEMAS["authority"])
    errors = list(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(load(invalid)))
    if not errors:
        raise SystemExit("NO_AUTHORITY + ALLOW was incorrectly accepted")


def check_unverified_disclosure_fail_closed():
    invalid = load(FIX / "invalid-unverified-primary-disclosure-edge.json")
    try:
        check_skap_disclosure_refs(invalid)
    except SystemExit:
        return
    raise SystemExit("unverified disclosure edge was incorrectly accepted as PRIMARY")


def check_target_reconciliation(skap_disclosure):
    propagation = validate("graph", FIX / "data-propagation-graph.reconciliation.sample.json")
    expected = validate("target_set", SAMPLES["target_set"])
    actual = build_target_set(skap_disclosure, propagation, expected["generated_at"])
    if actual != expected:
        raise SystemExit("deterministic reclamation target reconciliation does not match expected fixture")

    mismatch = dict(propagation)
    mismatch["subject_ref"] = "subject:different-user"
    try:
        build_target_set(skap_disclosure, mismatch, expected["generated_at"])
    except ValueError:
        pass
    else:
        raise SystemExit("cross-subject reconciliation was incorrectly accepted")

    for target in actual["targets"]:
        if target["evidence_state"] in {"INFERRED_UNVERIFIED", "UNKNOWN"} and target["action_state"] == "ELIGIBLE":
            raise SystemExit("unverified target was incorrectly promoted to ELIGIBLE")


def check_skap_evidence_reconciliation(skap_disclosure):
    propagation = validate("graph", FIX / "data-propagation-graph.reconciliation.sample.json")
    expected = validate("skap_evidence_reconciliation", SAMPLES["skap_evidence_reconciliation"])
    actual = reconcile_skap_evidence(skap_disclosure, propagation, expected["generated_at"])
    if actual != expected:
        raise SystemExit("deterministic SKAP/evidence reconciliation does not match expected fixture")

    mismatch = dict(propagation)
    mismatch["subject_ref"] = "subject:different-user"
    try:
        reconcile_skap_evidence(skap_disclosure, mismatch, expected["generated_at"])
    except ValueError:
        pass
    else:
        raise SystemExit("cross-subject SKAP/evidence reconciliation was incorrectly accepted")

    extended = json.loads(json.dumps(skap_disclosure))
    extended["organizations"].append({"org_ref":"org:unmapped-provider","name":"Unmapped Provider","role":"ACCOUNT_PROVIDER"})
    extended["accounts"].append({"skap_account_ref":"skap:account:unmapped","provider_org_ref":"org:unmapped-provider","account_class":"other","status":"ACTIVE"})
    gap = reconcile_skap_evidence(extended, propagation, expected["generated_at"])
    unmapped = [a for a in gap["accounts"] if a["skap_account_ref"] == "skap:account:unmapped"]
    if len(unmapped) != 1 or unmapped[0]["classification"] != "KNOWN_BUT_UNMAPPED":
        raise SystemExit("known SKAP account without evidence mapping was not classified as KNOWN_BUT_UNMAPPED")

    inferred = next(e for e in skap_disclosure["disclosure_edges"] if e["evidence_state"] == "INFERRED_UNVERIFIED")
    if inferred["evidence_refs"]:
        raise SystemExit("fixture invariant changed: inferred edge unexpectedly has evidence refs")
    account = next(a for a in actual["accounts"] if a["skap_account_ref"] == "skap:account:example-social")
    if "org:example-broker" not in account["downstream_org_refs"]:
        raise SystemExit("inferred downstream organization disappeared from discovery context")
    if any(ref.startswith("observed-transfer:") for ref in account["evidence_refs"]):
        raise SystemExit("inferred edge was incorrectly promoted to observed transfer evidence")


def check_kv_custody():
    module_path = ROOT / "adapters" / "kv" / "reclamation_target_set_writer.py"
    spec = importlib.util.spec_from_file_location("reclamation_target_set_writer", module_path)
    if spec is None or spec.loader is None:
        raise SystemExit("cannot load reclamation target-set KV writer")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    target_set = load(SAMPLES["target_set"])

    with tempfile.TemporaryDirectory() as temp:
        kv_root = Path(temp)
        write_receipt = module.write_target_set(kv_root=kv_root, target_set=target_set, kv_instance_id="validator-kv")
        if write_receipt["result"] != "WRITTEN" or write_receipt["provider_deletion_success"] is not False:
            raise SystemExit("reclamation KV write receipt semantics invalid")
        readback = module.readback_target_set(kv_root=kv_root, write_receipt=write_receipt)
        if not readback["exact_byte_match"] or readback["sha256"] != write_receipt["sha256"]:
            raise SystemExit("reclamation KV exact-byte readback failed")
        retry = module.write_target_set(kv_root=kv_root, target_set=target_set, kv_instance_id="validator-kv")
        if retry["result"] != "NOOP" or retry["sha256"] != write_receipt["sha256"]:
            raise SystemExit("reclamation KV idempotent retry failed")
        cross_subject = dict(write_receipt)
        cross_subject["subject_ref"] = "subject:different-user"
        try:
            module.readback_target_set(kv_root=kv_root, write_receipt=cross_subject)
        except module.ReclamationKVError:
            pass
        else:
            raise SystemExit("cross-subject reclamation KV readback was incorrectly accepted")


def main():
    inventory = validate("inventory", SAMPLES["inventory"])
    graph = validate("graph", SAMPLES["graph"])
    validate("authority", SAMPLES["authority"])
    skap_disclosure = validate("skap_disclosure", SAMPLES["skap_disclosure"])
    check_cross_refs(inventory, graph)
    check_skap_disclosure_refs(skap_disclosure)
    check_authority_fail_closed()
    check_unverified_disclosure_fail_closed()
    check_target_reconciliation(skap_disclosure)
    check_skap_evidence_reconciliation(skap_disclosure)
    check_kv_custody()
    print("Digital Data Reclamation foundation + SKAP evidence reconciliation + KV custody validation: PASS")


if __name__ == "__main__":
    main()
