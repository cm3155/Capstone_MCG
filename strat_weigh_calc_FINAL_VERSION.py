
# Final Strategic Weighing Calculator

import pandas as pd

# SETTINGS
BASE_WEIGHTS = {
    "MD&A": 5,
    "Business Overview": 4,
    "Earnings Call Transcript": 4,
    "Risk Factors": 3,
    "Market Risk": 3,
    "News Article": 2
}

# Define document type average word counts for scaling
DOC_TYPE_AVG_WORDS = {
    "Business Overview": 11038,
    "Earnings Call Transcript": 11138,
    "Risk Factors": 7249,
    "Market Risk": 7471
}

# Load strategy input file
df = pd.read_csv("strategy_data.csv")

# Assign base weight to each document
df["base_weight"] = df["document_type"].map(BASE_WEIGHTS)

# Adjust weight based on word count only for medium importance docs (3 or 4)
def scale_weight(row):
    doc_type = row["document_type"]
    base_weight = row["base_weight"]
    if base_weight in [3, 4] and doc_type in DOC_TYPE_AVG_WORDS:
        avg_words = DOC_TYPE_AVG_WORDS[doc_type]
        scale = avg_words / max(row["word_count"], 1)
        scale = min(max(scale, 0.5), 1.5)
        adjusted_weight = base_weight * scale
        return min(max(adjusted_weight, base_weight - 1), base_weight + 1)
    else:
        return base_weight

df["scaled_weight"] = df.apply(scale_weight, axis=1)

# Calculate raw scores
df["raw_base_score"] = df["total_hits"] * df["base_weight"]
df["raw_scaled_score"] = df["total_hits"] * df["scaled_weight"]

# Group by bank and subcategory
grouped = df.groupby(["bank_name", "subcategory"]).agg({
    "total_hits": "sum",
    "raw_base_score": "sum",
    "raw_scaled_score": "sum",
    "document_type": "count"
}).reset_index().rename(columns={"document_type": "total_documents"})

# Normalize raw scores per subcategory to 1–5 scale
def minmax_normalize(series):
    return 1 + 4 * (series - series.min()) / (series.max() - series.min())

grouped["normalized_base_score"] = grouped.groupby("subcategory")["raw_base_score"].transform(minmax_normalize)
grouped["normalized_scaled_score"] = grouped.groupby("subcategory")["raw_scaled_score"].transform(minmax_normalize)

# Save final output
grouped.to_csv("/mnt/data/strategic_weighting_output_FIXED.csv", index=False)
print("✅ Strategic weighting output saved to: strategic_weighting_output_FIXED.csv")
