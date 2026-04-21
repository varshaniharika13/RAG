from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass(slots=True)
class Document:
    doc_id: str
    title: str
    source: str
    text: str
    page: int | None = None


@dataclass(slots=True)
class Chunk:
    chunk_id: str
    doc_id: str
    text: str
    title: str
    source: str
    page: int | None
    metadata: Dict[str, str | int | float] = field(default_factory=dict)


@dataclass(slots=True)
class RetrievedChunk:
    chunk: Chunk
    score: float


@dataclass(slots=True)
class RAGResponse:
    answer: str
    citations: List[Dict[str, str | int]]
    supported: bool
    refusal_reason: str | None = None
