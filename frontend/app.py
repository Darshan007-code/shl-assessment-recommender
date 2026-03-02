import streamlit as st
import pandas as pd

st.set_page_config(page_title="SHL Assessment Recommender")

st.title("SHL Assessment Recommendation System")

st.markdown(
    "Enter a **Job Role or Description** and receive the most relevant SHL assessments."
)

# Load dataset
data = pd.read_excel("Gen_AI Dataset.xlsx", sheet_name="Train-Set")

records = []

for _, row in data.iterrows():
    job_description = str(row["Query"])
    urls = str(row["Assessment_url"]).split(",")

    for url in urls:
        records.append({
            "job": job_description,
            "query": job_description.lower(),
            "url": url.strip()
        })

# User Input
user_query = st.text_area("Job Description", height=150)

if st.button("Get Recommendations"):

    if not user_query.strip():
        st.warning("Please enter a job description.")
    else:

        st.subheader("Entered Job Description")
        st.write(user_query)

        q = user_query.lower()
        results = []

        for item in records:
            if any(word in item["query"] for word in q.split()):
                results.append(item)

        st.subheader("Recommended SHL Assessments")

        if results:

            for idx, rec in enumerate(results[:10], 1):

                st.markdown("---")

                # Assessment Title
                st.markdown(f"### {idx}. {rec['job']}")

                # Role Description
                st.markdown(
                    f"**Role / Job Description:** {rec['job']}"
                )

                # Clickable Link
                st.markdown(
                    f"🔗 [Open SHL Assessment]({rec['url']})"
                )

        else:
            st.info("No matching assessments found.")