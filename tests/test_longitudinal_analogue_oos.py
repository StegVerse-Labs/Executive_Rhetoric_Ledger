from scripts.calibrate_longitudinal_analogue_oos import build_calibration


def _state(idx: int, a: float, b: float, a_ret: float, b_ret: float) -> dict:
    return {
        "state_id": f"s{idx}",
        "as_of_utc": f"2026-01-{idx+1:02d}T00:00:00Z",
        "feature_version": "test.v1",
        "features": {
            "a_return_1d_pct": a_ret,
            "b_return_1d_pct": b_ret,
            "cross_asset_breadth_positive_1d": float(a_ret > 0) / 2 + float(b_ret > 0) / 2,
        },
        "prices": {"A-USD": a, "B-USD": b},
        "research_authority": "ERL",
        "execution_authority": "NONE",
        "may_authorize_order": False,
    }


def test_oos_calibration_never_authorizes_strategy_or_execution():
    panel = {"states": [
        _state(0, 100, 100, 0, 0),
        _state(1, 102, 99, 2, -1),
        _state(2, 104, 98, 1.96, -1.01),
        _state(3, 103, 100, -0.96, 2.04),
        _state(4, 106, 99, 2.91, -1),
        _state(5, 108, 98, 1.89, -1.01),
    ]}
    result = build_calibration(panel, min_history=2, top_k=2, min_evaluations=20)
    assert result["evaluation_count"] == 3
    assert result["calibration_state"] == "NOT_CALIBRATED"
    assert result["strategy_influence_authorized"] is False
    assert result["execution_authority"] == "NONE"
    assert result["may_authorize_order"] is False


def test_oos_uses_only_prior_history_for_each_evaluation():
    panel = {"states": [
        _state(0, 100, 100, 0, 0),
        _state(1, 101, 99, 1, -1),
        _state(2, 102, 98, 0.99, -1.01),
        _state(3, 103, 97, 0.98, -1.02),
        _state(4, 104, 96, 0.97, -1.03),
    ]}
    result = build_calibration(panel, min_history=2, top_k=5, min_evaluations=1)
    assert [row["history_states"] for row in result["evaluations"]] == [2, 3]
    assert all(row["analogue_count"] <= row["history_states"] for row in result["evaluations"])


def test_oos_calibration_is_deterministic():
    panel = {"states": [
        _state(0, 100, 100, 0, 0),
        _state(1, 102, 99, 2, -1),
        _state(2, 101, 101, -0.98, 2.02),
        _state(3, 104, 100, 2.97, -0.99),
        _state(4, 105, 102, 0.96, 2),
    ]}
    first = build_calibration(panel, min_history=2, top_k=2, min_evaluations=20)
    second = build_calibration(panel, min_history=2, top_k=2, min_evaluations=20)
    assert first == second
