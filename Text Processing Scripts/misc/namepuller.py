

import os

def list_immediate_subfolders(directory):
    return [
        os.path.join(directory, name) 
        for name in os.listdir(directory) 
        if os.path.isdir(os.path.join(directory, name))
    ]

# Example usage
if __name__ == "__main__":
    folder_path = r"C:/Users/cassi/Capstone_MCG/All_Data_Processed_Engineered"  # Replace with your target directory
    subfolders = list_immediate_subfolders(folder_path)

    # Print the list of immediate subfolders
    for folder in subfolders:
        print(folder)

