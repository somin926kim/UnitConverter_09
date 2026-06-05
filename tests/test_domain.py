"""Track B — Domain / Logic (Phase 1: D-CNV-01 ~ D-CNV-04)."""

import pytest

from converter import convert_all, to_meter


def test_d_cnv_01_to_meter_feet():
    # Given: 1 feet
    # When: to_meter("feet", 1)
    result = to_meter("feet", 1)
    # Then: 0.3048 m (±ε)
    assert result == pytest.approx(0.3048)


def test_d_cnv_02_convert_all_feet():
    # Given: 2.5 meter
    # When: convert_all("meter", 2.5)
    result = convert_all("meter", 2.5)
    # Then: 8.20210 ft (소수 5자리)
    assert result["feet"] == pytest.approx(8.20210, abs=1e-5)


def test_d_cnv_03_feet_yard_consistency():
    # Given: 1 feet
    # When: convert_all("feet", 1) — yard 값이 meter 경유 결과와 일치
    result = convert_all("feet", 1)
    # Then: meter 경유 yard와 일치
    expected_yard = round(to_meter("feet", 1) * 1.09361, 5)
    assert result["yard"] == pytest.approx(expected_yard, abs=1e-5)


def test_d_cnv_04_convert_all_yard():
    # Given: 2.5 meter
    # When: convert_all("meter", 2.5)
    result = convert_all("meter", 2.5)
    # Then: 2.73403 yard (소수 5자리)
    assert result["yard"] == pytest.approx(2.73403, abs=1e-5)
