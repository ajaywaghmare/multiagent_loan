import os
import faiss
import pickle
import openai
from typing import List
import fitz
import numpy as np

openai.api_key = "sk-Your-API-KEY"  # Replace with your actual key


def extract_text_from_pdf(pdf_path: str) -> str:
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks


def get_openai_embeddings(texts: List[str], model: str = "text-embedding-3-small") -> List[List[float]]:
    embeddings = []
    batch_size = 100  # OpenAI supports up to 8192 tokens per request
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        response = openai.embeddings.create(input=batch, model=model)
        batch_embeddings = [item.embedding for item in response.data]
        embeddings.extend(batch_embeddings)
    return embeddings


def build_vector_db_from_texts(texts: List[str], index_path: str, texts_path: str):
    print("Generating OpenAI embeddings...")
    embeddings = get_openai_embeddings(texts)

    dim = len(embeddings[0])
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings).astype("float32"))

    faiss.write_index(index, index_path)
    with open(texts_path, "wb") as f:
        pickle.dump(texts, f)

    print("FAISS index and chunks saved.")


if __name__ == "__main__":
    # Config
    pdf_path = "rag/policies/Loan_Policy_Doc.pdf"
    output_dir = "rag"
    os.makedirs(output_dir, exist_ok=True)

    full_text = extract_text_from_pdf(pdf_path)
    chunks = chunk_text(full_text, chunk_size=500, overlap=50)
    print(f"Extracted {len(chunks)} chunks from PDF")

    build_vector_db_from_texts(
        texts=chunks,
        index_path=os.path.join(output_dir, "policy_index.faiss"),
        texts_path=os.path.join(output_dir, "policy_texts.pkl"),
    )
