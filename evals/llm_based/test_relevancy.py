
import json
from pathlib import Path

from deepeval import evaluate
from deepeval.metrics import AnswerRelevancyMetric
from deepeval.test_case import LLMTestCase

from evals.config import get_eval_settings
from evals.utils.agent_runner import run_agent


DATASET_PATH = (
    Path(__file__).resolve().parents[1]
    / "datasets"
    / "basic_cases.json"
)


def load_cases():
    with open(DATASET_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def build_relevancy_cases():
    cases = load_cases()

    relevancy_cases = [
        case
        for case in cases
        if case["type"] == "relevancy"
    ]

    test_cases = []

    for case in relevancy_cases:
        actual_output = run_agent(case["input"])

        test_cases.append(
            LLMTestCase(
                input=case["input"],
                actual_output=actual_output,
            )
        )

        print(f"\nCase: {case['id']}")
        print(f"Input: {case['input']}")
        print(f"Output: {actual_output}")

    return test_cases


def test_answer_relevancy():
    settings = get_eval_settings()

    metric = AnswerRelevancyMetric(
        threshold=settings["threshold"],
        model=settings["model"],
        include_reason=True,
    )

    test_cases = build_relevancy_cases()

    assert test_cases, "No relevancy cases found"

    evaluate(
        test_cases=test_cases,
        metrics=[metric],
    )
