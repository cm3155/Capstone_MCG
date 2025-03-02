import pdfplumber
import os
from tqdm import tqdm

# Set the folder where your PDFs are stored
pdf_folder = "C:/Users/cassi/Capstone_MCG/pdf_earning_calls"  # UPDATE THIS PATH
output_folder = "C:/Users/cassi/Capstone_MCG/txt_earning_calls"  # UPDATE THIS PATH

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Loop through all PDFs in the folder
for pdf_file in tqdm(os.listdir(pdf_folder), desc="Processing PDFs"):
    if pdf_file.endswith(".pdf"):  # Ensure only PDF files are processed
        pdf_path = os.path.join(pdf_folder, pdf_file)
        output_txt = os.path.join(output_folder, pdf_file.replace(".pdf", ".txt"))

        try:
            with pdfplumber.open(pdf_path) as pdf:
                text_data = [page.extract_text() for page in pdf.pages if page.extract_text()]

            # Combine text from all pages
            full_text = "\n\n".join(text_data)

            # Save extracted text to a TXT file
            with open(output_txt, "w", encoding="utf-8") as txt_file:
                txt_file.write(full_text)

            print(f"Saved: {output_txt}")

        except Exception as e:
            print(f" Error processing {pdf_file}: {str(e)}")

print(f"Conversion complete, saved in: {output_folder}")
