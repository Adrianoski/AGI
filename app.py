import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from chunking import process_pdf
from router import assign_chunks, load_registry, merge_close_slms
import chromadb
from sentence_transformers import SentenceTransformer
import gradio as gr
import json

embedding_model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")
chroma_client = chromadb.PersistentClient(path="./chroma_db")

CHUNK_SIZE = 2000
OVERLAP = 150


def get_registry_display() -> str:
    registry = load_registry()
    if not registry:
        return "Registry vuoto."
    lines = []
    for slm_name, entry in registry.items():
        centroid_preview = [round(v, 4) for v in entry["centroid"][:4]]
        lines.append(
            f"{slm_name}\n"
            f"  chunks  : {entry['chunk_count']}\n"
            f"  centroid: [{', '.join(str(v) for v in centroid_preview)}, ...]\n"
            f"  json    : {entry['chunks_json']}\n"
        )
    return "\n".join(lines)


def get_collections():
    return [c.name for c in chroma_client.list_collections()]


def upload_and_chunk(pdf_file, collection_name):
    if pdf_file is None:
        return "Nessun file caricato.", "", gr.update(choices=get_collections()), get_registry_display()
    if not collection_name.strip():
        return "Inserisci un nome per la collection.", "", gr.update(choices=get_collections()), get_registry_display()

    collection = chroma_client.get_or_create_collection(collection_name.strip())
    chunks = process_pdf(
        pdf_path=pdf_file,
        collection=collection,
        embedding_model=embedding_model,
        chunk_size=CHUNK_SIZE,
        overlap=OVERLAP
    )

    assignments = assign_chunks(chunks, embedding_model, threshold=0.65)
    merges = merge_close_slms(threshold=0.70)

    merge_line = f"\n{len(merges)} SLM uniti per prossimità." if merges else ""
    summary = (
        f"{len(chunks)} chunk salvati nella collection '{collection_name}'.\n"
        f"{len(assignments)} SLM aggiornati nel registry.{merge_line}"
    )
    preview_data = [
        {"id": c["id"][:8] + "...", "chapter": c["chapter"], "text": c["text"][:130] + "..."}
        for c in chunks[:5]
    ]
    preview = json.dumps(preview_data, indent=2, ensure_ascii=False)
    return summary, preview, gr.update(choices=get_collections()), get_registry_display()


CSS = """
@import url('https://fonts.googleapis.com/css2?family=Lora:wght@400;500;600&family=DM+Sans:wght@300;400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; }

body, .gradio-container {
    background: #f5f0e8 !important;
    color: #2e2b26 !important;
    font-family: 'DM Sans', sans-serif !important;
    min-height: 100vh;
}

.gradio-container {
    max-width: 780px !important;
    min-width: 640px !important;
    margin: 0 auto !important;
    padding: 52px 48px !important;
}

#card {
    background: #fdfaf4;
    border: 1px solid #e8e0d0;
    border-radius: 16px;
    padding: 44px 48px;
    box-shadow: 0 4px 32px rgba(100,85,60,0.07), 0 1px 4px rgba(100,85,60,0.05);
}

#hdr {
    margin-bottom: 36px;
}

#hdr h1 {
    font-family: 'Lora', serif !important;
    font-size: 1.65rem !important;
    font-weight: 600 !important;
    color: #2e2b26 !important;
    letter-spacing: -0.01em;
    margin: 0 0 6px 0 !important;
    line-height: 1.2;
}

#hdr p {
    font-size: 0.8rem;
    color: #9c9184;
    letter-spacing: 0.04em;
    margin: 0;
    font-weight: 300;
}

.block, .gr-box, .gr-form {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
}

label > span {
    font-family: 'DM Sans', sans-serif !important;
    color: #7a7268 !important;
    font-size: 0.72rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.07em !important;
    text-transform: uppercase !important;
    margin-bottom: 6px !important;
    display: block;
}

input[type=text] {
    background: #f5f0e8 !important;
    border: 1px solid #ddd5c4 !important;
    color: #2e2b26 !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
    padding: 11px 14px !important;
    transition: border-color 0.18s ease, box-shadow 0.18s ease !important;
}

input[type=text]:focus {
    border-color: #b5a98a !important;
    box-shadow: 0 0 0 3px rgba(181,169,138,0.15) !important;
    outline: none !important;
}

.upload-button, .file-preview, [data-testid="file-upload"] {
    background: #f5f0e8 !important;
    border: 1.5px dashed #cfc5b0 !important;
    border-radius: 12px !important;
    color: #9c9184 !important;
    transition: border-color 0.18s ease !important;
    min-height: 100px !important;
}

.upload-button:hover {
    border-color: #b5a98a !important;
}

button.primary {
    background: #5c7a5c !important;
    border: none !important;
    color: #f5f0e8 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.06em !important;
    border-radius: 10px !important;
    padding: 13px 0 !important;
    width: 100% !important;
    cursor: pointer !important;
    transition: background 0.2s ease, transform 0.12s ease, box-shadow 0.2s ease !important;
    box-shadow: 0 2px 12px rgba(92,122,92,0.18) !important;
    margin-top: 8px !important;
}

button.primary:hover {
    background: #4d6b4d !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 18px rgba(92,122,92,0.25) !important;
}

button.primary:active {
    transform: translateY(0) !important;
}

#status textarea {
    background: #eef4ee !important;
    border: 1px solid #c8d8c8 !important;
    color: #3d6b3d !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.84rem !important;
    font-weight: 400 !important;
    padding: 10px 14px !important;
}

#preview textarea {
    background: #f5f0e8 !important;
    border: 1px solid #ddd5c4 !important;
    color: #7a7268 !important;
    border-radius: 10px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.72rem !important;
    line-height: 1.7 !important;
    padding: 12px 14px !important;
}

.gr-dropdown select, select {
    background: #f5f0e8 !important;
    border: 1px solid #ddd5c4 !important;
    color: #2e2b26 !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.85rem !important;
    padding: 10px 14px !important;
}

.divider {
    border: none;
    border-top: 1px solid #e8e0d0;
    margin: 28px 0;
}

footer { display: none !important; }

#registry textarea {
    background: #f5f0e8 !important;
    border: 1px solid #ddd5c4 !important;
    color: #5a4a2a !important;
    border-radius: 10px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.72rem !important;
    line-height: 1.7 !important;
    padding: 12px 14px !important;
}

"""

with gr.Blocks(
    title="PDF Ingestion",
    theme=gr.themes.Base(
        primary_hue="green",
        neutral_hue="stone",
        font=[gr.themes.GoogleFont("DM Sans"), "sans-serif"],
    ),
    css=CSS
) as demo:

    with gr.Column(elem_id="card"):
        with gr.Column(elem_id="hdr"):
            gr.HTML(
                "<h1>PDF Ingestion</h1>"
                "<p>Carica un documento PDF per avviare il processo di chunking e indicizzazione</p>"
            )

        pdf_input = gr.File(
            label="Documento PDF",
            file_types=[".pdf"],
            type="filepath"
        )

        collection_input = gr.Textbox(
            label="Nome Collection",
            placeholder="es. slm_propulsion"
        )

        run_btn = gr.Button("Avvia Chunking", variant="primary")

        gr.HTML('<hr class="divider">')

        status_out = gr.Textbox(
            label="Stato",
            interactive=False,
            elem_id="status"
        )

        preview_out = gr.Textbox(
            label="Anteprima — primi 5 chunk",
            lines=10,
            interactive=False,
            elem_id="preview"
        )

        collections_out = gr.Dropdown(
            label="Collection in ChromaDB",
            choices=get_collections(),
            interactive=False
        )

        gr.HTML('<hr class="divider">')

        registry_out = gr.Textbox(
            label="Registry SLM",
            lines=10,
            interactive=False,
            elem_id="registry"
        )

    run_btn.click(
        fn=upload_and_chunk,
        inputs=[pdf_input, collection_input],
        outputs=[status_out, preview_out, collections_out, registry_out]
    )

if __name__ == "__main__":
    # startup_merges = merge_close_slms(threshold=0.70)
    # if startup_merges:
    #     print(f"[startup] Merge SLM: {len(startup_merges)} unioni eseguite")
    #     for m in startup_merges:
    #         print(f"  {m['removed']} → {m['kept']}  (sim={m['similarity']})")
    demo.launch(server_name="0.0.0.0", server_port=7860)