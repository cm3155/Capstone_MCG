from openai import OpenAI

import os
import requests

# Replace with your actual DeepSeek API key
DEEPSEEK_API_KEY = '"sk-6cdebe6c89e944278f9f58db6a0fe608"'
DEEPSEEK_API_URL = 'https://api.deepseek.com/'  # Replace with actual API endpoint

def clean_text_with_deepseek(text):
    headers = {
        'Authorization': f'Bearer {DEEPSEEK_API_KEY}',
        'Content-Type': 'application/json',
    }
    
    data = {
        'prompt': "Read this text file and remove any information that does not pertain to the bank named in the title of the file. Also, keep the formatting the same and keep the table of contents. Send back as a cleaned text file",
        'text': text
    }
    
    response = requests.post(DEEPSEEK_API_URL, headers=headers, json=data)
    
    if response.status_code == 200:
        # Assuming the API returns the cleaned text directly as plain text
        return response.text
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

def process_directory(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
            
            cleaned_text = clean_text_with_deepseek(text)
            
            if cleaned_text:
                cleaned_file_path = os.path.join(directory, f'cleaned_{filename}')
                with open(cleaned_file_path, 'w', encoding='utf-8') as cleaned_file:
                    cleaned_file.write(cleaned_text)
                print(f"Processed and saved: {cleaned_file_path}")
            else:
                print(f"Failed to process: {filename}")

if __name__ == "__main__":
    directory = 'C:/Users/cassi/Capstone_MCG/News_Sources_TXT'  # Replace with your directory path
    process_directory(directory)