import pdfplumber

def pdf_to_txt(pdf_path, txt_path):
    # Open the PDF file
    with pdfplumber.open(pdf_path) as pdf:
        # Open a txt file for writing
        with open(txt_path, 'w', encoding='utf-8') as txt_file:
            # Loop through each page of the PDF
            for page in pdf.pages:
                # Extract text from each page
                text = page.extract_text()
                if text:  # If text is found, write to the txt file
                    txt_file.write(text)
                else:
                    txt_file.write("\n")  # If no text found on the page, add a newline
            print(f"Text extracted and saved to {txt_path}")

# Define the PDF file and output TXT file paths
pdf_file_path = 'C:/Users/cassi/Capstone_MCG/SEC_Data/bank_of_new_york_mellon_corporation,_the/2020/10-K_2020-02-27_Management_Discussion_&_Analysis_(MD&A).pdf'  # Replace with your PDF file path
txt_file_path = 'C:/Users/cassi/Capstone_MCG/SEC_Data/bank_of_new_york_mellon_corporation,_the/2020/10-K_2020-02-27_Management_Discussion_&_Analysis_(MD&A).txt'  # Replace with your desired output txt file path

# Convert PDF to TXT
pdf_to_txt(pdf_file_path, txt_file_path)