METER_TO_FEET = 3.28084
METER_TO_YARD = 1.09361


def to_meter(unit: str, value: float) -> float:
    if unit == "meter":
        return value
    if unit == "feet":
        return value / METER_TO_FEET
    raise ValueError(f"Unknown unit: {unit}")


def convert_all(unit: str, value: float) -> dict[str, float]:
    meter_value = to_meter(unit, value)
    results = {
        "meter": round(meter_value, 5),
        "feet": round(meter_value * METER_TO_FEET, 5),
        "yard": round(meter_value * METER_TO_YARD, 5),
    }
    results.pop(unit, None)
    return results
