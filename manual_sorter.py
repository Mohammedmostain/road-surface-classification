import os
import shutil
import tkinter as tk
import random
from PIL import Image, ImageTk, ImageEnhance

# --- CONFIGURATION ---
SOURCE_FOLDER = "traffic_screenshots"
FOLDERS = {
    '1': "labeled_dataset/fully_covered",
    '2': "labeled_dataset/partially_covered",
    '3': "labeled_dataset/clear_road"
}

# --- SETTINGS ---
KEEP_ORIGINAL = True     # Set to False if you want to DELETE the original after creating augmented copies
DO_AUGMENTATION = True   # Set to False to disable the "Cheat Code" entirely

class ImageSorter:
    def __init__(self, master):
        self.master = master
        self.master.title("Traffic Sorter: Label or Delete")
        
        # Create folders
        for path in FOLDERS.values():
            if not os.path.exists(path):
                os.makedirs(path)

        # Get images
        self.image_list = [f for f in os.listdir(SOURCE_FOLDER) if f.endswith(('.png', '.jpg', '.jpeg'))]
        self.current_index = 0

        # UI
        instructions = "KEYS:\n1: Full Snow\n2: Partial\n3: Clear\n\nX: DELETE Image (Junk)"
        self.label_instruction = tk.Label(master, text=instructions, font=("Arial", 14, "bold"), justify="left")
        self.label_instruction.pack(pady=10)

        self.canvas = tk.Label(master)
        self.canvas.pack()

        self.label_status = tk.Label(master, text="", font=("Arial", 10))
        self.label_status.pack(pady=10)

        # Bind Keys
        master.bind('1', lambda e: self.process_image('1'))
        master.bind('2', lambda e: self.process_image('2'))
        master.bind('3', lambda e: self.process_image('3'))
        master.bind('x', lambda e: self.delete_image()) # New "Trash" Key
        master.bind('X', lambda e: self.delete_image()) 

        self.load_image()

    def load_image(self):
        if self.current_index >= len(self.image_list):
            self.label_status.config(text="No more images to sort!")
            self.canvas.config(image='')
            return

        image_name = self.image_list[self.current_index]
        image_path = os.path.join(SOURCE_FOLDER, image_name)

        try:
            img = Image.open(image_path)
            img.thumbnail((800, 600))
            self.photo = ImageTk.PhotoImage(img)
            self.canvas.config(image=self.photo)
            self.label_status.config(text=f"Image {self.current_index + 1} / {len(self.image_list)}: {image_name}")
        except Exception as e:
            print(f"Error loading {image_name}: {e}")
            self.delete_image() # Auto-delete corrupted files

    def delete_image(self):
        """Deletes the current image from source without labeling."""
        if self.current_index >= len(self.image_list): return
        
        filename = self.image_list[self.current_index]
        file_path = os.path.join(SOURCE_FOLDER, filename)
        
        try:
            os.remove(file_path) # <--- THIS DELETE COMMAND
            print(f"Deleted junk file: {filename}")
        except Exception as e:
            print(f"Could not delete: {e}")

        self.current_index += 1
        self.load_image()

    def process_image(self, key):
        if self.current_index >= len(self.image_list): return

        filename = self.image_list[self.current_index]
        src_path = os.path.join(SOURCE_FOLDER, filename)
        target_folder = FOLDERS[key]
        
        # 1. Load image into memory first
        try:
            with Image.open(src_path) as img:
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                base_name = os.path.splitext(filename)[0]

                # 2. Generate Augmented Copies (The "Cheat Code")
                if DO_AUGMENTATION:
                    # Flip
                    img.transpose(Image.FLIP_LEFT_RIGHT).save(os.path.join(target_folder, f"{base_name}_flip.jpg"))
                    # Rotate
                    img.rotate(random.uniform(-10, 10)).save(os.path.join(target_folder, f"{base_name}_rot1.jpg"))
                    img.rotate(random.uniform(-10, 10)).save(os.path.join(target_folder, f"{base_name}_rot2.jpg"))
                    # Brightness
                    enhancer = ImageEnhance.Brightness(img)
                    enhancer.enhance(random.uniform(0.7, 1.3)).save(os.path.join(target_folder, f"{base_name}_light1.jpg"))

                # 3. Handle the Original File
                if KEEP_ORIGINAL:
                    # Save a copy of the original to the destination
                    img.save(os.path.join(target_folder, filename))
            
            # 4. DELETE from Source (This cleans your traffic_screenshots folder)
            os.remove(src_path)
            print(f"Processed {filename} -> {target_folder}")

        except Exception as e:
            print(f"Error processing {filename}: {e}")

        self.current_index += 1
        self.load_image()

if __name__ == "__main__":
    if not os.path.exists(SOURCE_FOLDER):
        print(f"Source folder '{SOURCE_FOLDER}' not found.")
    else:
        root = tk.Tk()
        app = ImageSorter(root)
        root.mainloop()