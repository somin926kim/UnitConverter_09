FORMAT_ERROR = "Invalid format. Use unit:value (ex: meter:2.5)"


class ValidationError(Exception):
    pass


def validate(input_str: str) -> tuple[str, float]:
    if not input_str:
        raise ValidationError(FORMAT_ERROR)
    raise NotImplementedError
