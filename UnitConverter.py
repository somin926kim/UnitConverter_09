from converter import convert_all
from validator import ValidationError, validate

OUTPUT_UNITS = ("feet", "yard", "meter")


def process(input_str: str) -> list[str]:
    unit, value = validate(input_str)
    results = convert_all(unit, value)
    lines = []
    for target_unit in OUTPUT_UNITS:
        if target_unit in results:
            converted = results[target_unit]
            lines.append(f"{value} {unit} = {converted:.1f} {target_unit}")
    return lines


def main():
    input_str = input("Insert value for converting (ex: meter:2.5): ")
    try:
        lines = process(input_str)
    except ValidationError as e:
        print(e.args[0])
        return
    for line in lines:
        print(line)


if __name__ == "__main__":
    main()
