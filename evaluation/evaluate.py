import pandas as pd
import requests

API_URL = "http://127.0.0.1:8000/recommend"
DATA_PATH = "Gen_AI Dataset.xlsx"
OUTPUT_CSV = "submission.csv"


def get_recommendations(query):

    response = requests.post(
        API_URL,
        json={"query": query}
    )

    data = response.json()

    return [
        r["assessment_url"]
        for r in data["recommendations"]
    ]


print("Loading dataset...")

test_df = pd.read_excel(DATA_PATH, sheet_name="Test-Set")

submission_rows = []

for _, row in test_df.iterrows():

    query = row["Query"]

    predicted = get_recommendations(query)

    for url in predicted:
        submission_rows.append({
            "Query": query,
            "Assessment_url": url
        })

submission = pd.DataFrame(submission_rows)

submission.to_csv(OUTPUT_CSV, index=False)

print("Submission file saved:", OUTPUT_CSV)