import os
from pdfminer.high_level import extract_text

def pdf_to_txt(pdf_path):
    # Extract text using pdfminer.six
    return extract_text(pdf_path)

def replace_txt_in_folders(base_dir):
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.lower().endswith('.pdf'):
                pdf_path = os.path.join(root, file)
                txt_path = os.path.splitext(pdf_path)[0] + '.txt'
                
                # Convert PDF to text using pdfminer
                text = pdf_to_txt(pdf_path)
                
                # If extracted text is empty, print a warning
                if not text:
                    print(f"Warning: No valid text extracted from {pdf_path}")
                    continue
                
                # Replace the existing txt file with the new one
                with open(txt_path, 'w', encoding='utf-8') as txt_file:
                    txt_file.write(text)

                print(f"Replaced {txt_path} with text extracted from {pdf_path}")

# Specify the root directory where the search begins
base_directory = 'C:/Users/cassi/Capstone_MCG/SEC_Data'
replace_txt_in_folders(base_directory)