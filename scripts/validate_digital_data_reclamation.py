#!/usr/bin/env python3
import json
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
FIX = ROOT / "fixtures" / "digital-data-reclamation"
SCHEMAS = {
    "inventory": ROOT / "schemas" / "personal-data-inventory.schema.json",
    "graph": ROOT / "schemas" / "data-propagation-graph.schema.json",
    "authority": ROOT / "schemas" / "derived-data-authority-receipt.schema.json",
    "skap_disclosure": ROOT / "schemas" / "skap-account-disclosure-graph.schema.json",
}
SAMPLES = {
    "inventory": FIX / "personal-data-inventory.sample.json",
    "graph": FIX / "data-propagation-graph.sample.json",
    "authority": FIX / "derived-data-authority-receipt.sample.json",
    "skap_disclosure": FIX / "skap-account-disclosure-graph.sample.json",
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
    provider_refs = {item["provider_org_ref"] for item in doc["accounts"]}
    if not provider_refs.issubset(org_refs):
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
    errors = list(
        Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(load(invalid))
    )
    if not errors:
        raise SystemExit("NO_AUTHORITY + ALLOW was incorrectly accepted")


def main():
    inventory = validate("inventory", SAMPLES["inventory"])
    graph = validate("graph", SAMPLES["graph"])
    validate("authority", SAMPLES["authority"])
    skap_disclosure = validate("skap_disclosure", SAMPLES["skap_disclosure"])
    check_cross_refs(inventory, graph)
    check_skap_disclosure_refs(skap_disclosure)
    check_authority_fail_closed()
    print("Digital Data Reclamation foundation validation: PASS")


if __name__ == "__main__":
    main()
