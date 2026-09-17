import os
from PIL import Image
import tkinter as tk
from tkinter import filedialog

def process_images(folder_path):
    output_folder = os.path.join(folder_path, "processed")
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            img_path = os.path.join(folder_path, filename)
            img = Image.open(img_path).convert("RGBA")  # Ensure image has alpha

            # Separate channels
            r, g, b, a = img.split()

            # Merge RGB and convert to grayscale
            gray = Image.merge("RGB", (r, g, b)).convert("L")

            # Recombine grayscale with original alpha
            final_img = Image.merge("RGBA", (gray, gray, gray, a))

            # Save to output folder
            save_path = os.path.join(output_folder, filename)
            final_img.save(save_path)
            print(f"Processed: {filename}")

    print(f"\nDone. Grayscale images with transparency saved to: {output_folder}")

def select_folder_and_run():
    root = tk.Tk()
    root.withdraw()
    folder_selected = filedialog.askdirectory(title="Select Folder with Images")

    if folder_selected:
        process_images(folder_selected)
    else:
        print("No folder selected.")

if __name__ == "__main__":
    select_folder_and_run()
