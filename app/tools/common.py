
import ast
import operator
from datetime import datetime, timezone

from langchain_core.tools import tool


_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
}

_MAX_EXPONENT = 1000


def _evaluate(node):
    if isinstance(node, ast.Constant) and isinstance(
        node.value,
        (int, float),
    ):
        return node.value

    if isinstance(node, ast.UnaryOp):
        op = _ALLOWED_OPERATORS.get(type(node.op))

        if op is None:
            raise ValueError("Unsupported unary operator")

        return op(_evaluate(node.operand))

    if isinstance(node, ast.BinOp):
        op = _ALLOWED_OPERATORS.get(type(node.op))

        if op is None:
            raise ValueError("Unsupported binary operator")

        left = _evaluate(node.left)
        right = _evaluate(node.right)

        # Guard against resource-exhaustion via extreme exponents.
        if isinstance(node.op, ast.Pow) and (
            abs(right) > _MAX_EXPONENT
        ):
            raise ValueError(
                f"Exponent too large (max {_MAX_EXPONENT})"
            )

        return op(left, right)

    raise ValueError("Unsupported expression")


@tool
def calculate(expression: str) -> str:
    """
    Evaluate a basic arithmetic expression.

    Examples:
    - 25 * 4
    - 150 / 5 + 10
    """

    try:
        tree = ast.parse(expression, mode="eval")

        result = _evaluate(tree.body)

        return str(result)

    except Exception as exc:
        return f"Calculation error: {exc}"


@tool
def get_current_time() -> str:
    """
    Get the current UTC time.
    """

    return datetime.now(timezone.utc).isoformat()
