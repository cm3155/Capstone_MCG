import os
import csv

def txt_files_to_csv(directory, output_csv):
    """Recursively reads all .txt files in a directory (including subfolders) and writes their contents into a CSV file."""
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Content'])  # Header row
        
        for root, _, files in os.walk(directory):
            for filename in files:
                if filename.endswith('.txt'):
                    filepath = os.path.join(root, filename)
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read().replace('\n', ' ')  # Ensure content is in one line
                        writer.writerow([content])

if __name__ == "__main__":
    input_directory = "C:/Users/cassi/Capstone_MCG/All_Data"  # Change this to your directory path
    output_csv = "all_raw_data.csv"
    txt_files_to_csv(input_directory, output_csv)
    print(f"CSV file '{output_csv}' has been created successfully.")
