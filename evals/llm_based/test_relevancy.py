"""
LLM-based evaluation: Answer Relevancy via DeepEval + Groq.

This test invokes the agent for each relevancy case, then scores the
agent output using the ``AnswerRelevancyMetric`` backed by a Groq
evaluation model (see ``evals.config``).

The test **asserts** that every case meets the configured threshold.
"""

import json
from pathlib import Path

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
            (
                case,
                LLMTestCase(
                    input=case["input"],
                    actual_output=actual_output,
                ),
            )
        )

        print(f"\nCase: {case['id']}")
        print(f"Input: {case['input']}")
        print(
            f"Output: {actual_output.encode('ascii', errors='replace').decode()}"
        )

    return test_cases


def test_answer_relevancy():
    settings = get_eval_settings()

    metric = AnswerRelevancyMetric(
        threshold=settings["threshold"],
        model=settings["model"],
        include_reason=True,
        async_mode=False,
    )

    case_pairs = build_relevancy_cases()

    assert case_pairs, "No relevancy cases found"

    failures = []

    for case_meta, test_case in case_pairs:
        metric.measure(test_case)
        score = metric.score
        reason = metric.reason

        print(f"\nCase: {case_meta['id']}")
        print(f"  Score:     {score}")
        print(f"  Threshold: {settings['threshold']}")
        print(f"  Reason:    {reason}")
        print(
            f"  Result:    {'PASS' if score >= settings['threshold'] else 'FAIL'}"
        )

        if score < settings["threshold"]:
            failures.append(
                f"Case {case_meta['id']}: score={score:.3f} "
                f"< threshold={settings['threshold']}"
            )

    assert not failures, (
        f"{len(failures)} relevancy case(s) below threshold:\n"
        + "\n".join(failures)
    )
