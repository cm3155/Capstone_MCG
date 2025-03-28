import os

def delete_zero_kb_files(root_folder):
    if os.path.exists(root_folder) and os.path.isdir(root_folder):
        for subdir, _, files in os.walk(root_folder):
            for file in files:
                file_path = os.path.join(subdir, file)
                if os.path.isfile(file_path) and os.path.getsize(file_path) == 0:
                    try:
                        os.remove(file_path)
                        print(f"Deleted: {file_path}")
                    except Exception as e:
                        print(f"Error deleting {file_path}: {e}")
    else:
        print(f"Root folder not found: {root_folder}")

# Example usage
root_folder_to_check = "C:/Users/cassi/Capstone_MCG/SEC_Data"  # Update with actual path
delete_zero_kb_files(root_folder_to_check)
