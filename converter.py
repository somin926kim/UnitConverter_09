METER_TO_FEET = 3.28084


def to_meter(unit: str, value: float) -> float:
    if unit == "feet":
        return value / METER_TO_FEET
    raise ValueError(f"Unknown unit: {unit}")


def convert_all(unit: str, value: float) -> dict[str, float]:
    if unit == "meter":
        return {"feet": round(value * METER_TO_FEET, 5)}
    raise ValueError(f"Unknown unit: {unit}")
