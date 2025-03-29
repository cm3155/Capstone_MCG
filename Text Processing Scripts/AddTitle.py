import os

def insert_filename_as_first_line(directory):
    # Walk through all directories and subdirectories
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                
                try:
                    # Get the filename without extension
                    title = os.path.splitext(file)[0]
                    
                    # Read the existing content
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Write the title followed by the existing content
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(title + '\n' + content)
                        
                    print(f"Successfully processed: {file_path}")
                
                except PermissionError:
                    print(f"Permission denied: {file_path}")
                except Exception as e:
                    print(f"Error processing {file_path}: {str(e)}")

if __name__ == "__main__":
    # Use your specific directory path here
    target_directory = r"C:/Users/cassi/Capstone_MCG/LastSources_Txt"
    
    if os.path.isdir(target_directory):
        print(f"Starting processing of: {target_directory}")
        insert_filename_as_first_line(target_directory)
        print("All txt files have been processed.")
    else:
        print(f"Directory not found: {target_directory}")
        print("Please check the path and try again.")

