"""
test_retrieval.py
-----------------
Testa il retrieval (senza caricare nessun LLM).
Dato una query, trova i top-k chunk più rilevanti nel ChromaDB.

Usage:
    python test_retrieval.py "la tua domanda qui"
    python test_retrieval.py "la tua domanda" --top_k 10
"""

import json
import argparse
from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer

REGISTRY_PATH = Path("registry.json")
CHROMA_PATH = "./chroma_db"
EMBED_MODEL = "sentence-transformers/all-mpnet-base-v2"

parser = argparse.ArgumentParser()
parser.add_argument("query", nargs="?", default=None)
parser.add_argument("--top_k", type=int, default=5)
args = parser.parse_args()

query = args.query or input("Query: ").strip()

print(f"\nCarico embedding model: {EMBED_MODEL} ...")
model = SentenceTransformer(EMBED_MODEL)

print("Connessione a ChromaDB ...")
client = chromadb.PersistentClient(path=CHROMA_PATH)
collections = {c.name: client.get_collection(c.name) for c in client.list_collections()}
print(f"  {len(collections)} collection(s): {list(collections.keys())}")

# Carica registry per mappare chunk → SLM
registry = {}
if REGISTRY_PATH.exists():
    with open(REGISTRY_PATH) as f:
        registry = json.load(f)

chunk_to_slm = {}
for slm_name, entry in registry.items():
    chunks_path = Path(entry.get("chunks_json", ""))
    if chunks_path.exists():
        with open(chunks_path) as f:
            for c in json.load(f):
                chunk_to_slm[c["id"]] = slm_name

# Encoding query
query_emb = model.encode([query], normalize_embeddings=True, convert_to_numpy=True)[0].tolist()

# Retrieval su tutte le collections
print(f"\nQuery: \"{query}\"")
print(f"Top {args.top_k} risultati:\n")
print("=" * 80)

all_results = []
for col_name, col in collections.items():
    if col.count() == 0:
        continue
    res = col.query(
        query_embeddings=[query_emb],
        n_results=min(args.top_k, col.count()),
        include=["documents", "distances", "metadatas"]
    )
    for doc, dist, meta, cid in zip(
        res["documents"][0],
        res["distances"][0],
        res["metadatas"][0],
        res["ids"][0]
    ):
        all_results.append({
            "score": round(1.0 - dist ** 2 / 2, 4),  # L2 dist → cosine sim (normalized vecs)
            "collection": col_name,
            "slm": chunk_to_slm.get(cid, "?"),
            "chapter": meta.get("chapter", "—"),
            "id": cid,
            "text": doc,
        })

# Ordina per score globale, prendi top_k
all_results.sort(key=lambda x: x["score"], reverse=True)
top = all_results[:args.top_k]

for i, r in enumerate(top, 1):
    print(f"[{i}] Score: {r['score']}  |  SLM: {r['slm']}  |  Capitolo: {r['chapter']}")
    print(f"     Collection: {r['collection']}  |  ID: {r['id'][:12]}...")
    print()
    print(r["text"][:400] + ("..." if len(r["text"]) > 400 else ""))
    print("-" * 80)
