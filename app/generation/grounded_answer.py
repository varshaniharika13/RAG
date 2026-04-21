from __future__ import annotations

import json
from typing import Protocol

from app.generation.citation_validator import validate_citations
from app.types import AskResponse, RetrievalChunk

REFUSAL_TEXT = "I don’t have enough evidence in the provided documents to answer that reliably."


class ChatModel(Protocol):
    def generate(self, prompt: str) -> str:
        ...


def build_grounded_prompt(question: str, chunks: list[RetrievalChunk]) -> str:
    context_blocks = []
    for idx, chunk in enumerate(chunks, start=1):
        context_blocks.append(
            f"[{idx}] chunk_id={chunk.chunk_id} source={chunk.source}\n{chunk.text}"
        )

    context = "\n\n".join(context_blocks)

    return (
        "You are a policy QA assistant.\n"
        "Rules:\n"
        "1) Every claim must be grounded in provided evidence.\n"
        "2) Cite evidence with chunk_id for each paragraph.\n"
        "3) If evidence is weak or missing, return refusal text exactly.\n"
        "4) Return JSON with keys: answer, citations, supported.\n\n"
        f"Question: {question}\n\n"
        f"Evidence:\n{context}\n"
    )


def generate_grounded_answer(
    question: str,
    chunks: list[RetrievalChunk],
    model: ChatModel,
    supported: bool,
    confidence: float,
    unsupported_reason: str | None,
) -> AskResponse:
    if not supported:
        short_answer = REFUSAL_TEXT if confidence < 0.4 else f"{REFUSAL_TEXT} ({unsupported_reason})"
        return AskResponse(
            answer=short_answer,
            citations=[],
            supported=False,
            confidence=confidence,
            unsupported_reason=unsupported_reason,
        )

    prompt = build_grounded_prompt(question, chunks)
    raw = model.generate(prompt)

    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        return AskResponse(
            answer=REFUSAL_TEXT,
            citations=[],
            supported=False,
            confidence=0.0,
            unsupported_reason="Model returned invalid JSON",
        )

    answer = payload.get("answer", "")
    citations = payload.get("citations", [])
    citation_check = validate_citations(answer, citations, chunks)
    if not citation_check.valid:
        return AskResponse(
            answer=REFUSAL_TEXT,
            citations=[],
            supported=False,
            confidence=0.0,
            unsupported_reason="; ".join(citation_check.errors),
        )

    return AskResponse(
        answer=answer,
        citations=citations,
        supported=bool(payload.get("supported", True)),
        confidence=confidence,
        unsupported_reason=None,
    )
