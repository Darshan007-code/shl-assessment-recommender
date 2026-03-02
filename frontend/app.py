import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/recommend"

st.title("SHL Assessment Recommendation System")

query = st.text_area("Enter Job Description")

if st.button("Get Recommendations"):

    if query.strip() == "":
        st.warning("Please enter a query.")
    else:
        response = requests.post(
            API_URL,
            json={"query": query}
        )

        data = response.json()

        st.subheader("Recommended Assessments")

        for r in data["recommendations"]:
            st.markdown(
                f"- [{r['assessment_name']}]({r['assessment_url']})"
            )