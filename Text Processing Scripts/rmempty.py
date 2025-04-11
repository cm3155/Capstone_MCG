import os

def remove_empty_folders(root_dir):
    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=False):
        # Check if the folder is empty
        if not dirnames and not filenames:
            try:
                os.rmdir(dirpath)
                print(f"Removed empty folder: {dirpath}")
            except OSError as e:
                print(f"Error removing {dirpath}: {e}")

# Example usage
remove_empty_folders('C:/Users/cassi/Capstone_MCG/All_Data_Processed_Engineered')
