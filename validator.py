FORMAT_ERROR = "Invalid format. Use unit:value (ex: meter:2.5)"
NEGATIVE_ERROR = "Negative values are not allowed"


class ValidationError(Exception):
    pass


def validate(input_str: str) -> tuple[str, float]:
    if not input_str or ":" not in input_str:
        raise ValidationError(FORMAT_ERROR)

    unit, value_str = input_str.split(":", 1)

    try:
        value = float(value_str)
    except ValueError:
        raise ValidationError(f"Invalid number: {value_str}")

    if value < 0:
        raise ValidationError(NEGATIVE_ERROR)

    raise NotImplementedError
