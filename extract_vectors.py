"""
extract_vectors.py
──────────────────
Reads ChromaDB collections + SLM registry (centroids & chunk assignments),
applies dimensionality reduction (PCA / t-SNE / UMAP), computes action radii
for each SLM centroid, and exports a JSON for the Three.js visualizer.

Usage:
    python extract_vectors.py --method pca
    python extract_vectors.py --method tsne
    python extract_vectors.py --method umap
    python extract_vectors.py --method all

Options:
    --db_path       ChromaDB path                  (default: ./chroma_db)
    --registry      Registry JSON path             (default: ./registry.json)
    --output        Output JSON path               (default: ./vectors.json)
    --threshold     Cosine similarity threshold    (default: 0.75)
    --perplexity    t-SNE perplexity               (default: 30)
    --n_neighbors   UMAP n_neighbors               (default: 15)
    --min_dist      UMAP min_dist                  (default: 0.1)
"""

import argparse
import json
import sys
from pathlib import Path
import numpy as np
import chromadb

# ── CLI ────────────────────────────────────────────────────────────────
parser = argparse.ArgumentParser(description="Extract & reduce vectors with SLM centroids")
parser.add_argument("--db_path",      default="./chroma_db",    help="ChromaDB path")
parser.add_argument("--registry",     default="./registry.json", help="SLM registry JSON")
parser.add_argument("--output",       default="./vectors.json",  help="Output JSON")
parser.add_argument("--method",       default="pca",
                    choices=["pca", "tsne", "umap", "all"])
parser.add_argument("--threshold",    type=float, default=0.75,  help="Cosine similarity threshold")
parser.add_argument("--perplexity",   type=float, default=30)
parser.add_argument("--n_neighbors",  type=int,   default=15)
parser.add_argument("--min_dist",     type=float, default=0.1)
args = parser.parse_args()

# ── LOAD REGISTRY ──────────────────────────────────────────────────────
print(f"[1/5] Loading SLM registry from: {args.registry}")
registry_path = Path(args.registry)
if not registry_path.exists():
    print(f"ERROR: Registry not found at {args.registry}")
    sys.exit(1)

with open(registry_path, "r") as f:
    registry = json.load(f)

slm_names = list(registry.keys())
print(f"       Found {len(slm_names)} SLM(s)")

# Load chunk-to-SLM mapping from slm_data JSONs
chunk_to_slm = {}
slm_chunk_ids = {}
for slm_name, entry in registry.items():
    chunks_path = Path(entry.get("chunks_json", ""))
    slm_chunk_ids[slm_name] = []
    if chunks_path.exists():
        with open(chunks_path, "r") as f:
            chunk_list = json.load(f)
        for c in chunk_list:
            cid = c["id"]
            chunk_to_slm[cid] = slm_name
            slm_chunk_ids[slm_name].append(cid)
    else:
        print(f"  WARN: {chunks_path} not found for {slm_name}")

# ── LOAD CHROMADB ──────────────────────────────────────────────────────
print(f"[2/5] Loading ChromaDB from: {args.db_path}")
client = chromadb.PersistentClient(path=args.db_path)
collections = client.list_collections()

if not collections:
    print("ERROR: No collections found.")
    sys.exit(1)

print(f"       Found {len(collections)} collection(s): {[c.name for c in collections]}")

# ── EXTRACT EMBEDDINGS ─────────────────────────────────────────────────
print("[3/5] Extracting embeddings...")

all_embeddings = []
all_meta = []

for col_ref in collections:
    col = client.get_collection(col_ref.name)
    data = col.get(include=["embeddings", "metadatas", "documents"])

    embeddings = data.get("embeddings", [])
    metadatas  = data.get("metadatas", [])
    documents  = data.get("documents", [])
    ids        = data.get("ids", [])

    if embeddings is None or (hasattr(embeddings, '__len__') and len(embeddings) == 0):
        print(f"  WARN: Collection '{col_ref.name}' empty, skipping.")
        continue

    for i, emb in enumerate(embeddings):
        chunk_id = ids[i] if i < len(ids) else f"chunk_{i}"
        meta = metadatas[i] if i < len(metadatas) and metadatas[i] else {}
        doc  = documents[i] if i < len(documents) and documents[i] else ""

        owning_slm = chunk_to_slm.get(chunk_id, "unassigned")

        all_embeddings.append(emb)
        all_meta.append({
            "collection": col_ref.name,
            "slm":        owning_slm,
            "id":         chunk_id,
            "chapter":    meta.get("chapter", meta.get("source", "—")),
            "preview":    doc[:140] + "…" if len(doc) > 140 else doc,
        })

n_chunks = len(all_embeddings)
n_dim    = len(all_embeddings[0]) if all_embeddings else 0
print(f"       {n_chunks} chunks · {n_dim}D · {len(slm_names)} SLM centroids")

if n_chunks == 0:
    print("ERROR: No embeddings found.")
    sys.exit(1)

# ── BUILD CENTROID VECTORS ─────────────────────────────────────────────
print("[4/5] Preparing centroids from registry...")

centroid_vecs = []
centroid_info = []
for slm_name in slm_names:
    entry = registry[slm_name]
    centroid_emb = entry.get("centroid_embedding", [])
    if not centroid_emb:
        print(f"  WARN: No centroid_embedding for {slm_name}, skipping.")
        continue
    centroid_vecs.append(centroid_emb)
    centroid_info.append({
        "slm_name":      slm_name,
        "chunk_count":   entry.get("chunk_count", len(slm_chunk_ids.get(slm_name, []))),
        "collection":    entry.get("collection", ""),
        "topic_summary": entry.get("topic_summary", ""),
        "keywords":      entry.get("keywords", []),
    })

n_centroids = len(centroid_vecs)

# ── DIMENSIONALITY REDUCTION ──────────────────────────────────────────
print(f"[5/5] Reducing {n_dim}D → 3D ...")

X_all = np.array(all_embeddings + centroid_vecs, dtype=np.float32)

methods_to_run = ["pca", "tsne", "umap"] if args.method == "all" else [args.method]
reductions = {}

for method in methods_to_run:
    print(f"       → {method.upper()} ...", end=" ", flush=True)

    if method == "pca":
        from sklearn.decomposition import PCA
        reducer = PCA(n_components=3, random_state=42)
        X_3d = reducer.fit_transform(X_all)
        variance = reducer.explained_variance_ratio_
        print(f"(variance: {sum(variance)*100:.1f}%)")

    elif method == "tsne":
        from sklearn.manifold import TSNE
        perp = min(args.perplexity, max(5, len(X_all) - 1))
        reducer = TSNE(n_components=3, perplexity=perp, random_state=42,
                       max_iter=1000, init="pca")
        X_3d = reducer.fit_transform(X_all)
        print("done")

    elif method == "umap":
        try:
            import umap
        except ImportError:
            print("SKIP (pip install umap-learn)")
            continue
        reducer = umap.UMAP(n_components=3, n_neighbors=args.n_neighbors,
                            min_dist=args.min_dist, random_state=42)
        X_3d = reducer.fit_transform(X_all)
        print("done")

    # Normalize to [-1, 1]
    mins = X_3d.min(axis=0)
    maxs = X_3d.max(axis=0)
    ranges = maxs - mins
    ranges[ranges == 0] = 1
    X_norm = 2 * (X_3d - mins) / ranges - 1

    chunk_coords    = X_norm[:n_chunks]
    centroid_coords = X_norm[n_chunks:]

    # ── COMPUTE RADII ──
    centroid_radii = []
    for ci, cinfo in enumerate(centroid_info):
        slm_name = cinfo["slm_name"]
        c_pos = centroid_coords[ci]

        assigned_indices = [
            j for j, m in enumerate(all_meta) if m["slm"] == slm_name
        ]

        if assigned_indices:
            distances = [
                np.linalg.norm(chunk_coords[j] - c_pos)
                for j in assigned_indices
            ]
            max_r  = float(np.max(distances))
            mean_r = float(np.mean(distances))
            std_r  = float(np.std(distances))
        else:
            max_r = mean_r = std_r = 0.0

        centroid_radii.append({
            "max_radius":  round(max_r, 6),
            "mean_radius": round(mean_r, 6),
            "std_radius":  round(std_r, 6),
        })

    reductions[method] = {
        "chunks":    chunk_coords.tolist(),
        "centroids": centroid_coords.tolist(),
        "radii":     centroid_radii,
    }

# ── EXPORT ─────────────────────────────────────────────────────────────
output = {
    "meta": {
        "n_chunks":       n_chunks,
        "n_slms":         n_centroids,
        "original_dim":   n_dim,
        "methods":        list(reductions.keys()),
        "threshold":      args.threshold,
    },
    "chunk_meta":     all_meta,
    "centroid_info":  centroid_info,
    "reductions":     reductions,
}

with open(args.output, "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False)

size_mb = len(json.dumps(output)) / (1024 * 1024)
print(f"\n  ✓ Exported → {args.output} ({size_mb:.2f} MB)")
print(f"    {n_chunks} chunks · {n_centroids} SLM centroids · {len(reductions)} method(s)")
print(f"    Open visualizer.html and load the JSON to explore.\n")