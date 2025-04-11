import os
import re
import html
from bs4 import BeautifulSoup

class TextPreprocessor:
    def __init__(self, input_dir: str, output_dir: str):
        self.input_dir = input_dir
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

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
        return text.strip()

    def process_all_files(self):
        for root, _, files in os.walk(self.input_dir):
            for file in files:
                if file.endswith(".txt"):
                    input_file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(root, self.input_dir)
                    output_dir_path = os.path.join(self.output_dir, relative_path)
                    os.makedirs(output_dir_path, exist_ok=True)
                    output_file_path = os.path.join(output_dir_path, file)

                    with open(input_file_path, 'r', encoding='utf-8') as f:
                        text = f.read()
                    cleaned_text = self.clean_text(text)
                    with open(output_file_path, 'w', encoding='utf-8') as f:
                        f.write(cleaned_text)

preprocessor = TextPreprocessor(input_dir='C:/Users/cassi/Capstone_MCG/All_Data', output_dir='C:/Users/cassi/Capstone_MCG/All_Data_Processed')
preprocessor.process_all_files()
