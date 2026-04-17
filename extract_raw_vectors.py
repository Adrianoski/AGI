"""
extract_raw_vectors.py
──────────────────────
Estrae tutti i chunk da ChromaDB e li proietta in 3D senza struttura SLM.
I chunk sono colorati per capitolo anziché per SLM.
Utile per esplorare la distribuzione naturale degli embedding prima di decidere
come clusterizzare.

Usage:
    python extract_raw_vectors.py
    python extract_raw_vectors.py --method tsne --output vectors_raw.json
    python extract_raw_vectors.py --collection LibroStoria
"""

import argparse
import json
import sys
from pathlib import Path
import numpy as np
import chromadb

parser = argparse.ArgumentParser()
parser.add_argument("--db_path",    default="./chroma_db")
parser.add_argument("--output",     default="./vectors.json")
parser.add_argument("--method",     default="pca", choices=["pca", "tsne", "umap", "all"])
parser.add_argument("--collection", default=None, help="Nome collection specifica (default: tutte)")
parser.add_argument("--perplexity", type=float, default=30)
args = parser.parse_args()

# ── LOAD CHROMADB ──────────────────────────────────────────────────────
print(f"[1/3] Carico ChromaDB da: {args.db_path}")
client = chromadb.PersistentClient(path=args.db_path)
collections = client.list_collections()

if not collections:
    print("ERROR: Nessuna collection trovata.")
    sys.exit(1)

if args.collection:
    collections = [c for c in collections if c.name == args.collection]
    if not collections:
        print(f"ERROR: Collection '{args.collection}' non trovata.")
        sys.exit(1)

print(f"       Collection: {[c.name for c in collections]}")

# ── EXTRACT ────────────────────────────────────────────────────────────
print("[2/3] Estraggo embedding...")
all_embeddings = []
all_meta = []

# Build a consistent color map: chapter → index
chapter_index = {}

for col_ref in collections:
    col = client.get_collection(col_ref.name)
    data = col.get(include=["embeddings", "metadatas", "documents"])

    embeddings = data.get("embeddings")
    metadatas  = data.get("metadatas") or []
    documents  = data.get("documents") or []
    ids        = data.get("ids") or []

    if embeddings is None or len(embeddings) == 0:
        print(f"  WARN: Collection '{col_ref.name}' vuota, skip.")
        continue

    for i, emb in enumerate(embeddings):
        meta    = metadatas[i] if i < len(metadatas) and metadatas[i] else {}
        doc     = documents[i] if i < len(documents) and documents[i] else ""
        chapter = meta.get("chapter", meta.get("source", "—"))

        if chapter not in chapter_index:
            chapter_index[chapter] = len(chapter_index)

        all_embeddings.append(emb)
        all_meta.append({
            "collection": col_ref.name,
            "slm":        chapter,          # riuso il campo 'slm' per il colore
            "id":         ids[i] if i < len(ids) else f"chunk_{i}",
            "chapter":    chapter,
            "preview":    (doc[:140] + "…") if len(doc) > 140 else doc,
        })

n_chunks = len(all_embeddings)
n_dim    = len(all_embeddings[0]) if all_embeddings else 0
n_chapters = len(chapter_index)
print(f"       {n_chunks} chunk · {n_dim}D · {n_chapters} capitoli")

if n_chunks == 0:
    print("ERROR: Nessun embedding trovato.")
    sys.exit(1)

# ── REDUCE ─────────────────────────────────────────────────────────────
print(f"[3/3] Riduzione {n_dim}D → 3D ...")
X = np.array(all_embeddings, dtype=np.float32)

methods_to_run = ["pca", "tsne", "umap"] if args.method == "all" else [args.method]
reductions = {}

for method in methods_to_run:
    print(f"  → {method.upper()} ...", end=" ", flush=True)

    if method == "pca":
        from sklearn.decomposition import PCA
        reducer = PCA(n_components=3, random_state=42)
        X_3d = reducer.fit_transform(X)
        var = sum(reducer.explained_variance_ratio_) * 100
        print(f"varianza spiegata: {var:.1f}%")

    elif method == "tsne":
        from sklearn.manifold import TSNE
        perp = min(args.perplexity, max(5, n_chunks - 1))
        reducer = TSNE(n_components=3, perplexity=perp, random_state=42,
                       max_iter=1000, init="pca")
        X_3d = reducer.fit_transform(X)
        print("done")

    elif method == "umap":
        try:
            import umap
        except ImportError:
            print("SKIP (pip install umap-learn)")
            continue
        reducer = umap.UMAP(n_components=3, n_neighbors=15, min_dist=0.1, random_state=42)
        X_3d = reducer.fit_transform(X)
        print("done")

    # Normalize to [-1, 1]
    mins = X_3d.min(axis=0)
    maxs = X_3d.max(axis=0)
    rng  = maxs - mins
    rng[rng == 0] = 1
    X_norm = 2 * (X_3d - mins) / rng - 1

    reductions[method] = {
        "chunks":    X_norm.tolist(),
        "centroids": [],   # nessun centroide in vista raw
        "radii":     [],
    }

# centroid_info vuoto — il visualizzatore lo gestisce già (legend vuota)
output = {
    "meta": {
        "n_chunks":     n_chunks,
        "n_slms":       0,
        "original_dim": n_dim,
        "methods":      list(reductions.keys()),
        "threshold":    0.0,
        "mode":         "raw_chapters",
    },
    "chunk_meta":    all_meta,
    "centroid_info": [],
    "reductions":    reductions,
}

with open(args.output, "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False)

size_mb = len(json.dumps(output)) / (1024 * 1024)
print(f"\n  Esportato → {args.output} ({size_mb:.2f} MB)")
print(f"  {n_chunks} chunk · {n_chapters} capitoli · colore = capitolo")
print(f"  Apri visualizer.html e carica il JSON.\n")
