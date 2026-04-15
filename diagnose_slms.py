"""
diagnose_slms.py
----------------
Mostra la distribuzione delle cosine similarity tra centroidi SLM
e stima quanti SLM resterebbero a ogni soglia di merge.
Non modifica nulla.

Usage:
    python diagnose_slms.py
"""

import json
import numpy as np
from pathlib import Path
from itertools import combinations

REGISTRY_PATH = Path("registry.json")

with open(REGISTRY_PATH) as f:
    registry = json.load(f)

slm_names = [k for k in registry if registry[k].get("centroid_embedding")]
centroids = {k: np.array(v["centroid_embedding"]) for k, v in registry.items() if v.get("centroid_embedding")}

print(f"SLM totali: {len(slm_names)}")
print(f"Chunk totali: {sum(v['chunk_count'] for v in registry.values())}\n")

# Calcola tutte le pairwise cosine similarities
scores = []
for a, b in combinations(slm_names, 2):
    ca, cb = centroids[a], centroids[b]
    na, nb = np.linalg.norm(ca), np.linalg.norm(cb)
    if na == 0 or nb == 0:
        continue
    scores.append(float(np.dot(ca, cb) / (na * nb)))

scores = np.array(scores)
print(f"Coppie analizzate: {len(scores)}")
print(f"Similarity max:    {scores.max():.4f}")
print(f"Similarity media:  {scores.mean():.4f}")
print(f"Similarity mediana:{np.median(scores):.4f}")
print(f"Similarity min:    {scores.min():.4f}\n")

# Stima SLM rimanenti per soglia (greedy approssimato: conta coppie sopra soglia)
print("Soglia  | Coppie sopra soglia | SLM stimati rimasti")
print("--------|---------------------|--------------------")
for t in [0.95, 0.90, 0.85, 0.80, 0.75, 0.70, 0.65, 0.60]:
    above = int((scores >= t).sum())
    # stima approssimata: ogni merge elimina 1 SLM
    # lower bound: non possiamo avere meno di 1
    estimated = max(1, len(slm_names) - above)
    print(f"  {t:.2f}  |        {above:>6}       |      {estimated:>5}")
