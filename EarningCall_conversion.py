import pdfplumber
import pandas as pd
import os
from tqdm import tqdm

# Set the folder where your PDFs are stored
pdf_folder = "/Users/vanessacarvajal/Desktop/Capstone_PDFs"  # UPDATE THIS PATH
output_folder = "/Users/vanessacarvajal/Desktop/ConvertedCSVs"  # UPDATE THIS PATH

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Loop through all PDFs in the folder
for pdf_file in tqdm(os.listdir(pdf_folder), desc="Processing PDFs"):
    if pdf_file.endswith(".pdf"):  # Ensure only PDF files are processed
        pdf_path = os.path.join(pdf_folder, pdf_file)
        output_csv = os.path.join(output_folder, pdf_file.replace(".pdf", ".csv"))

        try:
            with pdfplumber.open(pdf_path) as pdf:
                text_data = [{"Page": i+1, "Text": page.extract_text()} 
                             for i, page in enumerate(pdf.pages) if page.extract_text()]

            # Convert to DataFrame
            df = pd.DataFrame(text_data)

            # Save each PDF as an individual CSV file
            df.to_csv(output_csv, index=False, encoding="utf-8")

            print(f"✅ Saved: {output_csv}")

        except Exception as e:
            print(f"❌ Error processing {pdf_file}: {str(e)}")

print(f"🎉 Conversion complete! CSVs saved in: {output_folder}")
