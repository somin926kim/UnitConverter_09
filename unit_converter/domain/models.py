"""Domain value objects."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Unit:
    name: str
    ratio_to_meter: float


@dataclass(frozen=True)
class ParsedInput:
    unit: str
    value: float


@dataclass(frozen=True)
class ConversionResult:
    unit: str
    value: float
