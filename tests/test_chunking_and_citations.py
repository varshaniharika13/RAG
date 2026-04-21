from app.generation.citation_validator import validate_citations
from app.retrieval.chunking import fixed_chunk, heading_aware_chunk, recursive_chunk
from app.types import RetrievalChunk


def test_fixed_chunk_returns_multiple_chunks() -> None:
    text = "a" * 2000
    chunks = fixed_chunk(text, size=400, overlap=50)
    assert len(chunks) > 3


def test_heading_aware_chunk_uses_headings() -> None:
    text = "# Heading A\n" + ("x" * 300) + "\n# Heading B\n" + ("y" * 300)
    chunks = heading_aware_chunk(text, max_chars=350)
    assert len(chunks) >= 2


def test_recursive_chunk_respects_size() -> None:
    text = ("policy sentence. " * 500).strip()
    chunks = recursive_chunk(text)
    assert all(len(chunk) <= 700 for chunk in chunks)


def test_citation_validator_detects_missing_chunk() -> None:
    chunks = [RetrievalChunk(chunk_id="c1", text="text", source="doc")]
    result = validate_citations(
        answer="Policy answer.",
        citations=[{"chunk_id": "c2"}],
        retrieved_chunks=chunks,
    )
    assert not result.valid
