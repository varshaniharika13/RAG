from app.ingestion.chunking import chunk_document, extract_metadata_from_text
from app.utils.schemas import Document


def test_chunking_overlap_and_count():
    text = " ".join([f"tok{i}" for i in range(20)])
    doc = Document(doc_id="d1", title="Doc", source="x.md", text=text)
    chunks = chunk_document(doc, chunk_size=8, overlap=2)

    assert len(chunks) == 3
    assert chunks[0].metadata["start_token"] == 0
    assert chunks[1].metadata["start_token"] == 6


def test_metadata_extraction():
    text = "# Main Title\nBody\n## Section A\nMore"
    meta = extract_metadata_from_text(text)
    assert meta["title_hint"] == "Main Title"
    assert meta["section_hint"] == "Section A"
