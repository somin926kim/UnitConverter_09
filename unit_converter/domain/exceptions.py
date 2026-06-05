"""Domain exceptions."""


class DomainError(Exception):
    """Base exception for domain layer errors."""


class UnknownUnitError(DomainError):
    """Raised when a unit name is not registered."""

    def __init__(self, unit: str) -> None:
        super().__init__(f"Unknown unit: {unit}")
        self.unit = unit
