import os
import re
from collections import defaultdict

def extract_text_from_txt(txt_path):
    """Extract text from a TXT file."""
    with open(txt_path, "r", encoding="utf-8") as file:
        return file.read().strip()

def extract_phrases_with_pattern(text, pattern=r"\b(\w+(?:\s+\w+){6,})\s*\.\.\.\.\.\.\.\.\.\.\.\.\.\.\.\.\."):
    """Extract phrases of at least 7 words that are followed by a specific pattern."""
    return set(re.findall(pattern, text))

def flag_common_phrases(directory):
    """Check for identical phrases followed by a pattern across TXT files."""
    txt_texts = {}
    phrase_occurrences = defaultdict(set)
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(".txt"):
                txt_path = os.path.join(root, file)
                text = extract_text_from_txt(txt_path)
                
                if not text:
                    print(f"Warning: No text extracted from {txt_path}")
                    continue
                
                phrases = extract_phrases_with_pattern(text)
                txt_texts[txt_path] = phrases
                
                for phrase in phrases:
                    phrase_occurrences[phrase].add(txt_path)
    
    checked_pairs = set()
    total_pairs = 0
    flagged_articles = set()
    
    for phrase, txts in phrase_occurrences.items():
        if len(txts) > 1:
            txt_list = list(txts)
            for i in range(len(txt_list)):
                for j in range(i + 1, len(txt_list)):
                    txt1, txt2 = txt_list[i], txt_list[j]
                    if (txt1, txt2) not in checked_pairs:
                        print(f"Common phrase detected:")
                        print(f"  - '{phrase}'")
                        print(f"  - Found in:")
                        print(f"    * {txt1}")
                        print(f"    * {txt2}")
                        checked_pairs.add((txt1, txt2))
                        checked_pairs.add((txt2, txt1))
                        total_pairs += 1
            
            if len(txts) > 2:
                flagged_articles.add(phrase)
    
    print(f"Total document pairs with common phrases: {total_pairs}")
    
    if flagged_articles:
        print("Articles appearing more than twice:")
        for phrase in flagged_articles:
            print(f"- {phrase}")
    else:
        print("No articles appeared more than twice.")
    
    if not checked_pairs:
        print("No common phrases found across TXT files.")

# Specify the directory containing TXT files
base_directory = 'C:/Users/cassi/Capstone_MCG/News_Sources_TXT'
flag_common_phrases(base_directory)