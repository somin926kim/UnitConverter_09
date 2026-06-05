"""Validate parsed input against business rules."""

from unit_converter.application.exceptions import NEGATIVE_ERROR, ValidationError
from unit_converter.domain.exceptions import UnknownUnitError
from unit_converter.domain.models import ParsedInput
from unit_converter.domain.registry import UnitRegistry


class InputValidator:
    def __init__(self, registry: UnitRegistry) -> None:
        self._registry = registry

    def validate(self, parsed: ParsedInput) -> tuple[str, float]:
        if parsed.value < 0:
            raise ValidationError(NEGATIVE_ERROR)

        try:
            self._registry.get(parsed.unit)
        except UnknownUnitError:
            raise ValidationError(f"Unknown unit: {parsed.unit}") from None

        return parsed.unit, parsed.value
