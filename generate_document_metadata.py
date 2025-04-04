#Step 1 of 3 Part Process:
#1. Grab metadata of each document
#2. exploratory, checks word count for potential normalization by doc word count length
#3. applies weighting rubric, calculates by strategic weights
#

import os
import pandas as pd
import re

# Base path to your local GitHub repo
REPO_ROOT = "/Users/alexleu/Documents/Capstone_VSC_Python/Capstone_MCG"
NEWS_PATH = os.path.join(REPO_ROOT, "News_Sources_TXT")
SEC_PATH = os.path.join(REPO_ROOT, "SEC_Data")
EARNINGS_PATH = os.path.join(REPO_ROOT, "txt_earning_calls")

# Detect 10-K vs 10-Q from filename
def detect_sec_form(filename):
    fname = filename.lower()
    if "10-k" in fname:
        return "10-K"
    elif "10-q" in fname:
        return "10-Q"
    else:
        return "SEC Filing"

# Assign document type based on filename content
def classify_doc_type(filename, source_type):
    fname = filename.lower()

    if source_type in ["10-K", "10-Q", "SEC Filing"]:
        if "md&a" in fname or "management" in fname:
            return "MD&A"
        elif "risk" in fname and "market" not in fname:
            return "Risk Factors"
        elif "market" in fname:
            return "Market Risk"
        elif "business" in fname:
            return "Business Overview"
        else:
            return "SEC Other"

    elif source_type == "Earnings Call":
        return "Earnings Call Transcript" if "corrected transcript" in fname else "Earnings Other"

    elif source_type == "News":
        return "News Article"

    return "Other"

# Extract bank name from folder or filename
def extract_bank_name(root_path, filename, source_type):
    if source_type in ["10-K", "10-Q", "SEC Filing"]:
        try:
            parts = root_path.split(os.sep)
            return parts[parts.index("SEC_Data") + 1]
        except:
            return None

    elif source_type == "News":
        return filename.split("_")[0]

    elif source_type == "Earnings Call":
        return filename.split()[2] if filename.startswith("CORRECTED TRANSCRIPT") else filename.split()[0]

    return None

# Main crawling function
def crawl_directory(path, source_type_hint):
    entries = []
    for root, _, files in os.walk(path):
        for f in files:
            if not f.endswith('.txt'):
                continue

            full_path = os.path.join(root, f)

            try:
                with open(full_path, 'r', encoding='utf-8') as file:
                    word_count = len(file.read().split())
            except:
                word_count = 0

            # Identify form type (10-K/10-Q) for SEC docs
            form_type = detect_sec_form(f) if source_type_hint == "SEC Filing" else source_type_hint
            doc_type = classify_doc_type(f, form_type)
            bank_name = extract_bank_name(root, f, source_type_hint)

            entries.append({
                "document_id": os.path.splitext(f)[0],
                "filename": f,
                "full_path": full_path,
                "bank_name": bank_name,
                "source_type": form_type,  # Now shows 10-K, 10-Q, etc.
                "document_type": doc_type,
                "word_count": word_count
            })

    return entries

# Run all 3 sources
all_docs = (
    crawl_directory(NEWS_PATH, "News") +
    crawl_directory(SEC_PATH, "SEC Filing") +
    crawl_directory(EARNINGS_PATH, "Earnings Call")
)

# Create DataFrame and save
df = pd.DataFrame(all_docs)
save_path = os.path.join(REPO_ROOT, "document_metadata.csv")
df.to_csv(save_path, index=False)

print(f" Done! Metadata saved to: {save_path}")
