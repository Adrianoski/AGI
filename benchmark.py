"""
benchmark.py — Confronto RAG standard vs SLM-routed retrieval.

Metriche:
  - Latenza media (ms) per query
  - Dimensione del pool di ricerca (n. chunk esaminati)
  - Overlap@5 tra i due sistemi (per stimare la qualità relativa)

Uso:
    python3 benchmark.py
"""

import time
import json
import re
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi
import chromadb

from router import load_registry, find_top_n_slms

# ── Config ─────────────────────────────────────────────────────────────
TOP_N_SLMS        = 3
TOP_K             = 5
RRF_K             = 60
COLLECTION        = None                  # None = usa la prima collection disponibile
GENERATION_MODEL  = "Qwen/Qwen3.5-4B"    # modello HuggingFace per la generazione
MAX_NEW_TOKENS    = 256
OUTPUT_FILE       = "benchmark_answers.md"

# (query_en, query_it_for_bm25, expected_keywords_in_answer)
QUERIES = [
    (
        "Who imported spices into Europe during the Middle Ages?",
        "da chi venivano importate le spezie in europa nel medioevo?",
        ["arabi", "veneziana", "mercanti", "spezie", "oriente", "monopolio"],
    ),
    (
        "What territories did Charles V control?",
        "quali territori controllava Carlo V?",
        ["carlo", "spagna", "impero", "asburgo", "fiandre", "napoli"],
    ),
    (
        "What were the main causes of the French Revolution?",
        "quali furono le cause della rivoluzione francese?",
        ["crisi", "stato", "terzo", "nobiltà", "tasse", "assemblea"],
    ),
    (
        "How did James Watt's steam engine work?",
        "come funzionava la macchina a vapore di james watt?",
        ["vapore", "watt", "carbone", "industria", "energia", "cilindro"],
    ),
    (
        "What were the key principles of the Enlightenment?",
        "quali erano i principi fondamentali dell'illuminismo?",
        ["ragione", "kant", "libertà", "progresso", "filosofia", "diritti"],
    ),
    (
        "What was the American Revolution?",
        "che cosa fu la rivoluzione americana?",
        ["colonie", "indipendenza", "inglesi", "america", "tasse", "dichiarazione"],
    ),
    (
        "Who were the Mongols and how did they expand?",
        "chi erano i mongoli e come si espansero?",
        ["mongoli", "gengis", "khan", "asia", "impero", "conquista"],
    ),
    (
        "What was Luther's Protestant Reformation?",
        "che cosa fu la riforma protestante di lutero?",
        ["lutero", "chiesa", "bibbia", "riforma", "fede", "protestante"],
    ),
    (
        "How was the Italian state formed during the Risorgimento?",
        "come si formò lo stato italiano nel risorgimento?",
        ["cavour", "garibaldi", "mazzini", "unità", "piemonte", "italia"],
    ),
    (
        "What were the social consequences of the Industrial Revolution?",
        "quali furono le conseguenze sociali della rivoluzione industriale?",
        ["operai", "fabbriche", "lavoro", "borghesia", "città", "sfruttamento"],
    ),
]

# ── Helpers ────────────────────────────────────────────────────────────

def tokenize(text: str):
    return re.sub(r'[^\w\s]', ' ', text.lower()).split()


def rrf(rankings, k=RRF_K):
    scores = {}
    for ranking in rankings:
        for rank, idx in enumerate(ranking):
            scores[idx] = scores.get(idx, 0.0) + 1.0 / (k + rank + 1)
    return sorted(scores.keys(), key=lambda x: scores[x], reverse=True)


def cosine_scores(q_emb, embeddings):
    q_norm = float(np.linalg.norm(q_emb))
    scores = []
    for emb in embeddings:
        e = np.array(emb, dtype=np.float32)
        e_norm = float(np.linalg.norm(e))
        scores.append(float(np.dot(q_emb, e) / (q_norm * e_norm)) if e_norm > 0 else 0.0)
    return scores


# ── RAG standard: cerca su TUTTI i chunk della collection ──────────────

def retrieve_standard(query, q_emb, col, top_k=TOP_K):
    t0 = time.perf_counter()

    data = col.get(include=["embeddings", "documents", "metadatas"])
    embeddings = data["embeddings"]
    documents  = data["documents"]

    dense_scores = cosine_scores(q_emb, embeddings)
    dense_rank   = sorted(range(len(embeddings)), key=lambda i: dense_scores[i], reverse=True)

    bm25       = BM25Okapi([tokenize(d) for d in documents])
    bm25_sc    = bm25.get_scores(tokenize(query))
    bm25_rank  = sorted(range(len(embeddings)), key=lambda i: float(bm25_sc[i]), reverse=True)

    fused = rrf([dense_rank, bm25_rank])[:top_k]
    elapsed = (time.perf_counter() - t0) * 1000

    return [documents[i] for i in fused], len(embeddings), elapsed


# ── SLM-routed retrieval ───────────────────────────────────────────────

def retrieve_slm(query, q_emb, registry, chroma_client, top_k=TOP_K):
    t0 = time.perf_counter()

    top_slms = find_top_n_slms(q_emb, registry, n=TOP_N_SLMS)

    all_chunks = []
    for slm_name, _ in top_slms:
        entry = registry[slm_name]
        chunks_path = Path(entry["chunks_json"])
        if not chunks_path.exists():
            continue
        with open(chunks_path) as f:
            chunk_ids = [c["id"] for c in json.load(f)]
        col = chroma_client.get_collection(entry["collection"])
        data = col.get(ids=chunk_ids, include=["embeddings", "documents", "metadatas"])
        for i, emb in enumerate(data["embeddings"]):
            e = np.array(emb, dtype=np.float32)
            e_norm = float(np.linalg.norm(e))
            q_norm = float(np.linalg.norm(q_emb))
            ds = float(np.dot(q_emb, e) / (q_norm * e_norm)) if e_norm > 0 else 0.0
            all_chunks.append({"text": data["documents"][i], "score": ds})

    if not all_chunks:
        return [], 0, (time.perf_counter() - t0) * 1000

    dense_rank = sorted(range(len(all_chunks)), key=lambda i: all_chunks[i]["score"], reverse=True)
    bm25       = BM25Okapi([tokenize(c["text"]) for c in all_chunks])
    bm25_sc    = bm25.get_scores(tokenize(query))
    bm25_rank  = sorted(range(len(all_chunks)), key=lambda i: float(bm25_sc[i]), reverse=True)

    fused   = rrf([dense_rank, bm25_rank])[:top_k]
    elapsed = (time.perf_counter() - t0) * 1000

    return [all_chunks[i]["text"] for i in fused], len(all_chunks), elapsed


# ── Generation ────────────────────────────────────────────────────────

_gen_tok = None
_gen_mdl = None

def _load_gen_model(model_name: str):
    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM
    global _gen_tok, _gen_mdl
    if _gen_tok is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        dtype  = torch.float16 if device == "cuda" else torch.float32
        print(f"  Carico {model_name} su {device}...")
        _gen_tok = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
        _gen_mdl = AutoModelForCausalLM.from_pretrained(
            model_name, torch_dtype=dtype, trust_remote_code=True
        ).to(device).eval()


def generate(query: str, docs: list, model_name: str) -> str:
    import re, torch
    from SLMAgent import build_prompt
    _load_gen_model(model_name)
    device = next(_gen_mdl.parameters()).device
    prompt = build_prompt(query, docs)
    inputs = _gen_tok(prompt, return_tensors="pt", truncation=True, max_length=2048).to(device)
    with torch.no_grad():
        out = _gen_mdl.generate(
            **inputs,
            max_new_tokens=MAX_NEW_TOKENS,
            do_sample=False,
            pad_token_id=_gen_tok.eos_token_id,
        )
    text = _gen_tok.decode(out[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True).strip()
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()


# ── Main ───────────────────────────────────────────────────────────────

def main():
    print("Carico modelli...")
    emb_model    = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    registry     = load_registry()

    col_name = COLLECTION or chroma_client.list_collections()[0].name
    col      = chroma_client.get_collection(col_name)
    total_chunks = col.count()

    print(f"Collection: {col_name}  |  chunk totali: {total_chunks}  |  SLM: {len(registry)}")
    print(f"Query: {len(QUERIES)}  |  top-k={TOP_K}  |  top-N SLM={TOP_N_SLMS}  |  model={GENERATION_MODEL}\n")

    def hit_rate(docs, keywords):
        joined = " ".join(docs).lower()
        hits = sum(1 for kw in keywords if kw in joined)
        return hits / len(keywords) * 100 if keywords else 0.0

    std_times, slm_times = [], []
    std_pools, slm_pools = [], []
    overlaps, std_hits, slm_hits = [], [], []
    md_rows = []

    SEP = "=" * 110
    for idx, (query_en, query_it, expected_kws) in enumerate(QUERIES, 1):
        print(f"\n[{idx}/{len(QUERIES)}] {query_en}")

        q_emb = emb_model.encode(
            [query_en], normalize_embeddings=True, convert_to_numpy=True
        )[0].astype(np.float32)

        docs_std, pool_std, t_std = retrieve_standard(query_en, q_emb, col)
        docs_slm, pool_slm, t_slm = retrieve_slm(query_en, q_emb, registry, chroma_client)

        overlap = len(set(docs_std[:TOP_K]) & set(docs_slm[:TOP_K])) / TOP_K * 100
        hr_std  = hit_rate(docs_std, expected_kws)
        hr_slm  = hit_rate(docs_slm, expected_kws)

        std_times.append(t_std); slm_times.append(t_slm)
        std_pools.append(pool_std); slm_pools.append(pool_slm)
        overlaps.append(overlap)
        std_hits.append(hr_std); slm_hits.append(hr_slm)

        speedup = t_std / t_slm if t_slm > 0 else float("inf")

        print(f"  Retrieval  —  StdRAG: {t_std:.1f}ms (pool={pool_std})  |  SLM-RAG: {t_slm:.1f}ms (pool={pool_slm})  speedup={speedup:.1f}x")
        print(f"  Generazione StdRAG...")
        t_gen0 = time.perf_counter()
        ans_std = generate(query_it, docs_std, GENERATION_MODEL)
        t_gen_std = (time.perf_counter() - t_gen0) * 1000

        print(f"  Generazione SLM-RAG...")
        t_gen0 = time.perf_counter()
        ans_slm = generate(query_it, docs_slm, GENERATION_MODEL)
        t_gen_slm = (time.perf_counter() - t_gen0) * 1000

        print(f"  Gen times  —  StdRAG: {t_gen_std:.0f}ms  |  SLM-RAG: {t_gen_slm:.0f}ms")
        print(f"  StdRAG : {ans_std[:100]}…")
        print(f"  SLM-RAG: {ans_slm[:100]}…")

        md_rows.append({
            "query_en":   query_en,
            "query_it":   query_it,
            "ans_std":    ans_std,
            "ans_slm":    ans_slm,
            "t_ret_std":  t_std,
            "t_ret_slm":  t_slm,
            "t_gen_std":  t_gen_std,
            "t_gen_slm":  t_gen_slm,
            "speedup":    speedup,
            "pool_std":   pool_std,
            "pool_slm":   pool_slm,
            "hr_std":     hr_std,
            "hr_slm":     hr_slm,
            "overlap":    overlap,
        })

    # ── Salva Markdown ─────────────────────────────────────────────────
    avg_speedup    = np.mean(std_times) / np.mean(slm_times)
    pool_reduction = (1 - np.mean(slm_pools) / np.mean(std_pools)) * 100

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(f"# Benchmark RAG — {col_name}\n\n")
        f.write(f"**Modello:** {GENERATION_MODEL}  |  **top-k:** {TOP_K}  |  **top-N SLM:** {TOP_N_SLMS}\n\n")
        f.write(f"| Metrica | StdRAG | SLM-RAG |\n|---|---|---|\n")
        f.write(f"| Speedup retrieval | — | **{avg_speedup:.1f}x** |\n")
        f.write(f"| Pool medio | {int(np.mean(std_pools))} chunk | {int(np.mean(slm_pools))} chunk (-{pool_reduction:.0f}%) |\n")
        f.write(f"| Keyword hit | {np.mean(std_hits):.0f}% | **{np.mean(slm_hits):.0f}%** |\n")
        f.write(f"| Overlap medio top-{TOP_K} | {np.mean(overlaps):.0f}% | — |\n\n")
        f.write("---\n\n")

        for i, r in enumerate(md_rows, 1):
            f.write(f"## {i}. {r['query_en']}\n\n")
            f.write(f"*{r['query_it']}*\n\n")
            f.write(f"| | StdRAG | SLM-RAG |\n|---|---|---|\n")
            f.write(f"| **Retrieval** | {r['t_ret_std']:.1f} ms | {r['t_ret_slm']:.1f} ms ({r['speedup']:.1f}x) |\n")
            f.write(f"| **Generazione** | {r['t_gen_std']:.0f} ms | {r['t_gen_slm']:.0f} ms |\n")
            f.write(f"| **Totale** | {r['t_ret_std']+r['t_gen_std']:.0f} ms | {r['t_ret_slm']+r['t_gen_slm']:.0f} ms |\n")
            f.write(f"| **Pool chunk** | {r['pool_std']} | {r['pool_slm']} |\n")
            f.write(f"| **Keyword hit** | {r['hr_std']:.0f}% | {r['hr_slm']:.0f}% |\n\n")
            f.write(f"### Risposta StdRAG\n\n{r['ans_std']}\n\n")
            f.write(f"### Risposta SLM-RAG\n\n{r['ans_slm']}\n\n")
            f.write("---\n\n")

    print(f"\nFile salvato: {OUTPUT_FILE}")
    print(f"\nRIEPILOGO")
    print(f"  Speedup retrieval     : {avg_speedup:.1f}x")
    print(f"  Riduzione pool        : {pool_reduction:.1f}%  ({int(np.mean(std_pools))} → {int(np.mean(slm_pools))} chunk)")
    print(f"  Overlap medio top-{TOP_K}  : {np.mean(overlaps):.0f}%")
    print(f"  Keyword hit StdRAG    : {np.mean(std_hits):.0f}%")
    print(f"  Keyword hit SLM-RAG   : {np.mean(slm_hits):.0f}%")


if __name__ == "__main__":
    main()
