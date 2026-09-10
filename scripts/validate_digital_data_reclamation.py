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
}
SAMPLES = {
    "inventory": FIX / "personal-data-inventory.sample.json",
    "graph": FIX / "data-propagation-graph.sample.json",
    "authority": FIX / "derived-data-authority-receipt.sample.json",
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
    check_cross_refs(inventory, graph)
    check_authority_fail_closed()
    print("Digital Data Reclamation foundation validation: PASS")


if __name__ == "__main__":
    main()
