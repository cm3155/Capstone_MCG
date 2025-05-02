import os
from pdfminer.high_level import extract_text

def pdf_to_txt(pdf_path):
    # Extract text using pdfminer.six
    return extract_text(pdf_path)

def replace_txt_and_delete_pdfs(base_dir):
    pdf_files_remaining = False
    
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.lower().endswith('.pdf'):
                pdf_path = os.path.join(root, file)
                txt_path = os.path.splitext(pdf_path)[0] + '.txt'
                
                # Convert PDF to text
                text = pdf_to_txt(pdf_path)
                
                if not text:
                    print(f"Warning: No valid text extracted from {pdf_path}")
                    pdf_files_remaining = True
                    continue
                
                # Write extracted text to a .txt file
                with open(txt_path, 'w', encoding='utf-8') as txt_file:
                    txt_file.write(text)
                
                # Delete the original PDF
                try:
                    os.remove(pdf_path)
                    print(f"Deleted {pdf_path} after conversion.")
                except Exception as e:
                    print(f"Error deleting {pdf_path}: {e}")
                    pdf_files_remaining = True
    
    # Check if any PDFs remain in the directory
    for root, _, files in os.walk(base_dir):
        if any(file.lower().endswith('.pdf') for file in files):
            pdf_files_remaining = True
            break
    
    if pdf_files_remaining:
        print("Some PDF files could not be deleted or remain in the directory.")
    else:
        print("All PDFs successfully converted and deleted.")

# Specify the root directory where the search begins
base_directory = 'C:/Users/cassi/Capstone_MCG/SEC_Data'
replace_txt_and_delete_pdfs(base_directory)
