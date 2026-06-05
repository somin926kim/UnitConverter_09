from unit_converter.application.exceptions import FORMAT_ERROR, NEGATIVE_ERROR, ValidationError
from unit_converter.application.parser import InputParser
from unit_converter.application.validator import InputValidator
from unit_converter.domain.registry import UnitRegistry

_parser = InputParser()
_validator = InputValidator(UnitRegistry.default())


def validate(input_str: str) -> tuple[str, float]:
    parsed = _parser.parse(input_str)
    return _validator.validate(parsed)
