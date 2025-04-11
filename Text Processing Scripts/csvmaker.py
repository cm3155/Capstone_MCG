import os
import csv

def extract_file_info_with_text(root_dir, output_csv="extracted_file_info.csv"):
    rows = []

    for dirpath, _, filenames in os.walk(root_dir):
        for file in filenames:
            if file.endswith(".txt"):
                full_path = os.path.join(dirpath, file)
                parts = os.path.normpath(full_path).split(os.sep)

                try:
                    bank_name = parts[-3]
                    file_type = parts[-2]
                    file_name = parts[-1]

                    # Read file content
                    with open(full_path, 'r', encoding='utf-8') as f:
                        text_content = f.read()

                    rows.append({
                        "Bank Name": bank_name,
                        "File Type": file_type,
                        "File Name": file_name,
                        "Text Content": text_content
                    })
                except (IndexError, FileNotFoundError, UnicodeDecodeError) as e:
                    print(f"Skipping {full_path} due to error: {e}")

    # Write to CSV
    with open(output_csv, mode="w", newline='', encoding="utf-8") as csvfile:
        fieldnames = ["Bank Name", "File Type", "File Name", "Text Content"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in rows:
            writer.writerow(row)

    print(f"Done! Extracted {len(rows)} entries to {output_csv}")

# Example usage
extract_file_info_with_text("C:/Users/cassi/Capstone_MCG/All_Data_Processed_Engineered")

