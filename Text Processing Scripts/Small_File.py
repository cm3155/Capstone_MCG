import os
import csv

def find_small_txt_files(directory, output_csv):
    files_data = []
    
    # Single-layer traversal
    for root, _, files in os.walk(directory):  # No need for nested directory traversal
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                file_size = os.path.getsize(file_path) / 1024  # Convert to KB
                
                if 0 < file_size <= 3:  # Check if file size is 3 KB or less
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        text = f.read()
                    
                    # Extract folder and subfolder relative to the main directory
                    relative_path = os.path.relpath(root, directory)
                    folder_parts = relative_path.split(os.sep)
                    
                    folder = folder_parts[0] if len(folder_parts) > 0 else ""
                    subfolder = folder_parts[1] if len(folder_parts) > 1 else ""
                    
                    # Avoid duplicate entries
                    if [file, folder, subfolder, text] not in files_data:
                        files_data.append([file, folder, subfolder, text])
    
    # Write to CSV
    with open(output_csv, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["File Name", "Folder", "Subfolder", "Text Content"])
        writer.writerows(files_data)
    
    print(f"CSV file '{output_csv}' created successfully with {len(files_data)} entries.")

# Example usage
directory_path = "C:/Users/cassi/Capstone_MCG/SEC_data"
output_csv_path = "C:/Users/cassi/Capstone_MCG/sm_file_output.csv"
find_small_txt_files(directory_path, output_csv_path)