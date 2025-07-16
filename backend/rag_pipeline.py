import os
import json
import faiss
import pickle
from pathlib import Path
from sentence_transformers import SentenceTransformer

# Paths
PROCESSED_FILE = Path("data/processed/legal_chunks.json")
INDEX_DIR = Path("vector_store/")
INDEX_PATH = INDEX_DIR / "faiss.index"
METADATA_PATH = INDEX_DIR / "metadata.pkl"

# Embedding model
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def embed_chunks(chunks, model):
    texts = [chunk["content"] for chunk in chunks]
    embeddings = model.encode(texts, show_progress_bar=True, convert_to_numpy=True)
    return embeddings


def build_vector_store():
    print("🔍 Loading chunks...")
    with open(PROCESSED_FILE, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    print(f"🧠 Loading embedding model: {EMBED_MODEL}")
    model = SentenceTransformer(EMBED_MODEL)

    print(f"📈 Embedding {len(chunks)} chunks...")
    embeddings = embed_chunks(chunks, model)

    print("💾 Building FAISS index...")
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    faiss.write_index(index, str(INDEX_PATH))

    with open(METADATA_PATH, "wb") as f:
        pickle.dump(chunks, f)

    print(f"\n✅ FAISS index saved to: {INDEX_PATH}")
    print(f"✅ Metadata saved to: {METADATA_PATH}")


if __name__ == "__main__":
    build_vector_store()
