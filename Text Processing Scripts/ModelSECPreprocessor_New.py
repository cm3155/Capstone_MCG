import os
import re
import csv
import nltk
import spacy
from bs4 import BeautifulSoup
import html
from typing import Dict, List

nltk.download('punkt__tab')
nltk.download('wordnet')
nltk.download('omw-1.4')
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer

class ModelSECPreprocessor:
    def __init__(self, stopwords_file="stopwords-en.txt"): 
        # Load stopwords from file
        self.basicstopwords = self.load_stopwords(stopwords_file) #Stopwords from https://github.com/stopwords-iso/stopwords-en/blob/master/stopwords-en.txt
        self.customstopwords = { #SEC common stopwords
            '10k','10q', '10-K', '10-Q', 'company', 'corporation', 'inc', 'ltd', 'filing', 'report', 'fiscal',
            'year', 'quarter', 'financial', 'statement', 'form', 'securities',
            'exchange', 'commission', 'item', 'pursuant', 'section', 'act',
            'following', 'page', 'please', 'see', 'note', 'table'
        }
        self.stopwords = self.basicstopwords.union(self.customstopwords)
        self.stemmer = PorterStemmer()
        self.lemmatizer = WordNetLemmatizer()

    def load_stopwords(self, stopwords_file):
        """Reads stopwords from a file and returns them as a set."""
        try:
            with open(stopwords_file, "r", encoding='utf-8') as f:
                stopwords = set(f.read().splitlines())  # Load stopwords into a set
            return stopwords
        except FileNotFoundError:
            print(f"Warning: {stopwords_file} not found")
            return set()
        

    def clean_text(self, text: str) -> str:
        # Convert to lowercase
        text = text.lower()

        # Remove HTML
        text = BeautifulSoup(text, 'html.parser').get_text()
        text = html.unescape(text)

        # Remove common SEC filing headers/footers
        text = re.sub(r'form\s+10-[kq].*?filing', '', text, flags=re.IGNORECASE | re.DOTALL)
        text = re.sub(r'united states\s+securities and exchange commission.*?washington', '', text, flags=re.IGNORECASE)
        
        # Basic cleaning
        text = re.sub(r'&#\d+;', ' ', text) # Remove HTML numeric character references (e.g., &#123;)
        text = re.sub(r'&[a-zA-Z]+;', ' ', text) # Remove HTML named character entities (e.g., &amp;, &lt;)
        text = re.sub(r'\b\d+[a-zA-Z]\b', '', text) #Remove standalone number followed by a letter
        text = re.sub(r'\s*\n\s*', ' ', text) # Replace newline characters with a space, also removing any leading/trailing spaces around newlines
        text = re.sub(r'[•®©™]', '', text) # Remove special symbols
        text = re.sub(r'[^\w\s]', '', text)  # Remove all punctuation
        text = re.sub(r'\s+', ' ', text)      # Normalize whitespace
        text = re.sub(r'[\n\r\t]+', ' ', text)  # Replace newlines and tabs with space
        text = re.sub(r'\s{2,}', ' ', text)     # Remove multiple spaces
        
        # Remove standalone numbers and dates
        text = re.sub(r'\b\d+(?:\.\d+)?\s*(?:dollars|cents|shares)?\b', '', text)
        text = re.sub(r'\b(?:january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{1,2},\s+\d{4}\b', '', text, flags=re.IGNORECASE)

        words = word_tokenize(text)
        words = [self.lemmatizer.lemmatize(self.stemmer.stem(word)) for word in words if word not in self.stopwords]
        return ' '.join(words).strip()
    
    name_remover = spacy.load("en_core_web_sm")

    def remove_named_entities(text):
        doc = name_remover(text)
        return " ".join([token.text for token in doc if token.ent_type_ == ""])

    def preprocess_for_analysis(self, text: str) -> str:
        # Remove very short lines (likely headers/footers)
        lines = text.split('\n')
        lines = [line for line in lines if len(line.strip()) > 30]
        text = ' '.join(lines)
        
        # Remove common boilerplate phrases
        boilerplate = [
            "for the fiscal year ended",
            "for the period ended",
            "for the quarter ended",
            "table of contents",
            "index to financial statements",
        ]
        
        for phrase in boilerplate:
            text = text.replace(phrase, '')
        
        return text.strip()
    
    def extract_text_from_folders(self, root_folder: str) -> List[Dict[str, str]]:
        data = []
        for foldername, _, filenames in os.walk(root_folder):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                        text = file.read()
                    if text.strip():
                        cleaned_text = self.clean_text(text)
                        folder_levels = foldername.replace(root_folder, '').strip(os.sep).split(os.sep)
                        row = {
                            'Company_Name': folder_levels[0] if len(folder_levels) > 0 else '',
                            'Year': folder_levels[1] if len(folder_levels) > 1 else '',
                            'Filename': filename,
                            'Text': cleaned_text
                        }
                        data.append(row)
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
        return data

    def save_to_csv(self, data: List[Dict[str, str]], output_file: str):
        fieldnames = ['Company_Name', 'Year', 'Filename', 'Text']
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)   
    
    def process_folders(self, root_folder: str, output_file: str):
        """Processes multiple folders and saves structured text data to CSV."""
        data = self.extract_text_from_folders(root_folder)
        self.save_to_csv(data, output_file)

if __name__ == "__main__":
    root_folder = input("Enter the root folder path: ")
    output_file = input("Enter the output CSV file path: ")
    preprocessor = ModelSECPreprocessor()
    preprocessor.process_folders(root_folder, output_file)
    print(f"CSV file saved to {output_file}")