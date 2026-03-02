import pandas as pd
import json

print("Loading Excel dataset...")

DATA_PATH = "Gen_AI Dataset.xlsx"

train_df = pd.read_excel(DATA_PATH, sheet_name="Train-Set")

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

print("Total records created:", len(records))

with open("data/processed_catalog.json", "w", encoding="utf-8") as f:
    json.dump(records, f, indent=2)

print("Processed dataset saved.")