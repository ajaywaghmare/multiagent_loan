import os
import faiss
import pickle
from sentence_transformers import SentenceTransformer

# Load policies
with open("rag/policies/loan_policy.txt", "r") as f:
    lines = [line.strip() for line in f.readlines() if line.strip()]

# Embed
model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(lines)

# Create output directory if it doesn't exist
output_dir = "rag"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Create and add to FAISS index
embedding_dim = embeddings[0].shape[0]
index = faiss.IndexFlatL2(embedding_dim)
index.add(embeddings)

# Save index
faiss.write_index(index, os.path.join(output_dir, "policy_index.faiss"))

# Save policy texts
with open(os.path.join(output_dir, "policy_texts.pkl"), "wb") as f:
    pickle.dump(lines, f)

print("✅ FAISS vector index built successfully.")