
import json
from pathlib import Path

from app.tools.common import calculate


DATASET_PATH = (
    Path(__file__).resolve().parents[1]
    / "datasets"
    / "basic_cases.json"
)


def load_cases():
    with open(DATASET_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def normalize_number(value: str) -> float:
    return float(value.strip())


def test_calculator_cases():
    cases = load_cases()

    calculator_cases = [
        case
        for case in cases
        if case["type"] == "calculator"
    ]

    assert calculator_cases, "No calculator cases found"

    for case in calculator_cases:
        result = calculate.invoke(
            {
                "expression": case["input"]
                .replace("Calculate ", "")
                .rstrip(".")
            }
        )

        actual = normalize_number(result)
        expected = normalize_number(
            case["expected_output"]
        )

        assert actual == expected, (
            f"Failed case: {case['id']}\n"
            f"Expected: {expected}\n"
            f"Actual: {actual}"
        )
