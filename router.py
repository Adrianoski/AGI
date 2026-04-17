"""
router.py — SLM registry, assignment, routing, and merge logic.

SLM (Semantic Language Map): a semantic cluster of chunks from ChromaDB.
Primary representation: centroid_embedding (mean of all chunk embeddings).
Secondary representation: summary_embedding (embedding of LLM-generated topic_summary).
"""

import json
import uuid
import numpy as np
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple
from sentence_transformers import SentenceTransformer


REGISTRY_PATH = "registry.json"
SLM_DATA_DIR = Path("slm_data")

# NEW: Summary regeneration threshold
SLM_SUMMARY_EVERY_N: int = 20

# NEW: Representative chunk selection
TOP_REPRESENTATIVE: int = 20   # most central chunks used for summary
TOP_DIVERSE: int = 5           # least central chunks added for coverage


# Hardcoded summary LLM — always used, never configurable by the user
SUMMARY_MODEL: str = "Qwen/Qwen2.5-7B-Instruct"

# Model-agnostic summary function type.
# Input:  list of chunk texts (representative subset)
# Output: (topic_summary: str, keywords: List[str])
SummaryFn = Callable[[List[str]], Tuple[str, List[str]]]

# Module-level cache: loaded once on first use
_summary_tok = None
_summary_mdl = None


# ── I/O helpers ────────────────────────────────────────────────────────

def _ensure_dirs() -> None:
    SLM_DATA_DIR.mkdir(exist_ok=True)


def load_registry() -> Dict:
    path = Path(REGISTRY_PATH)
    if not path.exists():
        return {}
    with open(path, "r") as f:
        return json.load(f)


def save_registry(registry: Dict) -> None:
    with open(REGISTRY_PATH, "w") as f:
        json.dump(registry, f, indent=2)


# ── NEW: Centroid computation ───────────────────────────────────────────

def _update_centroid(
    old_centroid: Optional[List[float]],
    new_embedding: np.ndarray,
    n: int,
) -> List[float]:
    """
    Incrementally update a normalized centroid by adding one new embedding.

    Args:
        old_centroid: current centroid as a float list, or None if first chunk.
        new_embedding: embedding of the incoming chunk (1-D float32 array).
        n: chunk count AFTER adding the new chunk.

    Returns:
        Updated, L2-normalized centroid as a float list.
    """
    if old_centroid is None or n == 1:
        vec = new_embedding.astype(np.float32)
    else:
        c = np.array(old_centroid, dtype=np.float32)
        vec = (c * (n - 1) + new_embedding) / n
    norm = float(np.linalg.norm(vec))
    return (vec / norm).tolist() if norm > 0 else vec.tolist()


# ── NEW: Representative chunk selection ────────────────────────────────

def _select_representative_chunks(
    chunk_ids: List[str],
    centroid: np.ndarray,
    chroma_client,
    collection_name: str,
    top_n: int = TOP_REPRESENTATIVE,
    top_diverse: int = TOP_DIVERSE,
) -> List[str]:
    """
    Select the most informative chunk texts for summary generation.

    Strategy:
        - top_n chunks with highest cosine similarity to centroid (core coverage)
        - top_diverse chunks with lowest similarity (boundary coverage)

    Returns:
        List of chunk text strings (deduplicated, order not guaranteed).
    """
    try:
        col = chroma_client.get_collection(collection_name)
    except Exception:
        return []

    data = col.get(ids=chunk_ids, include=["embeddings", "documents"])
    embeddings = data.get("embeddings")
    documents: List[str] = data.get("documents") or []

    if embeddings is None or len(embeddings) == 0:
        return []

    c_norm = float(np.linalg.norm(centroid))
    scored: List[Tuple[int, float]] = []

    for i, emb in enumerate(embeddings):
        e = np.array(emb, dtype=np.float32)
        e_norm = float(np.linalg.norm(e))
        sim = float(np.dot(centroid, e) / (c_norm * e_norm)) if (c_norm > 0 and e_norm > 0) else 0.0
        scored.append((i, sim))

    scored.sort(key=lambda x: x[1], reverse=True)

    selected: set = set()
    for idx, _ in scored[:top_n]:
        selected.add(idx)
    for idx, _ in scored[-top_diverse:]:
        selected.add(idx)

    return [documents[i] for i in selected if i < len(documents)]


def unload_summary_model() -> None:
    """
    Deallocate the Qwen summary model from memory.
    Call after refresh_all_summaries to free GPU/CPU RAM.
    """
    import gc
    import torch

    global _summary_tok, _summary_mdl

    if _summary_mdl is not None:
        _summary_mdl.cpu()
        del _summary_mdl
        _summary_mdl = None

    if _summary_tok is not None:
        del _summary_tok
        _summary_tok = None

    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

    print("[router] Modello summary deallocato.")


# ── Qwen summary function ──────────────────────────────────────────────

def _qwen_summary_fn(texts: List[str]) -> Tuple[str, List[str]]:
    """
    Generate topic_summary and keywords using Qwen2.5-7B-Instruct.
    Model is loaded once and cached at module level.
    """
    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM

    global _summary_tok, _summary_mdl

    if _summary_tok is None or _summary_mdl is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        dtype = torch.float16 if device == "cuda" else torch.float32
        print(f"[router] Carico {SUMMARY_MODEL} su {device}...")
        _summary_tok = AutoTokenizer.from_pretrained(SUMMARY_MODEL, trust_remote_code=True)
        _summary_mdl = AutoModelForCausalLM.from_pretrained(
            SUMMARY_MODEL, torch_dtype=dtype, trust_remote_code=True
        ).to(device).eval()

    device = next(_summary_mdl.parameters()).device
    excerpt = "\n\n".join(f"[Chunk {i+1}]: {t[:400]}" for i, t in enumerate(texts[:10]))
    prompt = (
        "You are a knowledge indexing assistant.\n"
        "Given the following text chunks, extract:\n"
        "1. A SUMMARY: one sentence describing the main topic.\n"
        "2. KEYWORDS: 15-25 specific keywords for every chunk (comma-separated).\n"
        "   Include: named entities, technical terms, places, people, events, concepts.\n"
        "   Do NOT include generic words like 'chapter', 'text', 'document'.\n\n"
        f"CHUNKS:\n{excerpt}\n\n"
        "SUMMARY:\n"
    )
    inputs = _summary_tok(prompt, return_tensors="pt", truncation=True, max_length=2048).to(device)
    with torch.no_grad():
        out = _summary_mdl.generate(
            **inputs,
            max_new_tokens=150,
            do_sample=migrate_centroids_to_summaries,
            pad_token_id=_summary_tok.eos_token_id,
        )
    decoded = _summary_tok.decode(out[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True).strip()

    topic_summary = decoded
    keywords: List[str] = []
    if "KEYWORDS:" in decoded:
        parts = decoded.split("KEYWORDS:", 1)
        topic_summary = parts[0].strip()
        raw_keywords = [k.strip() for k in parts[1].replace("\n", ",").split(",") if k.strip()]
        # Stop at first keyword that looks like Qwen self-commentary:
        # - longer than 60 chars (not a keyword)
        # - starts with "Note:" or "The " (meta-commentary pattern)
        _noise_prefixes = ("note:", "the summary", "the keyword", "a knowledge", "while the")
        clean: List[str] = []
        for kw in raw_keywords:
            if len(kw) > 60:
                break
            if kw.lower().startswith(_noise_prefixes):
                break
            clean.append(kw)
        keywords = clean

    return topic_summary, keywords


# ── Summary update ─────────────────────────────────────────────────────

def update_slm_summary(
    registry: Dict,
    slm_name: str,
    embedding_model: SentenceTransformer,
    chroma_client,
    summary_fn: Optional[SummaryFn] = None,
) -> None:
    """
    Regenerate topic_summary and keywords for an SLM using representative chunks.
    Always uses _qwen_summary_fn unless a custom summary_fn is passed.
    """
    if summary_fn is None:
        summary_fn = _qwen_summary_fn
    entry = registry[slm_name]
    chunks_path = Path(entry["chunks_json"])
    if not chunks_path.exists():
        return

    with open(chunks_path) as f:
        chunk_ids = [c["id"] for c in json.load(f)]
    if not chunk_ids:
        return

    centroid = np.array(entry["centroid_embedding"], dtype=np.float32)
    texts = _select_representative_chunks(
        chunk_ids, centroid, chroma_client, entry["collection"]
    )
    if not texts:
        return

    topic_summary, keywords = summary_fn(texts)
    if not topic_summary:
        return

    # Encode keywords as the routing vector — denser semantic signal than full sentences.
    # Fall back to topic_summary if no keywords were extracted.
    routing_text = ", ".join(keywords) if keywords else topic_summary
    summary_emb = embedding_model.encode(
        [routing_text], normalize_embeddings=True, convert_to_numpy=True
    )[0].tolist()

    entry["topic_summary"] = topic_summary
    entry["keywords"] = keywords
    entry["summary_embedding"] = summary_emb


# ── NEW: Batch summary refresh (call after full ingestion) ─────────────

def refresh_all_summaries(
    embedding_model: SentenceTransformer,
    chroma_client,
    summary_fn: Optional[SummaryFn] = None,
) -> int:
    """
    Regenerate topic_summary and summary_embedding for every SLM in the registry.
    Called automatically after every ingestion run.
    Always uses Qwen2.5-7B-Instruct (loaded once and cached).

    Returns:
        Number of SLMs updated.
    """
    registry = load_registry()
    count = 0
    for slm_name in list(registry.keys()):
        update_slm_summary(registry, slm_name, embedding_model, chroma_client, summary_fn)
        count += 1
    save_registry(registry)
    return count




# ── UPDATED: SLM creation ──────────────────────────────────────────────

def create_slm(
    registry: Dict,
    chunk_id: str,
    embedding: np.ndarray,
    collection_name: str,
) -> str:
    """
    Create a new SLM seeded from a single chunk.
    Centroid is initialized to the chunk embedding.
    Summary is left empty; call update_slm_summary / refresh_all_summaries later.
    """
    _ensure_dirs()
    slm_name = f"slm_{uuid.uuid4().hex[:8]}"

    registry[slm_name] = {
        "collection":        collection_name,
        "chunks_json":       str(SLM_DATA_DIR / f"{slm_name}_chunks.json"),
        "chunk_count":       1,
        "centroid_embedding": embedding.tolist(),  # NEW
        "topic_summary":     "",                   # NEW (populated by summary_fn)
        "keywords":          [],                   # NEW
        "summary_embedding": [],                   # NEW (populated by summary_fn)
    }

    chunks_path = SLM_DATA_DIR / f"{slm_name}_chunks.json"
    with open(chunks_path, "w") as f:
        json.dump([{"id": chunk_id}], f, indent=2)

    return slm_name


# ── UPDATED: Single chunk assignment ───────────────────────────────────

def assign_chunk(
    chunk_id: str,
    embedding: np.ndarray,
    collection_name: str,
    chroma_client,
    embedding_model: Optional[SentenceTransformer] = None,
    threshold: float = 0.65,
    summary_fn: Optional[SummaryFn] = None,
) -> str:
    """
    Assign a chunk to the most similar SLM (by centroid cosine similarity),
    or create a new SLM if no match exceeds threshold.

    Centroid is updated incrementally on every assignment.
    Summary is regenerated every SLM_SUMMARY_EVERY_N chunks when summary_fn is provided.
    """
    registry = load_registry()

    best_slm: Optional[str] = None
    best_score: float = -1.0
    e_norm = float(np.linalg.norm(embedding))

    for slm_name, entry in registry.items():
        centroid = entry.get("centroid_embedding")
        if not centroid:
            continue
        c = np.array(centroid, dtype=np.float32)
        c_norm = float(np.linalg.norm(c))
        if c_norm == 0 or e_norm == 0:
            continue
        score = float(np.dot(embedding, c) / (e_norm * c_norm))
        if score > best_score:
            best_score = score
            best_slm = slm_name

    if best_slm is None or best_score < threshold:
        slm_name = create_slm(registry, chunk_id, embedding, collection_name)
        save_registry(registry)
        return slm_name

    # Add chunk to existing SLM
    entry = registry[best_slm]
    n = entry["chunk_count"] + 1
    entry["chunk_count"] = n

    # UPDATED: Incremental centroid update
    entry["centroid_embedding"] = _update_centroid(
        entry.get("centroid_embedding"), embedding, n
    )

    chunks_path = Path(entry["chunks_json"])
    with open(chunks_path, "r") as f:
        chunks = json.load(f)
    chunks.append({"id": chunk_id})
    with open(chunks_path, "w") as f:
        json.dump(chunks, f, indent=2)

    # Periodic summary refresh during ingestion (optional)
    if (
        n % SLM_SUMMARY_EVERY_N == 0
        and summary_fn is not None
        and embedding_model is not None
    ):
        update_slm_summary(registry, best_slm, embedding_model, chroma_client, summary_fn)

    save_registry(registry)
    return best_slm


# ── UPDATED: Batch chunk assignment ────────────────────────────────────

def assign_chunks(
    chunks: List[Dict],
    embedding_model: SentenceTransformer,
    collection_name: str,
    chroma_client,
    threshold: float = 0.65,
    summary_fn: Optional[SummaryFn] = None,
) -> Dict[str, List[str]]:
    """
    Assign all chunks from a document to SLMs.
    Pass summary_fn to enable periodic in-flight summary updates (every SLM_SUMMARY_EVERY_N chunks).
    Call refresh_all_summaries after ingestion for a full summary pass.
    """
    assignments: Dict[str, List[str]] = {}
    for chunk in chunks:
        embedding = np.array(chunk["embedding"], dtype=np.float32)
        slm_name = assign_chunk(
            chunk_id=chunk["id"],
            embedding=embedding,
            collection_name=collection_name,
            chroma_client=chroma_client,
            embedding_model=embedding_model,
            threshold=threshold,
            summary_fn=summary_fn,
        )
        assignments.setdefault(slm_name, []).append(chunk["id"])
    return assignments


# ── Chapter-based SLM assignment ──────────────────────────────────────

def assign_chunks_by_chapter(
    chunks: List[Dict],
    collection_name: str,
) -> Dict[str, List[str]]:
    """
    Create one SLM per chapter using the 'chapter' metadata already present
    on each chunk (set by chunking.extract_chapters).

    This is the primary assignment strategy when chapter structure is detected.
    Each chapter becomes a single SLM; centroid is computed from all chunk
    embeddings in that chapter.

    Args:
        chunks:          list of dicts with keys id, text, chapter, embedding.
        collection_name: ChromaDB collection name stored in each SLM entry.

    Returns:
        assignments dict {slm_name: [chunk_id, ...]}
    """
    _ensure_dirs()

    # Group chunks by chapter title
    chapter_groups: Dict[str, List[Dict]] = {}
    for chunk in chunks:
        chapter = chunk.get("chapter", "Document") or "Document"
        chapter_groups.setdefault(chapter, []).append(chunk)

    registry = load_registry()
    assignments: Dict[str, List[str]] = {}

    for chapter_title, chapter_chunks in chapter_groups.items():
        slm_name = f"slm_{uuid.uuid4().hex[:8]}"

        chunk_ids = [c["id"] for c in chapter_chunks]

        # Compute centroid from all chunk embeddings in this chapter
        vecs = np.array([c["embedding"] for c in chapter_chunks], dtype=np.float32)
        centroid = vecs.mean(axis=0)
        norm = float(np.linalg.norm(centroid))
        centroid = (centroid / norm).tolist() if norm > 0 else centroid.tolist()

        # Write chunk list to disk
        chunks_path = SLM_DATA_DIR / f"{slm_name}_chunks.json"
        with open(chunks_path, "w") as f:
            json.dump([{"id": cid} for cid in chunk_ids], f, indent=2)

        registry[slm_name] = {
            "collection":         collection_name,
            "chunks_json":        str(chunks_path),
            "chunk_count":        len(chunk_ids),
            "centroid_embedding": centroid,
            "topic_summary":      chapter_title,   # use chapter title as initial summary
            "keywords":           [],
            "summary_embedding":  [],
        }
        assignments[slm_name] = chunk_ids

    save_registry(registry)
    print(f"[chapter] {len(assignments)} SLM creati da {len(chunks)} chunk "
          f"({len(chapter_groups)} capitoli) in '{collection_name}'.")
    return assignments


def assign_chunks_auto(
    chunks: List[Dict],
    embedding_model: SentenceTransformer,
    collection_name: str,
    chroma_client,
    threshold: float = 0.65,
) -> Tuple[Dict[str, List[str]], str]:
    """
    Primary entry point for chunk assignment.

    Strategy:
      - If multiple distinct chapters are detected → assign_chunks_by_chapter()
      - Otherwise (single 'Document' section or no chapters) → assign_chunks()

    Returns:
        (assignments, strategy_used)  where strategy_used is 'chapter' or 'cosine'.
    """
    chapters = {c.get("chapter", "Document") for c in chunks}
    # Fallback if only one chapter label (e.g. "Document") detected
    if len(chapters) <= 1:
        return assign_chunks(chunks, embedding_model, collection_name, chroma_client, threshold), "cosine"

    return assign_chunks_by_chapter(chunks, collection_name), "chapter"


# ── HDBSCAN batch clustering ───────────────────────────────────────────

# Path where the fitted HDBSCAN model is persisted between runs.
HDBSCAN_MODEL_PATH = Path("hdbscan_model.pkl")


def cluster_chunks_hdbscan(
    collection_name: str,
    chroma_client,
    min_cluster_size: int = 5,
    min_samples: int = 3,
    noise_threshold: float = 0.60,
    force_refit: bool = False,
) -> Dict[str, List[str]]:
    """
    Cluster ALL chunks in a ChromaDB collection using HDBSCAN.

    Replaces assign_chunks() for batch ingestion.  For incremental ingestion
    (new document added later), the saved model is reused via approximate_predict().
    If the fraction of noise points exceeds noise_threshold, HDBSCAN is refitted
    on all chunks automatically.

    Args:
        collection_name:  ChromaDB collection to cluster.
        chroma_client:    persistent ChromaDB client.
        min_cluster_size: minimum number of chunks to form a cluster (HDBSCAN param).
        min_samples:      controls how conservative the clustering is (HDBSCAN param).
        noise_threshold:  if fraction of noise points > this, refit from scratch.
        force_refit:      always refit even if a saved model exists.

    Returns:
        assignments dict {slm_name: [chunk_id, ...]} — same shape as assign_chunks().

    Notes:
        - Chunks labelled as noise (label == -1) by HDBSCAN are assigned to the
          nearest cluster centroid (fallback cosine assignment).
        - Requires: pip install hdbscan
    """
    try:
        import hdbscan as hdbscan_lib
        import pickle
    except ImportError:
        raise ImportError("pip install hdbscan")

    _ensure_dirs()

    # ── Load all embeddings from ChromaDB ──────────────────────────────
    col = chroma_client.get_collection(collection_name)
    data = col.get(include=["embeddings", "documents", "metadatas"])
    embeddings = data.get("embeddings")
    ids        = data.get("ids") or []

    if embeddings is None or len(embeddings) == 0:
        print("[hdbscan] Nessun embedding trovato nella collection.")
        return {}

    X = np.array(embeddings, dtype=np.float32)
    n_total = len(X)
    print(f"[hdbscan] {n_total} chunk da clusterizzare...")

    # ── PCA reduction before HDBSCAN ──────────────────────────────────
    # In 768D cosine distances are compressed in a narrow range → HDBSCAN
    # collapses everything into one cluster. PCA to 50D separates the
    # principal directions and makes density differences visible.
    from sklearn.decomposition import PCA
    n_components = min(50, n_total - 1, X.shape[1])
    print(f"[hdbscan] PCA {X.shape[1]}D → {n_components}D ...")
    pca = PCA(n_components=n_components, random_state=42)
    X_reduced = pca.fit_transform(X)
    var_explained = pca.explained_variance_ratio_.sum() * 100
    print(f"[hdbscan] Varianza spiegata: {var_explained:.1f}%")

    # ── Fit or reuse model ─────────────────────────────────────────────
    clusterer = None
    labels = None

    if not force_refit and HDBSCAN_MODEL_PATH.exists():
        print("[hdbscan] Carico modello salvato, uso approximate_predict()...")
        with open(HDBSCAN_MODEL_PATH, "rb") as f:
            saved = pickle.load(f)
        clusterer = saved["clusterer"]
        saved_pca = saved["pca"]
        X_pred = saved_pca.transform(X)
        labels_new, _ = hdbscan_lib.approximate_predict(clusterer, X_pred)
        noise_frac = float(np.sum(labels_new == -1)) / n_total
        print(f"[hdbscan] Noise fraction con modello esistente: {noise_frac:.1%}")

        if noise_frac > noise_threshold:
            print(f"[hdbscan] Noise > {noise_threshold:.0%} — rifitto da zero.")
            clusterer = None

        if clusterer is not None:
            labels = labels_new
            X_reduced = X_pred

    if clusterer is None:
        print("[hdbscan] Fitto HDBSCAN su tutti i chunk...")
        clusterer = hdbscan_lib.HDBSCAN(
            min_cluster_size=min_cluster_size,
            min_samples=min_samples,
            metric="euclidean",     # euclidean is correct after PCA reduction
            prediction_data=True,
        )
        labels = clusterer.fit_predict(X_reduced)
        with open(HDBSCAN_MODEL_PATH, "wb") as f:
            pickle.dump({"clusterer": clusterer, "pca": pca}, f)
        print(f"[hdbscan] Modello salvato in {HDBSCAN_MODEL_PATH}")

    unique_labels = set(labels)
    n_clusters = len(unique_labels - {-1})
    n_noise = int(np.sum(labels == -1))
    print(f"[hdbscan] {n_clusters} cluster · {n_noise} noise ({n_noise/n_total:.1%})")

    # ── Assign noise points to nearest cluster centroid ────────────────
    # Build centroid per cluster label first
    cluster_centroids: Dict[int, np.ndarray] = {}
    for lbl in unique_labels:
        if lbl == -1:
            continue
        mask = labels == lbl
        c = X[mask].mean(axis=0)
        norm = np.linalg.norm(c)
        cluster_centroids[lbl] = c / norm if norm > 0 else c

    if n_noise > 0 and cluster_centroids:
        for i, lbl in enumerate(labels):
            if lbl != -1:
                continue
            e = X[i]
            e_norm = np.linalg.norm(e)
            best_lbl, best_score = -1, -2.0
            for cl, centroid in cluster_centroids.items():
                score = float(np.dot(e / e_norm, centroid)) if e_norm > 0 else 0.0
                if score > best_score:
                    best_score = score
                    best_lbl = cl
            labels[i] = best_lbl
        print(f"[hdbscan] {n_noise} noise riassegnati al cluster più vicino.")

    # ── Build SLM registry from clusters ──────────────────────────────
    registry = load_registry()

    # Remove previous SLMs for this collection so we start fresh
    to_remove = [k for k, v in registry.items() if v.get("collection") == collection_name]
    for k in to_remove:
        chunks_path = Path(registry[k]["chunks_json"])
        if chunks_path.exists():
            chunks_path.unlink()
        del registry[k]
    if to_remove:
        print(f"[hdbscan] Rimossi {len(to_remove)} SLM precedenti per '{collection_name}'.")

    # Create one SLM per cluster
    label_to_slm: Dict[int, str] = {}
    for lbl in sorted(set(labels)):
        slm_name = f"slm_{uuid.uuid4().hex[:8]}"
        mask = np.where(labels == lbl)[0]
        chunk_ids_for_cluster = [ids[i] for i in mask]

        # Compute centroid
        vecs = X[mask]
        centroid = vecs.mean(axis=0)
        norm = np.linalg.norm(centroid)
        centroid = (centroid / norm).tolist() if norm > 0 else centroid.tolist()

        # Write chunk list to disk
        _ensure_dirs()
        chunks_path = SLM_DATA_DIR / f"{slm_name}_chunks.json"
        with open(chunks_path, "w") as f:
            json.dump([{"id": cid} for cid in chunk_ids_for_cluster], f, indent=2)

        registry[slm_name] = {
            "collection":         collection_name,
            "chunks_json":        str(chunks_path),
            "chunk_count":        len(chunk_ids_for_cluster),
            "centroid_embedding": centroid,
            "topic_summary":      "",
            "keywords":           [],
            "summary_embedding":  [],
        }
        label_to_slm[lbl] = slm_name

    save_registry(registry)

    assignments = {
        label_to_slm[lbl]: [ids[i] for i in np.where(labels == lbl)[0]]
        for lbl in sorted(set(labels))
    }
    print(f"[hdbscan] {len(assignments)} SLM creati e salvati nel registry.")
    return assignments


# ── UPDATED: Query-time routing ────────────────────────────────────────

def find_top_n_slms(
    query_embedding: np.ndarray,
    registry: Dict,
    n: int = 2,
) -> List[Tuple[str, float]]:
    """
    Route a query to the top-n SLMs by cosine similarity with summary_embedding.
    SLMs without a summary_embedding are skipped.

    Args:
        query_embedding: normalized query embedding (1-D float32).
        registry:        loaded registry dict.
        n:               number of SLMs to return.

    Returns:
        List of (slm_name, score) sorted descending.
    """
    q_norm = float(np.linalg.norm(query_embedding))
    if q_norm == 0:
        raise ValueError("Query embedding is a zero vector.")

    scores: List[Tuple[str, float]] = []

    for slm_name, entry in registry.items():
        summary_emb = entry.get("summary_embedding")
        if not summary_emb:
            continue

        sv = np.array(summary_emb, dtype=np.float32)
        sv_norm = float(np.linalg.norm(sv))
        if sv_norm == 0:
            continue

        score = float(np.dot(query_embedding, sv) / (q_norm * sv_norm))
        scores.append((slm_name, score))

    if not scores:
        raise RuntimeError("Nessun SLM con summary_embedding valido. Esegui prima l'ingestion.")

    scores.sort(key=lambda x: x[1], reverse=True)
    return scores[:n]


# ── UPDATED: SLM merge ─────────────────────────────────────────────────

def merge_close_slms(
    threshold: float = 0.90,
    embedding_model: Optional[SentenceTransformer] = None,
    chroma_client=None,
    summary_fn: Optional[SummaryFn] = None,
) -> List[Dict]:
    """
    Iteratively merge SLM pairs whose centroid_embedding cosine similarity >= threshold.
    Keeps the SLM with more chunks. Merged centroid is a weighted mean of both centroids.
    Regenerates summary after merge if summary_fn is provided.
    """
    merges: List[Dict] = []

    while True:
        registry = load_registry()
        slm_names = list(registry.keys())
        if len(slm_names) < 2:
            break

        best_pair: Optional[Tuple[str, str]] = None
        best_score: float = -1.0

        for i in range(len(slm_names)):
            for j in range(i + 1, len(slm_names)):
                a, b = slm_names[i], slm_names[j]
                ca = registry[a].get("centroid_embedding")
                cb = registry[b].get("centroid_embedding")
                if ca is None or cb is None:
                    continue
                ca_arr = np.array(ca, dtype=np.float32)
                cb_arr = np.array(cb, dtype=np.float32)
                na, nb = np.linalg.norm(ca_arr), np.linalg.norm(cb_arr)
                if na == 0 or nb == 0:
                    continue
                score = float(np.dot(ca_arr, cb_arr) / (na * nb))
                if score > best_score:
                    best_score = score
                    best_pair = (a, b)

        if best_pair is None or best_score < threshold:
            break

        a, b = best_pair
        count_a = registry[a]["chunk_count"]
        count_b = registry[b]["chunk_count"]
        kept, removed = (a, b) if count_a >= count_b else (b, a)

        # Merge chunk lists
        kept_path = Path(registry[kept]["chunks_json"])
        removed_path = Path(registry[removed]["chunks_json"])

        kept_chunks: List = []
        if kept_path.exists():
            with open(kept_path, "r") as f:
                kept_chunks = json.load(f)
        if removed_path.exists():
            with open(removed_path, "r") as f:
                kept_chunks += json.load(f)
            removed_path.unlink()

        with open(kept_path, "w") as f:
            json.dump(kept_chunks, f, indent=2)

        # UPDATED: Weighted centroid merge
        ca_arr = np.array(registry[kept].get("centroid_embedding", []), dtype=np.float32)
        cb_arr = np.array(registry[removed].get("centroid_embedding", []), dtype=np.float32)
        total = count_a + count_b
        merged = (ca_arr * count_a + cb_arr * count_b) / total
        norm = np.linalg.norm(merged)
        if norm > 0:
            merged /= norm

        registry[kept]["chunk_count"] = total
        registry[kept]["centroid_embedding"] = merged.tolist()
        del registry[removed]
        save_registry(registry)

        # Regenerate summary post-merge
        if embedding_model is not None and chroma_client is not None and summary_fn is not None:
            registry = load_registry()
            update_slm_summary(registry, kept, embedding_model, chroma_client, summary_fn)
            save_registry(registry)

        merges.append({"kept": kept, "removed": removed, "similarity": round(best_score, 6)})

    return merges


# ── UPDATED: Migration ─────────────────────────────────────────────────

def migrate_centroids_to_summaries(
    embedding_model: SentenceTransformer,
    chroma_client,
) -> int:
    """
    Migrate existing SLM entries to the new centroid-based format.
    Recomputes centroid_embedding from chunk embeddings stored in ChromaDB.
    Removes stale TF-IDF artifacts (summary, last_summary_at).
    Regenerates summaries with Qwen for all migrated SLMs.
    Skips SLMs that already have centroid_embedding.

    Returns:
        Number of SLMs migrated.
    """
    registry = load_registry()
    migrated: List[str] = []

    for slm_name, entry in registry.items():
        if entry.get("centroid_embedding"):
            continue

        chunks_path = Path(entry.get("chunks_json", ""))
        if not chunks_path.exists():
            continue

        with open(chunks_path) as f:
            chunk_ids = [c["id"] for c in json.load(f)]
        if not chunk_ids:
            continue

        try:
            col = chroma_client.get_collection(entry["collection"])
        except Exception:
            continue

        data = col.get(ids=chunk_ids, include=["embeddings"])
        embeddings = data.get("embeddings")
        if embeddings is None or len(embeddings) == 0:
            continue

        arr = np.array(embeddings, dtype=np.float32)
        centroid = arr.mean(axis=0)
        norm = np.linalg.norm(centroid)
        if norm > 0:
            centroid /= norm

        entry["centroid_embedding"] = centroid.tolist()
        entry.setdefault("topic_summary", "")
        entry.setdefault("keywords", [])
        entry.setdefault("summary_embedding", [])
        entry.pop("summary", None)
        entry.pop("last_summary_at", None)

        migrated.append(slm_name)

    if not migrated:
        return 0

    save_registry(registry)

    # Regenerate summaries for migrated SLMs
    registry = load_registry()
    for slm_name in migrated:
        update_slm_summary(registry, slm_name, embedding_model, chroma_client)
    save_registry(registry)

    return len(migrated)
