METER_TO_FEET = 3.28084


def to_meter(unit: str, value: float) -> float:
    if unit == "feet":
        return value / METER_TO_FEET
    raise ValueError(f"Unknown unit: {unit}")
