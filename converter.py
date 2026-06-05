from unit_converter.domain.converter import UnitConverter
from unit_converter.domain.registry import UnitRegistry

_registry = UnitRegistry.default()
_converter = UnitConverter(_registry)

to_meter = _converter.to_meter
convert_all = _converter.convert_all
