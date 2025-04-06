import os
import re

def clean_transcript(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Find the first occurrence of 'MANAGEMENT DISCUSSION SECTION' and remove everything before it
    match = re.search(r'MANAGEMENT DISCUSSION SECTION', content, re.IGNORECASE)
    if match:
        content = content[match.start():].strip()
    
    # Remove FactSet copyright lines with variable years
    content = re.sub(r'\d{1,2}-\d{3}-FACTSET www\.callstreet\.com Copyright © \d{4}-\d{4} FactSet CallStreet, LLC', '', content)
    content = re.sub(r'\d{1,2}-\d{3}-FACTSET www\.callstreet\.com Copyright © \d{4} FactSet CallStreet, LLC', '', content)
    
    # Overwrite the file with the cleaned content
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content.strip())

def process_directory(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path) and filename.endswith('.txt'):
            clean_transcript(file_path)
            print(f'Processed: {filename}')

if __name__ == "__main__":
    directory = input("Enter the directory path: ")
    process_directory(directory)
    print("Processing complete.")