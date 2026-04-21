from __future__ import annotations

from app.config.loader import load_settings
from app.generation.generator import GroundedGenerator
from app.ingestion.chunking import chunk_document
from app.retrieval.retriever import HybridRetriever
from app.utils.observability import get_logger, log_request
from app.utils.schemas import Document, RAGResponse


class RAGPipeline:
    def __init__(self, settings_path: str | None = None):
        self.settings = load_settings(settings_path)
        self.logger = get_logger("rag.pipeline")
        self.generator = GroundedGenerator(
            min_score_to_answer=self.settings["retrieval"]["min_score_to_answer"]
        )

    def ask(self, question: str, docs: list[Document]) -> RAGResponse:
        chunks = []
        for doc in docs:
            chunks.extend(
                chunk_document(
                    doc,
                    chunk_size=self.settings["chunking"]["chunk_size"],
                    overlap=self.settings["chunking"]["chunk_overlap"],
                )
            )

        retriever = HybridRetriever(
            chunks,
            k1=self.settings["retrieval"]["bm25_k1"],
            b=self.settings["retrieval"]["bm25_b"],
        )
        hits = retriever.retrieve(question, top_k=self.settings["retrieval"]["top_k"])
        response, latency_ms = self.generator.answer(question, hits)
        log_request(self.logger, question, hits, response, latency_ms)
        return response
