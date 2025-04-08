API_KEY = 'a827471cc41eb76abd6b4ef9c704e86bd503aa3d76a4c951c08fdb6dc0a5abbe'

from sec_api import ExtractorApi
import os

extractorApi = ExtractorApi(API_KEY)

def pprint(text, line_length=100):
  words = text.split(' ')
  lines = []
  current_line = ''
  for word in words:
      if len(current_line + ' ' + word) <= line_length:
          current_line += ' ' + word
      else:
          lines.append(current_line.strip())
          current_line = word
  if current_line:
      lines.append(current_line.strip())
  print(''.join(lines))

filing_10_k_url = 'https://www.sec.gov/Archives/edgar/data/0000019617/000001961722000319/jpm-20220331.htm'


sections = extractorApi.get_section(filing_10_k_url, 'part1item2', "text")

output_dir = "extracted_filings"
os.makedirs(output_dir, exist_ok=True)  # Ensure directory exists

output_file = os.path.join(output_dir, "10-Q_2022-02_MD&A.txt")

# Save the extracted text to a file
with open(output_file, "w", encoding="utf-8") as file:
    file.write(sections)

print(f"Extracted section saved to {output_file}")