"""
benchmark.py — Confronto RAG standard vs SLM-routed retrieval.

Metriche:
  - Latenza media (ms) per query
  - Dimensione del pool di ricerca (n. chunk esaminati)
  - Overlap@5 tra i due sistemi (per stimare la qualità relativa)

Uso:
    python3 benchmark.py
"""

import time
import json
import re
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi
import chromadb
from router import load_registry, find_top_n_slms

# ── Config ─────────────────────────────────────────────────────────────
TOP_N_SLMS        = 3
TOP_K             = 5
RRF_K             = 60
COLLECTION        = None                  # non usato — il benchmark cerca su tutte le collection
GENERATION_MODEL  = "Qwen/Qwen3.5-4B"    # modello HuggingFace per la generazione
MAX_NEW_TOKENS    = 256
MAX_INPUT_TOKENS  = 131072                # 128K — Qwen3.5-4B nativo è 256K, niente rope scaling necessario
OUTPUT_FILE       = f"benchmark_answers_spacy_4B_3_WAYS_5PDF_{TOP_N_SLMS}_SLM_TOK_K_{TOP_K}.md"

QUERIES = [
    # ── ORIGINAL 10 ──────────────────────────────────────────────────────────
    (
        "Who imported spices into Europe during the Middle Ages?",
        "Chi importava le spezie in Europa nel Medioevo?",
        ["arabi", "veneziana", "mercanti", "spezie", "oriente", "monopolio"],
        (
            "The spice trade was controlled by Arab merchants together with the "
            "Venetian republic, who held the monopoly by crossing Muslim "
            "territories. The many risks of the journey and the various changes "
            "of hands considerably raised the price of the goods."
        ),
    ),
    (
        "What territories did Charles V control?",
        "Quali territori controllava Carlo V?",
        ["carlo", "spagna", "impero", "asburgo", "fiandre", "napoli"],
        (
            "Charles V controlled a vast empire that included Spain, the "
            "Habsburg territories, Flanders, the Kingdom of Naples, and the "
            "American colonies. His reign was marked by conflicts with France, "
            "the Lutheran German princes, and the Ottoman Empire."
        ),
    ),
    (
        "What were the main causes of the French Revolution?",
        "Quali furono le principali cause della Rivoluzione Francese?",
        ["crisi", "stato", "terzo", "nobiltà", "tasse", "assemblea"],
        (
            "The main causes of the French Revolution were the economic crisis "
            "of the Ancien Régime, the fiscal injustices that burdened the third "
            "estate, the convening of the Estates General, and the growing "
            "influence of public opinion. The nobility and clergy enjoyed fiscal "
            "privileges that fuelled popular discontent."
        ),
    ),
    (
        "What were the key principles of the Enlightenment?",
        "Quali erano i principi fondamentali dell'Illuminismo?",
        ["ragione", "philosophes", "libertà", "progresso", "lume", "diritti"],
        (
            "The Enlightenment was founded on the primacy of the 'natural light' "
            "of reason as a tool for knowledge and criticism of reality. The "
            "philosophes advocated a new vision of economics and politics based "
            "on freedom, progress, and the natural rights of the individual."
        ),
    ),
    (
        "Who were the Mongols and how did they expand?",
        "Chi erano i Mongoli e come si espansero?",
        ["mongoli", "gengis", "khan", "asia", "impero", "tartari"],
        (
            "The Mongols were a people of horsemen led by Genghis Khan, who "
            "launched his offensive toward China by crossing the Great Wall, "
            "then occupied the steppes of southern Russia, conquered Samarkand "
            "and Bukhara, and attacked Persia, Georgia, and Bulgaria. They were "
            "called Tartars by Europeans. After his death the kingdom was "
            "divided among his four sons, giving rise to four Khanates."
        ),
    ),
    (
        "What was Luther's Protestant Reformation?",
        "Che cos'era la Riforma protestante di Lutero?",
        ["lutero", "chiesa", "bibbia", "riforma", "fede", "protestante"],
        (
            "Luther's Protestant Reformation marked a definitive break with "
            "Catholic doctrine, reaffirmed in the Augsburg Confession presented "
            "by Philip Melanchthon at the Diet of Augsburg in 1530. The Peace of "
            "Augsburg of 1555 officially recognised the Protestant religion by "
            "establishing the principle 'cuius regio eius religio'."
        ),
    ),
    (
        "How was the Italian state formed during the Risorgimento?",
        "Come si formò lo Stato italiano durante il Risorgimento?",
        ["cavour", "garibaldi", "mazzini", "unità", "piemonte", "italia"],
        (
            "Italian unification was the result of the Risorgimento, led by "
            "figures such as Mazzini (founder of Young Italy), Cavour (who "
            "conducted diplomatic policy and the Second War of Independence), "
            "and Garibaldi (who led the Expedition of the Thousand). Piedmont "
            "was the fulcrum of the unification process."
        ),
    ),
    (
        "What were the social consequences of the Industrial Revolution?",
        "Quali furono le conseguenze sociali della Rivoluzione Industriale?",
        ["operai", "fabbriche", "lavoro", "proletariato", "borghesia", "sfruttamento"],
        (
            "The Industrial Revolution brought about the birth of the "
            "working-class proletariat, who worked in factories under "
            "exploitative conditions. The divide between the property-owning "
            "bourgeoisie and the working class deepened. The negative effects of "
            "industrialisation included exhausting working hours and poor "
            "sanitary conditions."
        ),
    ),

    # ── NUOVE 30 ─────────────────────────────────────────────────────────────
    (
        "How did the population of Europe change from the year 1000 to the 14th century?",
        "Come cambiò la popolazione europea dall'anno 1000 al XIV secolo?",
        ["popolazione", "raddoppiando", "40 milioni", "80 milioni", "carestie", "disboscare"],
        (
            "The European population grew from the year 1000 until the beginning "
            "of the fourteenth century, doubling from around 40 million to "
            "around 80 million inhabitants. This made it necessary to clear new "
            "land to increase agricultural production, although cyclical famines "
            "occurring every decade caused thousands of deaths."
        ),
    ),
    (
        "How did the plague spread from Crimea to Europe?",
        "Come si diffuse la peste dalla Crimea all'Europa?",
        ["crimea", "genovesi", "catapulte", "cadaveri", "genova", "venezia", "sicilia"],
        (
            "The first epidemic of plague broke out in a Genoese colony in "
            "Crimea besieged by the Tartars, who hurled infected corpses over "
            "the walls using catapults. Genoese citizens fleeing the siege "
            "spread the contagion by sea. Around 1347 the plague reached Genoa, "
            "Venice, and Sicily, spreading the following year to Tuscany, "
            "France, England, Spain, and Germany. By 1353 it had killed "
            "approximately one third of the European population."
        ),
    ),
    (
        "Who were blamed for spreading the plague and what happened to them?",
        "Chi fu accusato di diffondere la peste e cosa accadde loro?",
        ["ebrei", "pogrom", "pozzi", "capro espiatorio", "emarginati", "lebbrosi"],
        (
            "Scapegoats included the marginalised, lepers, and above all Jews, "
            "who were accused of poisoning well water or of contaminating the "
            "air with poisons. As a result, thousands of Jews were persecuted — "
            "in pogroms — across France, Germany, and Switzerland."
        ),
    ),
    (
        "Who was Henry the Navigator and what was his contribution to exploration?",
        "Chi era Enrico il Navigatore e qual fu il suo contributo all'esplorazione?",
        ["enrico il navigatore", "sagres", "caravella", "algarve", "venti", "atlantico"],
        (
            "Henry the Navigator was the king of Portugal who founded a naval "
            "school at his residence at Cape Sagres in the Algarve. There, "
            "information was gathered on tides, winds, and the Atlantic Ocean. "
            "He promoted the replacement of the galley with the more "
            "manoeuvrable caravel and launched Portuguese explorations toward "
            "the Azores and the circumnavigation of Africa."
        ),
    ),
    (
        "What was Calvin's doctrine of predestination?",
        "Qual era la dottrina della predestinazione di Calvino?",
        ["predestinazione", "eletti", "dannati", "calvino", "grazia", "paradiso"],
        (
            "Calvin affirmed the absolute sovereignty of God over humanity and "
            "the doctrine of predestination: mankind is divided into the elect, "
            "destined for Heaven, and the damned. With his imperfect nature, man "
            "cannot save himself through his own faith; it is God who "
            "predestines him to salvation. Calvin recognised only baptism and "
            "the Eucharist as valid sacraments."
        ),
    ),
    (
        "What was England's Glorious Revolution?",
        "Che cos'era la Gloriosa Rivoluzione inglese?",
        ["gloriosa rivoluzione", "inghilterra", "parlamento", "sovrano", "costituzionale"],
        (
            "The Glorious Revolution in England is described in the context of "
            "the transition from absolutism toward more constitutional forms of "
            "government in seventeenth-century England, in which Parliament "
            "limited the absolute power of the sovereign."
        ),
    ),
    (
        "What were the main features of the First Industrial Revolution?",
        "Quali furono le principali caratteristiche della Prima Rivoluzione Industriale?",
        ["rivoluzione industriale", "fabbrica", "operai", "carbone", "watt", "inghilterra"],
        (
            "The First Industrial Revolution was characterised by the "
            "introduction of new technologies such as James Watt's steam engine, "
            "the emergence of the factory as a centre of concentrated "
            "production, the massive use of coal, and the transformation of "
            "social relations with the birth of the working-class proletariat."
        ),
    ),
    (
        "Who were the philosophes and what was their central idea?",
        "Chi erano i philosophes e qual era la loro idea centrale?",
        ["philosophes", "ragione", "lume", "conoscenza", "critica", "illuminismo"],
        (
            "The philosophes were the thinkers of the Enlightenment who "
            "championed the primacy of the 'natural light' of reason as a tool "
            "for knowledge and criticism of social and political reality. They "
            "proposed a new vision of economics and politics grounded in natural "
            "rights and progress."
        ),
    ),
    (
        "What were the economic causes of the French Revolution?",
        "Quali furono le cause economiche della Rivoluzione Francese?",
        ["crisi economica", "ancien regime", "stati generali", "terzo stato", "debito"],
        (
            "The economic crisis is identified as one of the main preconditions "
            "of the French Revolution. The Ancien Régime was characterised by "
            "fiscal privileges for the nobility and clergy, while the burden of "
            "taxation fell on the third estate. The convening of the Estates "
            "General was a direct response to this financial crisis."
        ),
    ),
    (
        "What was the War of the Vendée during the French Revolution?",
        "Che cos'era la guerra della Vandea durante la Rivoluzione Francese?",
        ["vandea", "rivoluzionari", "guerra", "interna", "controrivoluzione"],
        (
            "The War of the Vendée was one of the internal difficulties of the "
            "French Revolution: a civil conflict that pitted the revolutionaries "
            "against part of the French population — particularly peasants and "
            "those loyal to the monarchy and the Church — in the Vendée region."
        ),
    ),
    (
        "What were Napoleon's main military campaigns and how did his empire end?",
        "Quali furono le principali campagne militari di Napoleone e come finì il suo impero?",
        ["campagna d'italia", "mosca", "sant'elena", "consolato", "impero", "sconfitta"],
        (
            "Napoleon led the Italian campaign, during which the Republics were "
            "established, and the Egyptian campaign, which accelerated his "
            "political rise; he then installed the Consulate and the Empire, "
            "extending his hegemony over Europe. The conquest of Moscow marked "
            "the beginning of his decline; the empire ended with his final "
            "defeat and exile to the island of Saint Helena."
        ),
    ),
    (
        "What did the Congress of Vienna decide and who were its main actors?",
        "Cosa stabilì il Congresso di Vienna e chi furono i suoi protagonisti?",
        ["congresso di vienna", "restaurazione", "santa alleanza", "europa", "equilibrio"],
        (
            "The Congress of Vienna established a new European order aimed at "
            "restoring the situation prior to the French Revolution and "
            "Napoleon's conquests. It led to the creation of the Holy Alliance "
            "among the conservative powers. The main actors were representatives "
            "of the great European powers that had defeated Napoleon."
        ),
    ),
    (
        "Who was Mazzini and what was the Giovine Italia?",
        "Chi era Mazzini e cos'era la Giovine Italia?",
        ["mazzini", "giovine italia", "dio e popolo", "repubblica", "indipendenza"],
        (
            "Giuseppe Mazzini was one of the leading figures of the Risorgimento "
            "and founder of Young Italy (Giovine Italia), an association that "
            "advocated the independence and unification of Italy as a free "
            "republican nation, inspired by the motto 'God and the People'."
        ),
    ),
    (
        "What was Cavour's role in the unification of Italy?",
        "Qual fu il ruolo di Cavour nell'unificazione d'Italia?",
        ["cavour", "seconda guerra", "spedizione dei mille", "piemonte", "diplomatica"],
        (
            "Count Camillo Benso di Cavour was the central political figure in "
            "the unification process. He introduced reforms in the Kingdom of "
            "Sardinia, pursued a foreign policy that led to an alliance with "
            "France, directed the Second War of Independence, and created the "
            "diplomatic conditions for Garibaldi's Expedition of the Thousand."
        ),
    ),
    (
        "What was the Monroe Doctrine and in what context was it issued?",
        "Che cos'era la dottrina Monroe e in quale contesto fu proclamata?",
        ["monroe", "america latina", "indipendenza", "colonizzazione", "europa", "intervento"],
        (
            "The Monroe Doctrine was proclaimed in the context of the Latin "
            "American independence struggles and liberal uprisings. It asserted "
            "the principle that America should not be considered a field for "
            "further European colonisation, opposing the interventionism of Old "
            "World powers in the Americas."
        ),
    ),
    (
        "How were the price revolution of the 16th century and the geographical discoveries connected?",
        "Come erano collegate la rivoluzione dei prezzi del XVI secolo e le scoperte geografiche?",
        ["rivoluzione dei prezzi", "bodin", "oro", "argento", "americhe", "inflazione"],
        (
            "In the sixteenth century, prices rose by approximately 400%. The "
            "thinker Jean Bodin explained this phenomenon by arguing that the "
            "massive importation of gold and silver from the Americas by Spain "
            "and Portugal had caused the devaluation of money. Wage earners were "
            "the most penalised, as inflation eroded their already meagre "
            "purchasing power."
        ),
    ),
]
# ── Helpers ────────────────────────────────────────────────────────────

def tokenize(text: str):
    return re.sub(r'[^\w\s]', ' ', text.lower()).split()


def rrf(rankings, k=RRF_K):
    scores = {}
    for ranking in rankings:
        for rank, idx in enumerate(ranking):
            scores[idx] = scores.get(idx, 0.0) + 1.0 / (k + rank + 1)
    return sorted(scores.keys(), key=lambda x: scores[x], reverse=True)


def cosine_scores(q_emb, embeddings):
    q_norm = float(np.linalg.norm(q_emb))
    scores = []
    for emb in embeddings:
        e = np.array(emb, dtype=np.float32)
        e_norm = float(np.linalg.norm(e))
        scores.append(float(np.dot(q_emb, e) / (q_norm * e_norm)) if e_norm > 0 else 0.0)
    return scores


# ── RAG standard: cerca su TUTTI i chunk di TUTTE le collection ────────

def retrieve_standard(query, q_emb, chroma_client, top_k=TOP_K):
    t0 = time.perf_counter()

    embeddings, documents = [], []
    for col_info in chroma_client.list_collections():
        col  = chroma_client.get_collection(col_info.name)
        data = col.get(include=["embeddings", "documents"])
        embeddings.extend(data["embeddings"])
        documents.extend(data["documents"])

    dense_scores = cosine_scores(q_emb, embeddings)
    dense_rank   = sorted(range(len(embeddings)), key=lambda i: dense_scores[i], reverse=True)

    bm25       = BM25Okapi([tokenize(d) for d in documents])
    bm25_sc    = bm25.get_scores(tokenize(query))
    bm25_rank  = sorted(range(len(embeddings)), key=lambda i: float(bm25_sc[i]), reverse=True)

    fused = rrf([dense_rank, bm25_rank])[:top_k]
    elapsed = (time.perf_counter() - t0) * 1000

    return [documents[i] for i in fused], len(embeddings), elapsed


# ── SLM-routed retrieval ───────────────────────────────────────────────

def retrieve_slm(query, q_emb, registry, chroma_client, top_k=TOP_K):
    t0 = time.perf_counter()

    top_slms = find_top_n_slms(q_emb, registry, n=TOP_N_SLMS)

    all_chunks = []
    for slm_name, _ in top_slms:
        entry = registry[slm_name]
        chunks_path = Path(entry["chunks_json"])
        if not chunks_path.exists():
            continue
        with open(chunks_path) as f:
            chunk_ids = [c["id"] for c in json.load(f)]
        col = chroma_client.get_collection(entry["collection"])
        data = col.get(ids=chunk_ids, include=["embeddings", "documents", "metadatas"])
        for i, emb in enumerate(data["embeddings"]):
            e = np.array(emb, dtype=np.float32)
            e_norm = float(np.linalg.norm(e))
            q_norm = float(np.linalg.norm(q_emb))
            ds = float(np.dot(q_emb, e) / (q_norm * e_norm)) if e_norm > 0 else 0.0
            all_chunks.append({"text": data["documents"][i], "score": ds})

    if not all_chunks:
        return [], 0, (time.perf_counter() - t0) * 1000

    dense_rank = sorted(range(len(all_chunks)), key=lambda i: all_chunks[i]["score"], reverse=True)
    bm25       = BM25Okapi([tokenize(c["text"]) for c in all_chunks])
    bm25_sc    = bm25.get_scores(tokenize(query))
    bm25_rank  = sorted(range(len(all_chunks)), key=lambda i: float(bm25_sc[i]), reverse=True)

    fused   = rrf([dense_rank, bm25_rank])[:top_k]
    elapsed = (time.perf_counter() - t0) * 1000

    return [all_chunks[i]["text"] for i in fused], len(all_chunks), elapsed


# ── SLM-Full: routing + tutti i chunk del cluster (no retrieval interno) ──

def retrieve_slm_full(query, q_emb, registry, chroma_client):
    """Solo routing semantico: passa al LLM TUTTI i chunk dei top-N SLM,
    senza ulteriore filtraggio dense/BM25 intra-cluster."""
    t0 = time.perf_counter()

    top_slms = find_top_n_slms(q_emb, registry, n=TOP_N_SLMS)

    docs = []
    for slm_name, _ in top_slms:
        entry = registry[slm_name]
        chunks_path = Path(entry["chunks_json"])
        if not chunks_path.exists():
            continue
        with open(chunks_path) as f:
            chunk_ids = [c["id"] for c in json.load(f)]
        col = chroma_client.get_collection(entry["collection"])
        data = col.get(ids=chunk_ids, include=["documents"])
        docs.extend(data["documents"])

    elapsed = (time.perf_counter() - t0) * 1000
    return docs, len(docs), elapsed


# ── Generation ────────────────────────────────────────────────────────

_gen_tok = None
_gen_mdl = None

def _load_gen_model(model_name: str):
    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM
    global _gen_tok, _gen_mdl
    if _gen_tok is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        dtype  = torch.int8 if device == "cuda" else torch.float32
        print(f"  Carico {model_name} su {device} (max_input_tokens={MAX_INPUT_TOKENS})...")
        _gen_tok = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
        _gen_tok.model_max_length = MAX_INPUT_TOKENS
        _gen_mdl = AutoModelForCausalLM.from_pretrained(
            model_name, torch_dtype=dtype, trust_remote_code=True
        ).to(device).eval()


def generate(query: str, docs: list, model_name: str) -> str:
    import torch
    from SLMAgent import build_messages, _apply_chat_template_no_think
    _load_gen_model(model_name)
    device = next(_gen_mdl.parameters()).device
    # apply_chat_template with enable_thinking=False prevents <think> tokens at the source.
    text = _apply_chat_template_no_think(_gen_tok, build_messages(query, docs))
    inputs = _gen_tok(text, return_tensors="pt", truncation=True, max_length=MAX_INPUT_TOKENS).to(device)
    with torch.no_grad():
        out = _gen_mdl.generate(
            **inputs,
            max_new_tokens=MAX_NEW_TOKENS,
            do_sample=False,
            pad_token_id=_gen_tok.eos_token_id,
        )
    return _gen_tok.decode(out[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True).strip()


# ── Main ───────────────────────────────────────────────────────────────

def main():
    print("Carico modelli...")
    emb_model    = SentenceTransformer("BAAI/bge-m3")
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    registry     = load_registry()

    all_cols     = chroma_client.list_collections()
    total_chunks = sum(chroma_client.get_collection(c.name).count() for c in all_cols)
    col_names    = [c.name for c in all_cols]

    print(f"Collections: {col_names}  |  chunk totali: {total_chunks}  |  SLM: {len(registry)}")
    print(f"Query: {len(QUERIES)}  |  top-k={TOP_K}  |  top-N SLM={TOP_N_SLMS}  |  model={GENERATION_MODEL}\n")

    def hit_rate(docs, keywords):
        joined = " ".join(docs).lower()
        hits = sum(1 for kw in keywords if kw in joined)
        return hits / len(keywords) * 100 if keywords else 0.0

    std_times, slm_times, full_times = [], [], []
    std_pools, slm_pools, full_pools = [], [], []
    std_gens,  slm_gens,  full_gens  = [], [], []
    overlaps, std_hits, slm_hits, full_hits = [], [], [], []
    md_rows = []

    SEP = "=" * 110
    for idx, (query_en, query_it, expected_kws, ground_truth) in enumerate(QUERIES, 1):
        print(f"\n[{idx}/{len(QUERIES)}] {query_en}")

        # Retrieval con la query IT: BM25 lavora nella stessa lingua dei documenti
        # (confronto fair tra StdRAG e SLM-RAG sull'aspetto retrieval).
        # La generazione riceve query_it ma il system prompt forza l'output in inglese,
        # così evaluate_quality.py può usare query_en + mpnet senza language mismatch.
        q_emb = emb_model.encode(
            [query_it], normalize_embeddings=True, convert_to_numpy=True
        )[0].astype(np.float32)

        docs_std,  pool_std,  t_std  = retrieve_standard(query_it, q_emb, chroma_client)
        docs_slm,  pool_slm,  t_slm  = retrieve_slm(query_it, q_emb, registry, chroma_client)
        docs_full, pool_full, t_full = retrieve_slm_full(query_it, q_emb, registry, chroma_client)

        overlap = len(set(docs_std[:TOP_K]) & set(docs_slm[:TOP_K])) / TOP_K * 100
        hr_std  = hit_rate(docs_std,  expected_kws)
        hr_slm  = hit_rate(docs_slm,  expected_kws)
        hr_full = hit_rate(docs_full, expected_kws)

        std_times.append(t_std);   slm_times.append(t_slm);   full_times.append(t_full)
        std_pools.append(pool_std); slm_pools.append(pool_slm); full_pools.append(pool_full)
        overlaps.append(overlap)
        std_hits.append(hr_std);   slm_hits.append(hr_slm);   full_hits.append(hr_full)

        speedup = t_std / t_slm if t_slm > 0 else float("inf")

        print(f"  Retrieval  —  StdRAG: {t_std:.1f}ms (pool={pool_std})  |  "
              f"SLM-RAG: {t_slm:.1f}ms (pool={pool_slm})  |  "
              f"SLM-Full: {t_full:.1f}ms (pool={pool_full})  speedup={speedup:.1f}x")
        # Generazione: query EN per forzare risposte in inglese (Qwen 4B segue la lingua
        # della domanda; il system prompt da solo non basta su modelli piccoli).
        print(f"  Generazione StdRAG...")
        t_gen0 = time.perf_counter()
        ans_std = generate(query_en, docs_std, GENERATION_MODEL)
        t_gen_std = (time.perf_counter() - t_gen0) * 1000

        print(f"  Generazione SLM-RAG...")
        t_gen0 = time.perf_counter()
        ans_slm = generate(query_en, docs_slm, GENERATION_MODEL)
        t_gen_slm = (time.perf_counter() - t_gen0) * 1000

        print(f"  Generazione SLM-Full...")
        t_gen0 = time.perf_counter()
        ans_full = generate(query_en, docs_full, GENERATION_MODEL)
        t_gen_full = (time.perf_counter() - t_gen0) * 1000

        std_gens.append(t_gen_std); slm_gens.append(t_gen_slm); full_gens.append(t_gen_full)

        print(f"  Gen times  —  StdRAG: {t_gen_std:.0f}ms  |  SLM-RAG: {t_gen_slm:.0f}ms  |  SLM-Full: {t_gen_full:.0f}ms")
        print(f"  StdRAG  : {ans_std[:100]}…")
        print(f"  SLM-RAG : {ans_slm[:100]}…")
        print(f"  SLM-Full: {ans_full[:100]}…")

        md_rows.append({
            "query_en":     query_en,
            "query_it":     query_it,
            "ground_truth": ground_truth,
            "ans_std":      ans_std,
            "ans_slm":      ans_slm,
            "ans_full":     ans_full,
            "docs_std":     docs_std,
            "docs_slm":     docs_slm,
            "docs_full":    docs_full,
            "t_ret_std":    t_std,
            "t_ret_slm":    t_slm,
            "t_ret_full":   t_full,
            "t_gen_std":    t_gen_std,
            "t_gen_slm":    t_gen_slm,
            "t_gen_full":   t_gen_full,
            "speedup":      speedup,
            "pool_std":     pool_std,
            "pool_slm":     pool_slm,
            "pool_full":    pool_full,
            "hr_std":       hr_std,
            "hr_slm":       hr_slm,
            "hr_full":      hr_full,
            "overlap":      overlap,
        })

    # ── Salva Markdown ─────────────────────────────────────────────────
    avg_speedup        = np.mean(std_times) / np.mean(slm_times)
    avg_speedup_full   = np.mean(std_times) / np.mean(full_times) if np.mean(full_times) > 0 else 0.0
    pool_reduction     = (1 - np.mean(slm_pools)  / np.mean(std_pools)) * 100
    pool_reduction_full= (1 - np.mean(full_pools) / np.mean(std_pools)) * 100

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(f"# Benchmark RAG — {', '.join(col_names)}\n\n")
        f.write(f"**Modello:** {GENERATION_MODEL}  |  **top-k:** {TOP_K}  |  **top-N SLM:** {TOP_N_SLMS}\n\n")
        f.write(f"| Metrica | StdRAG | SLM-RAG | SLM-Full |\n|---|---|---|---|\n")
        f.write(f"| Speedup retrieval | — | **{avg_speedup:.1f}x** | **{avg_speedup_full:.1f}x** |\n")
        f.write(f"| Pool medio | {int(np.mean(std_pools))} chunk "
                f"| {int(np.mean(slm_pools))} chunk (-{pool_reduction:.0f}%) "
                f"| {int(np.mean(full_pools))} chunk ({pool_reduction_full:+.0f}%) |\n")
        f.write(f"| Generazione media | {np.mean(std_gens):.0f} ms | {np.mean(slm_gens):.0f} ms | {np.mean(full_gens):.0f} ms |\n")
        f.write(f"| Keyword hit | {np.mean(std_hits):.0f}% | **{np.mean(slm_hits):.0f}%** | {np.mean(full_hits):.0f}% |\n")
        f.write(f"| Overlap medio top-{TOP_K} (Std vs SLM) | {np.mean(overlaps):.0f}% | — | — |\n\n")
        f.write("---\n\n")

        for i, r in enumerate(md_rows, 1):
            f.write(f"## {i}. {r['query_en']}\n\n")
            f.write(f"*{r['query_it']}*\n\n")
            f.write(f"| | StdRAG | SLM-RAG | SLM-Full |\n|---|---|---|---|\n")
            f.write(f"| **Retrieval** | {r['t_ret_std']:.1f} ms | {r['t_ret_slm']:.1f} ms ({r['speedup']:.1f}x) | {r['t_ret_full']:.1f} ms |\n")
            f.write(f"| **Generazione** | {r['t_gen_std']:.0f} ms | {r['t_gen_slm']:.0f} ms | {r['t_gen_full']:.0f} ms |\n")
            f.write(f"| **Totale** | {r['t_ret_std']+r['t_gen_std']:.0f} ms "
                    f"| {r['t_ret_slm']+r['t_gen_slm']:.0f} ms "
                    f"| {r['t_ret_full']+r['t_gen_full']:.0f} ms |\n")
            f.write(f"| **Pool chunk** | {r['pool_std']} | {r['pool_slm']} | {r['pool_full']} |\n")
            f.write(f"| **Keyword hit** | {r['hr_std']:.0f}% | {r['hr_slm']:.0f}% | {r['hr_full']:.0f}% |\n\n")
            f.write(f"### Risposta StdRAG\n\n{r['ans_std']}\n\n")
            f.write(f"### Risposta SLM-RAG\n\n{r['ans_slm']}\n\n")
            f.write(f"### Risposta SLM-Full\n\n{r['ans_full']}\n\n")
            f.write(f"### Ground Truth\n\n{r['ground_truth']}\n\n")
            f.write("---\n\n")

    print(f"\nFile salvato: {OUTPUT_FILE}")

    # ── Salva JSON per evaluate_quality.py ────────────────────────────
    json_path = OUTPUT_FILE.replace(".md", f"_results.json")
    json_data = {
        "metadata": {
            "collections": col_names,
            "model":      GENERATION_MODEL,
            "top_k":      TOP_K,
            "top_n_slm":  TOP_N_SLMS,
        },
        "results": [
            {
                "query_en":     r["query_en"],
                "query_it":     r["query_it"],
                "ground_truth": r["ground_truth"],
                "std": {
                    "chunks":          r["docs_std"],
                    "answer":          r["ans_std"],
                    "t_ret_ms":        r["t_ret_std"],
                    "t_gen_ms":        r["t_gen_std"],
                    "pool":            r["pool_std"],
                    "keyword_hit_pct": r["hr_std"],
                },
                "slm": {
                    "chunks":          r["docs_slm"],
                    "answer":          r["ans_slm"],
                    "t_ret_ms":        r["t_ret_slm"],
                    "t_gen_ms":        r["t_gen_slm"],
                    "pool":            r["pool_slm"],
                    "keyword_hit_pct": r["hr_slm"],
                },
                "full": {
                    "chunks":          r["docs_full"],
                    "answer":          r["ans_full"],
                    "t_ret_ms":        r["t_ret_full"],
                    "t_gen_ms":        r["t_gen_full"],
                    "pool":            r["pool_full"],
                    "keyword_hit_pct": r["hr_full"],
                },
                "overlap_pct": r["overlap"],
                "speedup":     r["speedup"],
            }
            for r in md_rows
        ],
    }
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)
    print(f"JSON salvato:  {json_path}")
    print(f"\nRIEPILOGO")
    print(f"  Speedup retrieval SLM-RAG  : {avg_speedup:.1f}x")
    print(f"  Speedup retrieval SLM-Full : {avg_speedup_full:.1f}x")
    print(f"  Pool medio  StdRAG  : {int(np.mean(std_pools))} chunk")
    print(f"  Pool medio  SLM-RAG : {int(np.mean(slm_pools))} chunk  ({pool_reduction:+.0f}%)")
    print(f"  Pool medio  SLM-Full: {int(np.mean(full_pools))} chunk  ({pool_reduction_full:+.0f}%)")
    print(f"  Generazione StdRAG  : {np.mean(std_gens):.0f} ms")
    print(f"  Generazione SLM-RAG : {np.mean(slm_gens):.0f} ms")
    print(f"  Generazione SLM-Full: {np.mean(full_gens):.0f} ms")
    print(f"  Overlap medio top-{TOP_K}  : {np.mean(overlaps):.0f}%")
    print(f"  Keyword hit StdRAG  : {np.mean(std_hits):.0f}%")
    print(f"  Keyword hit SLM-RAG : {np.mean(slm_hits):.0f}%")
    print(f"  Keyword hit SLM-Full: {np.mean(full_hits):.0f}%")


if __name__ == "__main__":
    main()
