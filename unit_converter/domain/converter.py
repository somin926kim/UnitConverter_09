"""Unit conversion logic."""

from decimal import ROUND_HALF_UP, Decimal

from unit_converter.domain.registry import UnitRegistry

_QUANT = Decimal("0.00001")


def _round5(value: float) -> float:
    return float(Decimal(str(value)).quantize(_QUANT, rounding=ROUND_HALF_UP))


class UnitConverter:
    def __init__(self, registry: UnitRegistry) -> None:
        self._registry = registry

    def to_meter(self, unit: str, value: float) -> float:
        if unit == "meter":
            return value
        if unit == "feet":
            return value / self._registry.get("feet").ratio_to_meter
        raise ValueError(f"Unknown unit: {unit}")

    def convert_all(self, unit: str, value: float) -> dict[str, float]:
        meter_value = self.to_meter(unit, value)
        meter_decimal = Decimal(str(meter_value))
        feet_ratio = self._registry.get("feet").ratio_to_meter
        yard_ratio = self._registry.get("yard").ratio_to_meter
        results = {
            "meter": _round5(meter_value),
            "feet": float(
                (meter_decimal * Decimal(str(feet_ratio))).quantize(
                    _QUANT, rounding=ROUND_HALF_UP
                )
            ),
            "yard": float(
                (meter_decimal * Decimal(str(yard_ratio))).quantize(
                    _QUANT, rounding=ROUND_HALF_UP
                )
            ),
        }
        results.pop(unit, None)
        return results
