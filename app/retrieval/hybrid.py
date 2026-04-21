from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Iterable

import chromadb
import numpy as np
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer

from app.types import MetadataFilter, RetrievalChunk


@dataclass(slots=True)
class HybridWeights:
    dense: float = 0.6
    sparse: float = 0.4


class HybridRetriever:
    def __init__(
        self,
        collection_name: str,
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
        persist_directory: str = "./data/processed/chroma",
        weights: HybridWeights | None = None,
    ) -> None:
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection(collection_name)
        self.embedder = SentenceTransformer(embedding_model)
        self.weights = weights or HybridWeights()

    def _build_sparse_index(self, docs: Iterable[str]) -> tuple[BM25Okapi, list[list[str]]]:
        tokenized_docs = [doc.lower().split() for doc in docs]
        return BM25Okapi(tokenized_docs), tokenized_docs

    def search(
        self,
        query: str,
        top_k: int = 20,
        metadata_filter: MetadataFilter | None = None,
    ) -> list[RetrievalChunk]:
        if top_k <= 0:
            return []

        query_embedding = self.embedder.encode(query).tolist()
        raw = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=max(top_k, 50),
            include=["documents", "metadatas", "distances", "ids"],
        )

        ids = raw.get("ids", [[]])[0]
        docs = raw.get("documents", [[]])[0]
        metadatas = raw.get("metadatas", [[]])[0]
        distances = raw.get("distances", [[]])[0]

        candidates: list[RetrievalChunk] = []
        for chunk_id, text, md, distance in zip(ids, docs, metadatas, distances, strict=False):
            if metadata_filter and not metadata_filter.matches(md):
                continue
            dense_score = 1 / (1 + float(distance))
            candidates.append(
                RetrievalChunk(
                    chunk_id=chunk_id,
                    text=text,
                    source=md.get("source", "unknown"),
                    dense_score=dense_score,
                    metadata=md,
                )
            )

        if not candidates:
            return []

        bm25, _ = self._build_sparse_index([chunk.text for chunk in candidates])
        sparse_scores = bm25.get_scores(query.lower().split())

        dense = np.array([chunk.dense_score for chunk in candidates], dtype=float)
        sparse = np.array(sparse_scores, dtype=float)

        dense_norm = dense / dense.max() if dense.max() > 0 else dense
        sparse_norm = sparse / sparse.max() if sparse.max() > 0 else sparse

        merged: list[RetrievalChunk] = []
        for idx, chunk in enumerate(candidates):
            chunk.sparse_score = float(sparse_norm[idx])
            chunk.score = (
                self.weights.dense * float(dense_norm[idx])
                + self.weights.sparse * float(sparse_norm[idx])
            )
            merged.append(chunk)

        return sorted(merged, key=lambda c: c.score, reverse=True)[:top_k]

    def explain_scores(self, chunks: list[RetrievalChunk]) -> list[dict[str, Any]]:
        score_buckets: dict[str, float] = defaultdict(float)
        for chunk in chunks:
            score_buckets[chunk.source] += chunk.score
        return [
            {"source": source, "combined_score": round(score, 4)}
            for source, score in sorted(score_buckets.items(), key=lambda item: item[1], reverse=True)
        ]
