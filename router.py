"""
router.py — SLM registry, assignment, routing, and merge logic.

SLM (Semantic Language Map): a semantic cluster of chunks from ChromaDB.
Primary representation: centroid_embedding (mean of all chunk embeddings).
Secondary representation: summary_embedding (embedding of LLM-generated topic_summary).
"""

import json
import re
import uuid
import numpy as np
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple
from sentence_transformers import SentenceTransformer


REGISTRY_PATH = "registry.json"
SLM_DATA_DIR = Path("slm_data")

# How often (in chunks added) the summary is refreshed during incremental ingestion.
SLM_SUMMARY_EVERY_N: int = 20

# Maximum total characters fed to the summary LLM across all chunk excerpts.
# 4000 chars ≈ 1143 tokens; with ~200 token prompt + 80 token output = ~1423 tokens,
# safely within the 2048-token limit used in _qwen_infer.
MAX_EXCERPT_CHARS: int = 4000


# Hardcoded summary LLM — always used, never configurable by the user
SUMMARY_MODEL: str = "Qwen/Qwen2.5-7B-Instruct"
#SUMMARY_MODEL: str = "Qwen/Qwen3.5-9B"
# Model-agnostic summary function type.
# Input:  list of chunk texts (representative subset)
# Output: (topic_summary: str, keywords: List[str])
SummaryFn = Callable[[List[str]], Tuple[str, List[str]]]

# Module-level cache: loaded once on first use
_summary_tok = None
_summary_mdl = None
_kw_llm      = None   # KeyLLM TextGeneration instance, built from _summary_mdl

_KW_PROMPT = (
    "You are a knowledge indexing assistant.\n"
    "I have the following document:\n[DOCUMENT]\n\n"
    "Extract 10-15 specific keywords from the document above.\n"
    "Use the same language as the document.\n"
    "Include: named entities (people, places, battles, events), dates or historical periods, "
    "factions, ideologies, movements, trade routes, concepts, technical terms.\n"
    "Exclude: generic words like 'chapter', 'text', 'section', 'page', 'document', "
    "'summary', 'list', 'approfondimenti', 'sintesi', 'mappe'.\n"
    "Exclude: page numbers, formatting labels, index entries.\n"
    "Return ONLY a comma-separated list of keywords:\n"
)


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


# ── All-chunk text retrieval ───────────────────────────────────────────

def _get_all_chunk_texts(
    chunk_ids: List[str],
    chroma_client,
    collection_name: str,
) -> List[str]:
    """
    Retrieve the text of EVERY chunk in the cluster from ChromaDB.

    Using all chunks (instead of a representative subset) ensures that the
    keywords extracted by the summary LLM cover the full semantic breadth of
    the cluster, not just its core or boundary.

    Returns:
        List of chunk text strings in ChromaDB storage order.
    """
    try:
        col = chroma_client.get_collection(collection_name)
    except Exception:
        return []

    data = col.get(ids=chunk_ids, include=["documents"])
    return data.get("documents") or []


def unload_summary_model() -> None:
    """
    Deallocate the Qwen summary model from memory.
    Call after refresh_all_summaries to free GPU/CPU RAM.
    """
    import gc
    import torch

    global _summary_tok, _summary_mdl, _kw_llm

    _kw_llm = None

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

def _qwen_infer(prompt: str, max_new_tokens: int) -> str:
    """Single inference call to the cached Qwen model. Returns decoded output text."""
    import torch

    device = next(_summary_mdl.parameters()).device
    inputs = _summary_tok(prompt, return_tensors="pt", truncation=True, max_length=2048).to(device)
    with torch.no_grad():
        out = _summary_mdl.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False,
            pad_token_id=_summary_tok.eos_token_id,
        )
    return _summary_tok.decode(out[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True).strip()


_NOISE_PREFIXES = ("note:", "the summary", "the keyword", "a knowledge", "while the")

# Italian + English stop words for KeyBERT and keyword filtering
_COMBINED_STOPWORDS = [
    # Italian articles, prepositions, conjunctions, pronouns
    "di", "a", "da", "in", "con", "su", "per", "tra", "fra",
    "il", "lo", "la", "i", "gli", "le", "un", "uno", "una",
    "e", "ed", "o", "ma", "se", "che", "non", "si",
    "ai", "al", "del", "della", "dei", "degli", "delle",
    "nel", "nella", "nei", "negli", "nelle",
    "dal", "dalla", "dai", "dagli", "dalle",
    "sul", "sulla", "sui", "sugli", "sulle",
    "col", "coi", "allo", "alla", "agli", "alle",
    "questo", "questa", "questi", "queste",
    "quello", "quella", "quelli", "quelle",
    "cui", "loro", "anche", "come", "più", "poi", "però",
    "quando", "dove", "chi", "suo", "sua", "suoi", "sue",
    "era", "erano", "fu", "furono", "è", "sono",
    "molto", "tanto", "tutto", "tutti", "tutte", "tutta",
    "ogni", "altro", "altra", "altri", "altre",
    "già", "ancora", "sempre", "mai", "solo",
    "vi", "ci", "mi", "ti", "ne", "li",
    "verso", "dopo", "prima", "durante", "mentre",
    "tale", "tali", "quanto", "nostro", "nostra",
    # English
    "the", "of", "and", "in", "to", "a", "is", "it", "its",
    "by", "for", "or", "at", "be", "as", "an", "was", "are",
    "with", "this", "that", "from", "on", "were", "not", "but",
    "have", "had", "has", "he", "she", "they", "we",
]

# Single-word noise terms from book structure/index
_NOISE_SINGLE_WORDS = frozenset([
    "approfondimenti", "multimediali", "sintesi", "mappe", "concettuali",
    "sezione", "volume", "capitolo", "pagina", "temi", "idea", "ricerca",
    "premesse", "elenco", "presentazione", "immagini", "utilizzate",
    "applicazioni", "caratteri", "protagonisti", "conseguenze", "invenzioni",
    "protagonista", "riassunto", "riepilogo", "scheda", "glossario",
])

# PDF artifact prefixes (line-break markers, encoding artifacts)
_KW_ARTIFACT_PREFIXES = ("br ", "c3 ", "c2 ", "br\n", "_")


def _is_meaningful_kw(kw: str) -> bool:
    """Return True if kw is a keyword worth keeping — not noise, not a fragment."""
    kw = kw.strip()
    if len(kw) < 4:
        return False
    # Starts with a digit (e.g. "18 organizzazione", "2media storia", "113 prussia")
    if kw[0].isdigit():
        return False
    # Ends with a 2+ digit number after space (page refs: "restaurazione 153", "napoleon 146")
    if re.search(r'\s\d{2,}$', kw):
        return False
    # PDF artifact prefixes
    if any(kw.lower().startswith(p) for p in _KW_ARTIFACT_PREFIXES):
        return False
    words = kw.lower().split()
    # All words are very short (e.g. "la xv", "il br", "dal xv")
    if all(len(w) <= 2 for w in words):
        return False
    # Single-word structural noise
    if len(words) == 1 and words[0] in _NOISE_SINGLE_WORDS:
        return False
    return True


def _parse_raw_keywords(raw: str) -> List[str]:
    """Parse a comma-separated keyword string, filtering out noise tokens."""
    result: List[str] = []
    for kw in raw.replace("\n", ",").split(","):
        kw = kw.strip()
        if not kw or len(kw) > 60:
            continue
        if kw.lower().startswith(_NOISE_PREFIXES):
            continue
        if not _is_meaningful_kw(kw):
            continue
        result.append(kw)
    return result


def make_keybert_summary_fn(
    embedding_model=None,
) -> "SummaryFn":
    """
    Return a SummaryFn that extracts keywords using KeyBERT.

    Pass the already-loaded SentenceTransformer embedding_model to reuse it
    instead of loading a separate copy.  If None, KeyBERT loads its default.

    Extraction per chunk (1- and 2-gram, MMR for diversity), then aggregated
    via _merge_keywords.
    """
    from keybert import KeyBERT

    kw_model = KeyBERT(model=embedding_model) if embedding_model is not None else KeyBERT()
    print(f"[router] KeyBERT inizializzato.")

    def _fn(texts: List[str]) -> Tuple[str, List[str]]:
        all_raw: List[str] = []
        for text in texts:
            if not text or not text.strip():
                continue
            results = kw_model.extract_keywords(
                text,
                keyphrase_ngram_range=(1, 2),
                stop_words=_COMBINED_STOPWORDS,
                use_mmr=True,
                diversity=0.6,
                top_n=10,
            )
            for kw, _score in results:
                if _is_meaningful_kw(kw):
                    all_raw.append(kw)
        return "", _merge_keywords(all_raw)

    return _fn


def _merge_keywords(keywords: List[str]) -> List[str]:
    """
    Deduplicate and merge a flat list of keywords collected across all chunks.

    Steps:
      1. Case-insensitive dedup — count occurrences, keep the most common casing.
      2. Substring absorption — if keyword A (normalized) is a substring of keyword B,
         A is dropped and its count is added to B (the more specific form wins).
      3. Sort by frequency descending so the most cross-chunk keywords come first.
    """
    # Step 1: normalize and count
    freq: Dict[str, int] = {}       # norm → count
    canonical: Dict[str, str] = {}  # norm → best original form (first seen)
    for kw in keywords:
        norm = kw.lower().strip().rstrip(".,;:")
        if not norm:
            continue
        if norm not in freq:
            freq[norm] = 0
            canonical[norm] = kw
        freq[norm] += 1

    # Step 2: substring absorption (longer/more-specific absorbs shorter/generic)
    norms = sorted(freq.keys(), key=len, reverse=True)  # longest first
    absorbed: set = set()
    for i, longer in enumerate(norms):
        if longer in absorbed:
            continue
        for shorter in norms[i + 1:]:
            if shorter in absorbed:
                continue
            if shorter in longer:  # e.g. "napoleon" ⊂ "napoleon bonaparte"
                freq[longer] += freq[shorter]
                absorbed.add(shorter)

    # Step 3: build result sorted by frequency, apply final noise filter, cap at 30
    result = [
        (canonical[n], freq[n])
        for n in norms
        if n not in absorbed and _is_meaningful_kw(canonical[n])
    ]
    result.sort(key=lambda x: -x[1])
    return [kw for kw, _ in result[:30]]


# Maximum prompts per GPU forward pass.
# RTX 4080 SUPER (16GB): Qwen2.5-7B float16 ≈ 14GB weights → ~2GB headroom.
# KV cache per sequence at ~870 token (720 input + 150 output) ≈ 50MB → max ~16.
# 8 is the safe ceiling accounting for PyTorch allocator fragmentation.
KEYWORD_BATCH_SIZE: int = 8


def _get_kw_pipe():
    """
    Build (or return cached) a HuggingFace text-generation pipeline
    wrapping the already-loaded Qwen model.
    Left-padding is forced so causal generation is correct when batch_size > 1.
    """
    from transformers import pipeline as hf_pipeline

    global _kw_llm
    if _kw_llm is not None:
        return _kw_llm

    _summary_tok.padding_side = "left"
    _kw_llm = hf_pipeline(
        "text-generation",
        model=_summary_mdl,
        tokenizer=_summary_tok,
        do_sample=False,
        pad_token_id=_summary_tok.eos_token_id,
        max_new_tokens=150,
        return_full_text=False,
    )
    return _kw_llm


def _qwen_summary_fn(texts: List[str]) -> Tuple[str, List[str]]:
    """
    Generate keywords for every chunk via GPU-batched HF pipeline inference.
    All prompts are built upfront; the pipeline processes KEYWORD_BATCH_SIZE
    prompts per forward pass (true GPU batching, not sequential).
    Keywords from all chunks are aggregated and deduplicated by _merge_keywords.
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

    # ── SUMMARY (disabilitata) ─────────────────────────────────────────
    # SUMMARY_SAMPLE = 20
    # SUMMARY_CHARS  = 200
    # if len(texts) <= SUMMARY_SAMPLE:
    #     sample = texts
    # else:
    #     idxs = [round(i * (len(texts) - 1) / (SUMMARY_SAMPLE - 1)) for i in range(SUMMARY_SAMPLE)]
    #     sample = [texts[i] for i in idxs]
    # excerpt = "\n\n".join(f"[Chunk {i+1}]: {t[:SUMMARY_CHARS]}" for i, t in enumerate(sample))
    # summary_prompt = (
    #     "You are a knowledge indexing assistant.\n"
    #     "Given the following text chunks, write ONE sentence describing the main topic.\n"
    #     "Reply with the sentence only, no labels, no extra text.\n\n"
    #     f"CHUNKS:\n{excerpt}\n\n"
    #     "SUMMARY:\n"
    # )
    # topic_summary = _qwen_infer(summary_prompt, max_new_tokens=80)
    # topic_summary = topic_summary.split("\n")[0].strip()
    topic_summary = ""

    # ── KEYWORDS via KeyLLM (sequential, un chunk per chiamata) ───────
    # llm = _get_kw_llm()
    # all_raw: List[str] = []
    # BATCH = 8
    # for batch_start in range(0, len(texts), BATCH):
    #     batch = texts[batch_start: batch_start + BATCH]
    #     batch_results = llm.extract_keywords(batch)
    #     for chunk_kws in batch_results:
    #         if not chunk_kws:
    #             continue
    #         for kw in chunk_kws:
    #             kw_str = kw[0] if isinstance(kw, tuple) else kw
    #             all_raw.extend(_parse_raw_keywords(kw_str))

    # ── KEYWORDS via GPU batching diretto ─────────────────────────────
    # Tutti i prompt vengono costruiti in anticipo sostituendo [DOCUMENT]
    # col testo di ogni chunk. Il pipeline processa KEYWORD_BATCH_SIZE prompt
    # per forward pass: più sequenze in parallelo sulla GPU invece di una
    # alla volta come fa KeyLLM internamente.
    pipe = _get_kw_pipe()
    prompts = [_KW_PROMPT.replace("[DOCUMENT]", t) for t in texts]
    all_raw: List[str] = []

    outputs = pipe(prompts, batch_size=KEYWORD_BATCH_SIZE)
    for out in outputs:
        generated = out[0]["generated_text"]
        all_raw.extend(_parse_raw_keywords(generated))

    keywords = _merge_keywords(all_raw)
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
    Regenerate topic_summary and keywords for an SLM using ALL chunks in the cluster.
    Always uses _qwen_summary_fn unless a custom summary_fn is passed.

    All chunk texts are passed to the summary function so that keywords reflect
    the full semantic content of the cluster, not just a representative subset.
    """
    if summary_fn is None:
        summary_fn = make_keybert_summary_fn()
    entry = registry[slm_name]
    chunks_path = Path(entry["chunks_json"])
    if not chunks_path.exists():
        return

    with open(chunks_path) as f:
        chunk_ids = [c["id"] for c in json.load(f)]
    if not chunk_ids:
        return

    # Fetch texts for every chunk in the cluster (no centroid-based filtering).
    texts = _get_all_chunk_texts(chunk_ids, chroma_client, entry["collection"])
    if not texts:
        return

    topic_summary, keywords = summary_fn(texts)
    if not topic_summary and not keywords:
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
