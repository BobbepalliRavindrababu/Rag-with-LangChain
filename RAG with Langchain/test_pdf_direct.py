import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Test the actual vector similarity calculation
model = SentenceTransformer('all-MiniLM-L6-v2')

# Sample texts from a resume
texts = [
    "Software engineer with 5 years of experience in Python and machine learning",
    "Fitness trainer certified in personal training and nutrition"
]

# Create embeddings
embeddings = model.encode(texts, convert_to_numpy=True)
print(f"Embeddings shape: {embeddings.shape}")
print(f"Original embeddings:\n{embeddings}\n")

# Normalize
faiss.normalize_L2(embeddings)
print(f"Normalized embeddings:\n{embeddings}\n")

# Create index with Inner Product
dimension = embeddings.shape[1]
index = faiss.IndexFlatIP(dimension)
index.add(embeddings.astype('float32'))
print(f"Created IndexFlatIP with dimension {dimension}")

# Test query
query = "what is this document about?"
query_embedding = model.encode([query], convert_to_numpy=True)
print(f"\nQuery embedding (before norm): {query_embedding}")

faiss.normalize_L2(query_embedding)
print(f"Query embedding (after norm): {query_embedding}")

# Search
scores, indices = index.search(query_embedding.astype('float32'), 2)
print(f"\nSearch results:")
print(f"Scores: {scores}")
print(f"Indices: {indices}")

for i, (idx, score) in enumerate(zip(indices[0], scores[0])):
    print(f"  Result {i+1}: idx={idx}, score={score:.4f}, text='{texts[idx]}'")
