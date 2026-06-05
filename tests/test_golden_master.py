"""Golden Master — Phase 1 Core behavior snapshot (REFACTOR regression guard)."""

import pytest

from UnitConverter import process
from converter import convert_all, to_meter
from validator import FORMAT_ERROR, NEGATIVE_ERROR, ValidationError, validate

CLI_PROCESS_GOLDEN = {
    "meter:2.5": [
        "2.5 meter = 8.2 feet",
        "2.5 meter = 2.7 yard",
    ],
    "meter:1": [
        "1.0 meter = 3.3 feet",
        "1.0 meter = 1.1 yard",
    ],
    "feet:1": [
        "1.0 feet = 0.3 yard",
        "1.0 feet = 0.3 meter",
    ],
    "feet:3": [
        "3.0 feet = 1.0 yard",
        "3.0 feet = 0.9 meter",
    ],
}

CONVERT_ALL_GOLDEN = {
    ("meter", 2.5): {"feet": 8.20210, "yard": 2.73403},
    ("meter", 1): {"feet": 3.28084, "yard": 1.09361},
    ("feet", 1): {"meter": 0.3048, "yard": 0.33333},
    ("feet", 3): {"meter": 0.9144, "yard": 1.0},
}

TO_METER_GOLDEN = {
    ("feet", 1): 0.3048,
    ("meter", 2.5): 2.5,
}

VALIDATION_ERROR_GOLDEN = {
    "": FORMAT_ERROR,
    "meter": FORMAT_ERROR,
    ":2.5": FORMAT_ERROR,
    "meter:": FORMAT_ERROR,
    "meter:-1": NEGATIVE_ERROR,
    "mile:1": "Unknown unit: mile",
}

@pytest.mark.parametrize(
    ("input_str", "expected_lines"),
    list(CLI_PROCESS_GOLDEN.items()),
    ids=list(CLI_PROCESS_GOLDEN.keys()),
)
def test_golden_cli_process(input_str, expected_lines):
    assert process(input_str) == expected_lines


def test_golden_cli_main_meter_2_5(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda _: "meter:2.5")
    import UnitConverter

    UnitConverter.main()
    assert capsys.readouterr().out == (
        "2.5 meter = 8.2 feet\n2.5 meter = 2.7 yard\n"
    )


def test_golden_cli_main_validation_error(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda _: "meter:-1")
    import UnitConverter

    UnitConverter.main()
    assert capsys.readouterr().out == f"{NEGATIVE_ERROR}\n"


@pytest.mark.parametrize(
    ("unit", "value", "expected"),
    [
        (unit, value, expected)
        for (unit, value), expected in CONVERT_ALL_GOLDEN.items()
    ],
    ids=[f"{unit}:{value}" for unit, value in CONVERT_ALL_GOLDEN],
)
def test_golden_convert_all(unit, value, expected):
    result = convert_all(unit, value)
    assert result == pytest.approx(expected, abs=1e-5)


@pytest.mark.parametrize(
    ("unit", "value", "expected"),
    [(unit, value, expected) for (unit, value), expected in TO_METER_GOLDEN.items()],
    ids=[f"{unit}:{value}" for unit, value in TO_METER_GOLDEN],
)
def test_golden_to_meter(unit, value, expected):
    assert to_meter(unit, value) == pytest.approx(expected, abs=1e-5)


@pytest.mark.parametrize(
    ("input_str", "message"),
    list(VALIDATION_ERROR_GOLDEN.items()),
    ids=list(VALIDATION_ERROR_GOLDEN.keys()),
)
def test_golden_validation_errors(input_str, message):
    with pytest.raises(ValidationError) as exc_info:
        validate(input_str)
    assert exc_info.value.args[0] == message
