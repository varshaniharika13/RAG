from __future__ import annotations

import json
from pathlib import Path

from app.api.pipeline import RAGPipeline
from app.config.loader import load_settings
from app.utils.schemas import Document


def run_evaluation(settings_path: str | None = None) -> tuple[float, dict]:
    settings = load_settings(settings_path)
    sample_path = Path(settings["evaluation"]["sample_path"])
    rows = json.loads(sample_path.read_text(encoding="utf-8"))

    pipeline = RAGPipeline(settings_path)
    correct = 0
    total = len(rows)
    details = []

    for row in rows:
        doc = Document(
            doc_id=row["doc"]["doc_id"],
            title=row["doc"]["title"],
            source=row["doc"]["source"],
            text=row["doc"]["text"],
            page=row["doc"].get("page"),
        )
        res = pipeline.ask(row["question"], [doc])
        passed = bool(res.supported) == bool(row["expected_supported"])
        correct += int(passed)
        details.append({"id": row["id"], "passed": passed})

    score = (correct / total) if total else 0.0
    return score, {"total": total, "correct": correct, "details": details}


def main() -> int:
    settings = load_settings()
    threshold = settings["evaluation"]["quality_threshold"]
    score, report = run_evaluation()
    print(json.dumps({"score": score, "threshold": threshold, **report}, indent=2))
    return 0 if score >= threshold else 1


if __name__ == "__main__":
    raise SystemExit(main())
