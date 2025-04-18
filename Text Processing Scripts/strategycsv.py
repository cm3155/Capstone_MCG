import pandas as pd
import re
from collections import defaultdict

# Load data
text_df = pd.read_csv('strategy_text_data.csv')  # Replace with actual filename
keyword_df = pd.read_csv('keywords.csv')

# Clean and prepare keyword data
keyword_df.columns = keyword_df.columns.str.strip()
keyword_df['Keyword'] = keyword_df['Keyword'].str.lower().str.strip()

# Group keywords by category
keywords_by_category = defaultdict(list)
for _, row in keyword_df.iterrows():
    category = row['Category']
    keyword = re.escape(row['Keyword'])
    keywords_by_category[category].append(keyword)

# Function to count keyword occurrences in a document
def count_keywords(text):
    text = str(text).lower()
    return {
        'Data': len(re.findall(r'\b(?:' + '|'.join(keywords_by_category.get('Data', [])) + r')\b', text)),
        'Analytics': len(re.findall(r'\b(?:' + '|'.join(keywords_by_category.get('Analytics', [])) + r')\b', text)),
        'Technology': len(re.findall(r'\b(?:' + '|'.join(keywords_by_category.get('Technology', [])) + r')\b', text)),
        'Analog': len(re.findall(r'\b(?:' + '|'.join(keywords_by_category.get('Analog', [])) + r')\b', text)),
    }

# Apply keyword count per row
keyword_counts = text_df['Text Content'].apply(count_keywords)
keyword_df_expanded = pd.DataFrame(keyword_counts.tolist())

# Concatenate in the correct column order
before_text = text_df.loc[:, :'Word Count']
after_text = text_df.loc[:, 'Text Content':]
final_df = pd.concat([before_text, keyword_df_expanded[['Data', 'Analytics', 'Technology', 'Analog']], after_text], axis=1)

# Save output
final_df.to_csv('strategy_data.csv', index=False)
