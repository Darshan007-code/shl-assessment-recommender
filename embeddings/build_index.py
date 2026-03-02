import json
import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

print("Loading processed dataset...")

with open("data/processed_catalog.json", "r", encoding="utf-8") as f:
    data = json.load(f)

texts = [item["text"] for item in data]

print("Loading embedding model...")
model = SentenceTransformer("paraphrase-MiniLM-L3-v2")

print("Generating embeddings...")
embeddings = model.encode(texts)

embeddings = np.array(embeddings).astype("float32")

dimension = embeddings.shape[1]

print("Building FAISS index...")
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

faiss.write_index(index, "data/faiss.index")

with open("data/metadata.pkl", "wb") as f:
    pickle.dump(data, f)

print("Index built successfully.")
print("Total vectors stored:", index.ntotal)