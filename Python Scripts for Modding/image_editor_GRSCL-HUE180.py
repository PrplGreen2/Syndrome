import os
from PIL import Image
import tkinter as tk
from tkinter import filedialog
import colorsys

def process_images(folder_path):
    output_folder = os.path.join(folder_path, "processed")
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            img_path = os.path.join(folder_path, filename)
            original_img = Image.open(img_path)
            has_alpha = original_img.mode in ("RGBA", "LA")

            img = original_img.convert("RGBA") if has_alpha else original_img.convert("RGB")
            r, g, b = img.split()[:3]
            gray = Image.merge("RGB", (r, g, b)).convert("L")  # Grayscale RGB

            # Prepare base image for pixel processing
            gray_rgb = gray.convert("RGB")
            pixels = gray_rgb.load()
            width, height = gray_rgb.size

            for y in range(height):
                for x in range(width):
                    r, g, b = pixels[x, y]

                    # Normalize to [0,1]
                    r /= 255.0
                    g /= 255.0
                    b /= 255.0

                    # Convert to HSV
                    h, s, v = colorsys.rgb_to_hsv(r, g, b)

                    # Apply transformations
                    h = (h + 0.5) % 1.0        # Hue +180°
                    s = 1.0                    # Saturation 100%
                    v = min(v * 1.4, 1.0)      # Brightness +40%

                    # Back to RGB
                    r, g, b = colorsys.hsv_to_rgb(h, s, v)
                    pixels[x, y] = (int(r * 255), int(g * 255), int(b * 255))

            # If the original had alpha, restore it
            if has_alpha:
                alpha = original_img.split()[-1]
                final_img = gray_rgb.convert("RGBA")
                final_img.putalpha(alpha)
            else:
                final_img = gray_rgb

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
