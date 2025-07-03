import faiss
import pickle
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

# Load index
index = faiss.read_index("rag/policy_index.faiss")
with open("rag/policy_texts.pkl", "rb") as f:
    policy_texts = pickle.load(f)

def retrieve_relevant_policies(query, top_k=2):
    embedding = model.encode([query])
    D, I = index.search(embedding, top_k)
    results = [policy_texts[i] for i in I[0]]
    print("📥 RAG Query:", query)
    print("📤 Retrieved:", results)
    return "\n".join(results)
