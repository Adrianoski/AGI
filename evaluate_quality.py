"""
evaluate_quality.py — Valutazione qualitativa RAG con RAGAS + Claude come giudice.

Metriche calcolate (StdRAG vs SLM-RAG):
  - Contextual Precision  — chunk pertinenti / chunk recuperati
  - Contextual Recall     — fatti di ground-truth coperti dai chunk
  - Answer Relevancy      — risposta pertinente alla domanda
  - Faithfulness          — risposta fondata sul contesto
  - Hallucination         — 1 − Faithfulness (derivata)

Prerequisiti:
    pip install "ragas>=0.2" langchain-openai langchain-huggingface
    export OPENAI_API_KEY=sk-...

Uso:
    python3 evaluate_quality.py
    python3 evaluate_quality.py --input benchmark_answers_results.json --output quality_report.md
"""

import os
import json
import argparse
import math
import numpy as np
from pathlib import Path


# ── I/O ────────────────────────────────────────────────────────────────────────

def load_results(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


# ── RAGAS dataset ──────────────────────────────────────────────────────────────

def build_samples(results: list, mode: str):
    from ragas import SingleTurnSample
    samples = []
    for r in results:
        chunks = r[mode]["chunks"]
        if not chunks:
            chunks = ["Nessun contesto recuperato."]
        samples.append(SingleTurnSample(
            user_input=r["query_en"],
            response=r[mode]["answer"],
            retrieved_contexts=chunks,
            reference=r["ground_truth"],
        ))
    return samples


# ── RAGAS evaluation ───────────────────────────────────────────────────────────

def run_ragas(samples, llm, embeddings):
    from ragas import EvaluationDataset, evaluate, RunConfig
    from ragas.metrics import (
        LLMContextPrecisionWithReference,
        LLMContextRecall,
        ResponseRelevancy,
        Faithfulness,
    )
    metrics = [
        LLMContextPrecisionWithReference(llm=llm),
        LLMContextRecall(llm=llm),
        ResponseRelevancy(llm=llm, embeddings=embeddings),
        Faithfulness(llm=llm),
    ]
    dataset = EvaluationDataset(samples=samples)
    # max_workers=1 → richieste sequenziali, evita burst che saturano TPM
    run_config = RunConfig(max_workers=1, timeout=120)
    return evaluate(dataset=dataset, metrics=metrics, run_config=run_config)


# ── Report ─────────────────────────────────────────────────────────────────────

METRIC_KEYS = {
    "llm_context_precision_with_reference": "Contextual Precision",
    "llm_context_recall":                  "Contextual Recall",
    "response_relevancy":                  "Answer Relevancy",
    "faithfulness":                        "Faithfulness",
}


def _fmt(val) -> str:
    if val is None or (isinstance(val, float) and math.isnan(val)):
        return "—"
    return f"{float(val):.3f}"


def _mean(score_obj, key: str) -> float:
    try:
        return float(score_obj[key])
    except Exception:
        return float("nan")


def _per_sample(score_obj, key: str) -> list:
    try:
        return [s.get(key, float("nan")) for s in score_obj.scores]
    except Exception:
        return []


def write_report(results, score_std, score_slm, metadata, output_path):
    col   = metadata.get("collection", "?")
    model = metadata.get("model", "?")

    # aggregate means
    means_std = {k: _mean(score_std, k) for k in METRIC_KEYS}
    means_slm = {k: _mean(score_slm, k) for k in METRIC_KEYS}

    # per-sample scores
    per_std = {k: _per_sample(score_std, k) for k in METRIC_KEYS}
    per_slm = {k: _per_sample(score_slm, k) for k in METRIC_KEYS}

    # efficiency aggregates from JSON
    std_ret  = np.mean([r["std"]["t_ret_ms"] for r in results])
    slm_ret  = np.mean([r["slm"]["t_ret_ms"] for r in results])
    std_pool = np.mean([r["std"]["pool"]      for r in results])
    slm_pool = np.mean([r["slm"]["pool"]      for r in results])
    std_hr   = np.mean([r["std"]["keyword_hit_pct"] for r in results])
    slm_hr   = np.mean([r["slm"]["keyword_hit_pct"] for r in results])
    speedup  = std_ret / slm_ret if slm_ret > 0 else 0.0

    with open(output_path, "w", encoding="utf-8") as f:

        f.write(f"# Quality Report — {col}\n\n")
        f.write(f"**Modello generazione:** {model}  |  "
                f"**Giudice LLM:** gpt-4o  |  "
                f"**Query:** {len(results)}\n\n")

        # ── Metriche di qualità ────────────────────────────────────────
        f.write("## Metriche di qualità (RAGAS)\n\n")
        f.write("| Metrica | StdRAG | SLM-RAG | Δ (SLM−Std) |\n|---|---|---|---|\n")

        for key, label in METRIC_KEYS.items():
            s  = means_std[key]
            sl = means_slm[key]
            delta = sl - s if not (math.isnan(s) or math.isnan(sl)) else float("nan")
            sign  = "+" if delta > 0 else ""
            d_str = f"{sign}{_fmt(delta)}" if not math.isnan(delta) else "—"
            f.write(f"| {label} | {_fmt(s)} | {_fmt(sl)} | {d_str} |\n")

        # Hallucination = 1 − Faithfulness
        faith_key = "faithfulness"
        hall_std = 1 - means_std[faith_key] if not math.isnan(means_std[faith_key]) else float("nan")
        hall_slm = 1 - means_slm[faith_key] if not math.isnan(means_slm[faith_key]) else float("nan")
        delta_h  = hall_slm - hall_std if not (math.isnan(hall_std) or math.isnan(hall_slm)) else float("nan")
        sign_h   = "+" if delta_h > 0 else ""
        d_h_str  = f"{sign_h}{_fmt(delta_h)}" if not math.isnan(delta_h) else "—"
        f.write(f"| Hallucination *(1−Faith)* | {_fmt(hall_std)} | {_fmt(hall_slm)} | {d_h_str} |\n")

        f.write("\n---\n\n")

        # ── Metriche di efficienza ─────────────────────────────────────
        f.write("## Metriche di efficienza\n\n")
        f.write("| Metrica | StdRAG | SLM-RAG |\n|---|---|---|\n")
        f.write(f"| Retrieval medio | {std_ret:.1f} ms | {slm_ret:.1f} ms |\n")
        f.write(f"| Pool medio | {std_pool:.0f} chunk | {slm_pool:.0f} chunk |\n")
        f.write(f"| Speedup retrieval | — | **{speedup:.1f}x** |\n")
        f.write(f"| Keyword hit | {std_hr:.0f}% | {slm_hr:.0f}% |\n")

        f.write("\n---\n\n")

        # ── Dettaglio per query ────────────────────────────────────────
        f.write("## Dettaglio per query\n\n")

        cp = "llm_context_precision_with_reference"
        cr = "llm_context_recall"
        ar = "response_relevancy"
        fa = "faithfulness"

        header = (
            "| # | Query | CP Std | CP SLM | CR Std | CR SLM "
            "| AR Std | AR SLM | Faith Std | Faith SLM |\n"
        )
        f.write(header)
        f.write("|---|---|---|---|---|---|---|---|---|---|\n")

        n = len(results)
        for i, r in enumerate(results):
            label = r["query_en"][:48] + ("…" if len(r["query_en"]) > 48 else "")

            def gs(key, src):
                lst = per_std[key] if src == "std" else per_slm[key]
                return _fmt(lst[i]) if i < len(lst) else "—"

            f.write(
                f"| {i+1} | {label} "
                f"| {gs(cp,'std')} | {gs(cp,'slm')} "
                f"| {gs(cr,'std')} | {gs(cr,'slm')} "
                f"| {gs(ar,'std')} | {gs(ar,'slm')} "
                f"| {gs(fa,'std')} | {gs(fa,'slm')} |\n"
            )

        f.write("\n---\n\n")

        # ── Risposte complete per ogni query ───────────────────────────
        f.write("## Risposte per query\n\n")
        for i, r in enumerate(results, 1):
            f.write(f"### {i}. {r['query_en']}\n\n")
            f.write(f"*{r['query_it']}*\n\n")
            f.write(f"**Ground Truth:** {r['ground_truth']}\n\n")
            f.write(f"**StdRAG:** {r['std']['answer']}\n\n")
            f.write(f"**SLM-RAG:** {r['slm']['answer']}\n\n")
            f.write("---\n\n")


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Valutazione qualitativa RAG con RAGAS + Claude"
    )
    parser.add_argument(
        "--input",  default="benchmark_answers_results.json",
        help="JSON prodotto da benchmark.py"
    )
    parser.add_argument(
        "--output", default="quality_report.md",
        help="File markdown di output"
    )
    args = parser.parse_args()

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit(
            "Errore: OPENAI_API_KEY non impostata.\n"
            "  export OPENAI_API_KEY=sk-..."
        )

    if not Path(args.input).exists():
        raise SystemExit(
            f"Errore: file '{args.input}' non trovato.\n"
            "  Esegui prima: python3 benchmark.py"
        )

    data     = load_results(args.input)
    results  = data["results"]
    metadata = data.get("metadata", {})
    print(f"Query caricate: {len(results)}  |  collection: {metadata.get('collection','?')}")

    # ── Setup LLM e embeddings ─────────────────────────────────────────
    from langchain_openai import ChatOpenAI
    from ragas.llms import LangchainLLMWrapper
    from ragas.embeddings import LangchainEmbeddingsWrapper
    from langchain_huggingface import HuggingFaceEmbeddings

    llm = LangchainLLMWrapper(ChatOpenAI(
        model="gpt-4o",
        api_key=api_key,
        temperature=0,
        max_tokens=1024,
        max_retries=8,          # retry automatico con exponential backoff
    ))
    embeddings = LangchainEmbeddingsWrapper(
        HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
    )

    # ── Valutazione ────────────────────────────────────────────────────
    print("\nValutazione StdRAG con RAGAS...")
    score_std = run_ragas(build_samples(results, "std"), llm, embeddings)

    print("Valutazione SLM-RAG con RAGAS...")
    score_slm = run_ragas(build_samples(results, "slm"), llm, embeddings)

    # ── Report ─────────────────────────────────────────────────────────
    write_report(results, score_std, score_slm, metadata, args.output)
    print(f"\nReport salvato: {args.output}")


if __name__ == "__main__":
    main()