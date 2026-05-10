"""
orchestrator.py — CLARA orchestrator implementing the query processing workflow.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
from sentence_transformers import SentenceTransformer

from agent import ClusterAgent, EvidenceSet
from router import find_top_n_slms, load_registry


@dataclass
class DSLInvocation:
    """One step of the per-query DSL trace."""
    agent: str
    role: str                   # "primary" | "secondary" | "orchestrator"
    operation: str              # "local_retrieve" | "select_evidence" | "provide_evidence" | "generate" | "route" | "aggregate"
    input_summary: str          # short, human-readable
    output_size: int            # |result| where applicable
    elapsed_ms: float


@dataclass
class QueryResult:

    query: str
    answer: str
    primary: str
    secondaries: List[str]
    routing: List[Tuple[str, float]]   # (slm_name, score) for top-K
    primary_evidence: EvidenceSet
    secondary_evidence: Dict[str, EvidenceSet]
    gamma: EvidenceSet                 # primary ∪ all secondaries
    pool_size: int                     # |M*| + Σ|M_i^-| chunks examined
    retrieval_ms: float
    generation_ms: float
    trace: List[DSLInvocation] = field(default_factory=list)


# ── Orchestrator ───────────────────────────────────────────────────────

class Orchestrator:

    def __init__(
        self,
        registry: Optional[Dict] = None,
        chroma_client: Any = None,
        embedding_model: SentenceTransformer = None,
    ) -> None:
        if chroma_client is None or embedding_model is None:
            raise ValueError(
                "Orchestrator requires both chroma_client and embedding_model."
            )
        self.registry: Dict = registry if registry is not None else load_registry()
        self.chroma_client = chroma_client
        self.embedding_model = embedding_model

        # Build cluster-agent registry A = {A_1, ..., A_m}.
        self.agents: Dict[str, ClusterAgent] = {
            name: ClusterAgent.from_registry_entry(
                slm_name=name,
                entry=entry,
                embedding_model=embedding_model,
                chroma_client=chroma_client,
            )
            for name, entry in self.registry.items()
        }

        # Bounded runtime pool of SLMs (mirrors the caching pattern in
        # benchmark.py / app.py: load once on first use, reuse afterwards).
        # Pool capacity B is implicit: we keep at most one model per name.
        self._slm_pool: Dict[str, Tuple[Any, Any]] = {}

    # ── SLM runtime pool ──────────────────────────────────────────────

    def _bind_slm(self, model_name: str) -> Tuple[Any, Any]:
        """Lazy-load (tokenizer, model) and cache it in the runtime pool."""
        if model_name in self._slm_pool:
            return self._slm_pool[model_name]

        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer

        device = "cuda" if torch.cuda.is_available() else "cpu"
        # INT8 on CUDA, fp32 on CPU — same convention used in benchmark.py.
        dtype = torch.int8 if device == "cuda" else torch.float32

        print(f"[orchestrator] Loading SLM '{model_name}' on {device} (dtype={dtype})...")
        tok = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
        mdl = AutoModelForCausalLM.from_pretrained(
            model_name, torch_dtype=dtype, trust_remote_code=True
        ).to(device).eval()
        self._slm_pool[model_name] = (tok, mdl)
        return self._slm_pool[model_name]

    # ── Semantic routing (§3.3, step 1) ──────────────────────────────

    def _route(self, query_embedding: np.ndarray, K: int) -> List[Tuple[str, float]]:
        """Top-K cluster agents by cosine similarity with summary embeddings."""
        return find_top_n_slms(query_embedding, self.registry, n=K)

    # ── Public API ────────────────────────────────────────────────────

    def process_query(
        self,
        query: str,
        *,
        K: int = 3,
        model_name: Optional[str] = None,
        tau_size_primary: int = 5,
        tau_size_secondary: int = 2,
        tau_rel: float = 0.0,
        retrieve_top_k_primary: int = 20,
        retrieve_top_k_secondary: int = 10,
        max_new_tokens: int = 256,
    ) -> QueryResult:

        if not self.agents:
            raise RuntimeError(
                "Agent registry is empty. Run document ingestion first."
            )

        trace: List[DSLInvocation] = []
        K = max(1, min(K, len(self.agents)))

        # ── 1. Semantic routing ──────────────────────────────────────
        t0 = time.perf_counter()
        q_emb = self.embedding_model.encode(
            [query], normalize_embeddings=True, convert_to_numpy=True
        )[0].astype(np.float32)
        routing = self._route(q_emb, K=K)
        t_route = (time.perf_counter() - t0) * 1000
        trace.append(DSLInvocation(
            agent="orchestrator",
            role="orchestrator",
            operation="route",
            input_summary=f"K={K}, |A|={len(self.agents)}",
            output_size=len(routing),
            elapsed_ms=t_route,
        ))

        if not routing:
            raise RuntimeError("Routing returned no candidate agents.")

        # Per §3.3: highest-scoring agent is the primary; the rest are secondaries.
        primary_name, primary_score = routing[0]
        secondary_pairs = routing[1:]
        primary_agent = self.agents[primary_name]
        secondary_agents = [self.agents[name] for name, _ in secondary_pairs]

        # ── 2. Primary agent invocation ──────────────────────────────
        t0 = time.perf_counter()
        ranked_primary = primary_agent.local_retrieve(query, top_k=retrieve_top_k_primary)
        t_lr = (time.perf_counter() - t0) * 1000
        trace.append(DSLInvocation(
            agent=primary_name,
            role="primary",
            operation="local_retrieve",
            input_summary=f"|M_j|={primary_agent.memory_size()}",
            output_size=len(ranked_primary),
            elapsed_ms=t_lr,
        ))

        t0 = time.perf_counter()
        E_star = primary_agent.select_evidence(
            query, ranked_primary, tau_size=tau_size_primary, tau_rel=tau_rel
        )
        t_se = (time.perf_counter() - t0) * 1000
        trace.append(DSLInvocation(
            agent=primary_name,
            role="primary",
            operation="select_evidence",
            input_summary=f"tau_size={tau_size_primary}, tau_rel={tau_rel}",
            output_size=len(E_star),
            elapsed_ms=t_se,
        ))

        # ── 3. Conditional secondary invocation ──────────────────────
        secondary_evidence: Dict[str, EvidenceSet] = {}
        if K > 1:
            for sec in secondary_agents:
                t0 = time.perf_counter()
                E_i = sec.provide_evidence(
                    query,
                    tau_size=tau_size_secondary,
                    tau_rel=tau_rel,
                    retrieve_top_k=retrieve_top_k_secondary,
                )
                t_pe = (time.perf_counter() - t0) * 1000
                secondary_evidence[sec.name] = E_i
                trace.append(DSLInvocation(
                    agent=sec.name,
                    role="secondary",
                    operation="provide_evidence",
                    input_summary=f"|M_j|={sec.memory_size()}, tau_size={tau_size_secondary}",
                    output_size=len(E_i),
                    elapsed_ms=t_pe,
                ))

        # Aggregate Γ = E* ∪ E_1^- ∪ ... ∪ E_{K-1}^-, deduplicating by chunk id.
        t0 = time.perf_counter()
        gamma: EvidenceSet = []
        seen_ids = set()
        for src in [E_star] + list(secondary_evidence.values()):
            for chunk in src:
                cid = chunk.get("id")
                if cid in seen_ids:
                    continue
                seen_ids.add(cid)
                gamma.append(chunk)
        t_agg = (time.perf_counter() - t0) * 1000
        trace.append(DSLInvocation(
            agent="orchestrator",
            role="orchestrator",
            operation="aggregate",
            input_summary=f"|E*|={len(E_star)}, secondaries={len(secondary_evidence)}",
            output_size=len(gamma),
            elapsed_ms=t_agg,
        ))

        retrieval_ms = sum(
            inv.elapsed_ms for inv in trace if inv.operation != "generate"
        )
        pool_size = primary_agent.memory_size() + sum(
            self.agents[name].memory_size() for name, _ in secondary_pairs
        )

        # ── 4. Response generation (primary-only) ────────────────────
        answer = ""
        generation_ms = 0.0
        if model_name:
            slm_runtime = self._bind_slm(model_name)
            t0 = time.perf_counter()
            answer = primary_agent.generate(
                query=query,
                gamma=gamma,
                slm_runtime=slm_runtime,
                role="primary",
                max_new_tokens=max_new_tokens,
            )
            generation_ms = (time.perf_counter() - t0) * 1000
            trace.append(DSLInvocation(
                agent=primary_name,
                role="primary",
                operation="generate",
                input_summary=f"|Γ|={len(gamma)}, model={model_name}",
                output_size=len(answer),
                elapsed_ms=generation_ms,
            ))

        return QueryResult(
            query=query,
            answer=answer,
            primary=primary_name,
            secondaries=[name for name, _ in secondary_pairs],
            routing=routing,
            primary_evidence=E_star,
            secondary_evidence=secondary_evidence,
            gamma=gamma,
            pool_size=pool_size,
            retrieval_ms=retrieval_ms,
            generation_ms=generation_ms,
            trace=trace,
        )

    # ── Convenience: pretty-print a trace ─────────────────────────────

    @staticmethod
    def format_trace(result: QueryResult) -> str:
        """Render the DSL invocation trace as a readable block."""
        lines: List[str] = []
        lines.append(f"Query: {result.query}")
        route_str = ", ".join(f"{n} ({s:.3f})" for n, s in result.routing)
        lines.append(f"Routing top-{len(result.routing)}: {route_str}")
        lines.append(
            f"Primary: {result.primary}  |  Secondaries: "
            f"{result.secondaries if result.secondaries else '—'}"
        )
        lines.append("")
        lines.append("DSL trace:")
        for inv in result.trace:
            lines.append(
                f"  [{inv.role:<12}] {inv.agent:<14} "
                f"{inv.operation:<17} → out={inv.output_size:<4} "
                f"({inv.elapsed_ms:6.2f} ms)  {inv.input_summary}"
            )
        lines.append("")
        lines.append(
            f"Pool examined: {result.pool_size} chunks  |  "
            f"|Γ| = {len(result.gamma)}  |  retrieval = {result.retrieval_ms:.2f} ms  |  "
            f"generation = {result.generation_ms:.2f} ms"
        )
        return "\n".join(lines)


# ── Module-level convenience: one-shot query ───────────────────────────

def run_query(
    query: str,
    chroma_client: Any,
    embedding_model: SentenceTransformer,
    *,
    K: int = 3,
    model_name: Optional[str] = None,
    registry: Optional[Dict] = None,
    **kwargs: Any,
) -> QueryResult:
    """Build an orchestrator on the fly and process a single query."""
    orch = Orchestrator(
        registry=registry,
        chroma_client=chroma_client,
        embedding_model=embedding_model,
    )
    return orch.process_query(query, K=K, model_name=model_name, **kwargs)
