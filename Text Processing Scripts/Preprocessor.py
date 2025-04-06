import os
import re
import csv
import spacy
from bs4 import BeautifulSoup
import html
from typing import List
from tqdm import tqdm  

class ModelSECPreprocessor:
    def __init__(self, stopwords_file="C:/Users/cassi/Capstone_MCG/stopwords.txt"):
        self.basicstopwords = self.load_stopwords(stopwords_file)
        self.customstopwords = {
            'company', 'corporation', 'inc', 'ltd', 'filing', 'report', 'fiscal',
            'year', 'quarter', 'financial', 'statement', 'form', 'securities',
            'exchange', 'commission', 'item', 'pursuant', 'section', 'act',
            'following', 'page', 'please', 'see', 'note', 'table', 'corrected',
            'transcript', 'earnings', 'call', 'copyright', 'correct',
        }
        self.stopwords = self.basicstopwords.union(self.customstopwords)
        self.nlp = spacy.load("en_core_web_md")

    def load_stopwords(self, stopwords_file):
        try:
            with open(stopwords_file, "r", encoding='utf-8') as f:
                stopwords = set(f.read().splitlines())
            return stopwords
        except FileNotFoundError:
            print(f"Warning: {stopwords_file} not found")
            return set()

    def remove_named_entities(self, text: str) -> str:
        doc = self.nlp(text)
        return " ".join([token.text for token in doc if token.ent_type_ == ""])

    def clean_text(self, text: str) -> str:
        text = text.lower()
        text = BeautifulSoup(text, 'html.parser').get_text()
        text = html.unescape(text)
        text = re.sub(r'form\s+10-[kq].*?filing', '', text, flags=re.IGNORECASE | re.DOTALL)
        text = re.sub(r'united states\s+securities and exchange commission.*?washington', '', text, flags=re.IGNORECASE)
        text = re.sub(r'&#\d+;', ' ', text)
        text = re.sub(r'&[a-zA-Z]+;', ' ', text)
        text = re.sub(r'\b\d+[a-zA-Z]\b', '', text)
        text = re.sub(r'\s*\n\s*', ' ', text)
        text = re.sub(r'[•®©™]', '', text)
        text = re.sub(r'[^\w\s]', '', text)
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[\n\r\t]+', ' ', text)
        text = re.sub(r'\s{2,}', ' ', text)
        text = text.replace('_', ' ')
        text = re.sub(r'\b\d+(?:\.\d+)?\s*(?:dollars|cents|shares)?\b', '', text)
        text = re.sub(
            r'\b(?:january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{1,2},\s+\d{4}\b',
            '', text, flags=re.IGNORECASE)
        text = self.remove_named_entities(text)

        boilerplate = [
            "for the fiscal year ended",
            "for the period ended",
            "for the quarter ended",
            "table of contents",
            "index to financial statements",
        ]
        for phrase in boilerplate:
            text = text.replace(phrase, '')

        words = text.split()
        words = [word for word in words if word not in self.stopwords]
        return ' '.join(words).strip()

    def extract_text_from_folders(self, root_folder: str) -> List[str]:
        texts = []
        all_files = []

        # Collect all files first (for tqdm to show total)
        for foldername, _, filenames in os.walk(root_folder):
            for filename in filenames:
                all_files.append(os.path.join(foldername, filename))

        for file_path in tqdm(all_files, desc="Processing files"):
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                    text = file.read()
                if text.strip():
                    cleaned_text = self.clean_text(text)
                    texts.append(cleaned_text)
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
        return texts

    def save_to_csv(self, texts: List[str], output_file: str):
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Text"])
            for text in texts:
                writer.writerow([text])

    def process_folders(self, root_folder: str, output_file: str):
        texts = self.extract_text_from_folders(root_folder)
        self.save_to_csv(texts, output_file)

if __name__ == "__main__":
    root_folder = input("Enter the root folder path: ")
    output_file = input("Enter the output CSV file path: ")
    preprocessor = ModelSECPreprocessor()
    preprocessor.process_folders(root_folder, output_file)
    print(f"\n✅ CSV file saved to {output_file}")
