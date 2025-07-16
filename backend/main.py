from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import faiss
import pickle
from sentence_transformers import SentenceTransformer
from llama_cpp import Llama
from pathlib import Path

# --- Configuration ---
INDEX_PATH = Path("backend/vector_store/faiss.index")
METADATA_PATH = Path("backend/vector_store/metadata.pkl")
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
LLM_PATH = "model.gguf"
TOP_K = 3

# --- Load Components ---
print("🔁 Loading FAISS index and metadata...")
index = faiss.read_index(str(INDEX_PATH))
with open(METADATA_PATH, "rb") as f:
    metadata = pickle.load(f)

print(f"🧠 Loading embedding model: {EMBED_MODEL}")
embedder = SentenceTransformer(EMBED_MODEL)

print(f"🚀 Loading local GGUF model: {LLM_PATH}")
llm = Llama(
    model_path=LLM_PATH,
    n_ctx=2048,
    n_threads=8,
    n_gpu_layers=-1,
    chat_format="llama-2"
)

# --- FastAPI App ---
app = FastAPI()


class QuestionRequest(BaseModel):
    query: str
    top_k: int = TOP_K


def get_top_chunks(query: str, top_k: int) -> List[str]:
    embedding = embedder.encode([query])
    scores, indices = index.search(embedding, top_k)
    return [metadata[i]["content"] for i in indices[0]]


def build_prompt(context_chunks: List[str], query: str) -> str:
    context = "/n/n".join(context_chunks)
    prompt = (
        "Answer the following question based on the provided Malaysian employment law context:/n/n"
        f"Context:/n{context}/n/n"
        f"Question:/n{query}/n/n"
        "Answer:"
    )
    return prompt


@app.post("/ask")
async def ask_question(request: QuestionRequest):
    context_chunks = get_top_chunks(request.query, request.top_k)
    prompt = build_prompt(context_chunks, request.query)

    output = llm(prompt, max_tokens=512, stop=["User:", "Question:"], echo=False)
    answer = output["choices"][0]["text"].strip()

    return {
        "query": request.query,
        "answer": answer,
        "context": context_chunks
    }
