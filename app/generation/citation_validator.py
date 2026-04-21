from __future__ import annotations

from dataclasses import dataclass

from app.types import RetrievalChunk


@dataclass(slots=True)
class CitationValidationResult:
    valid: bool
    errors: list[str]


def validate_citations(answer: str, citations: list[dict], retrieved_chunks: list[RetrievalChunk]) -> CitationValidationResult:
    errors: list[str] = []
    if not citations:
        errors.append("No citations included in response")

    chunk_ids = {chunk.chunk_id for chunk in retrieved_chunks}
    cited_ids = set()
    for citation in citations:
        chunk_id = citation.get("chunk_id")
        if not chunk_id:
            errors.append("Citation missing chunk_id")
            continue
        cited_ids.add(chunk_id)
        if chunk_id not in chunk_ids:
            errors.append(f"Cited chunk does not exist in retrieval set: {chunk_id}")

    paragraphs = [p.strip() for p in answer.split("\n\n") if p.strip()]
    if paragraphs and not cited_ids:
        errors.append("Answer has paragraphs but no valid chunk citations")

    return CitationValidationResult(valid=not errors, errors=errors)
