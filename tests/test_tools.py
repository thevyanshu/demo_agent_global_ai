
from app.tools.common import calculate


def test_calculate_addition():
    result = calculate.invoke(
        {"expression": "10 + 5"}
    )

    assert result == "15"


def test_calculate_multiplication():
    result = calculate.invoke(
        {"expression": "25 * 4"}
    )

    assert result == "100"


def test_calculate_division():
    result = calculate.invoke(
        {"expression": "150 / 5 + 10"}
    )

    assert float(result) == 40.0
