import uuid
import re
from typing import List, Dict
from pathlib import Path

import fitz
import chromadb
from sentence_transformers import SentenceTransformer


def extract_chapters(pdf_path: str) -> List[Dict[str, str]]:
    doc = fitz.open(pdf_path)
    full_text = "\n".join(page.get_text() for page in doc)
    doc.close()

    chapter_pattern = re.compile(
        r'(?m)^(Chapter\s+\d+[^\n]*|CHAPTER\s+\d+[^\n]*|\d+\.\s+[A-Z][^\n]{3,})',
    )

    matches = list(chapter_pattern.finditer(full_text))
    if not matches:
        return [{"chapter": "Document", "text": full_text.strip()}]

    chapters = []
    for i, match in enumerate(matches):
        title = match.group(0).strip()
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(full_text)
        text = full_text[start:end].strip()
        if text:
            chapters.append({"chapter": title, "text": text})

    return chapters


def chunk_chapter(chapter: Dict[str, str], chunk_size: int = 1000, overlap: int = 100) -> List[Dict[str, str]]:
    text = chapter["text"]
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append({
            "chapter": chapter["chapter"],
            "text": text[start:end].strip()
        })
        start += chunk_size - overlap
    return chunks


def process_pdf(
    pdf_path: str,
    collection: chromadb.Collection,
    embedding_model: SentenceTransformer,
    chunk_size: int = 1000,
    overlap: int = 100
) -> List[Dict]:
    chapters = extract_chapters(pdf_path)

    raw_chunks = []
    for chapter in chapters:
        raw_chunks.extend(chunk_chapter(chapter, chunk_size, overlap))

    chunks = []
    for raw in raw_chunks:
        chunk_id = str(uuid.uuid4())
        embedding = embedding_model.encode(
            [raw["text"]], normalize_embeddings=True, convert_to_numpy=True
        )[0].tolist()

        chunk = {
            "id": chunk_id,
            "text": raw["text"],
            "chapter": raw["chapter"],
            "embedding": embedding
        }
        chunks.append(chunk)

    collection.add(
        ids=[c["id"] for c in chunks],
        embeddings=[c["embedding"] for c in chunks],
        documents=[c["text"] for c in chunks],
        metadatas=[{"chapter": c["chapter"]} for c in chunks]
    )

    return chunks