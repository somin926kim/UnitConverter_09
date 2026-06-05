from unit_converter.application.service import build_default_service
from validator import ValidationError

_service = build_default_service()


def process(input_str: str) -> list[str]:
    return _service.run(input_str)


def main():
    service = build_default_service()
    raw = input("Insert value for converting (ex: meter:2.5): ")
    try:
        for line in service.run(raw):
            print(line)
    except ValidationError as e:
        print(e.args[0])


if __name__ == "__main__":
    main()
