import tkinter as tk
from tkinter import filedialog
from PIL import Image
import os

def create_alpha_mask():
    # Hide the root window
    root = tk.Tk()
    root.withdraw()

    # Ask user to select an image
    file_path = filedialog.askopenfilename(
        title="Select an image",
        filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.webp;*.tiff;*.bmp")]
    )

    if not file_path:
        print("No file selected.")
        return

    # Load image and ensure it has an alpha channel
    img = Image.open(file_path).convert("RGBA")

    # Extract the alpha channel (transparency)
    alpha = img.getchannel("A")

    # Build the output filename
    dir_name, base_name = os.path.split(file_path)
    name, _ = os.path.splitext(base_name)
    save_path = os.path.join(dir_name, f"{name}_alpha.png")

    # Save the alpha mask
    alpha.save(save_path)

    print(f"✅ Alpha mask saved as: {save_path}")

if __name__ == "__main__":
    create_alpha_mask()