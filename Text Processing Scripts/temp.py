import os

def get_files_in_directory(directory, prefix=""):
    """Recursively get all files in a directory and return a set of names, with optional prefix stripping."""
    file_set = set()
    for root, _, files in os.walk(directory):
        for file in files:
            name, _ = os.path.splitext(file)  # Extract filename without extension
            if prefix and name.startswith(prefix):
                name = name[len(prefix):]  # Remove prefix if present
            file_set.add(name)
    return file_set

def compare_directories(dir1, dir2, prefix="cleaned_"):
    """Compare two directories where dir2 files have a prefix and print unique/missing files."""
    files_dir1 = get_files_in_directory(dir1)
    files_dir2 = get_files_in_directory(dir2, prefix)

    only_in_dir1 = files_dir1 - files_dir2  # Files in dir1 missing in cleaned version
    only_in_dir2 = files_dir2 - files_dir1  # Cleaned files with no original counterpart

    if only_in_dir1:
        print(f"Files in {dir1} without cleaned versions in {dir2}:")
        for file in sorted(only_in_dir1):
            print(f"  {file}")
    else:
        print(f"All files in {dir1} have a cleaned version.")

    if only_in_dir2:
        print(f"Cleaned files in {dir2} with no original counterpart in {dir1}:")
        for file in sorted(only_in_dir2):
            print(f"  {prefix}{file}")
    else:
        print(f"All cleaned files in {dir2} have an original version.")

if __name__ == "__main__":
    dir1 = input("Enter the path to the first directory (original files): ").strip()
    dir2 = input("Enter the path to the second directory (cleaned files): ").strip()
    
    if os.path.isdir(dir1) and os.path.isdir(dir2):
        compare_directories(dir1, dir2)
    else:
        print("One or both of the provided paths are not valid directories.")