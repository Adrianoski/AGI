# AGI
AGI is not an LLM (e fino a qui, siamo tutti d'accordo)

## Avvio

**Ingestion UI**
```bash
pip install gradio sentence-transformers chromadb pymupdf
python app.py
```
Apri `http://localhost:7860`, carica un PDF e assegna un nome alla collection.

**Visualizzatore vettori**
```bash
python extract_vectors.py --method pca
```
Poi apri `visualizer.html` direttamente nel browser, carica `vectors.json`.
