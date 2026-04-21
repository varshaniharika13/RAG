from __future__ import annotations

import json
import logging
from typing import Sequence

from app.utils.schemas import RAGResponse, RetrievedChunk


def get_logger(name: str = "rag") -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(message)s"))
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger


def log_request(
    logger: logging.Logger,
    question: str,
    retrieved: Sequence[RetrievedChunk],
    response: RAGResponse,
    latency_ms: float,
) -> None:
    payload = {
        "question": question,
        "retrieved_chunks": [
            {
                "chunk_id": hit.chunk.chunk_id,
                "score": round(hit.score, 6),
                "source": hit.chunk.source,
            }
            for hit in retrieved
        ],
        "latency_ms": round(latency_ms, 2),
        "scores": [round(hit.score, 6) for hit in retrieved],
        "citation_presence": bool(response.citations),
        "refusal_reason": response.refusal_reason,
        "supported": response.supported,
    }
    logger.info(json.dumps(payload))
