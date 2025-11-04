import os
import re
import shutil
from pathlib import Path

# --- Configuration ---
# Directory where all your 9,600 images are currently located (Source)
SOURCE_DIR = r"C:\Users\97517\Desktop\ML_miniproject\Fingerprint_dataset" 

# Directory where the new person-specific folders will be created (Destination)
DEST_DIR = r"C:\Users\97517\Desktop\ML_miniproject\Fingerprint_Organized_Data" 

# Common image extensions your script should look for
IMAGE_EXTENSIONS = ('.tif', '.png', '.jpg', '.jpeg')
# ---------------------

def organize_fingerprint_data(source_dir, dest_dir, extensions):
    """
    Moves all fingerprint images for a single person into a subfolder named after their Person ID.
    
    Args:
        source_dir (str): The directory containing all mixed images.
        dest_dir (str): The root directory for the organized output.
        extensions (tuple): A tuple of valid file extensions to process.
    """
    # Create the destination directory if it doesn't exist
    Path(dest_dir).mkdir(parents=True, exist_ok=True)
    print(f"Starting data organization from '{source_dir}'...")

    # Regex pattern to capture the Person ID (the number before the first underscore)
    # This captures '1' in '1_8.tif' or '1200' in '1200_1.png'.
    # Group 1: Person ID (P), Group 2: Impression ID (I), Group 3: Extension (ext)
    pattern = re.compile(r'^(\d+)_(\d+)(\.\w+)$', re.IGNORECASE)
    
    processed_count = 0
    skipped_count = 0
    
    # Iterate through all files in the source directory
    for filename in os.listdir(source_dir):
        # Check if the file has a recognizable image extension first
        if filename.lower().endswith(extensions):
            match = pattern.match(filename)
            
            if match:
                # Extract the Person ID (Group 1)
                person_id = match.group(1) 
                
                # Define the path for the new person-specific folder
                person_folder_path = Path(dest_dir) / person_id
                
                # Create the person's folder if it doesn't exist
                person_folder_path.mkdir(parents=True, exist_ok=True)
                
                # Define source and destination paths for the file
                source_path = Path(source_dir) / filename
                dest_path = person_folder_path / filename
                
                # Move the file
                try:
                    shutil.move(source_path, dest_path)
                    processed_count += 1
                except IOError as e:
                    print(f"Error moving file {filename}: {e}")
            else:
                print(f"Skipping file (name format mismatch): {filename}")
                skipped_count += 1
        else:
            print(f"Skipping file (unsupported extension): {filename}")
            skipped_count += 1

    print("-" * 50)
    print(f"Data organization complete!")
    print(f"Total files moved: {processed_count}")
    print(f"Total files skipped: {skipped_count}")
    print(f"Output directory structure: '{DEST_DIR}'")

# Run the function
organize_fingerprint_data(SOURCE_DIR, DEST_DIR, IMAGE_EXTENSIONS)