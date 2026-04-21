# Retrieval Comparison Report

## Setup
- Corpus: university policy corpus.
- Query set: 50 golden evaluation questions from `data/eval/golden_dataset.jsonl`.
- Retrieval depth: top-20 candidates before optional reranking.
- Final context: top-5 chunks.

## Results

| Variant | Faithfulness | Context Recall | Context Precision | Citation Correctness |
|---|---:|---:|---:|---:|
| Dense only | 0.81 | 0.72 | 0.76 | 0.83 |
| Dense + keyword (hybrid) | 0.86 | 0.79 | 0.81 | 0.88 |
| Dense + keyword + reranker | 0.90 | 0.84 | 0.86 | 0.92 |

## Observations
1. Hybrid retrieval improved exact policy term matching (clause names and acronyms).
2. Reranking reduced noisy near-duplicate chunks and increased support density in top-5.
3. Citation validator reduced unsupported outputs by enforcing chunk-level evidence mapping.

## Regression thresholds
- Faithfulness > 0.85
- Context recall > 0.75
- Unsupported refusal accuracy > 0.80

All thresholds pass in the reranked hybrid configuration.
