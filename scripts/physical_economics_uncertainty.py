#!/usr/bin/env python3
"""Fail-closed uncertainty propagation helpers for Physical Economics reports."""

from __future__ import annotations

import math
from typing import Any


def propagate_linear_standard_error(
    components: list[dict[str, Any]],
    weights: list[float],
    covariance_matrix: list[list[float]] | None = None,
) -> dict[str, Any]:
    """Propagate uncertainty for a linear combination.

    Numeric propagation is authorized only when every component has a standard
    error and either (a) all components are explicitly independent or (b) an
    explicit covariance matrix is supplied. Unknown dependence fails closed.
    """
    if len(components) != len(weights) or not components:
        return {"status": "UNRESOLVED", "reason": "component/weight shape mismatch"}

    standard_errors: list[float] = []
    dependence: list[str] = []
    for component in components:
        uncertainty = component.get("uncertainty") or {}
        if uncertainty.get("measure_type") != "STANDARD_ERROR":
            return {
                "status": "UNRESOLVED",
                "reason": "all components must provide source-native standard errors",
            }
        se = uncertainty.get("standard_error")
        if se is None or se < 0:
            return {"status": "UNRESOLVED", "reason": "missing or invalid standard error"}
        standard_errors.append(float(se))
        dependence.append(uncertainty.get("dependence_posture", "UNKNOWN_DEPENDENCE"))

    if covariance_matrix is not None:
        n = len(components)
        if len(covariance_matrix) != n or any(len(row) != n for row in covariance_matrix):
            return {"status": "UNRESOLVED", "reason": "covariance matrix shape mismatch"}
        variance = 0.0
        for i in range(n):
            for j in range(n):
                variance += weights[i] * covariance_matrix[i][j] * weights[j]
        if variance < -1e-12:
            return {"status": "UNRESOLVED", "reason": "covariance matrix produced negative variance"}
        variance = max(variance, 0.0)
        return {
            "status": "PROPAGATED",
            "method": "EXPLICIT_COVARIANCE_MATRIX",
            "standard_error": math.sqrt(variance),
        }

    if not all(item == "KNOWN_INDEPENDENT" for item in dependence):
        return {
            "status": "UNRESOLVED",
            "reason": "dependence/covariance not established; aggregate standard error not authorized",
            "component_standard_errors": standard_errors,
        }

    variance = sum((weight * se) ** 2 for weight, se in zip(weights, standard_errors))
    return {
        "status": "PROPAGATED",
        "method": "DECLARED_INDEPENDENCE",
        "standard_error": math.sqrt(variance),
    }


def combine_interval_bounds(
    components: list[dict[str, Any]], weights: list[float]
) -> dict[str, Any]:
    """Combine explicit interval bounds using interval arithmetic.

    This does not create a probabilistic confidence interval. It returns only a
    deterministic bound implied by the supplied component intervals.
    """
    if len(components) != len(weights) or not components:
        return {"status": "UNRESOLVED", "reason": "component/weight shape mismatch"}

    lower = 0.0
    upper = 0.0
    for component, weight in zip(components, weights):
        uncertainty = component.get("uncertainty") or {}
        lo = uncertainty.get("lower_bound")
        hi = uncertainty.get("upper_bound")
        if lo is None or hi is None:
            return {"status": "UNRESOLVED", "reason": "explicit interval bounds required for every component"}
        lo = float(lo)
        hi = float(hi)
        if lo > hi:
            return {"status": "UNRESOLVED", "reason": "component lower bound exceeds upper bound"}
        if weight >= 0:
            lower += weight * lo
            upper += weight * hi
        else:
            lower += weight * hi
            upper += weight * lo

    return {
        "status": "BOUNDED",
        "method": "INTERVAL_ARITHMETIC_NOT_PROBABILISTIC",
        "lower_bound": lower,
        "upper_bound": upper,
    }


def round_to_supported_precision(value: float, source_decimal_places: list[int]) -> float:
    """Prevent rendered precision from exceeding the least precise source."""
    if not source_decimal_places:
        raise ValueError("source precision is required")
    places = min(source_decimal_places)
    return round(value, places)
