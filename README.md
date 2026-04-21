# Campus Policy Assistant (RAG)

A retrieval-augmented generation (RAG) project that answers university policy questions with grounded citations.

## Phase status
- ✅ **Phase 0 complete**: project framing, domain selection, corpus definition, user stories, success criteria, architecture, and repo structure.
- 🚧 **Phase 1 next**: build baseline ingestion/retrieval/generation pipeline end-to-end.

## Domain
This project targets **university policy documents** (handbooks, registrar policy pages, conduct procedures, aid and enrollment policies).

## Core user stories
- As a user, I want to ask a policy question and get a grounded answer.
- As a user, I want exact citations (document/page/chunk references).
- As a user, I want abstention (“I don’t know”) when evidence is insufficient.
- As a developer, I want stable evaluation metrics to catch regressions.

## Success criteria
- Grounded, citation-backed answers.
- Strong top-k retrieval recall on eval questions.
- Reliable abstention on unsupported queries.
- Reproducible ingestion and indexing.

## Architecture (baseline)
```mermaid
flowchart TD
    A[Raw Documents\nPDF / Markdown / TXT / Web] --> B[Ingestion Pipeline]
    B --> C[Cleaning + Normalization]
    C --> D[Chunking\n500-800 tokens\n80-120 overlap]
    D --> E[Embeddings]
    E --> F[(Chroma Vector Store)]

    U[User Question] --> Q[Query Embedding]
    Q --> F
    F --> R[Top-k Retrieval\nk=5]
    R --> P[Prompt Builder\nquestion + chunks + citation rules]
    P --> L[LLM Generation]
    L --> O[Structured Response\nanswer + citations + supported]

    O --> API[/ask endpoint]
    O --> UI[Basic UI]
    O --> EV[Evaluation Harness]
```

## Planned response schema
```json
{
  "answer": "...",
  "citations": [
    {"doc": "policy.pdf", "page": 4, "chunk_id": "c17"}
  ],
  "supported": true
}
```

## Repository structure
```text
rag-project/
│
├── app/
│   ├── api/
│   ├── ingestion/
│   ├── retrieval/
│   ├── generation/
│   ├── evaluation/
│   ├── config/
│   └── utils/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── eval/
│
├── notebooks/
├── tests/
├── scripts/
├── prompts/
├── .github/workflows/
├── requirements.txt
└── README.md
```

## Key project artifacts
- Project proposal: `docs/project_proposal.md`
- Corpus manifest (15 docs): `data/raw/corpus_manifest.csv`

## Phase 1 implementation plan
1. **Ingestion**: load PDF/MD/TXT/web and normalize into a canonical document schema.
2. **Chunking**: chunk with metadata (doc_id, page, heading, start/end offsets, source path/url).
3. **Embeddings + Chroma**: embed chunks and persist vectors with metadata.
4. **Retrieval**: embed query and return top-k relevant chunks.
5. **Generation**: prompt model to answer from context only and cite supporting chunks.
6. **API/UI**: provide `/ask` endpoint and a minimal interface.
7. **Evaluation**: add groundedness/citation/abstention metrics.

## Professor checkpoint answers
- **What documents am I supporting?** University policy handbooks and policy webpages in the corpus manifest.
- **Who is this system for?** Students and advisors.
- **What does “good” mean?** Correct, grounded answers with trustworthy citations and safe abstention.
- **What does failure look like?** Hallucinated claims, missing/wrong citations, overconfident unsupported answers.
