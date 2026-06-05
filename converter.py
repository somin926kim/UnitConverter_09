from decimal import ROUND_HALF_UP, Decimal

METER_TO_FEET = 3.28084
METER_TO_YARD = 1.09361
_QUANT = Decimal("0.00001")


def _round5(value: float) -> float:
    return float(Decimal(str(value)).quantize(_QUANT, rounding=ROUND_HALF_UP))


def to_meter(unit: str, value: float) -> float:
    if unit == "meter":
        return value
    if unit == "feet":
        return value / METER_TO_FEET
    raise ValueError(f"Unknown unit: {unit}")


def convert_all(unit: str, value: float) -> dict[str, float]:
    meter_value = to_meter(unit, value)
    meter_decimal = Decimal(str(meter_value))
    results = {
        "meter": _round5(meter_value),
        "feet": float(
            (meter_decimal * Decimal(str(METER_TO_FEET))).quantize(
                _QUANT, rounding=ROUND_HALF_UP
            )
        ),
        "yard": float(
            (meter_decimal * Decimal(str(METER_TO_YARD))).quantize(
                _QUANT, rounding=ROUND_HALF_UP
            )
        ),
    }
    results.pop(unit, None)
    return results
