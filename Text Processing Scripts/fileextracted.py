import os
import csv

def collect_text_per_bank(root_dir, output_csv):
    bank_text_data = {}

    for dirpath, _, filenames in os.walk(root_dir):
        if filenames:
            # Extract bank name from the directory path
            parts = dirpath.split(os.sep)
            if len(parts) >= 2:
                bank_name = parts[-2]  # 'ally_financial_inc'
                
                if bank_name not in bank_text_data:
                    bank_text_data[bank_name] = []

                for file in filenames:
                    if file.endswith('.txt'):
                        file_path = os.path.join(dirpath, file)
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                bank_text_data[bank_name].append(f.read())
                        except Exception as e:
                            print(f"Could not read file {file_path}: {e}")

    # Write to CSV
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Bank Name', 'Text Data'])
        for bank, texts in bank_text_data.items():
            full_text = ' '.join(texts).replace('\n', ' ').strip()
            writer.writerow([bank, full_text])

# Example usage
collect_text_per_bank('C:/Users/cassi/Capstone_MCG/All_Data_Processed_Engineered', 'C:/Users/cassi/Capstone_MCG/text_data_per_bank.csv')
