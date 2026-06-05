"""Parse unit:value input strings."""

from unit_converter.application.exceptions import FORMAT_ERROR, ValidationError
from unit_converter.domain.models import ParsedInput


class InputParser:
    def parse(self, input_str: str) -> ParsedInput:
        if not input_str or ":" not in input_str:
            raise ValidationError(FORMAT_ERROR)

        unit, value_str = input_str.split(":", 1)

        if not unit or not value_str:
            raise ValidationError(FORMAT_ERROR)

        try:
            value = float(value_str)
        except ValueError:
            raise ValidationError(f"Invalid number: {value_str}")

        return ParsedInput(unit=unit, value=value)
