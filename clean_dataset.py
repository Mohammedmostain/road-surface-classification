import os

# --- CONFIGURATION ---
DATASET_PATH = "labeled_dataset"

# What text identifies a "fake" augmented file?
# Change this to match your files! (e.g., "aug_", "flip", "rotated")
KEYWORDS_TO_DELETE = [ "light1", "flip", "rot1", "rot2"] 

# Set to False to ACTUALLY delete files
DRY_RUN = False  

def clean_data():
    print(f"Scanning {DATASET_PATH}...")
    deleted_count = 0
    kept_count = 0

    for root, dirs, files in os.walk(DATASET_PATH):
        for filename in files:
            file_path = os.path.join(root, filename)
            
            # Check if filename contains any of the bad keywords
            if any(keyword in filename for keyword in KEYWORDS_TO_DELETE):
                if DRY_RUN:
                    print(f"[Would Delete]: {filename}")
                else:
                    os.remove(file_path)
                    print(f"[Deleted]: {filename}")
                deleted_count += 1
            else:
                kept_count += 1

    print("-" * 30)
    if DRY_RUN:
        print(f"Result: I WOULD delete {deleted_count} files.")
        print(f"Result: I WOULD keep {kept_count} original files.")
        print("ACTION: Change 'DRY_RUN = False' in the script to actually do it.")
    else:
        print(f"DONE! Deleted {deleted_count} files.")
        print(f"Remaining clean files: {kept_count}")

if __name__ == "__main__":
    clean_data()