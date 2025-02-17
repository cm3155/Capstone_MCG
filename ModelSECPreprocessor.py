import os
import re
import csv
from bs4 import BeautifulSoup
import html
from typing import Dict, List

class ModelSECPreprocessor:
    def __init__(self):
        # Basic stopwords that are very common in SEC filings
        self.stopwords = {
            'company', 'corporation', 'inc', 'ltd', 'filing', 'report', 'fiscal',
            'year', 'quarter', 'financial', 'statement', 'form', 'securities',
            'exchange', 'commission', 'item', 'pursuant', 'section', 'act',
            'following', 'page', 'please', 'see', 'note', 'table', "i", "me",
            "my", "myself", "we", "our", "ours", "ourselves", "you", "your", 
            "yours", "yourself", "yourselves", "he", "him", "his", "himself", 
            "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", 
            "their", "theirs", "themselves", "what", "which", "who", "whom", "this",
            "that", "these", "those", "am", "is", "are", "was", "were", "be",
            "been", "being", "have", "has", "had", "having", "do", "does", "did", 
            "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", 
            "until", "while", "of", "at", "by", "for", "with", "about", "against", 
            "between", "into", "through", "during", "before", "after", "above", 
            "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", 
            "under", "again", "further", "then", "once", "here", "there", "when", 
            "where", "why", "how", "all", "any", "both", "each", "few", "more", 
            "most", "other", "some", "such", "no", "nor", "not", "only", "own", 
            "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", 
            "don", "should", "now"
        }

    def clean_text(self, text: str) -> str:
        """Basic but efficient text cleaning"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove HTML
        text = BeautifulSoup(text, 'html.parser').get_text()
        text = html.unescape(text)

        
        # Remove common SEC filing headers/footers
        text = re.sub(r'form\s+10-[kq].*?filing', '', text, flags=re.IGNORECASE | re.DOTALL)
        text = re.sub(r'united states\s+securities and exchange commission.*?washington', '', text, flags=re.IGNORECASE)
        
        # Basic cleaning
        text = re.sub(r'[\n\r\t]+', ' ', text)  # Replace newlines and tabs with space
        text = re.sub(r'\s{2,}', ' ', text)     # Remove multiple spaces
        text = re.sub(r'[^\w\s.,!?-]', ' ', text)  # Remove special characters but keep basic punctuation
        
        # Remove standalone numbers and dates
        text = re.sub(r'\b\d+(?:\.\d+)?\s*(?:dollars|cents|shares)?\b', '', text)
        text = re.sub(r'\b(?:january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{1,2},\s+\d{4}\b', '', text, flags=re.IGNORECASE)
        
        return text.strip()
    '''
    def split_into_chunks(self, text: str, chunk_size: int = 1000) -> list:
        """Split text into chunks of approximately equal size"""
        words = text.split()
        return [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

    def process_file(self, filepath: str) -> Dict[str, str]:
        """Process a single file with basic cleaning"""
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                text = file.read()
                
            if not text.strip():
                return None
                
            cleaned_text = self.clean_text(text)
            chunks = self.split_into_chunks(cleaned_text)
            
            return {
                'processed_text': cleaned_text,
                'chunks': chunks
            }
            
        except Exception as e:
            print(f"Error processing {filepath}: {str(e)}")
            return None
    '''
    def preprocess_for_analysis(self, text: str) -> str:
        """Final preprocessing before model analysis"""
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
        """Extracts text from multiple folderC:/Users/cassi/Capstone/s and returns a structured list with folder hierarchy."""
        data = []
        for foldername, _, filenames in os.walk(root_folder):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                        text = file.read()
                    if text.strip():
                        cleaned_text = self.clean_text(text)
                        sentences = re.split(r'[.!?]', cleaned_text)
                        folder_levels = foldername.replace(root_folder, '').strip(os.sep).split(os.sep)
                        for sentence in sentences:
                            sentence = sentence.strip()
                            if sentence:
                                row = {f'level_{i+1}': folder_levels[i] if i < len(folder_levels) else '' for i in range(5)}
                                row['text'] = sentence
                                data.append(row)
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
        return data

    def save_to_csv(self, data: List[Dict[str, str]], output_file: str):
        """Saves extracted data to a CSV file with hierarchical folder structure."""
        fieldnames = [f'level_{i+1}' for i in range(5)] + ['text']
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