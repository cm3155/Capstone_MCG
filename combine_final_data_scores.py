# combine_final_data_scores.py

import pandas as pd
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# ========== SETTINGS ==========
# You can update these weights
PRESENCE_WEIGHT = 0.4
MATURITY_WEIGHT = 0.4
STRATEGIC_WEIGHT = 0.2

# Default file paths (update if using local default mode)
PRESENCE_PATH = "bank_keyword_scores_scaled.csv"
MATURITY_PATH = "maturity_scores.xlsx"
STRATEGIC_PATH = "v4_scaled_strategic_weighting_output.csv"

# ========== FILE LOADING MODE ==========
# If you want to manually upload files instead of using default paths, set to True
USE_FILE_PICKER = True

def load_file(prompt_text, filetypes):
    print(f"📂 Please select the file for: {prompt_text}")
    root = Tk()
    root.withdraw()
    file_path = askopenfilename(title=prompt_text, filetypes=filetypes)
    print(f"✅ Loaded file: {file_path}")
    return file_path

# ========== LOAD FILES ==========

if USE_FILE_PICKER:
    presence_path = load_file("Presence Scores CSV", [("CSV files", "*.csv")])
    maturity_path = load_file("Maturity Scores XLSX", [("Excel files", "*.xlsx")])
    strategic_path = load_file("Strategic Weights CSV", [("CSV files", "*.csv")])
else:
    presence_path = PRESENCE_PATH
    maturity_path = MATURITY_PATH
    strategic_path = STRATEGIC_PATH

presence_df = pd.read_csv(presence_path)
maturity_df = pd.read_excel(maturity_path)
strategic_df = pd.read_csv(strategic_path)

# ========== PREPARE DATA ==========

# Melt the presence scores to long format
presence_long = presence_df.melt(
    id_vars=["Bank Name"], 
    value_vars=["Data", "Analytics", "Technology", "Analog"],
    var_name="sub_category", 
    value_name="presence_score"
)

# Normalize column naming
maturity_df.columns = [col.strip().lower().replace(" ", "_") for col in maturity_df.columns]
maturity_long = pd.concat([
    maturity_df.assign(sub_category=subcat)[["bank_name", "sub_category", "normalized_maturity_score"]]
    for subcat in ["Data", "Analytics", "Technology", "Analog"]
], ignore_index=True)

# Strategic: clipped_scaled_score is the correct column
strategic_df.columns = [col.strip().lower().replace(" ", "_") for col in strategic_df.columns]
strategic_reduced = strategic_df[["bank_name", "subcategory", "clipped_scaled_score"]].copy()
strategic_reduced.columns = ["bank_name", "sub_category", "strategic_score"]

# ========== MERGE ALL ==========

final_df = presence_long.rename(columns={"Bank Name": "bank_name"}).merge(
    maturity_long, on=["bank_name", "sub_category"], how="left"
).merge(
    strategic_reduced, on=["bank_name", "sub_category"], how="left"
)

# ========== CALCULATE FINAL SCORE ==========

final_df["final_score"] = (
    final_df["presence_score"] * PRESENCE_WEIGHT +
    final_df["normalized_maturity_score"] * MATURITY_WEIGHT +
    final_df["strategic_score"] * STRATEGIC_WEIGHT
)

# Add rounded column
final_df["final_score_rounded"] = final_df["final_score"].round(2)

# ========== SAVE OUTPUT ==========

output_file = "final_combined_DATA_scores.csv"
final_df.to_csv(output_file, index=False)
print(f"✅ Final combined DATA scores saved to: {output_file}")