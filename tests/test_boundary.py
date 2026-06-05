"""Track A — UI / Boundary (Phase 1: U-IN-01 ~ U-IN-05)."""

import pytest


def test_u_in_01_empty_input():
    # Given: ""
    # When: parse/validate input
    # Then:
    pytest.fail("RED: U-IN-01 — empty input → Format error message")


def test_u_in_02_no_colon():
    # Given: "meter" (콜론 없음)
    # When: parse/validate input
    # Then:
    pytest.fail("RED: U-IN-02 — meter → Format error (콜론 없음)")


def test_u_in_03_reject_negative():
    # Given: "meter:-1"
    # When: parse/validate input
    # Then:
    pytest.fail("RED: U-IN-03 — meter:-1 → Reject negative values")


def test_u_in_04_unknown_unit():
    # Given: "mile:1"
    # When: parse/validate input
    # Then:
    pytest.fail("RED: U-IN-04 — mile:1 → Unknown unit error")


def test_u_in_05_empty_token():
    # Given: ":2.5" or "meter:"
    # When: parse/validate input
    # Then:
    pytest.fail("RED: U-IN-05 — :2.5 / meter: → Format error (빈 토큰)")
