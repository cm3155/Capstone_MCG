


#v4

import pandas as pd
import numpy as np
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# ---- File Selection ----
print("📂 Please select your strategy_data.csv file")
Tk().withdraw()
INPUT_FILE = askopenfilename(title="Select strategy_data.csv")
print(f" Loaded file: {INPUT_FILE}")

# ---- Load + Clean ----
df = pd.read_csv(INPUT_FILE)
df.columns = df.columns.str.strip()

# Rename to standard column format
df = df.rename(columns={
    "Bank Name": "bank_name",
    "File Type": "document_type",
    "Word Count": "word_count"
})

# ---- Assign Base Weights ----
BASE_WEIGHTS = {
    "MD&A": 5,
    "Business Overview": 4,
    "Market Risk": 4,
    "Earnings Call Transcript": 4,
    "Risk Factors": 3,
    "News Article": 2
}
df["base_weight"] = df["document_type"].map(BASE_WEIGHTS)

# ---- Word Count Based Adjustment (only for weight 3 and 4 docs) ----
DOC_TYPE_AVG_LENGTH = {
    "Business Overview": 11038,
    "Market Risk": 7471,
    "Earnings Call Transcript": 11138,
    "Risk Factors": 7249
}
def scale_weight(row):
    if row["base_weight"] not in [3, 4]:
        return row["base_weight"]
    avg = DOC_TYPE_AVG_LENGTH.get(row["document_type"], None)
    if avg is None or row["word_count"] == 0:
        return row["base_weight"]
    ratio = row["word_count"] / avg
    adj = min(max(ratio, 0.5), 1.5)  # cap between 0.5x and 1.5x
    delta = (adj - 1)  # +/- 0.5
    return round(min(5, max(1, row["base_weight"] + delta)), 2)
df["scaled_weight"] = df.apply(scale_weight, axis=1)

# ---- Melt subcategories into long form ----
subcat_cols = ["Data", "Analytics", "Technology", "Analog"]
long_df = df.melt(
    id_vars=["bank_name", "document_type", "word_count", "scaled_weight"],
    value_vars=subcat_cols,
    var_name="subcategory",
    value_name="hits"
)

# Filter for rows where the keyword hit at least once
long_df = long_df[long_df["hits"] > 0]

# ---- Aggregate Score Calculations ----
agg_df = long_df.groupby(["bank_name", "subcategory"]).agg(
    total_hits=("hits", "sum"),
    total_documents=("document_type", "count"),
    raw_base_score=("scaled_weight", lambda x: x.sum())
).reset_index()

# Total weighted score = hits × weight (approximate, more precise logic could be added)
long_df["weighted_score"] = long_df["hits"] * long_df["scaled_weight"]

doc_scores = long_df.groupby(["bank_name", "subcategory"]).agg(
    doc_score=("weighted_score", "sum"),
    total_documents=("document_type", "count")
).reset_index()
doc_scores["doc_normalized_score"] = doc_scores["doc_score"] / doc_scores["total_documents"]

# Merge in
final_df = pd.merge(agg_df, doc_scores, on=["bank_name", "subcategory", "total_documents"])

# ---- Min-Max Normalize Base and Doc-Normalized Scores ----
def normalize(group, colname):
    min_val, max_val = group[colname].min(), group[colname].max()
    if min_val == max_val:
        return pd.Series([3.0] * len(group), index=group.index)
    return ((group[colname] - min_val) / (max_val - min_val)) * 4 + 1

final_df["normalized_base_score"] = final_df.groupby("subcategory", group_keys=False).apply(
    lambda g: normalize(g, "raw_base_score")
)
final_df["normalized_doc_scaled_score"] = final_df.groupby("subcategory", group_keys=False).apply(
    lambda g: normalize(g, "doc_normalized_score")
)

# ---- Add Log & Clipped Scaled Scores (v4 extensions) ----
# Log transform
final_df["log_transformed"] = np.log1p(final_df["doc_normalized_score"])

# Clipped version (95th percentile cap)
final_df["clipped_score"] = final_df.groupby("subcategory")["doc_normalized_score"].transform(
    lambda x: np.minimum(x, x.quantile(0.95))
)

# Normalize both
final_df["log_scaled_score"] = final_df.groupby("subcategory", group_keys=False).apply(
    lambda g: normalize(g, "log_transformed")
)
final_df["clipped_scaled_score"] = final_df.groupby("subcategory", group_keys=False).apply(
    lambda g: normalize(g, "clipped_score")
)

# ---- Export Final ----
OUTPUT_FILE = "v4_scaled_strategic_weighting_output.csv"
final_df.to_csv(OUTPUT_FILE, index=False)
print(f"\n Strategic weighting v4 completed and saved to: {OUTPUT_FILE}")
