import os
import shutil

def merge_folders(src1, src2, dst):
    """Merge two folders with subdirectories into a destination folder."""
    for src in [src1, src2]:
        for root, dirs, files in os.walk(src):
            # Determine the relative path from the source folder
            relative_path = os.path.relpath(root, src)
            destination_path = os.path.join(dst, relative_path)
            
            # Create the directory if it doesn't exist
            os.makedirs(destination_path, exist_ok=True)
            
            for file in files:
                src_file = os.path.join(root, file)
                dst_file = os.path.join(destination_path, file)
                
                # If the file already exists, rename it
                if os.path.exists(dst_file):
                    base, ext = os.path.splitext(file)
                    new_dst_file = os.path.join(destination_path, f"{base}_copy{ext}")
                    shutil.copy2(src_file, new_dst_file)
                else:
                    shutil.copy2(src_file, dst_file)
    
    print(f"Folders '{src1}' and '{src2}' merged into '{dst}' successfully.")

# Example usage
src_folder1 = "C:/Users/cassi/Capstone_MCG/LastSources_CleanedTXT"
src_folder2 = "C:/Users/cassi/Capstone_MCG/News_Sources_CleanTXT"
destination_folder = "C:/Users/cassi/Capstone_MCG/News_Sources"
merge_folders(src_folder1, src_folder2, destination_folder)
