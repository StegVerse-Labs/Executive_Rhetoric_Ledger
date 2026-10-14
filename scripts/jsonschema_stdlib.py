"""Standard-library JSON Schema (Draft 2020-12) validation; replaces jsonschema/referencing.

Provides the surface this repository uses:
  Draft202012Validator(schema, format_checker=None, registry=None)
      .iter_errors(instance) -> ValidationError objects (.message, .path,
       .absolute_path, .schema_path, .validator, .instance)
      .validate(instance) / .is_valid(instance) / .check_schema(schema)
  validate(instance, schema, format_checker=None)
  FormatChecker, ValidationError, SchemaError
  Registry().with_resources([(uri, Resource.from_contents(schema)), ...])

Fail-closed: a schema using a keyword outside SUPPORTED or ANNOTATIONS raises
SchemaError instead of being silently ignored.

Format assertion follows what `jsonschema` checks when installed without its
optional extras (the hosted workflow posture): date, email, idn-email, ipv4,
ipv6, uuid and regex. Other formats (date-time, uri, ...) are annotations, as
they were there.
"""
from __future__ import annotations

import datetime as _dt
import ipaddress
import json
import re
import uuid as _uuid
from collections import deque
from typing import Any, Callable, Iterable, Iterator
from urllib.parse import unquote, urldefrag, urljoin

SUPPORTED = {
    "$ref", "$defs", "definitions", "type", "enum", "const",
    "properties", "patternProperties", "additionalProperties", "required",
    "propertyNames", "minProperties", "maxProperties", "dependentRequired",
    "items", "prefixItems", "contains", "minContains", "maxContains",
    "minItems", "maxItems", "uniqueItems",
    "minLength", "maxLength", "pattern", "format",
    "minimum", "maximum", "exclusiveMinimum", "exclusiveMaximum", "multipleOf",
    "allOf", "anyOf", "oneOf", "not", "if", "then", "else",
}
ANNOTATIONS = {
    "$schema", "$id", "$comment", "$anchor", "title", "description", "default",
    "examples", "deprecated", "readOnly", "writeOnly", "contentMediaType",
    "contentEncoding", "$vocabulary",
}


class ValidationError(Exception):
    def __init__(self, message: str, validator: str | None = None, path: Iterable = (),
                 schema_path: Iterable = (), instance: Any = None):
        super().__init__(message)
        self.message = message
        self.validator = validator
        self.path = deque(path)
        self.absolute_path = deque(path)
        self.relative_path = self.path
        self.schema_path = deque(schema_path)
        self.instance = instance

    def __str__(self) -> str:
        return self.message


class SchemaError(Exception):
    pass


def _check_date(value: str) -> bool:
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        return False
    _dt.date.fromisoformat(value)
    return True


class FormatChecker:
    CHECKERS: dict[str, Callable[[str], bool]] = {
        "date": _check_date,
        "email": lambda v: "@" in v,
        "idn-email": lambda v: "@" in v,
        "ipv4": lambda v: bool(ipaddress.IPv4Address(v)),
        "ipv6": lambda v: bool(ipaddress.IPv6Address(v)),
        "uuid": lambda v: bool(_uuid.UUID(v)) and all(v[i] == "-" for i in (8, 13, 18, 23)),
        "regex": lambda v: bool(re.compile(v)) or True,
    }

    def __init__(self, formats: Iterable[str] | None = None):
        self.checkers = dict(self.CHECKERS) if formats is None else {f: self.CHECKERS[f] for f in formats}

    def conforms(self, instance: Any, fmt: str) -> bool:
        check = self.checkers.get(fmt)
        if check is None or not isinstance(instance, str):
            return True
        try:
            return bool(check(instance))
        except (ValueError, TypeError, re.error):
            return False


class Resource:
    def __init__(self, contents: Any):
        self.contents = contents

    @classmethod
    def from_contents(cls, contents: Any, default_specification: Any = None) -> "Resource":
        return cls(contents)


class Registry:
    def __init__(self, resources: dict[str, Resource] | None = None):
        self._resources = dict(resources or {})

    def with_resources(self, pairs: Iterable[tuple[str, Resource]]) -> "Registry":
        merged = dict(self._resources)
        merged.update({uri: res for uri, res in pairs})
        return Registry(merged)

    def with_resource(self, uri: str, resource: Resource) -> "Registry":
        return self.with_resources([(uri, resource)])

    def get(self, uri: str) -> Any:
        res = self._resources.get(uri)
        return None if res is None else res.contents

    def items(self):
        return self._resources.items()


def _r(value: Any) -> str:
    return repr(value)


def _is_type(instance: Any, kind: str) -> bool:
    if kind == "null":
        return instance is None
    if kind == "boolean":
        return isinstance(instance, bool)
    if kind == "object":
        return isinstance(instance, dict)
    if kind == "array":
        return isinstance(instance, list)
    if kind == "string":
        return isinstance(instance, str)
    if kind == "number":
        return isinstance(instance, (int, float)) and not isinstance(instance, bool)
    if kind == "integer":
        if isinstance(instance, bool):
            return False
        return isinstance(instance, int) or (isinstance(instance, float) and instance.is_integer())
    raise SchemaError(f"unknown type {kind!r}")


def _equal(a: Any, b: Any) -> bool:
    if isinstance(a, bool) or isinstance(b, bool):
        return type(a) is type(b) and a == b
    if isinstance(a, dict) and isinstance(b, dict):
        return a.keys() == b.keys() and all(_equal(a[k], b[k]) for k in a)
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(_equal(x, y) for x, y in zip(a, b))
    return a == b


def _pointer(document: Any, fragment: str) -> Any:
    if fragment in ("", "/"):
        return document
    node = document
    for token in fragment.lstrip("/").split("/"):
        token = unquote(token).replace("~1", "/").replace("~0", "~")
        node = node[int(token)] if isinstance(node, list) else node[token]
    return node


class Draft202012Validator:
    def __init__(self, schema: Any, format_checker: FormatChecker | None = None,
                 registry: Registry | None = None, resolver: Any = None):
        self.schema = schema
        self.format_checker = format_checker
        self.registry = registry or Registry()
        self.check_schema(schema)

    # --- schema checks -------------------------------------------------
    @classmethod
    def check_schema(cls, schema: Any) -> None:
        def walk(node: Any, where: str) -> None:
            if isinstance(node, bool):
                return
            if not isinstance(node, dict):
                raise SchemaError(f"{where}: schema must be an object or boolean")
            unknown = set(node) - SUPPORTED - ANNOTATIONS
            if unknown:
                raise SchemaError(f"{where}: unsupported keyword(s) {sorted(unknown)} (fail-closed)")
            for key in ("properties", "patternProperties", "$defs", "definitions", "dependentSchemas"):
                for name, sub in (node.get(key) or {}).items():
                    walk(sub, f"{where}/{key}/{name}")
            for key in ("additionalProperties", "items", "contains", "not", "if", "then", "else", "propertyNames"):
                if key in node and isinstance(node[key], (dict, bool)):
                    walk(node[key], f"{where}/{key}")
            for key in ("allOf", "anyOf", "oneOf", "prefixItems"):
                for i, sub in enumerate(node.get(key) or []):
                    walk(sub, f"{where}/{key}/{i}")
            if "pattern" in node:
                re.compile(node["pattern"])
        walk(schema, "#")

    # --- public API ----------------------------------------------------
    def iter_errors(self, instance: Any) -> Iterator[ValidationError]:
        base = self.schema.get("$id", "") if isinstance(self.schema, dict) else ""
        yield from self._descend(instance, self.schema, (), (), base, self.schema)

    def is_valid(self, instance: Any) -> bool:
        return next(self.iter_errors(instance), None) is None

    def validate(self, instance: Any) -> None:
        for error in self.iter_errors(instance):
            raise error

    # --- reference resolution -------------------------------------------
    def _resolve(self, ref: str, base: str, root: Any) -> tuple[Any, str, Any]:
        uri, fragment = urldefrag(urljoin(base, ref) if base else ref)
        if not uri or uri == urldefrag(base)[0]:
            return _pointer(root, fragment), base, root
        candidates = [uri, urldefrag(ref)[0]]
        for candidate in candidates:
            doc = self.registry.get(candidate)
            if doc is not None:
                return _pointer(doc, fragment), uri, doc
        for _, res in self.registry.items():
            doc = res.contents
            if isinstance(doc, dict) and doc.get("$id") and urldefrag(doc["$id"])[0] == uri:
                return _pointer(doc, fragment), uri, doc
        raise SchemaError(f"Unresolvable JSON pointer or reference: {ref!r}")

    # --- core ------------------------------------------------------------
    def _descend(self, instance: Any, schema: Any, path: tuple, spath: tuple,
                 base: str, root: Any) -> Iterator[ValidationError]:
        if schema is True:
            return
        if schema is False:
            yield ValidationError(f"False schema does not allow {_r(instance)}", "false", path, spath, instance)
            return
        if "$id" in schema and schema is not root:
            base = urljoin(base, schema["$id"]) if base else schema["$id"]

        def err(keyword: str, message: str) -> ValidationError:
            return ValidationError(message, keyword, path, spath + (keyword,), instance)

        if "$ref" in schema:
            target, new_base, new_root = self._resolve(schema["$ref"], base, root)
            yield from self._descend(instance, target, path, spath + ("$ref",), new_base, new_root)

        if "type" in schema:
            types = schema["type"] if isinstance(schema["type"], list) else [schema["type"]]
            if not any(_is_type(instance, t) for t in types):
                yield err("type", f"{_r(instance)} is not of type {', '.join(_r(t) for t in types)}")
                return

        if "enum" in schema and not any(_equal(instance, e) for e in schema["enum"]):
            yield err("enum", f"{_r(instance)} is not one of {_r(schema['enum'])}")
        if "const" in schema and not _equal(instance, schema["const"]):
            yield err("const", f"{_r(schema['const'])} was expected")

        for key in ("allOf", "anyOf", "oneOf"):
            if key not in schema:
                continue
            branches = schema[key]
            results = [list(self._descend(instance, sub, path, spath + (key, i), base, root))
                       for i, sub in enumerate(branches)]
            if key == "allOf":
                for errors in results:
                    yield from errors
            elif key == "anyOf" and all(results):
                yield err(key, f"{_r(instance)} is not valid under any of the given schemas")
            elif key == "oneOf":
                passing = [i for i, errors in enumerate(results) if not errors]
                if not passing:
                    yield err(key, f"{_r(instance)} is not valid under any of the given schemas")
                elif len(passing) > 1:
                    shown = ", ".join(_r(branches[i]) for i in passing)
                    yield err(key, f"{_r(instance)} is valid under each of {shown}")

        if "not" in schema and not list(self._descend(instance, schema["not"], path, spath + ("not",), base, root)):
            yield err("not", f"{_r(instance)} should not be valid under {_r(schema['not'])}")

        if "if" in schema:
            if not list(self._descend(instance, schema["if"], path, spath + ("if",), base, root)):
                if "then" in schema:
                    yield from self._descend(instance, schema["then"], path, spath + ("then",), base, root)
            elif "else" in schema:
                yield from self._descend(instance, schema["else"], path, spath + ("else",), base, root)

        if isinstance(instance, dict):
            yield from self._object(instance, schema, path, spath, base, root, err)
        elif isinstance(instance, list):
            yield from self._array(instance, schema, path, spath, base, root, err)
        elif isinstance(instance, str):
            if "minLength" in schema and len(instance) < schema["minLength"]:
                yield err("minLength", f"{_r(instance)} should be non-empty" if schema["minLength"] == 1 else f"{_r(instance)} is too short")
            if "maxLength" in schema and len(instance) > schema["maxLength"]:
                yield err("maxLength", f"{_r(instance)} is too long")
            if "pattern" in schema and not re.search(schema["pattern"], instance):
                yield err("pattern", f"{_r(instance)} does not match {_r(schema['pattern'])}")
            if "format" in schema and self.format_checker and not self.format_checker.conforms(instance, schema["format"]):
                yield err("format", f"{_r(instance)} is not a {_r(schema['format'])}")
        elif _is_type(instance, "number"):
            if "minimum" in schema and instance < schema["minimum"]:
                yield err("minimum", f"{_r(instance)} is less than the minimum of {_r(schema['minimum'])}")
            if "maximum" in schema and instance > schema["maximum"]:
                yield err("maximum", f"{_r(instance)} is greater than the maximum of {_r(schema['maximum'])}")
            if "exclusiveMinimum" in schema and instance <= schema["exclusiveMinimum"]:
                yield err("exclusiveMinimum", f"{_r(instance)} is less than or equal to the minimum of {_r(schema['exclusiveMinimum'])}")
            if "exclusiveMaximum" in schema and instance >= schema["exclusiveMaximum"]:
                yield err("exclusiveMaximum", f"{_r(instance)} is greater than or equal to the maximum of {_r(schema['exclusiveMaximum'])}")
            if "multipleOf" in schema:
                quotient = instance / schema["multipleOf"]
                if not (isinstance(quotient, float) and quotient.is_integer()) and not (isinstance(quotient, int)):
                    yield err("multipleOf", f"{_r(instance)} is not a multiple of {_r(schema['multipleOf'])}")

    def _object(self, instance: dict, schema: dict, path, spath, base, root, err) -> Iterator[ValidationError]:
        for name in schema.get("required", []):
            if name not in instance:
                yield err("required", f"{_r(name)} is a required property")
        if "minProperties" in schema and len(instance) < schema["minProperties"]:
            yield err("minProperties", f"{_r(instance)} should be non-empty" if schema["minProperties"] == 1 else f"{_r(instance)} does not have enough properties")
        if "maxProperties" in schema and len(instance) > schema["maxProperties"]:
            yield err("maxProperties", f"{_r(instance)} has too many properties")
        for name, needed in (schema.get("dependentRequired") or {}).items():
            if name in instance:
                for other in needed:
                    if other not in instance:
                        yield err("dependentRequired", f"{_r(other)} is a dependency of {_r(name)}")
        properties = schema.get("properties", {})
        patterns = schema.get("patternProperties", {})
        for name, value in instance.items():
            if name in properties:
                yield from self._descend(value, properties[name], path + (name,), spath + ("properties", name), base, root)
            for pattern, sub in patterns.items():
                if re.search(pattern, name):
                    yield from self._descend(value, sub, path + (name,), spath + ("patternProperties", pattern), base, root)
        if "propertyNames" in schema:
            for name in instance:
                yield from self._descend(name, schema["propertyNames"], path, spath + ("propertyNames",), base, root)
        if "additionalProperties" in schema:
            extras = [n for n in instance if n not in properties and not any(re.search(p, n) for p in patterns)]
            extra_schema = schema["additionalProperties"]
            if extra_schema is False:
                if extras:
                    listed = ", ".join(_r(n) for n in extras)
                    verb = "was" if len(extras) == 1 else "were"
                    yield err("additionalProperties", f"Additional properties are not allowed ({listed} {verb} unexpected)")
            else:
                for name in extras:
                    yield from self._descend(instance[name], extra_schema, path + (name,), spath + ("additionalProperties",), base, root)

    def _array(self, instance: list, schema: dict, path, spath, base, root, err) -> Iterator[ValidationError]:
        if "minItems" in schema and len(instance) < schema["minItems"]:
            yield err("minItems", f"{_r(instance)} should be non-empty" if schema["minItems"] == 1 else f"{_r(instance)} is too short")
        if "maxItems" in schema and len(instance) > schema["maxItems"]:
            yield err("maxItems", f"{_r(instance)} is too long")
        if schema.get("uniqueItems"):
            for i, a in enumerate(instance):
                if any(_equal(a, b) for b in instance[i + 1:]):
                    yield err("uniqueItems", f"{_r(instance)} has non-unique elements")
                    break
        prefix = schema.get("prefixItems", [])
        for i, sub in enumerate(prefix[: len(instance)]):
            yield from self._descend(instance[i], sub, path + (i,), spath + ("prefixItems", i), base, root)
        if "items" in schema:
            for i in range(len(prefix), len(instance)):
                yield from self._descend(instance[i], schema["items"], path + (i,), spath + ("items",), base, root)
        if "contains" in schema:
            matches = sum(1 for item in instance if not list(self._descend(item, schema["contains"], path, spath + ("contains",), base, root)))
            low = schema.get("minContains", 1)
            if matches < low:
                yield err("contains", f"{_r(instance)} does not contain items matching the given schema")
            if "maxContains" in schema and matches > schema["maxContains"]:
                yield err("maxContains", f"{_r(instance)} contains too many items matching the given schema")


def validate(instance: Any, schema: Any, cls: type | None = None, format_checker: FormatChecker | None = None,
             registry: Registry | None = None) -> None:
    (cls or Draft202012Validator)(schema, format_checker=format_checker, registry=registry).validate(instance)


def load(path: str) -> Any:
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)
