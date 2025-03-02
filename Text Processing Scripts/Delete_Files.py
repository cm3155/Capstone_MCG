import os
import glob

def delete_files_in_subfolders(root_folder, keywords):
    if os.path.exists(root_folder) and os.path.isdir(root_folder):
        for subdir, _, _ in os.walk(root_folder):
            for keyword in keywords:
                pattern = os.path.join(subdir, f"*{keyword}*")
                files = glob.glob(pattern)
                for file in files:
                    try:
                        os.remove(file)
                        print(f"Deleted: {file}")
                    except Exception as e:
                        print(f"Error deleting {file}: {e}")
    else:
        print(f"Root folder not found: {root_folder}")

# Example usage
root_folder_to_check = "C:/Users/cassi/Capstone_MCG/SEC_Data"  # Update with actual path
keywords_to_delete = ["Corporate_Governance"]

delete_files_in_subfolders(root_folder_to_check, keywords_to_delete)
