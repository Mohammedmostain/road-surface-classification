import os
import shutil
import tkinter as tk
from PIL import Image, ImageTk

# --- CONFIGURATION ---
DATASET_FOLDER = "labeled_dataset"
FOLDERS = {
    '1': "labeled_dataset/fully_covered",
    '2': "labeled_dataset/partially_covered",
    '3': "labeled_dataset/clear_road"
}

class DatasetReviewer:
    def __init__(self, master):
        self.master = master
        self.master.title("Dataset Reviewer - Fix Your Mistakes")
        
        # 1. Gather all files from all subfolders
        self.all_files = [] # Format: (current_path, filename, category_name)
        
        if not os.path.exists(DATASET_FOLDER):
            print("Error: labeled_dataset folder not found!")
            return

        for category in os.listdir(DATASET_FOLDER):
            cat_path = os.path.join(DATASET_FOLDER, category)
            if os.path.isdir(cat_path):
                files = [f for f in os.listdir(cat_path) if f.endswith(('.png', '.jpg', '.jpeg'))]
                for f in files:
                    self.all_files.append((cat_path, f, category))

        self.current_index = 0
        
        # 2. UI Setup
        self.lbl_info = tk.Label(master, text="SPACE: Keep | X: Delete | 1/2/3: Move to Category", font=("Arial", 12, "bold"))
        self.lbl_info.pack(pady=10)

        self.lbl_category = tk.Label(master, text="", font=("Arial", 14, "bold"), fg="blue")
        self.lbl_category.pack()

        self.canvas = tk.Label(master)
        self.canvas.pack()

        self.lbl_status = tk.Label(master, text="", font=("Arial", 10))
        self.lbl_status.pack(pady=10)

        # 3. Bind Keys
        master.bind('<space>', lambda e: self.next_image()) # Keep
        master.bind('x', lambda e: self.delete_image())     # Delete
        master.bind('1', lambda e: self.move_image('1'))    # Move to Fully
        master.bind('2', lambda e: self.move_image('2'))    # Move to Partial
        master.bind('3', lambda e: self.move_image('3'))    # Move to Clear

        self.load_image()

    def load_image(self):
        if self.current_index >= len(self.all_files):
            self.lbl_status.config(text="Review Complete! No more images.")
            self.canvas.config(image='')
            self.lbl_category.config(text="DONE")
            return

        current_path, filename, category = self.all_files[self.current_index]
        full_path = os.path.join(current_path, filename)

        # Update labels
        self.lbl_category.config(text=f"Current Label: {category}")
        self.lbl_status.config(text=f"Image {self.current_index + 1} / {len(self.all_files)}")

        try:
            # Display Image
            img = Image.open(full_path)
            img.thumbnail((800, 600))
            self.photo = ImageTk.PhotoImage(img)
            self.canvas.config(image=self.photo)
        except Exception as e:
            print(f"Error loading {filename}: {e}")
            self.current_index += 1
            self.load_image()

    def next_image(self):
        """Keep the image and go to next."""
        self.current_index += 1
        self.load_image()

    def delete_image(self):
        """Deletes the current image."""
        current_path, filename, _ = self.all_files[self.current_index]
        full_path = os.path.join(current_path, filename)
        
        try:
            os.remove(full_path)
            print(f"Deleted: {filename}")
        except Exception as e:
            print(f"Error deleting: {e}")
            
        self.current_index += 1
        self.load_image()

    def move_image(self, key):
        """Moves image to a different folder if you mislabeled it."""
        current_path, filename, _ = self.all_files[self.current_index]
        src = os.path.join(current_path, filename)
        
        target_folder = FOLDERS[key]
        dst = os.path.join(target_folder, filename)

        # Don't move if it's already there
        if os.path.abspath(current_path) == os.path.abspath(target_folder):
            self.next_image()
            return

        try:
            shutil.move(src, dst)
            print(f"Moved {filename} -> {target_folder}")
        except Exception as e:
            print(f"Error moving: {e}")

        self.current_index += 1
        self.load_image()

if __name__ == "__main__":
    root = tk.Tk()
    app = DatasetReviewer(root)
    root.mainloop()