from app.generation.generator import GroundedGenerator, format_citation
from app.utils.schemas import Chunk, RetrievedChunk


def test_citation_formatting():
    hit = RetrievedChunk(
        chunk=Chunk("c7", "d1", "text", "Doc", "doc.md", 3),
        score=0.9,
    )
    c = format_citation(hit)
    assert c == {"doc": "Doc", "source": "doc.md", "chunk_id": "c7", "page": 3}


def test_refusal_behavior_for_low_score():
    gen = GroundedGenerator(min_score_to_answer=0.5)
    low = RetrievedChunk(chunk=Chunk("c1", "d", "irrelevant", "Doc", "x", None), score=0.2)
    res, _ = gen.answer("question", [low])
    assert res.supported is False
    assert res.refusal_reason == "low_evidence_score"
    assert res.citations == []
