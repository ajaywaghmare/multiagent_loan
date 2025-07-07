import faiss
import pickle
import openai
import numpy as np

# Hardcoded OpenAI API key — for local testing only
openai.api_key = "sk-Your-API-KEY"  # Replace with your actual key

# Load FAISS index and chunk texts
index = faiss.read_index("rag/policy_index.faiss")
with open("rag/policy_texts.pkl", "rb") as f:
    policy_texts = pickle.load(f)

def get_openai_embedding(text: str, model: str = "text-embedding-3-small") -> np.ndarray:
    response = openai.embeddings.create(input=[text], model=model)
    embedding = response.data[0].embedding
    return np.array(embedding).astype("float32")

def retrieve_relevant_policies(query, top_k=2):
    embedding = get_openai_embedding(query)
    D, I = index.search(np.array([embedding]), top_k)
    results = [policy_texts[i] for i in I[0]]
    print("RAG Query:", query)
    print("Retrieved:", results)
    return "\n".join(results)