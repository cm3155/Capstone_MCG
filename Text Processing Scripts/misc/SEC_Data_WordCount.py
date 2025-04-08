import os
import re
from collections import Counter

def extract_text_from_files(root_folder):
    """Extracts text from all files in the given root folder and its subdirectories."""
    all_text = ""
    
    for foldername, subfolders, filenames in os.walk(root_folder):
        for filename in filenames:
            file_path = os.path.join(foldername, filename)
            
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                    all_text += file.read() + " "
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
    
    return all_text

def clean_and_count_words(text):
    """Cleans text and counts word occurrences."""
    text = text.lower()
    text = re.sub(r'\d+', '', text) 
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)  # Remove special characters
    words = text.split()
    
    word_counts = Counter(words)
    return word_counts

def main():
    root_folder = input("Enter the root folder path: ")
    text = extract_text_from_files(root_folder)
    
    word_counts = clean_and_count_words(text)
    top_words = word_counts.most_common(50)
    
    print("\nTop 50 Most Frequent Words:")
    for word, count in top_words:
        print(f"{word}: {count}")

if __name__ == "__main__":
    main()