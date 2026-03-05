import json
import uuid
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional
from sentence_transformers import SentenceTransformer


REGISTRY_PATH = "registry.json"
SLM_DATA_DIR = Path("slm_data")


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


def get_centroid(registry: Dict, slm_name: str) -> Optional[np.ndarray]:
    entry = registry.get(slm_name)
    if not entry or not entry["centroid"]:
        return None
    return np.array(entry["centroid"])


def update_centroid(registry: Dict, slm_name: str, new_embedding: np.ndarray) -> None:
    entry = registry[slm_name]
    n = entry["chunk_count"]
    old_centroid = np.array(entry["centroid"])
    new_centroid = (old_centroid * n + new_embedding) / (n + 1)
    entry["centroid"] = new_centroid.tolist()
    entry["chunk_count"] += 1


def create_slm(registry: Dict, chunk_id: str, embedding: np.ndarray) -> str:
    slm_name = f"slm_{uuid.uuid4().hex[:8]}"
    _ensure_dirs()
    registry[slm_name] = {
        "collection": slm_name,
        "chunks_json": str(SLM_DATA_DIR / f"{slm_name}_chunks.json"),
        "centroid": embedding.tolist(),
        "chunk_count": 1,
    }
    chunks_path = SLM_DATA_DIR / f"{slm_name}_chunks.json"
    with open(chunks_path, "w") as f:
        json.dump([{"id": chunk_id}], f, indent=2)
    return slm_name


def assign_chunk(chunk_id: str, embedding: np.ndarray, threshold: float = 0.75) -> str:
    registry = load_registry()

    best_slm = None
    best_score = -1.0

    for slm_name in registry:
        centroid = get_centroid(registry, slm_name)
        if centroid is None:
            continue
        score = float(np.dot(embedding, centroid) / (np.linalg.norm(embedding) * np.linalg.norm(centroid)))
        if score > best_score:
            best_score = score
            best_slm = slm_name

    if best_slm is None or best_score < threshold:
        slm_name = create_slm(registry, chunk_id, embedding)
        save_registry(registry)
        return slm_name

    update_centroid(registry, best_slm, embedding)

    chunks_path = Path(registry[best_slm]["chunks_json"])
    with open(chunks_path, "r") as f:
        chunks = json.load(f)
    chunks.append({"id": chunk_id})
    with open(chunks_path, "w") as f:
        json.dump(chunks, f, indent=2)

    save_registry(registry)
    return best_slm


def assign_chunks(chunks: List[Dict], embedding_model: SentenceTransformer, threshold: float = 0.75) -> Dict[str, List[str]]:
    assignments = {}
    for chunk in chunks:
        embedding = np.array(chunk["embedding"])
        slm_name = assign_chunk(chunk["id"], embedding, threshold)
        assignments.setdefault(slm_name, []).append(chunk["id"])
    return assignments


def merge_close_slms(threshold: float = 0.90) -> List[Dict]:
    """
    Trova coppie di SLM i cui centroidi hanno cosine similarity >= threshold
    e le fonde iterativamente. Mantiene l'SLM con più chunk, aggiorna
    registry.json e i file slm_data/*_chunks.json.

    Returns:
        Lista di dict {"kept", "removed", "similarity"} per ogni merge eseguito.
    """
    merges = []

    while True:
        registry = load_registry()
        slm_names = list(registry.keys())

        if len(slm_names) < 2:
            break

        best_pair = None
        best_score = -1.0

        for i in range(len(slm_names)):
            for j in range(i + 1, len(slm_names)):
                a, b = slm_names[i], slm_names[j]
                ca = get_centroid(registry, a)
                cb = get_centroid(registry, b)
                if ca is None or cb is None:
                    continue
                norm_a = np.linalg.norm(ca)
                norm_b = np.linalg.norm(cb)
                if norm_a == 0 or norm_b == 0:
                    continue
                score = float(np.dot(ca, cb) / (norm_a * norm_b))
                if score > best_score:
                    best_score = score
                    best_pair = (a, b)

        if best_pair is None or best_score < threshold:
            break

        a, b = best_pair
        count_a = registry[a]["chunk_count"]
        count_b = registry[b]["chunk_count"]
        kept, removed = (a, b) if count_a >= count_b else (b, a)

        c_kept = np.array(registry[kept]["centroid"])
        c_removed = np.array(registry[removed]["centroid"])
        n_kept = registry[kept]["chunk_count"]
        n_removed = registry[removed]["chunk_count"]
        merged_centroid = (c_kept * n_kept + c_removed * n_removed) / (n_kept + n_removed)

        kept_path = Path(registry[kept]["chunks_json"])
        removed_path = Path(registry[removed]["chunks_json"])

        kept_chunks = []
        if kept_path.exists():
            with open(kept_path, "r") as f:
                kept_chunks = json.load(f)

        if removed_path.exists():
            with open(removed_path, "r") as f:
                kept_chunks += json.load(f)
            removed_path.unlink()

        with open(kept_path, "w") as f:
            json.dump(kept_chunks, f, indent=2)

        registry[kept]["centroid"] = merged_centroid.tolist()
        registry[kept]["chunk_count"] = n_kept + n_removed
        del registry[removed]
        save_registry(registry)

        merges.append({"kept": kept, "removed": removed, "similarity": round(best_score, 6)})

    return merges