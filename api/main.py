from fastapi import FastAPI
from pydantic import BaseModel
import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

app = FastAPI()

model = None
index = None
metadata = None


def load_resources():
    global model, index, metadata

    if model is None:
        print("Loading model...")
        model = SentenceTransformer("paraphrase-MiniLM-L3-v2")

    if index is None:
        print("Loading FAISS index...")
        index = faiss.read_index("data/faiss.index")

    if metadata is None:
        print("Loading metadata...")
        with open("data/metadata.pkl", "rb") as f:
            metadata = pickle.load(f)


class QueryRequest(BaseModel):
    query: str


@app.get("/")
def root():
    return {"message": "API running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/recommend")
def recommend(request: QueryRequest):

    load_resources()

    query_embedding = model.encode([request.query])
    query_embedding = np.array(query_embedding).astype("float32")

    distances, indices = index.search(query_embedding, 10)

    results = []

    for idx in indices[0]:
        item = metadata[idx]
        results.append({
            "assessment_name": item["name"],
            "assessment_url": item["url"]
        })

    return {"recommendations": results}