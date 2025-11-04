import os
import shutil
import random
from pathlib import Path

# --- Configuration for Splitting ---
# The root directory containing all the person folders (1, 2, 3, ... 1200)
ORG_ROOT_DIR = r"C:\Users\97517\Desktop\ML_miniproject\Fingerprint_Organized_Data"

# The directory where the final 'train' and 'test' folders will be created
FINAL_SPLIT_DIR = r"C:\Users\97517\Desktop\ML_miniproject\Fingerprint_Split_Dataset"

# Desired ratio for the split (e.g., 80% for training, 20% for testing)
TRAIN_RATIO = 0.8 
# -----------------------------------

def create_person_exclusive_split(org_root_dir, final_split_dir, train_ratio):
    """
    Splits person folders into 'train' and 'test' sets without mixing individuals.
    
    Args:
        org_root_dir (str): Directory containing all person folders (e.g., '1', '2', ...).
        final_split_dir (str): Target directory for the 'train' and 'test' folders.
        train_ratio (float): The proportion of people to allocate to the training set.
    """
    # 1. Prepare output directories
    train_dir = Path(final_split_dir) / 'train'
    test_dir = Path(final_split_dir) / 'test'
    
    # Ensure the root and split subdirectories are ready
    Path(final_split_dir).mkdir(parents=True, exist_ok=True)
    train_dir.mkdir(parents=True, exist_ok=True)
    test_dir.mkdir(parents=True, exist_ok=True)

    print(f"Reading person folders from: {org_root_dir}")
    
    # 2. Identify all person folders
    # We filter to only include directories (the person ID folders)
    person_folders = [d.name for d in Path(org_root_dir).iterdir() if d.is_dir()]
    
    if not person_folders:
        print("Error: No person folders found in the source directory.")
        return

    # 3. Randomly shuffle the list of person IDs
    random.seed(42) # Set a seed for reproducible splits
    random.shuffle(person_folders)

    # 4. Determine the split point
    num_people = len(person_folders)
    split_point = int(num_people * train_ratio)
    
    # 5. Split the person IDs
    train_people = person_folders[:split_point]
    test_people = person_folders[split_point:]

    print(f"\nTotal People Found: {num_people}")
    print(f"Train Set People: {len(train_people)}")
    print(f"Test Set People: {len(test_people)}")
    
    # 6. Move the folders
    
    # Function to move a folder and print progress
    def move_folders(person_list, destination):
        moved_count = 0
        for person_id in person_list:
            source_folder = Path(org_root_dir) / person_id
            destination_folder = destination / person_id
            
            try:
                # Use shutil.move to relocate the entire folder
                shutil.move(str(source_folder), str(destination_folder))
                moved_count += 1
            except Exception as e:
                print(f"Error moving folder {person_id}: {e}")
        return moved_count

    print("\n--- Moving Train Folders ---")
    train_moved = move_folders(train_people, train_dir)

    print("\n--- Moving Test Folders ---")
    test_moved = move_folders(test_people, test_dir)

    print("-" * 50)
    print("Person-Exclusive Split Complete!")
    print(f"Train folders successfully moved: {train_moved}")
    print(f"Test folders successfully moved: {test_moved}")
    print(f"The final dataset structure is ready at: '{FINAL_SPLIT_DIR}'")


# Run the function
create_person_exclusive_split(ORG_ROOT_DIR, FINAL_SPLIT_DIR, TRAIN_RATIO)