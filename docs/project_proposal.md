# RAG Project Proposal (Phase 0)

## Project title
**Campus Policy Assistant (RAG)**

## Domain selection
This project focuses on **university policy and student-facing administrative documents**.

### Why this domain
- Policy documents are long, dense, and frequently referenced.
- Users need precise, source-grounded answers (often with page-level evidence).
- Hallucinations are risky because policy misinterpretation can affect academic and conduct outcomes.

## Target users
- Students looking up academic, conduct, enrollment, and financial-aid policy details.
- Academic advisors and support staff who need quick, cited policy lookups.

## Supported document set (initial corpus)
The project starts with 15 documents (within the requested 10–30 range) listed in `data/raw/corpus_manifest.csv`.
Document types include:
- PDF handbooks and policy manuals
- Markdown/text policy pages
- Public webpages from university policy portals

## User stories
1. As a student, I want to ask a question about policy and get a grounded answer in plain language.
2. As a user, I want exact citations (document + page/chunk) for every factual claim.
3. As a user, I want the system to respond with “I don’t know based on the provided documents” when evidence is insufficient.
4. As an advisor, I want to inspect retrieved chunks to verify why an answer was produced.
5. As a developer, I want repeatable ingestion and evaluation pipelines to detect regressions.

## Success criteria (definition of “good”)
- **Groundedness**: 100% of non-trivial claims trace to at least one retrieved chunk citation.
- **Citation quality**: At least one correct citation for >= 90% of answered evaluation questions.
- **Abstention behavior**: On unanswerable eval queries, model abstains (supported=false) >= 85% of the time.
- **Retrieval quality**: Relevant chunk appears in top-5 retrieval >= 80% on eval set.
- **Reproducibility**: Given the same config + corpus snapshot, ingestion output is deterministic.

## Failure modes (what failure looks like)
- Hallucinated answers without supporting evidence.
- Wrong or misleading citations.
- Overconfident answers to unsupported questions.
- Retrieval misses key sections due to poor chunking/metadata.
- Non-reproducible pipeline outputs across runs.

## Scope for Phase 1 baseline
- Build an end-to-end RAG pipeline with ingestion -> chunking -> embeddings -> Chroma retrieval -> answer generation -> structured response.
- Expose `/ask` endpoint returning `answer`, `citations`, and `supported`.
- Keep architecture simple and observable before optimization.

## Out of scope (for now)
- Advanced rerankers or hybrid retrieval tuning.
- Multi-hop reasoning across many documents.
- Fine-tuning custom language models.

## Professor checkpoint answers
- **What documents am I supporting?** University policy handbooks/manuals and policy webpages listed in the corpus manifest.
- **Who is this system for?** Students and advisors needing fast, trusted policy answers.
- **What does “good” mean?** Correct, grounded answers with verifiable citations and reliable abstention.
- **What does failure look like?** Hallucinations, bad citations, unsupported confident answers, retrieval misses.
