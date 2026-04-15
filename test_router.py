"""
test_router.py
--------------
Test della logica router senza PDF né LLM.
Usa chunk sintetici e un ChromaDB in-memory.

Usage:
    python test_router.py
"""

import shutil
import numpy as np
import chromadb
from pathlib import Path
from sentence_transformers import SentenceTransformer

from router import (
    load_registry, save_registry,
    create_slm, assign_chunks, find_top_n_slms, merge_close_slms,
    refresh_all_summaries, _update_centroid, _select_representative_chunks,
)

EMBED_MODEL = "sentence-transformers/all-mpnet-base-v2"
TEST_COLLECTION = "test_collection"
REGISTRY_BACKUP = Path("registry.json.bak")
REGISTRY_PATH = Path("registry.json")
SLM_DATA_DIR = Path("slm_data")


# ── Helpers ────────────────────────────────────────────────────────────

def backup_registry():
    if REGISTRY_PATH.exists():
        shutil.copy(REGISTRY_PATH, REGISTRY_BACKUP)

def restore_registry():
    if REGISTRY_BACKUP.exists():
        shutil.copy(REGISTRY_BACKUP, REGISTRY_PATH)
        REGISTRY_BACKUP.unlink()
    elif REGISTRY_PATH.exists():
        REGISTRY_PATH.unlink()

def ok(label): print(f"  [OK] {label}")
def fail(label, reason): print(f"  [FAIL] {label}: {reason}")

def assert_close(a, b, tol=1e-4, label=""):
    if abs(a - b) > tol:
        fail(label, f"{a:.6f} != {b:.6f}")
    else:
        ok(label)

def assert_true(cond, label):
    if cond: ok(label)
    else: fail(label, "condition is False")


# ── Tests ──────────────────────────────────────────────────────────────

def test_incremental_centroid():
    print("\n=== test_incremental_centroid ===")
    rng = np.random.default_rng(42)

    vecs = [rng.standard_normal(384).astype(np.float32) for _ in range(5)]
    for v in vecs:
        v /= np.linalg.norm(v)

    centroid = None
    for i, v in enumerate(vecs, 1):
        centroid = _update_centroid(centroid, v, i)

    centroid_arr = np.array(centroid, dtype=np.float32)
    expected = np.mean(vecs, axis=0)
    expected /= np.linalg.norm(expected)

    # Centroid is normalized at each step → approximation of the true batch mean direction.
    # Cosine similarity with the exact normalized mean should be close to 1.0 (tolerance ~0.05).
    centroid_norm = centroid_arr / np.linalg.norm(centroid_arr)
    cos = float(np.dot(centroid_norm, expected))
    assert_close(cos, 1.0, tol=0.06, label="centroid direction approximates batch mean (cosine > 0.94)")
    assert_close(float(np.linalg.norm(centroid_arr)), 1.0, tol=1e-3, label="centroid is normalized")


def test_routing_score(embedding_model, chroma_client):
    print("\n=== test_routing_score ===")
    backup_registry()

    # Two groups of semantically similar texts
    group_a = [
        "gradient descent optimization convex loss function",
        "stochastic gradient convergence learning rate schedule",
        "optimizer momentum Adam weight decay regularization",
    ]
    group_b = [
        "neural network architecture transformer attention layer",
        "encoder decoder multi-head self-attention residual connection",
        "BERT GPT language model pre-training fine-tuning",
    ]

    col = chroma_client.get_or_create_collection(TEST_COLLECTION, metadata={"hnsw:space": "cosine"})

    all_chunks = []
    for texts in [group_a, group_b]:
        for t in texts:
            emb = embedding_model.encode([t], normalize_embeddings=True, convert_to_numpy=True)[0]
            cid = f"test_{abs(hash(t)) % 10**8}"
            col.add(ids=[cid], embeddings=[emb.tolist()], documents=[t], metadatas=[{"chapter": "test"}])
            all_chunks.append({"id": cid, "text": t, "embedding": emb.tolist()})

    assign_chunks(all_chunks, embedding_model, TEST_COLLECTION, chroma_client, threshold=0.60)

    # Mock summary_fn: encodes the first chunk text as summary (no Qwen needed)
    def mock_summary_fn(texts):
        return texts[0][:200], texts[0].split()[:10]

    refresh_all_summaries(embedding_model, chroma_client, summary_fn=mock_summary_fn)

    registry = load_registry()
    assert_true(len(registry) >= 2, f"at least 2 SLMs created ({len(registry)} found)")

    # Query about optimization → should route to group_a SLM
    query_a = "how does gradient descent minimize the loss?"
    q_emb = embedding_model.encode([query_a], normalize_embeddings=True, convert_to_numpy=True)[0]
    top = find_top_n_slms(q_emb, registry, n=2)
    assert_true(len(top) == 2, "find_top_n_slms returns exactly 2")
    assert_true(top[0][1] > top[1][1], "first SLM has higher score than second")
    print(f"  Query: '{query_a}'")
    for name, score in top:
        n_chunks = registry[name]["chunk_count"]
        print(f"    {name}  score={score:.4f}  chunks={n_chunks}")

    # Verify score is pure cosine similarity with summary_embedding
    entry = registry[top[0][0]]
    sv = np.array(entry["summary_embedding"], dtype=np.float32)
    sv_norm = np.linalg.norm(sv)
    q_norm = np.linalg.norm(q_emb)
    expected_score = float(np.dot(q_emb, sv) / (q_norm * sv_norm))
    assert_close(top[0][1], expected_score, tol=1e-4, label="score equals cosine(query, summary_embedding)")

    restore_registry()


def test_representative_chunks(embedding_model, chroma_client):
    print("\n=== test_representative_chunks ===")
    backup_registry()

    texts = [
        "optimization gradient descent convergence",
        "stochastic optimizer Adam learning rate",
        "convex function minimum saddle point",
        "deep learning neural network layer",       # outlier
        "random walk Brownian motion diffusion",    # outlier
    ]

    col = chroma_client.get_or_create_collection(TEST_COLLECTION + "_repr", metadata={"hnsw:space": "cosine"})
    chunk_ids = []
    for t in texts:
        emb = embedding_model.encode([t], normalize_embeddings=True, convert_to_numpy=True)[0]
        cid = f"repr_{abs(hash(t)) % 10**8}"
        col.add(ids=[cid], embeddings=[emb.tolist()], documents=[t], metadatas=[{"chapter": "test"}])
        chunk_ids.append(cid)

    # Build centroid from first 3 (optimization-related)
    embs = [embedding_model.encode([t], normalize_embeddings=True, convert_to_numpy=True)[0] for t in texts[:3]]
    centroid = np.mean(embs, axis=0)
    centroid /= np.linalg.norm(centroid)

    selected = _select_representative_chunks(
        chunk_ids, centroid, chroma_client, TEST_COLLECTION + "_repr",
        top_n=3, top_diverse=1
    )
    assert_true(len(selected) >= 1, f"at least 1 chunk selected ({len(selected)} found)")
    assert_true(len(selected) <= len(texts), "not more chunks than exist")
    print(f"  Selected {len(selected)}/{len(texts)} chunks")
    for t in selected:
        print(f"    - {t[:60]}")

    restore_registry()


def test_merge(embedding_model, chroma_client):
    print("\n=== test_merge ===")
    backup_registry()

    # Two nearly identical SLMs
    base_text = "optimization gradient descent convergence"
    texts = [
        base_text + " Adam",
        base_text + " SGD",
        base_text + " learning rate",
    ]

    col = chroma_client.get_or_create_collection(TEST_COLLECTION + "_merge", metadata={"hnsw:space": "cosine"})
    chunks = []
    for t in texts:
        emb = embedding_model.encode([t], normalize_embeddings=True, convert_to_numpy=True)[0]
        cid = f"merge_{abs(hash(t)) % 10**8}"
        col.add(ids=[cid], embeddings=[emb.tolist()], documents=[t], metadatas=[{"chapter": "test"}])
        chunks.append({"id": cid, "text": t, "embedding": emb.tolist()})

    # Force very low threshold so everything goes into separate SLMs first
    assign_chunks(chunks, embedding_model, TEST_COLLECTION + "_merge", chroma_client, threshold=0.9999)
    registry_before = load_registry()
    n_before = len(registry_before)

    # Then merge with low threshold (should merge the similar ones)
    merges = merge_close_slms(threshold=0.70, embedding_model=embedding_model, chroma_client=chroma_client)
    registry_after = load_registry()
    n_after = len(registry_after)

    print(f"  SLM prima: {n_before}, dopo merge: {n_after}, merge effettuati: {len(merges)}")
    assert_true(n_after <= n_before, "merge reduces or keeps SLM count")
    for m in merges:
        print(f"    merged '{m['removed']}' → '{m['kept']}' (similarity={m['similarity']})")

    restore_registry()


def test_registry_structure(embedding_model, chroma_client):
    print("\n=== test_registry_structure ===")
    backup_registry()

    text = "gradient descent optimization convergence rate"
    emb = embedding_model.encode([text], normalize_embeddings=True, convert_to_numpy=True)[0]
    col = chroma_client.get_or_create_collection(TEST_COLLECTION + "_struct", metadata={"hnsw:space": "cosine"})
    cid = "struct_test_001"
    col.add(ids=[cid], embeddings=[emb.tolist()], documents=[text], metadatas=[{"chapter": "test"}])

    registry = load_registry()
    slm_name = create_slm(registry, cid, emb, TEST_COLLECTION + "_struct")
    save_registry(registry)

    registry = load_registry()
    entry = registry[slm_name]

    required_fields = ["collection", "chunks_json", "chunk_count", "centroid_embedding", "topic_summary", "keywords", "summary_embedding"]
    for field in required_fields:
        assert_true(field in entry, f"field '{field}' present in registry entry")

    assert_true(entry["chunk_count"] == 1, "chunk_count initialized to 1")
    assert_true(len(entry["centroid_embedding"]) > 0, "centroid_embedding non-empty")
    assert_true(isinstance(entry["keywords"], list), "keywords is a list")
    assert_true(isinstance(entry["topic_summary"], str), "topic_summary is a string")

    restore_registry()


# ── Main ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Carico embedding model...")
    embedding_model = SentenceTransformer(EMBED_MODEL)

    print("Inizializzo ChromaDB in-memory...")
    chroma_client = chromadb.Client()  # in-memory, non tocca chroma_db su disco

    test_incremental_centroid()
    test_registry_structure(embedding_model, chroma_client)
    test_representative_chunks(embedding_model, chroma_client)
    test_routing_score(embedding_model, chroma_client)
    test_merge(embedding_model, chroma_client)

    print("\nDone.")
