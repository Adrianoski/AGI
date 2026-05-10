# CLARA

A Retrieval-Augmented Generation pipeline organised around a **two-level
semantic index**. Documents are partitioned into **SLMs** (*Small Language
Models*) — topic-specialised clusters of chunks — over which a router
dispatches incoming queries, drastically reducing the search space without
degrading answer quality.

Each SLM is conceptually a small, topic-specialised model of a slice of the
corpus, materialised as a cluster of related chunks plus a routing keyword
summary.

---

## Hypothesis

A standard RAG pipeline scores every query against every chunk in the corpus.
As the corpus grows, latency grows linearly and the signal of the top-k is
diluted by chunks that are semantically far from the query.

If a corpus has intrinsic semantic structure (chapters, topics, sub-domains),
a first stage of **semantic routing** towards a homogeneous neighbourhood of
chunks can:

- shrink the retrieval pool by an order of magnitude
- preserve or improve the relevance of the retrieved evidence
- yield a measurable speedup on retrieval

Each SLM carries two distinct vector representations:

- a *centroid embedding* — mean of the chunk embeddings, used for cluster
  maintenance (assignment of new chunks, merge of close clusters);
- a *summary embedding* — embedding of the keywords extracted from the
  cluster, used exclusively for query routing.

---

## Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│                              INGESTION                               │
└──────────────────────────────────────────────────────────────────────┘

  PDF ──► pymupdf4llm ──► Markdown ──► detect_doc_type
                                            │
                                            ▼
                              ┌──────────────────────────┐
                              │  CHUNKING_PROFILES       │
                              │  paper:    800 / 100     │
                              │  book:    1500 / 150     │
                              │  technical:1200/ 200     │
                              │  generic: 1500 / 150     │
                              └──────────────────────────┘
                                            │
              extract_chapters ─────────────┤
                                            ▼
                         RecursiveCharacterTextSplitter
                            (chunks with chapter metadata)
                                            │
                                            ▼
                            BAAI/bge-m3 (1024-D, normalised)
                                            │
                          ┌─────────────────┴─────────────────┐
                          │                                   │
                          ▼                                   ▼
                  ChromaDB collection                 assign_chunks_auto
                  (cosine, embeddings, docs,                  │
                   metadata)                  ┌───────────────┴──────────┐
                                              │                          │
                                  multi-chapter?                 single chapter?
                                              │                          │
                                              ▼                          ▼
                                   assign_chunks_by_chapter      assign_chunks (cosine,
                                   (one SLM per chapter)         threshold=0.55, opens
                                                                 a new SLM if no match
                                                                 above threshold)
                                              │                          │
                                              └──────────┬───────────────┘
                                                         ▼
                                               merge_close_slms (≥0.88)
                                                  fuses near SLMs
                                                         │
                                                         ▼
                                              refresh_all_summaries
                                              (spaCy NER + POS → keywords
                                              → summary_embedding)
                                                         │
                                                         ▼
                                                 registry.json
                                              + slm_data/*.json

┌──────────────────────────────────────────────────────────────────────┐
│                                QUERY                                 │
└──────────────────────────────────────────────────────────────────────┘

  Query (it/en)
       │
       ▼
   bge-m3 ──► query_embedding (normalised)
       │
       ▼
   find_top_n_slms (cosine vs summary_embedding)
       │              top-N SLMs (default N=3)
       ▼
   ┌───────────────────────────────────────────────────┐
   │  Pool = union of the chunks of the top-N SLMs     │
   │  (~ 6–15 chunks vs the full corpus)               │
   └───────────────────────────────────────────────────┘
       │
       ▼
   ┌─────────────────────────┐    ┌─────────────────────────┐
   │  Dense ranking          │    │  BM25 (rank_bm25)       │
   │  cosine(q, chunk_emb)   │    │  tokenize → score       │
   └────────────┬────────────┘    └────────────┬────────────┘
                └──────────────┬───────────────┘
                               ▼
                     RRF fusion (k=60)
                               │
                               ▼
                          top-K chunks
                               │
                               ▼
                  Qwen3.5-4B (system prompt forces EN output)
                  → streaming answer
```

### Three retrieval modes (compared in the benchmark)

| Mode        | Routing       | Intra-pool filter      | Typical pool  | Use case                                  |
|-------------|---------------|------------------------|---------------|-------------------------------------------|
| **StdRAG**  | none          | dense + BM25 + RRF     | full corpus   | baseline                                  |
| **SLM-RAG** | top-N SLMs    | dense + BM25 + RRF     | ~6–15 chunks  | speed + precision (default UI mode)       |
| **SLM-Full**| top-N SLMs    | none (forwards all)    | ~6–15 chunks  | maximum local recontextualisation         |

---

## Stack

| Layer              | Component                                          |
|--------------------|----------------------------------------------------|
| PDF parsing        | `pymupdf4llm` (Markdown output, headers preserved) |
| Chunking           | `langchain-text-splitters` (Recursive)             |
| Embedding model    | `BAAI/bge-m3` (1024-D, multilingual, normalised)   |
| Vector store       | ChromaDB persistent client (cosine)                |
| Keyword extraction | spaCy `it_core_news_lg` (NER + POS)                |
| Routing            | cosine similarity over `summary_embedding`         |
| Lexical retrieval  | `rank_bm25`                                        |
| Fusion             | Reciprocal Rank Fusion (k=60)                      |
| Generation LLM     | Qwen3.5-4B (HuggingFace, configurable)             |
| Summary LLM (opt.) | Qwen2.5-7B-Instruct (see `_qwen_summary_fn`)       |
| UI                 | Gradio (tabs: Ingestion / Query)                   |

### Source files

| File           | Responsibility                                                                  |
|----------------|---------------------------------------------------------------------------------|
| `app.py`       | Gradio UI, ingestion, streaming query with RRF fusion                           |
| `router.py`    | SLM registry, assignment, merge, summary, query-time routing                    |
| `chunking.py`  | PDF→Markdown, `detect_doc_type`, `extract_chapters`, adaptive profiles          |
| `SLMAgent.py`  | Prompt construction (`build_messages`, chat-template helper)                    |
| `benchmark.py` | 24 queries, three-way comparison Std/SLM/Full, Markdown + JSON output           |

---

## SLM — *Small Language Model*

An SLM is a topic-specialised cluster of chunks recorded in `registry.json`:

```json
{
  "slm_7d833ad1": {
    "collection":         "storia",
    "chunks_json":        "slm_data/slm_7d833ad1_chunks.json",
    "chunk_count":        2,
    "centroid_embedding": [0.0094, 0.0458, ...],
    "topic_summary":      "## 2.1. The route to the East ...",
    "keywords":           ["Henry the Navigator", "East", "Indies", ...],
    "summary_embedding":  [...]
  }
}
```

**Two vector representations for two distinct purposes**:

- `centroid_embedding` (1024-D, L2-normalised) → **assignment** (which SLM
  does a new chunk belong to?) and **merge** (which SLMs are close enough to
  be fused?). It is the mean of the cluster's chunk embeddings.
- `summary_embedding` (1024-D) → **routing** (which SLM should the query be
  routed to?). It is the embedding of the string `", ".join(keywords)`.
  Keywords concentrate the discriminative lexical signal that a user query is
  most likely to match, whereas mean embeddings tend to wash it out.

### Assignment strategies

`assign_chunks_auto()` picks automatically:

1. **`assign_chunks_by_chapter`** (preferred) — when chunks carry distinct
   `chapter` metadata (extracted by `chunking.extract_chapters`), one SLM is
   created per chapter. The centroid is the mean of the chapter's embeddings.

2. **`assign_chunks` (cosine, threshold 0.55)** — fallback for documents with
   no chapter structure. For each chunk:
   - compute the cosine similarity against every existing centroid;
   - if `best_score ≥ threshold` → assign and update the centroid
     incrementally:
     `new_centroid = normalise((old · (n-1) + new_emb) / n)`;
   - otherwise → seed a new SLM with this chunk.

### Merge

`merge_close_slms(threshold=0.88)` iteratively fuses the pair of SLMs with
the highest pairwise cosine above the threshold:

- the SLM with more chunks "wins" and absorbs the other;
- the merged centroid is a chunk-count-weighted mean
  `(c_a · n_a + c_b · n_b) / (n_a + n_b)`, then renormalised;
- the summary is regenerated for the merged cluster.

### Keyword extraction (spaCy)

Implemented in `make_spacy_summary_fn`:

1. **NER pass** — keep entities labelled `PER, ORG, GPE, LOC, MISC, PRODUCT,
   EVENT, WORK_OF_ART`. `DATE, CARDINAL, ORDINAL, PERCENT` are dropped (noisy).
2. **POS pass** — non-stop `NOUN` and `PROPN` tokens not already covered by
   entities, in lemma form.
3. **`_merge_keywords`** — case-insensitive dedup, *substring absorption*
   (e.g. `napoleon` is absorbed by `napoleon bonaparte`), sorted by frequency.
4. **`_is_meaningful_kw`** — quality filter: drops tokens shorter than 4
   characters, page references (e.g. `restaurazione 153`), PDF artefact
   prefixes, and short-token-only sequences.

> **Architectural note**: routing uses the embedding of `", ".join(keywords)`.
> The *order* of the keywords does not matter — only *which* keywords end up
> in the string. Capping the list length therefore directly impacts the
> semantic coverage of the routing signal.

---

## Quickstart

### Installation

```bash
pip install -r requirements.txt
python -m spacy download it_core_news_lg
```

For CUDA acceleration, install PyTorch with the appropriate backend. The
generation pipelines (Qwen3.5-4B) automatically load in `float16` when
`torch.cuda.is_available()`.

### Run the UI

```bash
python app.py
# → http://localhost:7860
```

- **Ingestion tab**: upload a PDF and a collection name → adaptive chunking,
  embedding, SLM assignment, merge, keyword refresh (spaCy).
- **Query tab**: question + HuggingFace model name → top-N SLM routing, hybrid
  retrieval (dense + BM25 + RRF), streaming generation with `<think>` tags
  filtered out client-side.

### Run the benchmark

```bash
python benchmark.py
```

Generates:

- `benchmark_answers_..._{TOP_N_SLMS}_SLM_TOK_K_{TOP_K}.md` — readable report
- `..._results.json` — structured results with chunks, answers, and timings

Configurable via the constants at the top of `benchmark.py` (`TOP_N_SLMS`,
`TOP_K`, `GENERATION_MODEL`, `MAX_NEW_TOKENS`, `MAX_INPUT_TOKENS`).

---

## Pipeline detail

### 1. PDF → Markdown → Chunks

```
PDF ──pymupdf4llm.to_markdown──► full_text (with markdown headers)
                                         │
                                         ▼
                              detect_doc_type (heuristic)
                                         │
                                         ▼
                              extract_chapters (regex on headers)
                                         │
                                         ▼
                              RecursiveCharacterTextSplitter
                                  (separators: \n\n, \n, ., space)
                                         │
                                         ▼
                              filter _index_noise (TOC, glossary, page nums)
                                         │
                                         ▼
                              batch embedding (bge-m3, batch_size=32)
                                         │
                                         ▼
                              persist in ChromaDB: id, text, chapter, embedding
```

**`detect_doc_type`** scores weighted signals over the first 8K characters:

- `paper`: `abstract`, `introduction`, `[1]`, `arxiv`, numbered sections
- `book`: `chapter`, `preface`, many `\n\n`, length > 50K chars
- `technical`: `api`, `def `, code blocks, `installation`
- `generic`: fallback when no score reaches 2

**Chunking profiles**:

| Type      | chunk_size | overlap |
|-----------|------------|---------|
| paper     | 800        | 100     |
| book      | 1500       | 150     |
| technical | 1200       | 200     |
| generic   | 1500       | 150     |

`extract_chapters` uses a strict regex matching numbered Italian-style
chapter titles (`## 1. IL 1300`) and all-caps section headings (`## L'ETÀ
DELLA RINASCITA`). When no match is found, the document is treated as a
single `"Document"` section.

### 2. Assignment & merge

`assign_chunks_auto` picks between the chapter-based and cosine-based
strategies; after assignment, `merge_close_slms` consolidates clusters that
ended up too close.

**Default thresholds** (in `app.py:upload_and_chunk`):

- assignment cosine: `0.55`
- merge cosine: `0.88`
- standalone `assign_chunk` threshold: `0.65`

### 3. Summary refresh

`refresh_all_summaries` iterates over every SLM and, for each:

1. Loads the **entire** set of chunks of the cluster from ChromaDB (no
   centroid-based filtering, so keywords cover the full semantic breadth).
2. Calls `summary_fn(texts)` → `(topic_summary, keywords)`.
3. Computes `routing_text = ", ".join(keywords)` (or `topic_summary` as
   fallback).
4. Embeds `routing_text` to obtain the `summary_embedding`.
5. Writes back to the registry.

`unload_summary_model()` releases the VRAM used by the summary LLM after the
refresh completes.

### 4. Routing

`find_top_n_slms` computes the cosine similarity between the query embedding
and every `summary_embedding` in the registry, returning the top-N. SLMs
without a valid `summary_embedding` are skipped.

### 5. Hybrid retrieval + RRF

In `app.py:_retrieve_hybrid` and in `benchmark.py:retrieve_*`:

- **Dense ranking**: cosine between the query embedding and every chunk in
  the pool.
- **BM25 ranking**: `BM25Okapi` over a simple tokenisation of query and
  documents.
- **RRF fusion**: `score(d) = Σ 1/(k + rank_i(d) + 1)` with `k=60`. The fused
  score ranks the pool; the top-K is forwarded to the generator.

### 6. Generation

`_generate_streaming` loads the model on demand (process-level cache),
applies the chat template with `enable_thinking=False` (Qwen3 family), and
generates tokens via a `TextIteratorStreamer` running on a daemon thread.
The `<think>...</think>` block is stripped client-side as the stream
arrives.

System prompt:

> "Answer the question using ONLY the information provided in the context
>  below. If the answer is not present in the context, respond with 'The
>  answer is not available in the provided context.' CRITICAL: You MUST
>  write your answer in English only."

Forcing English output lets a downstream evaluator compare the generated
answers against the English ground truth without language mismatch.

---

## Benchmark

### Setup

`benchmark.py` ships with **24 queries** on an Italian history textbook.
Each query has:

- an English version (used at generation time);
- an Italian version (used at retrieval time — BM25 needs language match);
- a list of expected keywords (`keyword_hit_pct` metric);
- an English ground truth.

### Efficiency metrics (per mode)

- `t_ret_ms` — retrieval latency (ms)
- `t_gen_ms` — generation latency (ms)
- `pool` — number of chunks actually examined
- `keyword_hit_pct` — fraction of expected keywords found in the retrieved
  chunks
- `overlap_pct` — top-K overlap between StdRAG and SLM-RAG

### Results (top-N=3, top-K=5, Qwen3.5-4B)

| Metric                    | StdRAG    | SLM-RAG          | SLM-Full         |
|---------------------------|-----------|------------------|------------------|
| Retrieval speedup         | —         | **4.8×**         | **11.4×**        |
| Average pool              | 219       | 11 (−95%)        | 11 (−95%)        |
| Average generation        | 3801 ms   | 3742 ms          | 4489 ms          |
| Keyword hit               | 62%       | 60%              | 64%              |
| Top-5 overlap (Std/SLM)   | 49%       | —                | —                |

**Trade-off**: SLM-RAG attains 60% keyword hit (vs 62% StdRAG) on a pool
~20× smaller. SLM-Full forwards the full ~11 chunks of the cluster to the
LLM, reaching 64%: forwarding the entire local neighbourhood compensates
for the lack of intra-pool ranking.

---

## Configuration & tuning

The thresholds are the parameters with the largest impact on behaviour:

| Param                 | Default | Where                       | Effect                                          |
|-----------------------|---------|-----------------------------|-------------------------------------------------|
| assignment threshold  | 0.55    | `app.py:upload_and_chunk`   | lower → many small SLMs; higher → few wide SLMs |
| merge threshold       | 0.88    | `app.py:upload_and_chunk`   | lower → aggressive merging; higher → fragmented |
| `SLM_SUMMARY_EVERY_N` | 20      | `router.py`                 | in-flight summary refresh every N chunks added  |
| `RRF_K`               | 60      | `app.py`                    | higher → more conservative fusion               |
| `TOP_N_SLMS`          | 3       | `app.py` / `benchmark.py`   | how many SLMs the router forwards               |
| `TOP_K_CHUNKS`        | 5       | `app.py` / `benchmark.py`   | how many chunks the LLM sees                    |

### Override the chunking profile

```python
process_pdf(
    pdf_path,
    collection,
    embedding_model,
    chunk_size=2000,   # overrides the adaptive profile
    overlap=200,
)
```

---

## Project structure

```
.
├── app.py                          # Gradio UI + streaming query
├── router.py                       # SLM logic (registry, assignment, routing, summary)
├── chunking.py                     # PDF→Markdown, detect_doc_type, profiles
├── SLMAgent.py                     # Prompt construction
├── benchmark.py                    # Three-way comparison on 24 queries
│
├── registry.json                   # SLM registry — generated at runtime
├── slm_data/                       # Chunk-id lists per SLM — generated at runtime
│   └── slm_<hex>_chunks.json
├── chroma_db/                      # ChromaDB persistent store — generated at runtime
│   └── chroma.sqlite3
│
├── requirements.txt
└── LICENSE
```

`registry.json`, `slm_data/`, and `chroma_db/` are gitignored: they are
rebuilt on first ingestion.

---

## License

See `LICENSE`.
