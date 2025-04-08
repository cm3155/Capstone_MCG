import os

# Set the folder where your TXT files are stored
txt_folder = "C:/Users/cassi/Capstone_MCG/News_Sources_TXT"  # UPDATE THIS PATH

# Loop through all TXT files in the folder and subfolders
for root, _, files in os.walk(txt_folder):
    for txt_file in files:
        if txt_file.endswith(".txt"):  # Ensure only TXT files are processed
            txt_path = os.path.join(root, txt_file)
            
            try:
                # Read the content of the TXT file
                with open(txt_path, "r", encoding="utf-8") as file:
                    content = file.read()
                
                # Find and remove everything after "SearchSummary"
                search_index = content.find("Search Summary")
                if search_index != -1:
                    content = content[:search_index]
                    
                    # Save the cleaned content back to the file
                    with open(txt_path, "w", encoding="utf-8") as file:
                        file.write(content)
                    
                    print(f"Cleaned: {txt_path}")
                
            except Exception as e:
                print(f"Error processing {txt_file}: {str(e)}")

print(f"Cleaning complete in: {txt_folder}")