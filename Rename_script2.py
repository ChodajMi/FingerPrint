import os
import re
import shutil
from pathlib import Path

# --- Configuration ---
SOURCE_DIR = r"C:\Users\97517\Desktop\ML_miniproject\fingerprint-datasets\74034_3_En_4_MOESM1_ESM\74034_3_En_4_MOESM1_ESM\FVC2004\Dbs\DB4_A"
DEST_DIR = r"C:\Users\97517\Desktop\ML_miniproject\FVC_2000"

# The OLD ID sequence starts with 1 (e.g., the '1' in '1_1.tif').
# This is the base number used for calculating the shift.
OLD_BASE_ID = 1 

# The NEW ID sequence starts with 101 (e.g., the '101' in '101_1.tif').
NEW_BASE_ID = 1101 
# ---------------------

def rename_and_copy_images(source_dir, dest_dir, old_base_id, new_base_id):
    """
    Renames images from the old X_Y format to the new ID_Y format (e.g., 1_1.tif -> 101_1.tif).
    It processes all files found whose first ID number is >= old_base_id.
    """
    Path(dest_dir).mkdir(parents=True, exist_ok=True)
    print(f"Starting rename process from {source_dir} to {dest_dir}...")

    # Regex pattern to capture ALL three parts: (First ID)_(Second ID).(Extension)
    # Example match for "1_1.tif": Group 1='1', Group 2='1', Group 3='tif'
    pattern = re.compile(r'(\d+)_(\d+)\.(\w+)')
    
    count = 0
    
    for filename in os.listdir(source_dir):
        match = pattern.match(filename)
        
        if match:
            # Group 1: The first number (the one we want to shift: X)
            # Group 2: The second number (the impression number: Y)
            # Group 3: File extension (ext)
            first_id = int(match.group(1))
            second_id = match.group(2)
            extension = match.group(3)
            
            # Check if the first ID is where our intended sequence starts (e.g., >= 1)
            if first_id >= old_base_id: 
                # Calculate the NEW first ID: 
                # Shift by the difference between new_base_id and old_base_id
                # Example: (1 - 1) + 101 = 101
                # Example: (10 - 1) + 101 = 110
                new_first_id = new_base_id + (first_id - old_base_id)
                
                # Construct the new filename: NEW_FIRST_ID_SECOND_ID.EXTENSION
                new_filename = f"{new_first_id}_{second_id}.{extension}"
                
                # Define source and destination paths
                source_path = os.path.join(source_dir, filename)
                dest_path = os.path.join(dest_dir, new_filename)
                
                # Copy the file
                try:
                    shutil.copy2(source_path, dest_path)
                    count += 1
                except IOError as e:
                    print(f"Error copying file {filename}: {e}")
            else:
                print(f"Skipping file whose first ID is less than {old_base_id}: {filename}")
        else:
            # This handles files that don't match the X_Y.ext pattern
            print(f"Skipping file: No match for X_Y.ext pattern in filename: {filename}")

    print("-" * 30)
    print(f"Finished renaming and copying {count} files.")
    print(f"Renamed images are saved in the '{DEST_DIR}' folder.")

# Run the function
rename_and_copy_images(SOURCE_DIR, DEST_DIR, OLD_BASE_ID, NEW_BASE_ID)