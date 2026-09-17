from PIL import Image
import os
import tkinter as tk
from tkinter import filedialog, messagebox

def swap_images(path1, path2):
    try:
        img1 = Image.open(path1)
        img2 = Image.open(path2)

        # Optional size check
        if img1.size != (256, 256) or img2.size != (256, 256):
            raise ValueError("Both images must be 256x256.")

        # Swap contents
        img1_copy = img1.copy()
        img2_copy = img2.copy()

        img2_copy.save(path1)
        img1_copy.save(path2)

        messagebox.showinfo("Success", "Images swapped successfully!")

    except Exception as e:
        messagebox.showerror("Error", str(e))


def select_and_swap():
    # Hide main window
    root = tk.Tk()
    root.withdraw()

    filetypes = [("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")]

    messagebox.showinfo("Select First Image", "Choose the first 256x256 image.")
    path1 = filedialog.askopenfilename(title="Select First Image", filetypes=filetypes)

    if not path1:
        return

    messagebox.showinfo("Select Second Image", "Choose the second 256x256 image.")
    path2 = filedialog.askopenfilename(title="Select Second Image", filetypes=filetypes)

    if not path2:
        return

    if not os.path.isfile(path1) or not os.path.isfile(path2):
        messagebox.showerror("Error", "Invalid file selection.")
        return

    swap_images(path1, path2)


if __name__ == "__main__":
    select_and_swap()