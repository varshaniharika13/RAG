from app.retrieval.retriever import HybridRetriever
from app.utils.schemas import Chunk


def test_retrieval_output_shape_and_ranking():
    chunks = [
        Chunk("c1", "d", "tuition payment deadline and fees", "Billing", "billing.md", 1),
        Chunk("c2", "d", "library silent floor policy", "Library", "library.md", 2),
    ]
    r = HybridRetriever(chunks)
    hits = r.retrieve("tuition fee deadline", top_k=2)

    assert len(hits) == 2
    assert hits[0].chunk.chunk_id == "c1"
    assert isinstance(hits[0].score, float)
