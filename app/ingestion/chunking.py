from __future__ import annotations

import re
from typing import Iterable, List

from app.utils.schemas import Chunk, Document

WORD_RE = re.compile(r"\S+")


def extract_metadata_from_text(text: str) -> dict[str, str]:
    title_match = re.search(r"^#\s+(.+)$", text, flags=re.MULTILINE)
    section_match = re.search(r"^##\s+(.+)$", text, flags=re.MULTILINE)
    return {
        "title_hint": title_match.group(1).strip() if title_match else "",
        "section_hint": section_match.group(1).strip() if section_match else "",
    }


def _token_windows(tokens: List[str], chunk_size: int, overlap: int) -> Iterable[tuple[int, int]]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    if overlap < 0:
        raise ValueError("overlap must be non-negative")
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    start = 0
    step = chunk_size - overlap
    while start < len(tokens):
        end = min(start + chunk_size, len(tokens))
        yield start, end
        if end == len(tokens):
            break
        start += step


def chunk_document(doc: Document, chunk_size: int, overlap: int) -> list[Chunk]:
    tokens = WORD_RE.findall(doc.text)
    chunks: list[Chunk] = []
    meta_hints = extract_metadata_from_text(doc.text)

    for idx, (start, end) in enumerate(_token_windows(tokens, chunk_size, overlap)):
        chunk_text = " ".join(tokens[start:end])
        chunks.append(
            Chunk(
                chunk_id=f"{doc.doc_id}_c{idx}",
                doc_id=doc.doc_id,
                text=chunk_text,
                title=doc.title,
                source=doc.source,
                page=doc.page,
                metadata={
                    "start_token": start,
                    "end_token": end,
                    **meta_hints,
                },
            )
        )

    return chunks
