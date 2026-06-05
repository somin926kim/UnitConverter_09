"""Application-layer exceptions and message constants."""

FORMAT_ERROR = "Invalid format. Use unit:value (ex: meter:2.5)"
NEGATIVE_ERROR = "Negative values are not allowed"


class ValidationError(Exception):
    """Raised when input cannot be parsed or validated."""
