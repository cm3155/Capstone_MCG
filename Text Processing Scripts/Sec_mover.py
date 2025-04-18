import os
import shutil

source_dir = 'C:/Users/cassi/Capstone_MCG/All_Data_Processed/SEC_Data'
target_dir = 'C:/Users/cassi/Capstone_MCG/All_Data_Processed/All_Data_Processed_Engineered'

for subfolder in os.listdir(source_dir):
    source_path = os.path.join(source_dir, subfolder)
    target_path = os.path.join(target_dir, subfolder)

    if os.path.isdir(source_path):
        os.makedirs(target_path, exist_ok=True)
        for item in os.listdir(source_path):
            src_file = os.path.join(source_path, item)
            dst_file = os.path.join(target_path, item)
            shutil.move(src_file, dst_file)  # or shutil.copy2() if you want to keep the original
