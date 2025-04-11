import os
import shutil
import re

# Source and destination directories
source_dir = r"C:\Users\cassi\Capstone_MCG\News_Sources"
destination_root = r"C:\Users\cassi\Capstone_MCG\All_Data_Processed_Engineered"

# Helper function to normalize bank names
def normalize_bank_name(raw_name):
    name = raw_name.lower()
    name = name.replace("corporation", "corp")
    name = name.replace("company", "")
    name = name.replace("inc.", "inc")
    name = name.replace("inc", "")
    name = name.replace("&", "and")
    name = name.replace(" ", "_")
    name = name.replace(",", "")
    name = name.replace("__", "_")
    name = name.strip("_")
    return name

# Walk through News_Sources files
for root, _, files in os.walk(source_dir):
    for file in files:
        if file.endswith(".txt") and file.startswith("clean_cleaned_"):
            match = re.match(r"clean_cleaned_(.+?)_\d{4}_Q\d\.txt", file)
            if match:
                raw_bank_name = match.group(1)
                normalized_name = normalize_bank_name(raw_bank_name)

                destination_dir = os.path.join(destination_root, normalized_name, "News_Sources")
                os.makedirs(destination_dir, exist_ok=True)

                original_path = os.path.join(root, file)
                destination_path = os.path.join(destination_dir, file)
                shutil.copy2(original_path, destination_path)
                print(f"Copied: {file} -> {destination_path}")
            else:
                print(f"Skipped: {file} — does not match expected pattern")
