"""Track A — UI / Boundary (Phase 1: U-IN-01 ~ U-IN-05, U-OUT-01)."""

import pytest

from validator import ValidationError, validate


def test_u_in_01_empty_input():
    # Given: ""
    # When: parse/validate input
    # Then: Format error message
    with pytest.raises(ValidationError, match="Invalid format"):
        validate("")


def test_u_in_02_no_colon():
    # Given: "meter" (콜론 없음)
    # When: parse/validate input
    # Then: Format error (콜론 없음)
    with pytest.raises(ValidationError, match="Invalid format"):
        validate("meter")


def test_u_in_03_reject_negative():
    # Given: "meter:-1"
    # When: parse/validate input
    # Then: Reject negative values
    with pytest.raises(ValidationError, match="Negative"):
        validate("meter:-1")


def test_u_in_04_unknown_unit():
    # Given: "mile:1"
    # When: parse/validate input
    # Then: Unknown unit error
    with pytest.raises(ValidationError, match="Unknown unit: mile"):
        validate("mile:1")


def test_u_in_05_empty_token():
    # Given: ":2.5" or "meter:"
    # When: parse/validate input
    # Then:
    pytest.fail("RED: U-IN-05 — :2.5 / meter: → Format error (빈 토큰)")


def test_u_out_01_meter_stdout():
    # Given: "meter:2.5"
    # When: run CLI (UnitConverter.py) with input
    # Then: stdout 2줄 (feet·yard만, README "2.5 meter = …"·소수 1자리); meter 단독/자기변환 줄 없음
    pytest.fail(
        "RED: U-OUT-01 — meter:2.5 → stdout 2줄(feet·yard, README 형식·소수 1자리); meter 줄 없음"
    )
