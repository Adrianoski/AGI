"""
SLMAgent.py — Prompt construction for the RAG generator.
"""

from typing import Dict, List

from transformers import AutoTokenizer


_SYSTEM_PROMPT = (
    "You are a precise assistant. Answer the question using ONLY the information "
    "provided in the context below. Do not use any external knowledge or information "
    "from your training. If the answer is not present in the context, respond with "
    "'The answer is not available in the provided context.' "
    "CRITICAL: You MUST write your answer in English only. The context may be in "
    "Italian, but your final answer must always be written in English."
)


def build_messages(query: str, context_chunks: List[str]) -> List[Dict]:
    """Return the prompt as a messages list suitable for apply_chat_template."""
    context = "\n\n".join(
        f"[Chunk {i+1}]:\n{chunk}" for i, chunk in enumerate(context_chunks)
    )
    return [
        {"role": "system", "content": _SYSTEM_PROMPT},
        {"role": "user", "content": f"CONTEXT:\n{context}\n\nQUESTION: {query}\n\nANSWER (in English):"},
    ]


def _apply_chat_template_no_think(tokenizer: AutoTokenizer, messages: List[Dict]) -> str:
    """Apply chat template with thinking disabled (Qwen3). Falls back gracefully for other models."""
    try:
        return tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True, enable_thinking=False
        )
    except TypeError:
        return tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
