from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd

app = FastAPI()

print("Loading dataset...")

data = pd.read_excel("Gen_AI Dataset.xlsx", sheet_name="Train-Set")

records = []

for _, row in data.iterrows():
    query = str(row["Query"])
    urls = str(row["Assessment_url"]).split(",")

    for url in urls:
        records.append({
            "query": query.lower(),
            "url": url.strip()
        })


class QueryRequest(BaseModel):
    query: str


@app.get("/")
def root():
    return {"message": "SHL API running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/recommend")
def recommend(request: QueryRequest):

    q = request.query.lower()
    results = []

    for item in records:
        if any(word in item["query"] for word in q.split()):
            results.append({
                "assessment_name": item["query"],
                "assessment_url": item["url"]
            })

    return {"recommendations": results[:10]}