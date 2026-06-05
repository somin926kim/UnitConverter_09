"""Track B — Domain / Logic (Phase 1: D-CNV-01 ~ D-CNV-04)."""

import pytest


def test_d_cnv_01_to_meter_feet():
    # Given: 1 feet
    # When: to_meter("feet", 1)
    # Then:
    pytest.fail("RED: D-CNV-01 — 1 feet → 0.3048 m (±ε)")


def test_d_cnv_02_convert_all_feet():
    # Given: 2.5 meter
    # When: convert_all("meter", 2.5)
    # Then:
    pytest.fail("RED: D-CNV-02 — 2.5 m → 8.20210 ft (소수 5자리)")


def test_d_cnv_03_feet_yard_consistency():
    # Given: 1 feet
    # When: convert_all("feet", 1) — yard 값이 meter 경유 결과와 일치
    # Then:
    pytest.fail("RED: D-CNV-03 — feet → yard, meter 경유 일관성")


def test_d_cnv_04_convert_all_yard():
    # Given: 2.5 meter
    # When: convert_all("meter", 2.5)
    # Then:
    pytest.fail("RED: D-CNV-04 — 2.5 m → 2.73403 yard (소수 5자리)")
