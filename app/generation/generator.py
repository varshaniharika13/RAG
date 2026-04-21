from __future__ import annotations

import time
from typing import Sequence

from app.utils.schemas import RAGResponse, RetrievedChunk


def format_citation(chunk: RetrievedChunk) -> dict[str, str | int]:
    citation = {
        "doc": chunk.chunk.title,
        "source": chunk.chunk.source,
        "chunk_id": chunk.chunk.chunk_id,
    }
    if chunk.chunk.page is not None:
        citation["page"] = chunk.chunk.page
    return citation


class GroundedGenerator:
    def __init__(self, min_score_to_answer: float):
        self.min_score_to_answer = min_score_to_answer

    def answer(self, question: str, retrieved: Sequence[RetrievedChunk]) -> tuple[RAGResponse, float]:
        start = time.perf_counter()
        if not retrieved:
            response = RAGResponse(
                answer="I don't know based on the provided documents.",
                citations=[],
                supported=False,
                refusal_reason="no_retrieval_hits",
            )
            return response, (time.perf_counter() - start) * 1000

        top = retrieved[0]
        if top.score < self.min_score_to_answer:
            response = RAGResponse(
                answer="I don't know based on the provided documents.",
                citations=[],
                supported=False,
                refusal_reason="low_evidence_score",
            )
            return response, (time.perf_counter() - start) * 1000

        snippets = [f"- {item.chunk.text[:180]}" for item in retrieved[:2]]
        answer = f"Based on the policy corpus, here's what I found:\n" + "\n".join(snippets)
        citations = [format_citation(item) for item in retrieved[:2]]
        response = RAGResponse(answer=answer, citations=citations, supported=True)
        return response, (time.perf_counter() - start) * 1000
