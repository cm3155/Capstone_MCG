#Step 2 of 3 Part Process:
#1. Grab metadata of each document
#2. exploratory, checks word count for potential normalization by doc word count length
#3. applies weighting rubric, calculates by strategic weights
#

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Load metadata
df = pd.read_csv("document_metadata.csv")
OUTPUT_DIR = "."  # Save to current repo folder

# Normalize word counts
overall_mean = df["word_count"].mean()
df["global_normalized"] = df["word_count"] / overall_mean
df["within_type_normalized"] = df.groupby("document_type")["word_count"].transform(lambda x: x / x.mean())

# ---- Generate One Combined Summary Table ----
summary = df.groupby("document_type").agg(
    doc_count=('word_count', 'count'),
    min_word_count=('word_count', 'min'),
    q1_word_count=('word_count', lambda x: x.quantile(0.25)),
    median_word_count=('word_count', 'median'),
    q3_word_count=('word_count', lambda x: x.quantile(0.75)),
    max_word_count=('word_count', 'max'),
    mean_word_count=('word_count', 'mean'),
    std_word_count=('word_count', 'std'),
    global_normalized_mean=('global_normalized', 'mean'),
    within_type_normalized_mean=('within_type_normalized', 'mean')
).reset_index()

# Save full combined CSV
summary_file = os.path.join(OUTPUT_DIR, "document_type_summary.csv")
summary.to_csv(summary_file, index=False)

# Save updated version of metadata with normalized columns
df.to_csv(os.path.join(OUTPUT_DIR, "document_metadata_with_normalized.csv"), index=False)

# ---- Create and Save Boxplot ----
plt.figure(figsize=(12, 6))
sns.boxplot(data=df, x="document_type", y="word_count")
plt.xticks(rotation=45)
plt.title("Document Length by Type (Word Count)")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "word_count_by_type.png"))
plt.show()

print(" EDA complete. Saved:")
print(f"-  Summary CSV: {summary_file}")
print(f"-  Full metadata: document_metadata_with_normalized.csv")
print(f"-  Plot: word_count_by_type.png")
