
#Step 3 of 3 Part Process:
#1. Grab metadata of each document
#2. exploratory, checks word count for potential normalization by doc word count length
#3. applies weighting rubric, calculates by strategic weights
#

#Not run yet because need to finish presence code first


import pandas as pd
import os

# -------- SETTINGS --------
MODE = "length_inverse"  # options: "length_inverse" or "density"
BASE_WEIGHTS = {
    "MD&A": 5,
    "Business Overview": 4,
    "Earnings Call Transcript": 3.5,
    "Risk Factors": 2.5,
    "Market Risk": 2,
    "News Article": 2
}
OUTPUT_FILE = "strategic_weighting_output.csv"

# -------- LOAD FILES --------
metadata_df = pd.read_csv("document_metadata_with_normalized.csv")
presence_df = pd.read_csv("presence_output.csv")  # You’ll plug in the real one later

# -------- CLEAN / PREP PRESENCE FILE --------
# Expecting: keyword, bank_name, document_id, document_type, subcategory, num_hits
presence_df["document_id"] = presence_df["document_id"].astype(str)
metadata_df["document_id"] = metadata_df["document_id"].astype(str)

# Merge presence and metadata
df = pd.merge(presence_df, metadata_df, on=["document_id", "bank_name", "document_type"], how="left")

# -------- ASSIGN STRATEGIC WEIGHTS --------

def calculate_effective_weight(row):
    base_weight = BASE_WEIGHTS.get(row["document_type"], 2)

    if MODE == "length_inverse":
        multiplier = 1 / row["within_type_normalized"] if row["within_type_normalized"] > 0 else 1
    elif MODE == "density":
        multiplier = row["num_hits"] / row["word_count"] if row["word_count"] > 0 else 0
    else:
        multiplier = 1  # fallback

    effective_weight = base_weight * multiplier
    return min(max(effective_weight, 1), 5)  # Clip between 1 and 5

df["strategic_weighting_score"] = df.apply(calculate_effective_weight, axis=1)

# -------- OUTPUT --------
df[[
    "bank_name",
    "document_id",
    "document_type",
    "subcategory",
    "keyword",
    "num_hits",
    "word_count",
    "within_type_normalized",
    "strategic_weighting_score"
]].to_csv(OUTPUT_FILE, index=False)

print(f" Strategic weighting calculation complete using mode: {MODE}")
print(f" Output saved to: {OUTPUT_FILE}")
