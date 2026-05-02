"""
SLMAgent.py — SLM data structure and retrieval logic.
"""

import json
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import chromadb


@dataclass
class SLMAgent:
    name: str
    model_name: str
    chunks_json_path: str
    collection_name: str

    # NEW: centroid and summary fields matching registry structure
    centroid_embedding: Optional[List[float]] = field(default=None)
    topic_summary: str = field(default="")
    keywords: List[str] = field(default_factory=list)
    summary_embedding: Optional[List[float]] = field(default=None)

    # Runtime model state (not serialized)
    tokenizer: Optional[AutoTokenizer] = field(default=None, repr=False)
    model: Optional[AutoModelForCausalLM] = field(default=None, repr=False)
    _chunk_ids: List[str] = field(default_factory=list, repr=False)
    _last_modified: float = field(default=0.0, repr=False)


def load_slm_agent(agent: SLMAgent, device: str = "cpu") -> SLMAgent:
    agent.tokenizer = AutoTokenizer.from_pretrained(agent.model_name, trust_remote_code=True)
    agent.model = AutoModelForCausalLM.from_pretrained(
        agent.model_name,
        torch_dtype=torch.float32 if device == "cpu" else torch.float16,
        trust_remote_code=True,
    ).to(device)
    agent.model.eval()
    _sync_chunk_ids(agent)
    return agent


def _sync_chunk_ids(agent: SLMAgent) -> None:
    """Reload chunk IDs from disk if the file has changed since last read."""
    path = Path(agent.chunks_json_path)
    mtime = path.stat().st_mtime
    if mtime != agent._last_modified:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        agent._chunk_ids = [entry["id"] for entry in data]
        agent._last_modified = mtime


def get_agent_chunk_ids(agent: SLMAgent) -> List[str]:
    _sync_chunk_ids(agent)
    return list(agent._chunk_ids)


def retrieve_top_k(
    query: str,
    chunk_ids: List[str],
    collection: chromadb.Collection,
    embedding_model: SentenceTransformer,
    top_k: int = 5,
) -> List[Tuple[str, float]]:
    query_emb = embedding_model.encode(
        [query], normalize_embeddings=True, convert_to_numpy=True
    )[0].tolist()
    response = collection.query(
        query_embeddings=[query_emb],
        n_results=min(top_k, len(chunk_ids)),
        where={"id": {"$in": chunk_ids}},
        include=["documents", "distances"],
    )
    docs = response["documents"][0]
    distances = response["distances"][0]
    return [(doc, 1.0 - dist ** 2 / 2) for doc, dist in zip(docs, distances)]


_SYSTEM_PROMPT = (
    "You are a precise assistant. Answer the question using ONLY the information "
    "provided in the context below. Do not use any external knowledge or information "
    "from your training. If the answer is not present in the context, respond with "
    "'The answer is not available in the provided context.'"
)


def build_messages(query: str, context_chunks: List[str]) -> List[Dict]:
    """Return the prompt as a messages list suitable for apply_chat_template."""
    context = "\n\n".join(
        f"[Chunk {i+1}]:\n{chunk}" for i, chunk in enumerate(context_chunks)
    )
    return [
        {"role": "system", "content": _SYSTEM_PROMPT},
        {"role": "user", "content": f"CONTEXT:\n{context}\n\nQUESTION: {query}\n\nANSWER:"},
    ]


def build_prompt(query: str, context_chunks: List[str]) -> str:
    """Legacy plain-string prompt — kept for callers that do not use chat templates."""
    context = "\n\n".join(
        f"[Chunk {i+1}]:\n{chunk}" for i, chunk in enumerate(context_chunks)
    )
    return (
        f"{_SYSTEM_PROMPT}\n\n"
        f"CONTEXT:\n{context}\n\n"
        f"QUESTION: {query}\n\n"
        "ANSWER:"
    )


def _apply_chat_template_no_think(tokenizer: AutoTokenizer, messages: List[Dict]) -> str:
    """Apply chat template with thinking disabled (Qwen3). Falls back gracefully for other models."""
    try:
        return tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True, enable_thinking=False
        )
    except TypeError:
        # Model tokenizer does not support enable_thinking (e.g. Qwen2.5)
        return tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )


def generate_answer(
    messages: List[Dict],
    tokenizer: AutoTokenizer,
    model: AutoModelForCausalLM,
    max_new_tokens: int = 512,
    temperature: float = 0.1,
    device: str = "cpu",
) -> str:
    # Use chat template with thinking disabled so <think> tokens are never generated.
    text = _apply_chat_template_no_think(tokenizer, messages)
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=2048).to(device)
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            do_sample=temperature > 0,
            pad_token_id=tokenizer.eos_token_id,
        )
    generated = outputs[0][inputs["input_ids"].shape[1]:]
    return tokenizer.decode(generated, skip_special_tokens=True).strip()


def rag(
    query: str,
    agent: SLMAgent,
    chroma_client: chromadb.Client,
    embedding_model: SentenceTransformer,
    top_k: int = 5,
    max_new_tokens: int = 512,
    temperature: float = 0.1,
    device: str = "cpu",
) -> Dict:
    if agent.model is None or agent.tokenizer is None:
        raise RuntimeError(f"Agent '{agent.name}' is not loaded. Call load_slm_agent() first.")

    chunk_ids = get_agent_chunk_ids(agent)
    collection = chroma_client.get_collection(agent.collection_name)

    retrieved = retrieve_top_k(query, chunk_ids, collection, embedding_model, top_k)
    context_chunks = [doc for doc, _ in retrieved]
    scores = [score for _, score in retrieved]

    messages = build_messages(query, context_chunks)
    answer = generate_answer(messages, agent.tokenizer, agent.model, max_new_tokens, temperature, device)

    return {
        "agent":            agent.name,
        "query":            query,
        "answer":           answer,
        "retrieved_chunks": context_chunks,
        "retrieval_scores": scores,
    }
