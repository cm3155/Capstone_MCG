
#Step 3 of 3 Part Process:
#1. Grab metadata of each document
#2. exploratory, checks word count for potential normalization by doc word count length
#3. applies weighting rubric, calculates by strategic weights
#

#Not run yet because need to finish presence code first


import pandas as pd
import os

# ------------ SETTINGS ------------
MODE = "length_inverse"  # or "none" to turn off scaling

BASE_WEIGHTS = {
    "MD&A": 5,
    "Business Overview": 4,
    "Earnings Call Transcript": 4,
    "Risk Factors": 3,
    "Market Risk": 4,
    "News Article": 2
}

SCALABLE_TYPES = {"Business Overview", "Market Risk", "Earnings Call Transcript", "Risk Factors"}

AVG_WORD_COUNTS = {
    "MD&A": 24168,
    "Business Overview": 11038,
    "Earnings Call Transcript": 11138,
    "Risk Factors": 7249,
    "Market Risk": 7471,
    "News Article": 1911
}

INPUT_FILE = "strategy_data.csv"  # Path to your local CSV
OUTPUT_FILE = "strategic_weighting_output.csv"

# ------------ LOAD & PREP INPUT ------------
df = pd.read_csv(INPUT_FILE).rename(columns={
    "Bank Name": "bank_name",
    "File Type": "document_type",
    "Word Count": "word_count"
})

# Melt subcategory columns into rows
subcategory_cols = ["Data", "Analytics", "Technology", "Analog"]
df = df.melt(
    id_vars=["ID", "bank_name", "document_type", "word_count", "Text Content"],
    value_vars=subcategory_cols,
    var_name="subcategory",
    value_name="num_hits"
)

df = df[df["num_hits"] > 0]  # Remove rows with no keyword hits

# ------------ CALCULATE WEIGHTS ------------
df["base_weight"] = df["document_type"].map(BASE_WEIGHTS).fillna(2)
df["avg_doc_length"] = df["document_type"].map(AVG_WORD_COUNTS)
df["within_type_normalized"] = df["word_count"] / df["avg_doc_length"]

def calc_scaled_weight(row):
    base = row["base_weight"]
    if MODE == "length_inverse" and row["document_type"] in SCALABLE_TYPES and row["within_type_normalized"] > 0:
        scaled = base * (1 / row["within_type_normalized"])
        return min(max(scaled, base - 0.99), base + 0.99)
    return base

df["scaled_weight"] = df.apply(calc_scaled_weight, axis=1)

# ------------ CALCULATE SCORES ------------
df["base_contribution"] = df["num_hits"] * df["base_weight"]
df["scaled_contribution"] = df["num_hits"] * df["scaled_weight"]

# Count number of documents per bank × subcategory
doc_counts = df.groupby(["bank_name", "subcategory"])["ID"].nunique().reset_index(name="total_documents")

# Aggregate results
grouped = df.groupby(["bank_name", "subcategory"]).agg(
    total_hits=("num_hits", "sum"),
    raw_base_score=("base_contribution", "sum"),
    raw_scaled_score=("scaled_contribution", "sum")
).reset_index()

# Merge document counts
grouped = grouped.merge(doc_counts, on=["bank_name", "subcategory"], how="left")

# Normalize to 1–5 scale per subcategory
def normalize(col):
    return 1 + 4 * (col - col.min()) / (col.max() - col.min()) if col.max() > col.min() else 3

grouped["normalized_base_score"] = grouped.groupby("subcategory")["raw_base_score"].transform(normalize)
grouped["normalized_scaled_score"] = grouped.groupby("subcategory")["raw_scaled_score"].transform(normalize)

# ------------ SAVE OUTPUT ------------
grouped.to_csv(OUTPUT_FILE, index=False)
print(f" Strategic weighing output saved to: {OUTPUT_FILE}")


# --- DEBUG SCALING COMPARISON + VISUALIZATION ---
import matplotlib.pyplot as plt
import seaborn as sns

# Compare scaled vs base raw + normalized scores using the grouped output
debug_df = grouped.copy()
debug_df["score_diff"] = debug_df["raw_scaled_score"] - debug_df["raw_base_score"]
debug_df["norm_diff"] = debug_df["normalized_scaled_score"] - debug_df["normalized_base_score"]

# Filter rows with meaningful differences (epsilon > 0.01)
scaling_debug = debug_df[(debug_df["score_diff"].abs() > 0.01) | (debug_df["norm_diff"].abs() > 0.01)]

# Show a few rows in console
print("\n🔍 Scaling Differences Detected (raw or normalized > 0.01):")
print(scaling_debug[["bank_name", "subcategory", "raw_base_score", "raw_scaled_score", "score_diff",
                     "normalized_base_score", "normalized_scaled_score", "norm_diff"]].head(10))

# Save to CSV
scaling_debug.to_csv("scaling_debug_check.csv", index=False)

# Plot histogram of raw score differences
plt.figure(figsize=(10, 6))
sns.histplot(debug_df["score_diff"], bins=20, kde=True)
plt.title("Histogram of Raw Scaled Score - Base Score")
plt.xlabel("Score Difference")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("score_diff_histogram.png")
plt.close()

# Plot histogram of normalized score differences
plt.figure(figsize=(10, 6))
sns.histplot(debug_df["norm_diff"], bins=20, kde=True, color="orange")
plt.title("Histogram of Normalized Scaled Score - Base Score")
plt.xlabel("Normalized Score Difference")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("normalized_score_diff_histogram.png")
plt.close()
