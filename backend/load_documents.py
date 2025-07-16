import os
import json
from pathlib import Path
from typing import List, Dict
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter


RAW_DOCS_DIR = Path("data/raw_docs")
PROCESSED_DIR = Path("data/processed")
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50



def extract_text_from_pdf(pdf_path: Path) -> str:
    reader = PdfReader(str(pdf_path))
    full_text = ""
    for page in reader.pages:
        text = page.extract_text()
        if text:
            full_text += text.strip() + "\n"
    return full_text


def chunk_text(text: str, source_name: str) -> List[Dict]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ".", " "]
    )
    chunks = splitter.split_text(text)
    return [{"content": chunk, "source": source_name} for chunk in chunks]


def process_all_documents():
    all_chunks = []
    for file in RAW_DOCS_DIR.glob("*.pdf"):
        print(f"Processing: {file.name}")
        text = extract_text_from_pdf(file)
        chunks = chunk_text(text, file.stem)
        all_chunks.extend(chunks)

    output_path = PROCESSED_DIR / "legal_chunks.json"
    if all_chunks:
        PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(all_chunks, f, ensure_ascii=False, indent=2)
    print(f"\n✅ Saved {len(all_chunks)} chunks to: {output_path}")


if __name__ == "__main__":
    process_all_documents()