from fastapi import FastAPI
from pydantic import BaseModel
import faiss
import pickle
import numpy as np
import json
import os
from sentence_transformers import SentenceTransformer

app = FastAPI()

model = None
index = None
metadata = None


def build_index_if_missing():
    if not os.path.exists("data"):
        os.makedirs("data")

    if not os.path.exists("data/faiss.index"):

        print("Index not found. Rebuilding...")

        with open("Gen_AI Dataset.xlsx", "rb"):
            pass

        import pandas as pd
        train_df = pd.read_excel("Gen_AI Dataset.xlsx", sheet_name="Train-Set")

        records = []

        for _, row in train_df.iterrows():
            query = str(row["Query"])
            urls = str(row["Assessment_url"]).split(",")

            for url in urls:
                records.append({
                    "name": query,
                    "url": url.strip(),
                    "text": query
                })

        texts = [item["text"] for item in records]

        global model
        if model is None:
            model = SentenceTransformer("paraphrase-MiniLM-L3-v2")

        embeddings = model.encode(texts)
        embeddings = np.array(embeddings).astype("float32")

        dimension = embeddings.shape[1]
        idx = faiss.IndexFlatL2(dimension)
        idx.add(embeddings)

        faiss.write_index(idx, "data/faiss.index")

        with open("data/metadata.pkl", "wb") as f:
            pickle.dump(records, f)


def load_resources():
    global model, index, metadata

    if model is None:
        model = SentenceTransformer("paraphrase-MiniLM-L3-v2")

    build_index_if_missing()

    if index is None:
        index = faiss.read_index("data/faiss.index")

    if metadata is None:
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