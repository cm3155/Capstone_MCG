import re
from bs4 import BeautifulSoup
import html
from typing import Dict

class ModelSECPreprocessor:
    def __init__(self):
        # Basic stopwords that are very common in SEC filings
        self.stopwords = {
            'company', 'corporation', 'inc', 'ltd', 'filing', 'report', 'fiscal',
            'year', 'quarter', 'financial', 'statement', 'form', 'securities',
            'exchange', 'commission', 'item', 'pursuant', 'section', 'act',
            'following', 'page', 'please', 'see', 'note', 'table'
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