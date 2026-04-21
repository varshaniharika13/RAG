from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Any


@dataclass(slots=True)
class RetrievalChunk:
    chunk_id: str
    text: str
    source: str
    score: float = 0.0
    dense_score: float = 0.0
    sparse_score: float = 0.0
    rerank_score: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class MetadataFilter:
    document_type: str | None = None
    category: str | None = None
    source: str | None = None
    start_date: date | None = None
    end_date: date | None = None

    def matches(self, metadata: dict[str, Any]) -> bool:
        if self.document_type and metadata.get("document_type") != self.document_type:
            return False
        if self.category and metadata.get("category") != self.category:
            return False
        if self.source and metadata.get("source") != self.source:
            return False

        doc_date_raw = metadata.get("date")
        if (self.start_date or self.end_date) and not doc_date_raw:
            return False
        if doc_date_raw:
            try:
                year, month, day = map(int, str(doc_date_raw).split("-"))
                doc_date = date(year, month, day)
            except ValueError:
                return False
            if self.start_date and doc_date < self.start_date:
                return False
            if self.end_date and doc_date > self.end_date:
                return False

        return True


@dataclass(slots=True)
class RetrievalDebug:
    query: str
    rewritten_query: str
    candidates: list[RetrievalChunk]
    selected: list[RetrievalChunk]


@dataclass(slots=True)
class AskResponse:
    answer: str
    citations: list[dict[str, str | int]]
    supported: bool
    confidence: float
    unsupported_reason: str | None = None
