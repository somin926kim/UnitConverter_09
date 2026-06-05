"""Output formatting strategies."""

OUTPUT_UNITS = ("feet", "yard", "meter")


class TableFormatter:
    def format(self, unit: str, value: float, results: dict[str, float]) -> list[str]:
        lines = []
        for target_unit in OUTPUT_UNITS:
            if target_unit in results:
                converted = results[target_unit]
                lines.append(f"{value} {unit} = {converted:.1f} {target_unit}")
        return lines
