from __future__ import annotations

import math
import re
from collections import Counter

from app.utils.schemas import Chunk, RetrievedChunk

TOKEN_RE = re.compile(r"[a-zA-Z0-9_]+")


def _tokenize(text: str) -> list[str]:
    return [t.lower() for t in TOKEN_RE.findall(text)]


class HybridRetriever:
    """Lightweight lexical retriever with BM25-style scoring for local testing/CI."""

    def __init__(self, chunks: list[Chunk], k1: float = 1.5, b: float = 0.75):
        self.chunks = chunks
        self.k1 = k1
        self.b = b
        self.doc_tokens = [_tokenize(c.text) for c in chunks]
        self.doc_lens = [len(tokens) for tokens in self.doc_tokens]
        self.avg_doc_len = (sum(self.doc_lens) / len(self.doc_lens)) if self.doc_lens else 0.0
        self.df = Counter()
        for tokens in self.doc_tokens:
            for term in set(tokens):
                self.df[term] += 1

    def _idf(self, term: str) -> float:
        n = len(self.chunks)
        df = self.df[term]
        return math.log(1 + ((n - df + 0.5) / (df + 0.5))) if df else 0.0

    def _score(self, q_tokens: list[str], d_tokens: list[str], d_len: int) -> float:
        tf = Counter(d_tokens)
        score = 0.0
        for q in q_tokens:
            if q not in tf:
                continue
            idf = self._idf(q)
            numer = tf[q] * (self.k1 + 1)
            denom = tf[q] + self.k1 * (1 - self.b + self.b * (d_len / (self.avg_doc_len or 1.0)))
            score += idf * (numer / denom)
        return score

    def retrieve(self, query: str, top_k: int = 5) -> list[RetrievedChunk]:
        q_tokens = _tokenize(query)
        scored = [
            RetrievedChunk(chunk=chunk, score=self._score(q_tokens, toks, d_len))
            for chunk, toks, d_len in zip(self.chunks, self.doc_tokens, self.doc_lens)
        ]
        scored.sort(key=lambda x: x.score, reverse=True)
        return scored[:top_k]
