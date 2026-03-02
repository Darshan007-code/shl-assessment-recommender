# SHL Assessment Recommendation System

Semantic search system that recommends SHL assessments from job descriptions.

## Setup

1. Create virtual environment

py -3.11 -m venv venv
venv\Scripts\activate


2. Install dependencies

pip install fastapi uvicorn sentence-transformers faiss-cpu numpy pandas requests streamlit openpyxl tqdm beautifulsoup4


## Rebuild Embeddings

Place `Gen_AI Dataset.xlsx` in project root.

Run:

python embeddings/prepare_data.py
python embeddings/build_index.py


## Run Backend

uvicorn api.main:app --reload


Test:

http://127.0.0.1:8000/health


## Run Frontend

streamlit run frontend/app.py


## Generate Submission

python evaluation/evaluate.py


This generates `submission.csv`.
