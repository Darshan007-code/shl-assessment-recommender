import streamlit as st
import pandas as pd

st.title("SHL Assessment Recommendation System")

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

user_query = st.text_area("Enter Job Description")

if st.button("Recommend"):

    q = user_query.lower()
    results = []

    for item in records:
        if any(word in item["query"] for word in q.split()):
            results.append(item["url"])

    st.subheader("Recommended Assessments")

    for r in results[:10]:
        st.write(r)