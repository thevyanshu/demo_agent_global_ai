"""Unit tests for calculator and time tools."""

from app.tools.common import calculate, get_current_time


# ── Happy-path arithmetic ────────────────────────────────────────────

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


def test_calculate_modulo():
    result = calculate.invoke(
        {"expression": "10 % 3"}
    )
    assert result == "1"


def test_calculate_power():
    result = calculate.invoke(
        {"expression": "2 ** 10"}
    )
    assert result == "1024"


def test_calculate_negative():
    result = calculate.invoke(
        {"expression": "-5 + 3"}
    )
    assert result == "-2"


# ── Error and edge cases ─────────────────────────────────────────────

def test_calculate_division_by_zero():
    result = calculate.invoke(
        {"expression": "10 / 0"}
    )
    assert "error" in result.lower()


def test_calculate_empty_expression():
    result = calculate.invoke(
        {"expression": ""}
    )
    assert "error" in result.lower()


def test_calculate_invalid_syntax():
    result = calculate.invoke(
        {"expression": "import os"}
    )
    assert "error" in result.lower()


def test_calculate_injection_attempt():
    result = calculate.invoke(
        {"expression": "__import__('os').system('dir')"}
    )
    assert "error" in result.lower()


def test_calculate_extreme_exponent():
    """Exponents larger than 1000 must be rejected."""
    result = calculate.invoke(
        {"expression": "2 ** 10000"}
    )
    assert "error" in result.lower()
    assert "exponent" in result.lower()


# ── Time tool ─────────────────────────────────────────────────────────

def test_get_current_time_returns_iso():
    result = get_current_time.invoke({})
    # ISO 8601 with timezone info
    assert "T" in result
    assert "+" in result or "Z" in result
