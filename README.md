# 🇲🇾 Malaysian Law RAG Chatbot (Local LLM)

A local Retrieval-Augmented Generation (RAG) chatbot that answers legal questions based on:

- 📘 **Employment Act 1955 (Act 265)** — Reprint as at 1 August 2023  
- 📕 **Employment (Amendment) Act 2022 (Act A1651)**

---

## 🧠 Architecture

This chatbot uses:

- **FAISS** + **Sentence Transformers** to retrieve relevant law sections  
- **Local LLM** via `llama-cpp-python` for offline inference (e.g., OpenChat GGUF)  
- **FastAPI** as backend API  
- **Streamlit** as the user interface

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
git clone https://github.com/pkcktkksh98/myemp-law-chatbot.git
cd myemp-law-chatbot
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
## 📚 Run `rag_pipeline()`

### 4. Build Vector Store with FAISS

```python
python backend/rag_pipeline.py
```

✅ This creates:
- `vector_store/faiss.index`
- `vector_store/metadata.pkl`

---
### 5. Download GGUF Model (e.g., OpenChat-3.5)

- Download from: [TheBloke/openchat-3.5-0106-GGUF](https://huggingface.co/TheBloke/openchat-3.5-0106-GGUF)
- Recommended: [`openchat-3.5-0106.Q5_K_M.gguf`](https://huggingface.co/TheBloke/openchat-3.5-0106-GGUF/blob/main/openchat-3.5-0106.Q5_K_M.gguf)
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
  "query": "What is the Employment Act 1955?",
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
