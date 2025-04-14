
import pandas as pd
import re
from collections import defaultdict
import numpy as np

# Load bank text data
bank_df = pd.read_csv('text_data_per_bank.csv')

# Load keyword categories
keyword_df = pd.read_csv('keywords.csv')
keyword_df.columns = keyword_df.columns.str.strip()
keyword_df['Keyword'] = keyword_df['Keyword'].str.lower().str.strip()

# Group keywords by category
keywords_by_category = defaultdict(list)
for _, row in keyword_df.iterrows():
    keywords_by_category[row['Category']].append(re.escape(row['Keyword']))

# Function to count keywords and total words
def count_keywords_and_words(text):
    text = text.lower()
    word_count = len(re.findall(r'\b\w+\b', text))
    category_counts = {}
    for category, keywords in keywords_by_category.items():
        pattern = r'\b(?:' + '|'.join(keywords) + r')\b'
        matches = re.findall(pattern, text)
        category_counts[category] = len(matches)
    return category_counts, word_count

# Aggregate results
results = []

for _, row in bank_df.iterrows():
    bank = row['Bank Name']
    text = row['Text Data']
    category_counts, total_words = count_keywords_and_words(text)
    normalized_counts = {cat: (count / total_words if total_words > 0 else 0) 
                         for cat, count in category_counts.items()}
    normalized_counts['Bank Name'] = bank
    results.append(normalized_counts)

# Convert to DataFrame
results_df = pd.DataFrame(results)
results_df.fillna(0, inplace=True)

# Extract category columns (skip 'Bank Name')
category_cols = [col for col in results_df.columns if col != 'Bank Name']

# Min-max scale each category to 1–5
# Min-max scale to 1–5, rounding to nearest whole number
for col in category_cols:
    min_val = results_df[col].min()
    max_val = results_df[col].max()
    if max_val == min_val:
        results_df[col] = 1  # All same → assign lowest score
    else:
        results_df[col] = (1 + 4 * (results_df[col] - min_val) / (max_val - min_val)).round().astype(int)


# Save output
results_df.to_csv('bank_keyword_scores_scaled.csv', index=False)
