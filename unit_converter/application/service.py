"""Conversion use-case orchestration."""

from unit_converter.application.formatter import TableFormatter
from unit_converter.application.parser import InputParser
from unit_converter.application.validator import InputValidator
from unit_converter.domain.converter import UnitConverter
from unit_converter.domain.registry import UnitRegistry


class ConversionService:
    def __init__(
        self,
        parser: InputParser,
        validator: InputValidator,
        converter: UnitConverter,
        formatter: TableFormatter,
    ) -> None:
        self._parser = parser
        self._validator = validator
        self._converter = converter
        self._formatter = formatter

    def run(self, raw: str) -> list[str]:
        parsed = self._parser.parse(raw)
        unit, value = self._validator.validate(parsed)
        results = self._converter.convert_all(unit, value)
        return self._formatter.format(unit, value, results)


def build_default_service() -> ConversionService:
    registry = UnitRegistry.default()
    return ConversionService(
        parser=InputParser(),
        validator=InputValidator(registry),
        converter=UnitConverter(registry),
        formatter=TableFormatter(),
    )
