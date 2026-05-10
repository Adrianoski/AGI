# CLARA

Sistema RAG (Retrieval-Augmented Generation) **a doppio livello di indicizzazione semantica** progettato per la lingua italiana. Il documento viene partizionato in **SLM** (*Semantic Language Maps*) — cluster semantici di chunk — su cui un router instrada le query, riducendo drasticamente lo spazio di ricerca senza degradare la qualità delle risposte.

---

## Tesi sperimentale

Il RAG standard fa retrieval su **tutti** i chunk del corpus. Quando il corpus cresce, la latenza cresce linearmente e il segnale del top-k si "diluisce" nel rumore di chunk semanticamente lontani.

**Ipotesi**: se il corpus ha struttura semantica intrinseca (capitoli, argomenti, sotto-domini), un primo livello di **routing semantico** verso un sotto-insieme di chunk *omogenei* può:

- ridurre il pool di ricerca di un ordine di grandezza
- mantenere o aumentare la pertinenza dei chunk recuperati
- portare a un **speedup misurabile** sul retrieval (4×–10× sui benchmark inclusi)

L'unità di routing è l'**SLM**: un cluster di chunk con relativo *centroide* (media degli embedding) e *summary embedding* (embedding delle keyword estratte).

---

## Architettura

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
                            (chunks con metadato chapter)
                                            │
                                            ▼
                            BAAI/bge-m3 (1024-D, normalizzato)
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
                                   (1 SLM per capitolo)          threshold=0.55, crea
                                                                 nuovo SLM se nessuno
                                                                 sopra soglia)
                                              │                          │
                                              └──────────┬───────────────┘
                                                         ▼
                                               merge_close_slms (≥0.88)
                                                  fonde SLM vicini
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
   bge-m3 ──► query_embedding (normalizzato)
       │
       ▼
   find_top_n_slms (cosine vs summary_embedding)
       │              top-N SLM (default N=3)
       ▼
   ┌───────────────────────────────────────────────────┐
   │  Pool = unione dei chunk dei top-N SLM            │
   │  (≈ 6–15 chunk vs 219 nel corpus full)            │
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
                  Qwen3.5-4B (system prompt EN-only)
                  → risposta in streaming
```

### Tre modalità di retrieval (confrontate nel benchmark)

| Modalità    | Routing       | Filtraggio intra-pool | Pool tipico   | Casi d'uso                               |
|-------------|---------------|-----------------------|---------------|------------------------------------------|
| **StdRAG**  | nessuno       | dense + BM25 + RRF    | tutti i chunk | baseline                                 |
| **SLM-RAG** | top-N SLM     | dense + BM25 + RRF    | ~6–15 chunk   | velocità + precisione (default)          |
| **SLM-Full**| top-N SLM     | nessuno (passa tutto) | ~6–15 chunk   | massima ricontestualizzazione, no filtri |

---

## Componenti

### Stack tecnologico

| Layer                | Componente                                       |
|----------------------|--------------------------------------------------|
| PDF parsing          | `pymupdf4llm` (Markdown output con header)       |
| Chunking             | `langchain-text-splitters` (Recursive)           |
| Embedding model      | `BAAI/bge-m3` (1024-D, multilingue, normalizzato)|
| Vector store         | ChromaDB persistente (cosine)                    |
| Keyword extraction   | spaCy `it_core_news_lg` (NER + POS)              |
| Routing              | cosine similarity su `summary_embedding`         |
| Lexical retrieval    | `rank_bm25`                                      |
| Fusion               | Reciprocal Rank Fusion (k=60)                    |
| LLM generazione      | Qwen3.5-4B (HuggingFace, configurabile)          |
| LLM riassunto (opz.) | Qwen2.5-7B-Instruct (vedi `_qwen_summary_fn`)    |
| UI                   | Gradio (tabs: Ingestion / Query)                 |
| Eval qualità         | RAGAS + GPT-4o come giudice                      |
| Visualizzazione      | Three.js + PCA/t-SNE/UMAP a 3D                   |

### File di codice

| File                       | Righe | Responsabilità                                                                                |
|----------------------------|-------|-----------------------------------------------------------------------------------------------|
| `app.py`                   | 715   | UI Gradio, ingestione, query con streaming, RRF fusion in-app                                 |
| `router.py`                | 1205  | Registry SLM, assignment, merge, summary, routing, HDBSCAN, spaCy/KeyBERT/Qwen extractors     |
| `chunking.py`              | 253   | PDF→Markdown, detect_doc_type, extract_chapters, profili adattivi                             |
| `SLMAgent.py`              | 184   | Dataclass agent, prompt template, `generate_answer`, modalità RAG end-to-end                  |
| `benchmark.py`             | 685   | 25 query con ground-truth, confronto Std/SLM/Full, output Markdown + JSON                     |
| `evaluate_quality.py`      | 294   | RAGAS (Precision, Recall, AR, Faithfulness, Hallucination)                                    |
| `show_slms.py`             | 63    | Report testuale: SLM, summary, keywords (ordinabile)                                          |
| `diagnose_slms.py`         | 52    | Distribuzione cosine pairwise tra centroidi, stima merge per soglia                           |
| `extract_vectors.py`       | 248   | Esporta chunk + centroidi in 3D (PCA/t-SNE/UMAP) con raggi d'azione                           |
| `extract_raw_vectors.py`   | 163   | Variante: chunk colorati per capitolo, senza struttura SLM                                    |
| `test_router.py`           | 262   | Test: assignment, merge, find_top_n, centroid update                                          |
| `test_retrieval.py`        | 92    | CLI: query → top-k chunk con score                                                            |
| `debug.py`                 | 18    | Snippet manuale Chroma (count, get by source)                                                 |

---

## SLM — *Semantic Language Map*

Un SLM è un cluster di chunk semanticamente affini, registrato in `registry.json`:

```json
{
  "slm_7d833ad1": {
    "collection":         "storia",
    "chunks_json":        "slm_data/slm_7d833ad1_chunks.json",
    "chunk_count":        2,
    "centroid_embedding": [0.0094, 0.0458, ...],
    "topic_summary":      "## 2.1. La via verso Oriente ...",
    "keywords":           ["Enrico il Navigatore", "Oriente", "Indie", ...],
    "summary_embedding":  [...]
  }
}
```

**Due rappresentazioni vettoriali per due scopi distinti**:

- `centroid_embedding` (1024-D, L2-normalizzato) → **assignment** (a quale SLM appartiene un nuovo chunk?) e **merge** (quali SLM sono troppo vicini e vanno fusi?). È la media degli embedding dei chunk dell'SLM.
- `summary_embedding` (1024-D) → **routing** (a quale SLM va instradata la query?). È l'embedding della stringa `", ".join(keywords)`. Le keyword sono semanticamente più significative degli embedding "medi" di chunk eterogenei.

### Strategie di assignment

`assign_chunks_auto()` sceglie automaticamente:

1. **`assign_chunks_by_chapter`** (preferita) — se i chunk hanno metadati `chapter` distinti (estratti da `chunking.extract_chapters`), crea **un SLM per capitolo**. Il centroide è la media degli embedding del capitolo.

2. **`assign_chunks` (cosine, soglia 0.55)** — fallback per documenti senza struttura. Per ogni chunk:
   - calcola la cosine vs il centroide di ogni SLM esistente
   - se `best_score ≥ threshold` → assegna; aggiorna il centroide incrementalmente:
     `new_centroid = normalize((old · (n-1) + new_emb) / n)`
   - altrimenti → crea un nuovo SLM seedato con questo chunk

3. **`cluster_chunks_hdbscan`** (alternativa batch) — clustering globale di tutti i chunk con HDBSCAN. Riduce prima a 50D con PCA (le distanze cosine in 768D+ collassano per *concentration of measure*), poi cluster per densità. Punti di rumore (`label == -1`) vengono riassegnati al cluster più vicino. Il modello viene persistito in `hdbscan_model.pkl` per ingestione incrementale via `approximate_predict()`.

### Merge degli SLM

`merge_close_slms(threshold=0.88)` fonde iterativamente le coppie con cosine pairwise più alta sopra soglia:

- l'SLM con più chunk "vince" e assorbe l'altro
- centroid merge **pesato per chunk_count**: `(c_a · n_a + c_b · n_b) / (n_a + n_b)` poi normalizzato
- il summary viene rigenerato dopo la fusione

### Keyword extraction (spaCy)

Implementata in `make_spacy_summary_fn` ([router.py:1148-1204](router.py#L1148)):

1. **Pass NER** — tiene entità con label in `{PER, ORG, GPE, LOC, MISC, PRODUCT, EVENT, WORK_OF_ART}`. Esclude `DATE, CARDINAL, ORDINAL, PERCENT` (rumorose).
2. **Pass POS** — `NOUN` e `PROPN` *non-stop*, **non già coperti da entità**, in forma lemmatizzata.
3. **`_merge_keywords`** — dedup case-insensitive, *substring absorption* (es. `napoleon` viene assorbito da `napoleon bonaparte`), sort per frequenza.
4. **`_is_meaningful_kw`** — filtro qualità: scarta token < 4 char, page-refs (`restaurazione 153`), prefissi-artefatto PDF, sequenze tutto-token-corti.

> **Nota architetturale**: il routing usa l'embedding di `", ".join(keywords)` ([router.py:493](router.py#L493)). Quindi *l'ordine delle keyword non conta*, conta solo *quali keyword finiscono nella stringa*. Un eventuale cap sulla lunghezza della lista impatta direttamente la copertura semantica del routing.

### Estrattori alternativi disponibili

- `make_keybert_summary_fn` — KeyBERT con il SentenceTransformer già caricato.
- `_qwen_summary_fn` (deprecato come default) — Qwen2.5-7B che genera 10–15 tag con few-shot prompt; più costoso, qualità simile a spaCy nei nostri test.

---

## Quickstart

### Installazione

```bash
pip install -r requirements.txt
python -m spacy download it_core_news_lg
```

Per CUDA, assicurati di avere PyTorch con il backend giusto. Le pipeline più pesanti (Qwen3.5-4B di generazione) caricano in `float16` automaticamente se `torch.cuda.is_available()`.

### UI di ingestione + query

```bash
python app.py
# → http://localhost:7860
```

Tab **Ingestion**: carica PDF + nome collection → chunking adattivo, embedding, assignment, merge, refresh keyword (spaCy).
Tab **Query**: domanda + nome modello HF → routing top-N SLM, retrieval ibrido, generazione in streaming con `<think>` filtrato.

### Benchmark a 3 modalità

```bash
python benchmark.py
```

Genera:

- `benchmark_answers_..._{TOP_N_SLMS}_SLM_TOK_K_{TOP_K}.md` — report leggibile
- `..._results.json` — input per `evaluate_quality.py`

Configurabile via costanti in cima a `benchmark.py` (`TOP_N_SLMS`, `TOP_K`, `GENERATION_MODEL`, `MAX_NEW_TOKENS`, `MAX_INPUT_TOKENS`).

### Valutazione qualitativa con RAGAS

```bash
export OPENAI_API_KEY=sk-...
python evaluate_quality.py --input <results>.json --output quality_report.md
```

Calcola: Contextual Precision, Contextual Recall, Answer Relevancy, Faithfulness, Hallucination (= 1 − Faithfulness). Confronto a 3 vie StdRAG / SLM-RAG / SLM-Full con delta vs baseline.

### Diagnostica & visualizzazione

```bash
python show_slms.py --sort chunks --output slm_report_spacy.txt
python diagnose_slms.py                              # distribuzione similarity tra centroidi
python extract_vectors.py --method pca               # vectors.json per visualizer.html
python extract_raw_vectors.py --method tsne          # variante senza struttura SLM
python test_retrieval.py "Chi importava le spezie?"  # CLI veloce
```

---

## Pipeline dettagliata

### 1. PDF → Markdown → Chunks

```
PDF ──pymupdf4llm.to_markdown──► full_text (con header markdown)
                                         │
                                         ▼
                              detect_doc_type (heuristic)
                                         │
                                         ▼
                              extract_chapters (regex su header)
                                         │
                                         ▼
                              RecursiveCharacterTextSplitter
                                  (separators: \n\n, \n, ., space)
                                         │
                                         ▼
                              filtra _index_noise (INDICE, Glossario, pag. NN)
                                         │
                                         ▼
                              embedding batch (bge-m3, batch_size=32)
                                         │
                                         ▼
                              salva su ChromaDB: id, text, chapter, embedding
```

**`detect_doc_type`** ([chunking.py:48-94](chunking.py#L48)) usa segnali pesati su 8K caratteri iniziali:

- `paper`: `abstract`, `introduction`, `[1]`, `arxiv`, sezioni numerate
- `book`: `chapter`, `preface`, molti `\n\n`, lunghezza > 50K char
- `technical`: `api`, `def `, code blocks, `installation`
- `generic`: fallback se nessuno scoring ≥ 2

**Profili di chunking** ([chunking.py:22-43](chunking.py#L22)):

| Tipo      | chunk_size | overlap |
|-----------|------------|---------|
| paper     | 800        | 100     |
| book      | 1500       | 150     |
| technical | 1200       | 200     |
| generic   | 1500       | 150     |

**`extract_chapters`** ([chunking.py:117-158](chunking.py#L117)) usa una regex stringente per capitoli numerati italiani (`## 1. IL 1300`) o titoli tutto-maiuscolo (`## L'ETÀ DELLA RINASCITA`). Se nessun match → fallback `"Document"` come unico capitolo.

### 2. Assignment & merge

Vedi [router.py:561-748](router.py#L561). Il flusso `assign_chunks_auto` decide tra strategia chapter-based e cosine-based; dopo l'assignment, `merge_close_slms` consolida cluster troppo vicini.

**Threshold defaults**:

- assignment cosine: `0.55` (in `app.py:upload_and_chunk`)
- merge cosine: `0.88` (in `app.py:upload_and_chunk`)
- threshold più strict in `assign_chunk` standalone: `0.65`

### 3. Refresh delle summary

`refresh_all_summaries` ([router.py:502-521](router.py#L502)) itera tutti gli SLM, per ognuno:

1. Carica l'**intero** insieme di chunk del cluster da ChromaDB (no centroid-based filtering, per coprire la breadth semantica)
2. Chiama `summary_fn(texts)` → `(topic_summary, keywords)`
3. Calcola `routing_text = ", ".join(keywords)` o fallback a `topic_summary`
4. Embedda `routing_text` → `summary_embedding`
5. Salva nel registry

`unload_summary_model()` libera la VRAM dopo il refresh.

### 4. Routing

`find_top_n_slms` ([router.py:945-985](router.py#L945)) calcola la cosine tra `query_embedding` e ogni `summary_embedding` nel registry. Ritorna i top-N ordinati. SLM senza `summary_embedding` valido vengono saltati.

### 5. Retrieval ibrido + RRF

In `app.py:_retrieve_hybrid` ([app.py:129-203](app.py#L129)) e in `benchmark.py:retrieve_*`:

- **Dense ranking**: cosine tra `query_embedding` e ogni chunk del pool
- **BM25 ranking**: `BM25Okapi` su `_tokenize` della query e dei documenti
- **RRF fusion** ([app.py:107-113](app.py#L107)): `score(d) = Σ 1/(k + rank_i(d) + 1)` con `k=60`. Sort per score → top-K.

### 6. Generazione

`_generate_streaming` ([app.py:206-236](app.py#L206)) carica il modello on-demand (cache di processo), applica il chat template con `enable_thinking=False` (Qwen3 family), genera in streaming con `TextIteratorStreamer` su un thread daemon. La regex `<think>...</think>` viene strippata in tempo reale dal frontend.

System prompt ([SLMAgent.py:85-92](SLMAgent.py#L85)):

> "Answer the question using ONLY the information provided in the context below.
>  If the answer is not present in the context, respond with 'The answer is not available in the provided context.'
>  CRITICAL: You MUST write your answer in English only."

Forzare l'output in inglese consente all'evaluator (RAGAS + mpnet) di lavorare senza language mismatch tra risposta (EN) e ground-truth (EN).

---

## Evaluation

### Setup

`benchmark.py` contiene **25 query** con:

- versione inglese (per generazione)
- versione italiana (per retrieval — match lessicale BM25)
- 5–6 keyword attese (metric: keyword hit rate)
- ground truth in inglese (per RAGAS)

Le query coprono il manuale "Storia 2" usato nei test (medioevo, scoperte geografiche, riforma, rivoluzione francese, napoleone, restaurazione, risorgimento, rivoluzione industriale).

### Metriche di efficienza

Misurate per ogni modalità (StdRAG / SLM-RAG / SLM-Full):

- `t_ret_ms` — latenza retrieval (ms)
- `t_gen_ms` — latenza generazione (ms)
- `pool` — n. chunk effettivamente esaminati
- `keyword_hit_pct` — % di keyword attese presenti nei chunk recuperati
- `overlap_pct` — overlap top-K tra StdRAG e SLM-RAG

### Risultati sul corpus 25-capitoli (top-N=3, top-K=5, Qwen3.5-4B)

Estratto da [benchmark_answers_spacy_3_WAYS_2PDF_25chapters_3_SLM_TOK_K_5.md](benchmark_answers_spacy_3_WAYS_2PDF_25chapters_3_SLM_TOK_K_5.md):

| Metrica                    | StdRAG    | SLM-RAG          | SLM-Full         |
|----------------------------|-----------|------------------|------------------|
| Speedup retrieval          | —         | **4.8×**         | **11.4×**        |
| Pool medio                 | 219 chunk | 11 chunk (−95%)  | 11 chunk (+95%)  |
| Generazione media          | 3801 ms   | 3742 ms          | 4489 ms          |
| Keyword hit                | 62%       | 60%              | 64%              |
| Overlap top-5 (Std vs SLM) | 49%       | —                | —                |

**Trade-off osservato**: SLM-RAG raggiunge il 60% di keyword hit (vs 62% StdRAG) con un pool 20× più piccolo. SLM-Full passa al LLM tutti i ~11 chunk del cluster, ottenendo 64% (sopra StdRAG): la "ricontestualizzazione" del cluster intero compensa il filtraggio interno saltato.

### Metriche di qualità (RAGAS, GPT-4o judge)

Calcolate da `evaluate_quality.py`. Ogni metrica è in `[0, 1]`:

| Metrica              | Significato                                                              |
|----------------------|--------------------------------------------------------------------------|
| Contextual Precision | I chunk recuperati sono pertinenti? (rapporto chunk utili / totale)      |
| Contextual Recall    | I fatti del ground-truth sono coperti dai chunk?                         |
| Answer Relevancy     | La risposta affronta la domanda? (similarity con ricostruzione query)    |
| Faithfulness         | La risposta si fonda sul contesto? (no allucinazioni)                    |
| Hallucination        | `1 − Faithfulness`                                                       |

Il report markdown include la tabella aggregata + le metriche per-query + le risposte complete a 3-vie con ground truth.

---

## Configurazione & tuning

### Soglie SLM

Le soglie sono i parametri più impattanti sul comportamento:

| Param                  | Default | File           | Effetto                                       |
|------------------------|---------|----------------|-----------------------------------------------|
| assign threshold       | 0.55    | `app.py:77`    | < → tanti SLM piccoli; > → pochi SLM larghi   |
| merge threshold        | 0.88    | `app.py:78`    | < → fusioni aggressive; > → SLM frammentati   |
| `SLM_SUMMARY_EVERY_N`  | 20      | `router.py:22` | Refresh in-flight ogni N chunk aggiunti       |
| `MAX_EXCERPT_CHARS`    | 4000    | `router.py:27` | Per Qwen summary (deprecato)                  |
| `RRF_K`                | 60      | `app.py:33`    | Più alto → fusion più conservativa            |
| `TOP_N_SLMS`           | 3       | `app.py:30`    | Quanti SLM passa il router                    |
| `TOP_K_CHUNKS`         | 5       | `app.py:31`    | Quanti chunk passa al LLM                     |

Usa `diagnose_slms.py` per studiare la distribuzione delle similarità prima di tunare la merge threshold.

### Override del chunking

```python
process_pdf(
    pdf_path,
    collection,
    embedding_model,
    chunk_size=2000,   # override profilo adattivo
    overlap=200,
)
```

### Cambiare estrattore di keyword

In `app.py:upload_and_chunk`:

```python
spacy_fn   = make_spacy_summary_fn("it_core_news_lg")
keybert_fn = make_keybert_summary_fn(embedding_model)

n_refreshed = refresh_all_summaries(embedding_model, chroma_client, summary_fn=spacy_fn)
# oppure: summary_fn=keybert_fn  oppure: nessun arg → Qwen LLM
```

---

## Struttura del progetto

```
.
├── app.py                          # UI Gradio + query streaming
├── router.py                       # Logica SLM (registry, assignment, routing, summary)
├── chunking.py                     # PDF→Markdown, detect_doc_type, profili
├── SLMAgent.py                     # Dataclass + prompt + RAG end-to-end
├── benchmark.py                    # Confronto 3 modalità su 25 query
├── evaluate_quality.py             # RAGAS + GPT-4o judge
├── show_slms.py                    # Report testuale del registry
├── diagnose_slms.py                # Distribuzione similarità tra centroidi
├── extract_vectors.py              # Export 3D con SLM (PCA/t-SNE/UMAP)
├── extract_raw_vectors.py          # Export 3D senza struttura SLM
├── test_router.py                  # Test logica router
├── test_retrieval.py               # CLI retrieval
├── debug.py                        # Snippet manuali Chroma
│
├── registry.json                   # Registry SLM (centroide, summary, keywords, embedding)
├── slm_data/
│   └── slm_<hex>_chunks.json       # Lista chunk_id per ogni SLM
├── chroma_db/                      # Vector store persistente
│   └── chroma.sqlite3
├── hdbscan_model.pkl               # (opz.) Modello HDBSCAN persistito
│
├── slm_report_spacy.txt            # Output di show_slms.py (estrazione spaCy)
├── slm_report_keybert.txt          # Output di show_slms.py (estrazione KeyBERT)
│
├── benchmark_answers_*.md          # Report benchmark leggibili
├── benchmark_answers_*_results.json# Input per evaluate_quality.py
├── final2PDF_3WAY.md / .json       # Report finale 3-way
├── FINAL2PDF.json / .md            # Snapshot risultati
│
├── leonetti-storia2.pdf            # Corpus di test (manuale di storia)
├── requirements.txt
└── LICENSE
```

---

## Visualizzazione 3D

`extract_vectors.py` esporta `vectors.json` con:

- coordinate 3D di ogni chunk (PCA / t-SNE / UMAP)
- coordinate 3D di ogni centroide SLM
- raggi d'azione (max, mean, std) calcolati come distanza chunk→centroide

Apri `visualizer.html` (Three.js) e carica `vectors.json` per esplorare la topologia semantica. I chunk sono colorati per SLM. Vedi `extract_raw_vectors.py` per una vista alternativa colorata per capitolo.

---

## Estensioni possibili

- **Cap proporzionale ai chunk** in `_merge_keywords`: SLM con N chunk → fino a `min(40·N, 200)` keyword, invece di un cap fisso (vedi commento in [router.py:336](router.py#L336)).
- **Bonus NER nel ranking keyword**: utile solo se si pesa l'embedding di routing (es. ripetizioni); con embedding uniforme l'ordine non conta.
- **Embedding pesato** per il routing: oggi `", ".join(keywords)` perde la frequenza; pesare con repeat-N o BM25-style cambierebbe il signal.
- **HDBSCAN come default** quando il documento non ha capitoli — già implementato in `cluster_chunks_hdbscan`.
- **Online ingestion**: `assign_chunk` supporta già l'incremental con `_update_centroid`; il summary refresh periodico (`SLM_SUMMARY_EVERY_N`) è il loop completo.

---

## Licenza

Vedi `LICENSE`.
