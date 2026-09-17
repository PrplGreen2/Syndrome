import os
from PIL import Image, ImageEnhance
import tkinter as tk
from tkinter import filedialog

def process_images(folder_path):
    output_folder = os.path.join(folder_path, "processed")
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            img_path = os.path.join(folder_path, filename)
            img = Image.open(img_path)

            has_alpha = img.mode in ("RGBA", "LA")
            img = img.convert("RGBA") if has_alpha else img.convert("RGB")

            # Separate alpha channel if present
            if has_alpha:
                r, g, b, a = img.split()
                gray = Image.merge("RGB", (r, g, b)).convert("L")
            else:
                gray = img.convert("L")

            # Enhance contrast
            enhancer = ImageEnhance.Contrast(gray)
            enhanced_gray = enhancer.enhance(1.2)

            # Recombine with alpha if needed
            if has_alpha:
                final_img = Image.merge("RGBA", (enhanced_gray, enhanced_gray, enhanced_gray, a))
            else:
                final_img = enhanced_gray

            # Save to output folder
            save_path = os.path.join(output_folder, filename)
            final_img.save(save_path)
            print(f"Processed: {filename}")

    print(f"\nDone. Processed images saved to: {output_folder}")

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
