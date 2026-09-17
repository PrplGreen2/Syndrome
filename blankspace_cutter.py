import os
from PIL import Image
from tkinter import Tk, filedialog

def crop_transparent_image(input_path, output_path):
    """Crop a PNG to remove transparent borders and save to output_path."""
    image = Image.open(input_path).convert("RGBA")
    bbox = image.getbbox()

    if bbox:
        cropped = image.crop(bbox)
    else:
        cropped = image  # if fully transparent

    cropped.save(output_path, "PNG")
    print(f"✔ Saved: {output_path}")


def select_images_and_crop():
    """Open file dialog, crop selected images, and save to 'Edited' folder."""
    # Hide the Tkinter main window
    root = Tk()
    root.withdraw()

    # Let user select multiple PNGs
    file_paths = filedialog.askopenfilenames(
        title="Select PNG images to crop",
        filetypes=[("PNG Images", "*.png")]
    )

    if not file_paths:
        print("No images selected. Exiting.")
        return

    for path in file_paths:
        directory = os.path.dirname(path)
        filename = os.path.basename(path)
        edited_folder = os.path.join(directory, "Edited")

        # Create "Edited" folder if it doesn't exist
        os.makedirs(edited_folder, exist_ok=True)

        output_path = os.path.join(edited_folder, filename)
        crop_transparent_image(path, output_path)

    print("\n✅ All selected images have been cropped and saved into their respective 'Edited' folders.")


if __name__ == "__main__":
    select_images_and_crop()