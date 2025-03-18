import os

def delete_empty_files(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.isfile(file_path) and os.path.getsize(file_path) == 0:
                try:
                    os.remove(file_path)
                    print(f"Deleted empty file: {file_path}")
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")

# Example usage
base_dir = "C:/Users/cassi/Capstone_MCG/SEC_Data"  # Update with your target directory
delete_empty_files(base_dir)