import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pathlib import Path
from typing import Dict, List, Tuple
import json
import numpy as np
import torch

from chunking import process_pdf
from router import (
    assign_chunks_auto, load_registry, merge_close_slms, find_top_n_slms,
    migrate_centroids_to_summaries, refresh_all_summaries, make_keybert_summary_fn,
)
import chromadb
from sentence_transformers import SentenceTransformer
import gradio as gr

embedding_model = SentenceTransformer("BAAI/bge-m3")
chroma_client = chromadb.PersistentClient(path="./chroma_db")

# Migrazione lazy: converte SLM con centroide → summary embedding
_migrated = migrate_centroids_to_summaries(embedding_model, chroma_client)
if _migrated:
    print(f"[migration] {_migrated} SLM migrati da centroide a summary embedding.")

CHUNK_SIZE = 1500
OVERLAP = 100
TOP_N_SLMS = 3
TOP_K_CHUNKS = 5
MAX_TOKENS = 256
RRF_K = 60
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
_model_cache: Dict = {}


# ── Ingestion ──────────────────────────────────────────────────────────

def get_registry_display() -> str:
    registry = load_registry()
    if not registry:
        return "Registry vuoto."
    lines = []
    for slm_name, entry in registry.items():
        summary_preview = entry.get("topic_summary", "—")[:80]
        lines.append(
            f"{slm_name}\n"
            f"  chunks     : {entry['chunk_count']}\n"
            f"  collection : {entry['collection']}\n"
            f"  summary    : {summary_preview}…\n"
        )
    return "\n".join(lines)


def get_collections():
    return [c.name for c in chroma_client.list_collections()]


def upload_and_chunk(pdf_file, collection_name):
    if pdf_file is None:
        return "Nessun file caricato.", "", gr.update(choices=get_collections()), get_registry_display()
    if not collection_name.strip():
        return "Inserisci un nome per la collection.", "", gr.update(choices=get_collections()), get_registry_display()

    col_name = collection_name.strip()
    collection = chroma_client.get_or_create_collection(
        col_name,
        metadata={"hnsw:space": "cosine"}
    )
    chunks, _, profile_summary = process_pdf(
        pdf_path=pdf_file,
        collection=collection,
        embedding_model=embedding_model,
    )

    assignments, _strategy = assign_chunks_auto(chunks, embedding_model, col_name, chroma_client, threshold=0.55)
    merges = merge_close_slms(threshold=0.88, embedding_model=embedding_model, chroma_client=chroma_client)

    keybert_fn = make_keybert_summary_fn(embedding_model)
    n_refreshed = refresh_all_summaries(embedding_model, chroma_client, summary_fn=keybert_fn)
    summary_line = f"\n{n_refreshed} SLM keyword estratte con KeyBERT."

    merge_line = f"\n{len(merges)} SLM uniti per prossimità." if merges else ""
    summary = (
        f"{len(chunks)} chunk salvati nella collection '{col_name}'.\n"
        f"Documento rilevato: {profile_summary}\n"
        f"{len(assignments)} SLM aggiornati nel registry.{merge_line}{summary_line}"
    )
    preview_data = [
        {"id": c["id"][:8] + "...", "chapter": c["chapter"], "text": c["text"][:130] + "..."}
        for c in chunks[:5]
    ]
    preview = json.dumps(preview_data, indent=2, ensure_ascii=False)
    return summary, preview, gr.update(choices=get_collections()), get_registry_display()


# ── Query ──────────────────────────────────────────────────────────────

def _tokenize(text: str) -> List[str]:
    import re
    return re.sub(r'[^\w\s]', ' ', text.lower()).split()


def _rrf(rankings: List[List[int]], k: int = RRF_K) -> List[int]:
    """Reciprocal Rank Fusion: fuse multiple rankings into one."""
    scores: Dict[int, float] = {}
    for ranking in rankings:
        for rank, idx in enumerate(ranking):
            scores[idx] = scores.get(idx, 0.0) + 1.0 / (k + rank + 1)
    return sorted(scores.keys(), key=lambda x: scores[x], reverse=True)


def _get_collection_for_slm(slm_entry: Dict):
    """Return the ChromaDB collection for an SLM entry, with fallback for legacy data."""
    collection_name = slm_entry.get("collection", "")
    try:
        return chroma_client.get_collection(collection_name), collection_name
    except Exception:
        cols = chroma_client.list_collections()
        if not cols:
            return None, ""
        col = chroma_client.get_collection(cols[0].name)
        return col, cols[0].name


def _retrieve_hybrid(
    query: str,
    query_emb: np.ndarray,
    top_slms: List[Tuple[str, float]],
    registry: Dict,
    top_k: int,
) -> Tuple[List[str], List[Dict], List[str], List[float]]:
    """
    Hybrid retrieval: dense (cosine) + BM25 fused with RRF over the
    chunks of the top-N SLMs.
    Returns (docs, metadatas, slm_sources, dense_scores).
    """
    from rank_bm25 import BM25Okapi

    all_chunks = []  # list of {text, meta, slm, dense_score}
    q_norm = float(np.linalg.norm(query_emb))

    for slm_name, _ in top_slms:
        slm_entry = registry[slm_name]
        chunks_path = Path(slm_entry["chunks_json"])
        if not chunks_path.exists():
            continue

        with open(chunks_path) as f:
            chunk_ids = [c["id"] for c in json.load(f)]
        if not chunk_ids:
            continue

        col, _ = _get_collection_for_slm(slm_entry)
        if col is None:
            continue

        data = col.get(ids=chunk_ids, include=["embeddings", "documents", "metadatas"])
        embeddings = data.get("embeddings")
        documents  = data.get("documents") or []
        metadatas  = data.get("metadatas") or []

        if embeddings is None or len(embeddings) == 0:
            continue

        for i, emb in enumerate(embeddings):
            e = np.array(emb, dtype=np.float32)
            e_norm = float(np.linalg.norm(e))
            dense_score = float(np.dot(query_emb, e) / (q_norm * e_norm)) if e_norm > 0 else 0.0
            all_chunks.append({
                "text":        documents[i] if i < len(documents) else "",
                "meta":        metadatas[i] if i < len(metadatas) else {},
                "slm":         slm_name,
                "dense_score": dense_score,
            })

    if not all_chunks:
        return [], [], [], []

    # Dense ranking
    dense_ranking = sorted(range(len(all_chunks)),
                           key=lambda i: all_chunks[i]["dense_score"], reverse=True)

    # BM25 ranking
    corpus = [_tokenize(c["text"]) for c in all_chunks]
    bm25 = BM25Okapi(corpus)
    bm25_scores = bm25.get_scores(_tokenize(query))
    bm25_ranking = sorted(range(len(all_chunks)),
                          key=lambda i: float(bm25_scores[i]), reverse=True)

    # RRF fusion
    fused = _rrf([dense_ranking, bm25_ranking])
    top_indices = fused[:top_k]

    return (
        [all_chunks[i]["text"]                        for i in top_indices],
        [all_chunks[i]["meta"] or {}                  for i in top_indices],
        [all_chunks[i]["slm"]                         for i in top_indices],
        [round(all_chunks[i]["dense_score"], 4)       for i in top_indices],
    )


def _generate_streaming(query: str, context_chunks: List[str], model_name: str, max_tokens: int):
    """Loads the model once, then streams generated tokens via TextIteratorStreamer."""
    from transformers import AutoTokenizer, AutoModelForCausalLM, TextIteratorStreamer
    from threading import Thread
    global _model_cache
    if model_name not in _model_cache:
        dtype = torch.float16 if DEVICE == "cuda" else torch.float32
        tok = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
        mdl = AutoModelForCausalLM.from_pretrained(
            model_name, torch_dtype=dtype, trust_remote_code=True
        ).to(DEVICE).eval()
        _model_cache[model_name] = (tok, mdl)

    tok, mdl = _model_cache[model_name]
    from SLMAgent import build_messages, _apply_chat_template_no_think
    text = _apply_chat_template_no_think(tok, build_messages(query, context_chunks))
    inputs = tok(text, return_tensors="pt", truncation=True, max_length=2048).to(DEVICE)

    streamer = TextIteratorStreamer(tok, skip_prompt=True, skip_special_tokens=True)
    gen_kwargs = {
        **inputs,
        "streamer":       streamer,
        "max_new_tokens": max_tokens,
        "temperature":    0.1,
        "do_sample":      False,
        "pad_token_id":   tok.eos_token_id,
    }
    Thread(target=mdl.generate, kwargs=gen_kwargs, daemon=True).start()

    for chunk in streamer:
        yield chunk


def query_fn(query: str, model_name: str):
    if not query.strip():
        yield "Inserisci una domanda.", "", "—"
        return

    registry = load_registry()
    if not registry:
        yield "Registry vuoto. Carica prima un PDF.", "", "—"
        return

    q_emb = embedding_model.encode(
        [query], normalize_embeddings=True, convert_to_numpy=True
    )[0].astype(np.float32)

    # 1. Route: find top-N SLMs by centroid similarity
    top_slms = find_top_n_slms(q_emb, registry, n=TOP_N_SLMS)

    routing_lines = "SLM selezionati (routing):\n"
    for slm_name, score in top_slms:
        n_chunks = registry[slm_name].get("chunk_count", "?")
        routing_lines += f"  {slm_name}  score={score:.4f}  chunks={n_chunks}\n"

    # 2. Hybrid retrieval: dense + BM25 + RRF
    docs, metas, slm_sources, dense_scores = _retrieve_hybrid(
        query, q_emb, top_slms, registry, TOP_K_CHUNKS
    )

    if not docs:
        yield "Nessun chunk trovato.", "", routing_lines
        return

    pool_size = sum(registry[s].get("chunk_count", 0) for s, _ in top_slms)
    routing_info = routing_lines + f"\nPool: {pool_size} chunk · dense + BM25 → RRF · device: {DEVICE}"

    chunks_text = ""
    for i, (doc, meta, slm, score) in enumerate(zip(docs, metas, slm_sources, dense_scores), 1):
        chapter = meta.get("chapter", "—") if meta else "—"
        chunks_text += f"[{i}] {score}  {slm}  {chapter}\n"
        chunks_text += (doc[:420] + "…" if len(doc) > 420 else doc) + "\n\n"

    if not model_name.strip():
        yield (
            "Nessun modello specificato — solo retrieval.\n\n"
            "Inserisci un nome modello HuggingFace per generare una risposta.",
            chunks_text, routing_info
        )
        return

    # 3. Show chunks immediately, then stream the answer
    loading_msg = (
        "⏳ Caricamento modello…"
        if model_name.strip() not in _model_cache
        else "⏳ Generazione in corso…"
    )
    yield loading_msg, chunks_text, routing_info

    try:
        import re as _re
        partial = ""
        for chunk in _generate_streaming(query, docs, model_name.strip(), MAX_TOKENS):
            partial += chunk
            display = _re.sub(r"<think>.*?</think>", "", partial, flags=_re.DOTALL).strip()
            yield display, chunks_text, routing_info
    except Exception as e:
        yield f"Errore durante la generazione:\n{e}", chunks_text, routing_info


# ── CSS ────────────────────────────────────────────────────────────────

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Variables ───────────────────────────────────────────── */
:root {
    --bg:          #0f1117;
    --surface:     #1a1d27;
    --surface2:    #22263a;
    --border:      #2d3148;
    --border2:     #3d4268;
    --text:        #e8e8f5;
    --text-muted:  #8b8fa8;
    --text-dim:    #4a4e6a;
    --accent:      #6366f1;
    --accent-h:    #818cf8;
    --accent-glow: rgba(99,102,241,0.18);
    --green:       #34d399;
    --green-bg:    #0d2620;
    --green-bd:    #1a4535;
    --radius:      14px;
    --radius-sm:   9px;
    --shadow:      0 4px 24px rgba(0,0,0,0.45);
}

*, *::before, *::after { box-sizing: border-box; }

body, .gradio-container {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Inter', sans-serif !important;
    min-height: 100vh;
}

.gradio-container {
    max-width: 100% !important;
    width: 100% !important;
    margin: 0 !important;
    padding: 0 40px 56px 40px !important;
}

/* ── Tabs ────────────────────────────────────────────────── */
.tabs > .tab-nav {
    background: var(--bg) !important;
    border-bottom: 1px solid var(--border) !important;
    padding: 0 8px !important;
    position: sticky;
    top: 0;
    z-index: 20;
    backdrop-filter: blur(12px);
}
.tabs > .tab-nav > button {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.9rem !important;
    font-weight: 500 !important;
    color: var(--text-muted) !important;
    letter-spacing: 0.01em !important;
    padding: 18px 28px !important;
    border: none !important;
    background: transparent !important;
    border-bottom: 2px solid transparent !important;
    transition: color 0.2s, border-color 0.2s !important;
    border-radius: 0 !important;
}
.tabs > .tab-nav > button.selected {
    color: var(--accent-h) !important;
    border-bottom-color: var(--accent) !important;
}
.tabs > .tab-nav > button:hover:not(.selected) {
    color: var(--text) !important;
    background: rgba(255,255,255,0.03) !important;
}

/* ── Cards ───────────────────────────────────────────────── */
#ingestion-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 48px 56px;
    max-width: 860px;
    margin: 36px auto 0 auto;
    box-shadow: var(--shadow);
}

#query-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 48px 56px;
    margin-top: 36px;
    box-shadow: var(--shadow);
}

/* ── Headers ─────────────────────────────────────────────── */
#ing-hdr, #q-hdr {
    margin-bottom: 36px;
    padding-bottom: 28px;
    border-bottom: 1px solid var(--border);
}
#ing-hdr h1, #q-hdr h1 {
    font-family: 'Inter', sans-serif !important;
    font-size: 1.75rem !important;
    font-weight: 700 !important;
    color: var(--text) !important;
    letter-spacing: -0.03em !important;
    margin: 0 0 6px 0 !important;
    line-height: 1.2 !important;
    background: linear-gradient(135deg, var(--text) 0%, var(--accent-h) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
#ing-hdr p, #q-hdr p {
    font-size: 0.9rem !important;
    color: var(--text-muted) !important;
    letter-spacing: 0.01em !important;
    margin: 0 !important;
    font-weight: 400 !important;
}

/* ── Gradio reset ────────────────────────────────────────── */
.block, .gr-box, .gr-form {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
}

/* ── Labels ──────────────────────────────────────────────── */
label > span, .svelte-1gfkn6j {
    font-family: 'Inter', sans-serif !important;
    color: var(--text-muted) !important;
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    margin-bottom: 8px !important;
    display: block !important;
}

/* ── Inputs & Textareas ──────────────────────────────────── */
input[type=text], textarea {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: var(--radius-sm) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.95rem !important;
    line-height: 1.65 !important;
    padding: 13px 16px !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
input[type=text]:focus, textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px var(--accent-glow) !important;
    outline: none !important;
}
input[type=text]::placeholder, textarea::placeholder {
    color: var(--text-dim) !important;
}

/* ── File upload ─────────────────────────────────────────── */
.upload-button, .file-preview, [data-testid="file-upload"] {
    background: var(--surface2) !important;
    border: 1.5px dashed var(--border2) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-muted) !important;
    font-size: 0.95rem !important;
    transition: border-color 0.2s, color 0.2s !important;
    min-height: 110px !important;
}
.upload-button:hover, [data-testid="file-upload"]:hover {
    border-color: var(--accent) !important;
    color: var(--accent-h) !important;
    background: rgba(99,102,241,0.05) !important;
}

/* ── Buttons ─────────────────────────────────────────────── */
button.primary {
    background: var(--accent) !important;
    border: none !important;
    color: #fff !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.9rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.02em !important;
    border-radius: var(--radius-sm) !important;
    padding: 14px 0 !important;
    width: 100% !important;
    cursor: pointer !important;
    transition: background 0.2s, box-shadow 0.2s, transform 0.1s !important;
    margin-top: 8px !important;
    box-shadow: 0 2px 12px rgba(99,102,241,0.35) !important;
}
button.primary:hover {
    background: var(--accent-h) !important;
    box-shadow: 0 4px 20px rgba(99,102,241,0.5) !important;
    transform: translateY(-1px) !important;
}
button.primary:active {
    transform: translateY(0) !important;
    box-shadow: 0 1px 6px rgba(99,102,241,0.3) !important;
}

/* ── Sliders ─────────────────────────────────────────────── */
input[type=range] {
    accent-color: var(--accent) !important;
}

/* ── Dropdown ────────────────────────────────────────────── */
select {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: var(--radius-sm) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 11px 14px !important;
}

/* ── Divider ─────────────────────────────────────────────── */
.divider {
    border: none;
    border-top: 1px solid var(--border);
    margin: 28px 0;
}

/* ── Ingestion outputs ───────────────────────────────────── */
#status textarea {
    background: var(--green-bg) !important;
    border: 1px solid var(--green-bd) !important;
    color: var(--green) !important;
    border-radius: var(--radius-sm) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.9rem !important;
}
#preview textarea {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    color: var(--text-muted) !important;
    border-radius: var(--radius-sm) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.82rem !important;
    line-height: 1.7 !important;
}
#registry textarea {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    color: #9ca3c8 !important;
    border-radius: var(--radius-sm) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.82rem !important;
    line-height: 1.8 !important;
}

/* ── Query outputs ───────────────────────────────────────── */
#answer textarea {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: var(--radius-sm) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.97rem !important;
    line-height: 1.8 !important;
}
#chunks-out textarea {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    color: var(--text-muted) !important;
    border-radius: var(--radius-sm) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.8rem !important;
    line-height: 1.75 !important;
}
#routing textarea {
    background: var(--green-bg) !important;
    border: 1px solid var(--green-bd) !important;
    color: #6ee7a0 !important;
    border-radius: var(--radius-sm) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.85rem !important;
    line-height: 1.7 !important;
}

/* ── Misc ────────────────────────────────────────────────── */
footer { display: none !important; }
svg { color: var(--text-dim) !important; }
.wrap { background: transparent !important; }

/* ── Scrollbar ───────────────────────────────────────────── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 99px; }
::-webkit-scrollbar-thumb:hover { background: var(--accent); }
"""

# ── UI ─────────────────────────────────────────────────────────────────

with gr.Blocks(
    title="Mecella/Laura RAG",
) as demo:

    with gr.Tabs():

        # ── INGESTION ──────────────────────────────────────────────────
        with gr.TabItem("Ingestion"):
            with gr.Column(elem_id="ingestion-card"):
                with gr.Column(elem_id="ing-hdr"):
                    gr.HTML(
                        "<h1>PDF Ingestion</h1>"
                        "<p>chunking · embedding · SLM routing · merge</p>"
                    )

                pdf_input = gr.File(
                    label="Documento PDF",
                    file_types=[".pdf"],
                    type="filepath"
                )
                collection_input = gr.Textbox(
                    label="Nome Collection",
                    placeholder="es. optimization_collection"
                )
                run_btn = gr.Button("Avvia Chunking", variant="primary")

                gr.HTML('<hr class="divider">')

                status_out = gr.Textbox(
                    label="Stato", interactive=False, elem_id="status"
                )
                preview_out = gr.Textbox(
                    label="Anteprima — primi 5 chunk",
                    lines=8, interactive=False, elem_id="preview"
                )
                collections_out = gr.Dropdown(
                    label="Collection in ChromaDB",
                    choices=get_collections(),
                    interactive=False
                )

                gr.HTML('<hr class="divider">')

                registry_out = gr.Textbox(
                    label="Registry SLM",
                    lines=10, interactive=False, elem_id="registry"
                )

        # ── QUERY ──────────────────────────────────────────────────────
        with gr.TabItem("Query"):
            with gr.Column(elem_id="query-card"):
                with gr.Column(elem_id="q-hdr"):
                    gr.HTML(
                        "<h1>Query</h1>"
                        "<p>top-N SLM routing · dense + BM25 · RRF fusion · generazione opzionale</p>"
                    )

                query_input = gr.Textbox(
                    label="Domanda",
                    lines=3,
                    placeholder="Es. Tell me about hybrid optimization methods..."
                )

                model_input = gr.Textbox(
                    label="Modello HuggingFace",
                    value="Qwen/Qwen3.5-4B",
                )

                query_btn = gr.Button("Invia Query", variant="primary")

                routing_out = gr.Textbox(
                    label="Routing", lines=4, interactive=False, elem_id="routing"
                )

                gr.HTML('<hr class="divider">')

                with gr.Row():
                    with gr.Column(scale=55):
                        answer_out = gr.Textbox(
                            label="Risposta",
                            lines=16, interactive=False, elem_id="answer"
                        )
                    with gr.Column(scale=45):
                        chunks_out = gr.Textbox(
                            label="Chunk recuperati",
                            lines=16, interactive=False, elem_id="chunks-out"
                        )

    # ── Events ─────────────────────────────────────────────────────────
    run_btn.click(
        fn=upload_and_chunk,
        inputs=[pdf_input, collection_input],
        outputs=[status_out, preview_out, collections_out, registry_out]
    )
    query_btn.click(
        fn=query_fn,
        inputs=[query_input, model_input],
        outputs=[answer_out, chunks_out, routing_out]
    )

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        theme=gr.themes.Base(
            primary_hue="violet",
            neutral_hue="slate",
            font=[gr.themes.GoogleFont("Inter"), "sans-serif"],
        ),
        css=CSS,
    )
