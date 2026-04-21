from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(slots=True)
class RetrievalLog:
    query: str
    rewritten_query: str
    retrieved_chunk_ids: list[str]
    rank_scores: list[float]
    final_answer: str
    supported: bool


class ExperimentLogger:
    def __init__(self, output_path: str = "reports/retrieval_logs.jsonl") -> None:
        self.output_path = Path(output_path)
        self.output_path.parent.mkdir(parents=True, exist_ok=True)

    def log(self, entry: RetrievalLog) -> None:
        with self.output_path.open("a", encoding="utf-8") as outfile:
            outfile.write(json.dumps(asdict(entry)) + "\n")
