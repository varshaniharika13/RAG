from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.evaluation.metrics import EvalSampleResult, summarize

DATASET_PATH = Path("data/eval/golden_dataset.jsonl")
REPORT_JSON = Path("reports/eval_report.json")
REPORT_CSV = Path("reports/eval_report.csv")


def load_dataset(path: Path) -> list[dict]:
    rows = []
    with path.open("r", encoding="utf-8") as infile:
        for line in infile:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def mock_pipeline_eval(row: dict) -> EvalSampleResult:
    supported = not row.get("unsupported", False)
    return EvalSampleResult(
        question=row["question"],
        faithfulness=0.9 if supported else 0.95,
        context_recall=0.82 if supported else 0.79,
        context_precision=0.8 if supported else 0.83,
        answer_relevance=0.88 if supported else 0.92,
        citation_correctness=0.91 if supported else 0.94,
        unsupported_refusal_correct=0.9 if not supported else 0.86,
    )


def write_reports(results: list[EvalSampleResult]) -> None:
    REPORT_JSON.parent.mkdir(parents=True, exist_ok=True)
    summary = summarize(results)
    with REPORT_JSON.open("w", encoding="utf-8") as out_json:
        json.dump({"summary": summary, "count": len(results)}, out_json, indent=2)

    with REPORT_CSV.open("w", encoding="utf-8", newline="") as out_csv:
        writer = csv.writer(out_csv)
        writer.writerow([
            "question",
            "faithfulness",
            "context_recall",
            "context_precision",
            "answer_relevance",
            "citation_correctness",
            "unsupported_refusal_correct",
        ])
        for result in results:
            writer.writerow(
                [
                    result.question,
                    result.faithfulness,
                    result.context_recall,
                    result.context_precision,
                    result.answer_relevance,
                    result.citation_correctness,
                    result.unsupported_refusal_correct,
                ]
            )


def main() -> None:
    rows = load_dataset(DATASET_PATH)
    results = [mock_pipeline_eval(row) for row in rows]
    write_reports(results)
    summary = summarize(results)

    print("Evaluation summary")
    for key, value in summary.items():
        print(f"- {key}: {value}")


if __name__ == "__main__":
    main()
