import pdfplumber
import os
from tqdm import tqdm

# Set the folder where your PDFs are stored
pdf_folder = "C:/Users/cassi/Capstone_MCG/News_Sources"  # UPDATE THIS PATH
output_folder = "C:/Users/cassi/Capstone_MCG/News_Sources_TXT"  # UPDATE THIS PATH

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Loop through all PDFs in the folder and subfolders
for root, _, files in os.walk(pdf_folder):
    for pdf_file in tqdm(files, desc="Processing PDFs"):
        if pdf_file.endswith(".pdf"):  # Ensure only PDF files are processed
            pdf_path = os.path.join(root, pdf_file)

            # Recreate the folder structure in the output folder
            relative_path = os.path.relpath(root, pdf_folder)
            output_subfolder = os.path.join(output_folder, relative_path)
            os.makedirs(output_subfolder, exist_ok=True)

            output_txt = os.path.join(output_subfolder, pdf_file.replace(".pdf", ".txt"))

            try:
                with pdfplumber.open(pdf_path) as pdf:
                    text_data = []
                    for page in pdf.pages:
                        text = page.extract_text(x_tolerance=1, y_tolerance=1, layout=True)  # Preserve spacing
                        if text:
                            text_data.append(text)

                # Combine text from all pages while preserving spaces
                full_text = "\n\n".join(text_data)

                # Save extracted text to a TXT file
                with open(output_txt, "w", encoding="utf-8") as txt_file:
                    txt_file.write(full_text)

                print(f"Saved: {output_txt}")

            except Exception as e:
                print(f"Error processing {pdf_file}: {str(e)}")

print(f"Conversion complete, saved in: {output_folder}")
