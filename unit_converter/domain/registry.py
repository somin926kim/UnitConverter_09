"""Unit registration and lookup."""

from unit_converter.domain.exceptions import UnknownUnitError
from unit_converter.domain.models import Unit


class UnitRegistry:
    def __init__(self) -> None:
        self._units: dict[str, Unit] = {}

    def register(self, name: str, ratio_to_meter: float) -> None:
        self._units[name] = Unit(name=name, ratio_to_meter=ratio_to_meter)

    def get(self, name: str) -> Unit:
        try:
            return self._units[name]
        except KeyError:
            raise UnknownUnitError(name) from None

    def all_units(self) -> list[str]:
        return list(self._units.keys())

    @classmethod
    def default(cls) -> "UnitRegistry":
        registry = cls()
        registry.register("meter", 1.0)
        registry.register("feet", 3.28084)
        registry.register("yard", 1.09361)
        return registry
