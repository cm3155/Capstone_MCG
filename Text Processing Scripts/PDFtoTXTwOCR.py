import pdfplumber
import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"

def pdf_to_text_with_ocr(pdf_path, output_txt_path):
    print(f"Opening PDF: {pdf_path}")
    extracted_text = ""

    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        print(f"Total pages found: {total_pages}")

        for i, page in enumerate(pdf.pages):
            print(f"Processing page {i + 1}/{total_pages}...")

            # Convert the scanned page to an image
            try:
                image = page.to_image(resolution=300).annotated
                print(f"Successfully converted page {i + 1} to an image.")
            except Exception as e:
                print(f"Error converting page {i + 1} to image: {e}")
                continue

            # Perform OCR on the image
            try:
                text = pytesseract.image_to_string(image, lang="spa")
                print(f"OCR completed for page {i + 1}, extracted {len(text)} characters.")
            except Exception as e:
                print(f"Error performing OCR on page {i + 1}: {e}")
                continue

            extracted_text += text + "\n"

    # Save extracted text to a file
    try:
        with open(output_txt_path, "w", encoding="utf-8") as txt_file:
            txt_file.write(extracted_text)
        print(f"Text extracted and saved to {output_txt_path}")
    except Exception as e:
        print(f"Error saving text to file: {e}")

# Example usage:
pdf_to_text_with_ocr('C:/Users/cassi/Downloads/del Moral - La mirada del hombre oscuro.pdf', 'C:/Users/cassi/Downloads/del Moral - La mirada del hombre oscuro.txt')
