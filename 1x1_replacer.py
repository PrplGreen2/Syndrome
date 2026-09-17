import tkinter as tk
from tkinter import filedialog
from PIL import Image

def main():
    # Hide the main Tkinter window
    root = tk.Tk()
    root.withdraw()

    # Ask user to select image files
    file_paths = filedialog.askopenfilenames(
        title="Select image files to replace",
        filetypes=[
            ("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp;*.webp"),
            ("All files", "*.*")
        ]
    )

    if not file_paths:
        print("No images selected. Exiting.")
        return

    # Create a 1x1 transparent image
    transparent_pixel = Image.new("RGBA", (1, 1), (0, 0, 0, 0))

    replaced_count = 0
    for filepath in file_paths:
        try:
            transparent_pixel.save(filepath)
            replaced_count += 1
        except Exception as e:
            print(f"Could not replace {filepath}: {e}")

    print(f"Replaced {replaced_count} image(s) with a 1×1 transparent square.")

if __name__ == "__main__":
    main()