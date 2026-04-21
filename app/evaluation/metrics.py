from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class EvalSampleResult:
    question: str
    faithfulness: float
    context_recall: float
    context_precision: float
    answer_relevance: float
    citation_correctness: float
    unsupported_refusal_correct: float


def average_metric(results: list[EvalSampleResult], field: str) -> float:
    if not results:
        return 0.0
    values = [getattr(result, field) for result in results]
    return round(sum(values) / len(values), 4)


def summarize(results: list[EvalSampleResult]) -> dict[str, float]:
    return {
        "faithfulness": average_metric(results, "faithfulness"),
        "context_recall": average_metric(results, "context_recall"),
        "context_precision": average_metric(results, "context_precision"),
        "answer_relevance": average_metric(results, "answer_relevance"),
        "citation_correctness": average_metric(results, "citation_correctness"),
        "unsupported_refusal_correct": average_metric(results, "unsupported_refusal_correct"),
    }
