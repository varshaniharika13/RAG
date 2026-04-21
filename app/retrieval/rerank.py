from __future__ import annotations

from sentence_transformers import CrossEncoder

from app.types import RetrievalChunk


class CrossEncoderReranker:
    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2") -> None:
        self.model = CrossEncoder(model_name)

    def rerank(self, query: str, candidates: list[RetrievalChunk], top_k: int = 5) -> list[RetrievalChunk]:
        if not candidates:
            return []
        pairs = [(query, chunk.text) for chunk in candidates]
        scores = self.model.predict(pairs)
        for chunk, score in zip(candidates, scores, strict=False):
            chunk.rerank_score = float(score)
        reranked = sorted(candidates, key=lambda c: c.rerank_score, reverse=True)
        return reranked[:top_k]
