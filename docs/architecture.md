# Architecture Diagram

```mermaid
flowchart LR
    subgraph Ingestion
      A[Document loaders\nPDF/MD/TXT/Web] --> B[Cleaner]
      B --> C[Chunker]
      C --> D[Embedding model]
      D --> E[(Chroma)]
    end

    subgraph Serving
      Q[User query] --> QE[Query embedder]
      QE --> E
      E --> RET[Top-k retriever]
      RET --> PR[Prompt composer]
      PR --> LLM[LLM]
      LLM --> RESP[JSON response\nanswer/citations/supported]
    end

    subgraph Evaluation
      RESP --> MET[Groundedness + citation + abstention metrics]
    end
```

## Metadata contract

### Document-level
- `doc_id`
- `source`
- `title`
- `page_number` (nullable)
- `section_heading` (nullable)
- `raw_text`
- `processed_text`

### Chunk-level
- `chunk_id`
- `parent_doc_id`
- `page`
- `heading`
- `start_char`
- `end_char`
- `source_ref` (URL/path)
