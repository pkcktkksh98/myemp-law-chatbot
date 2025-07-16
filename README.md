# 🇲🇾 Malaysian Law RAG Chatbot (Local LLM)

A local Retrieval-Augmented Generation (RAG) chatbot to answer Malaysian law-related questions using:

- 🧠 FAISS + Sentence Transformers for document retrieval
- 🔍 `llama-cpp-python` for local LLM inference (OpenChat model)
- ⚡ FastAPI backend for inference
- 💬 Streamlit frontend UI

---

## 📁 Project Structure

```
project/
├── backend/
│   └── main.py                # FastAPI RAG backend using llama-cpp-python
│
├── vector_store/
│   ├── faiss.index            # FAISS vector index
│   └── metadata.pkl           # Chunk metadata
│
├── model.gguf                 # Local LLaMA model (GGUF format)
├── streamlit_app.py           # Streamlit frontend
├── requirements.txt           # Python dependencies
└── README.md
```

---

## ✅ Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/yourusername/malaysian-law-chatbot.git
cd malaysian-law-chatbot
```

### 2. Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
# or
source venv/bin/activate  # macOS/Linux
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Download GGUF Model (e.g., OpenChat-3.5)

- Download from: https://huggingface.co/TheBloke/OpenChat-3.5-GGUF
- Recommended: `openchat-3.5-0106.Q5_K_M.gguf`
- Place the file in the root as `model.gguf`

---

## 🚀 Running the App

### 1. Start FastAPI Backend (Port 8000)

```bash
uvicorn backend.main:app --reload
```

### 2. Start Streamlit Frontend (Port 8501)

```bash
streamlit run streamlit_app.py
```

---

## 🔗 FastAPI API

### `POST /ask`

Request Body:

```json
{
  "query": "What is the punishment for theft in Malaysian law?",
  "top_k": 3
}
```

Response:

```json
{
  "query": "...",
  "answer": "...",
  "context": ["...", "...", "..."]
}
```

---

## 📋 Requirements

Add these to `requirements.txt`:

```text
faiss-cpu
fastapi
uvicorn
sentence-transformers
llama-cpp-python
streamlit
requests
```

---

## 💡 Example Prompt

> **Question:** What is the punishment for drug possession in Malaysia?

🔎 The app will:
1. Retrieve top `k` relevant law chunks using FAISS
2. Format them into a prompt
3. Send to local LLM via `llama-cpp-python`
4. Display answer + sources

---

## 🛠️ Notes

- Requires a GPU (e.g., RTX 4090) for faster inference with llama-cpp.
- The context length is set to 2048 for now (adjustable).
- Model used is Q5_K quantized OpenChat, but any GGUF model can be swapped in.

---

## 📄 License

MIT License.
