from __future__ import annotations

from dataclasses import dataclass

from app.retrieval.hybrid import HybridRetriever
from app.retrieval.query_rewrite import rewrite_query
from app.retrieval.rerank import CrossEncoderReranker
from app.types import MetadataFilter, RetrievalDebug, RetrievalChunk


@dataclass(slots=True)
class RetrievalThresholds:
    min_combined_score: float = 0.35
    min_rerank_score: float = 0.1
    min_supporting_chunks: int = 2


class RetrievalPipeline:
    def __init__(
        self,
        retriever: HybridRetriever,
        reranker: CrossEncoderReranker,
        thresholds: RetrievalThresholds | None = None,
    ) -> None:
        self.retriever = retriever
        self.reranker = reranker
        self.thresholds = thresholds or RetrievalThresholds()

    def retrieve(
        self,
        query: str,
        metadata_filter: MetadataFilter | None = None,
        retrieval_k: int = 20,
        final_k: int = 5,
    ) -> RetrievalDebug:
        rewritten_query = rewrite_query(query)
        candidates = self.retriever.search(
            rewritten_query,
            top_k=retrieval_k,
            metadata_filter=metadata_filter,
        )
        selected = self.reranker.rerank(rewritten_query, candidates, top_k=final_k)
        return RetrievalDebug(
            query=query,
            rewritten_query=rewritten_query,
            candidates=candidates,
            selected=selected,
        )

    def support_strength(self, chunks: list[RetrievalChunk]) -> tuple[bool, float, str | None]:
        if not chunks:
            return False, 0.0, "No chunks retrieved"

        high_combined = [c for c in chunks if c.score >= self.thresholds.min_combined_score]
        high_rerank = [c for c in chunks if c.rerank_score >= self.thresholds.min_rerank_score]

        supporting = min(len(high_combined), len(high_rerank))
        confidence = 0.5 * (sum(c.score for c in chunks) / len(chunks)) + 0.5 * (
            sum(max(c.rerank_score, 0.0) for c in chunks) / len(chunks)
        )
        supported = supporting >= self.thresholds.min_supporting_chunks

        reason = None
        if not supported:
            reason = (
                f"Only {supporting} chunks satisfied score thresholds; "
                f"need {self.thresholds.min_supporting_chunks}."
            )

        return supported, round(confidence, 4), reason
