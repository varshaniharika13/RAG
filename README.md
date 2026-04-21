# Campus Policy Assistant (RAG)

A retrieval-augmented generation (RAG) project that answers university policy questions with grounded citations.

## Phase status
- ✅ **Phase 0 complete**: project framing, domain selection, corpus definition, user stories, success criteria, architecture, and repo structure.
- ✅ **Phase 2 complete**: hybrid dense+keyword retrieval, reranking, metadata filtering, chunking experiments, and query rewriting.
- ✅ **Phase 3 complete**: citation-enforced generation, unsupported refusal logic, citation validation, and confidence gating.
- ✅ **Phase 4 scaffold complete**: golden dataset, evaluation runner, experiment logging, and regression report outputs.

## Retrieval upgrades (Phase 2)
- **Hybrid retrieval**: combines dense Chroma similarity and sparse BM25 scores (`app/retrieval/hybrid.py`).
- **Reranking**: cross-encoder reranker rescoring top-20 candidates and selecting top-5 (`app/retrieval/rerank.py`).
- **Metadata filtering**: supports filters for document type, category, source, and date range (`app/types.py`).
- **Chunking strategies**: fixed, heading-aware, and recursive chunking (`app/retrieval/chunking.py`).
- **Query rewriting**: acronym expansion and policy-term normalization (`app/retrieval/query_rewrite.py`).

## Grounding and citation discipline (Phase 3)
- Prompt enforces evidence-backed claims and chunk-level citations (`app/generation/grounded_answer.py`).
- Unsupported queries return refusal text when confidence/support is weak.
- Citation validator checks citation existence and mapping to retrieved chunks (`app/generation/citation_validator.py`).
- Confidence logic combines retrieval + rerank thresholds (`app/retrieval/pipeline.py`).

## Evaluation system (Phase 4)
- Golden dataset (50 samples): `data/eval/golden_dataset.jsonl`.
- Evaluation runner: `scripts/run_eval.py` (writes JSON+CSV reports under `reports/`).
- Metrics module for faithfulness/recall/precision/relevance/citation/refusal: `app/evaluation/metrics.py`.
- Retrieval experiment notebook: `notebooks/retrieval_experiments.ipynb`.
- Comparison report: `reports/retrieval_comparison.md`.
- Experiment logging utility: `app/evaluation/experiment_logger.py`.

## Quickstart
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/run_eval.py
```

## Planned response schema
```json
{
  "answer": "...",
  "citations": [
    {"doc": "policy.pdf", "page": 4, "chunk_id": "c17"}
  ],
  "supported": true,
  "confidence": 0.82
}
```
