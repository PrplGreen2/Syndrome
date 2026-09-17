import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import numpy as np


# ============================================================
# CLASS COLORS
# ============================================================

COLORS = {
    "Guardian":  (127, 61, 0),       # #7F3D00
    "Kabloom":   (255, 0, 0),        # #FF0000
    "Mega-Grow": (0, 255, 0),        # #00FF00
    "Smarty":    (191, 191, 191),    # #BFBFBF
    "Solar":     (255, 255, 0),      # #FFFF00
    "Beastly":   (0, 255, 255),      # #00FFFF
    "Brainy":    (255, 0, 255),      # #FF00FF
    "Crazy":     (127, 0, 255),      # #7F00FF
    "Hearty":    (255, 127, 0),      # #FF7F00
    "Sneaky":    (63, 63, 63),       # #3F3F3F
}


# ============================================================
# SETTINGS
# ============================================================

# The first divider is assumed to be at the top.
START_ANGLE = -90.0

# Width used to protect the 3-pixel divider lines.
# A small amount of extra space is included to preserve
# anti-aliased edges.
DIVIDER_PROTECTION = 2.5


# ============================================================
# FIND ICON BOUNDS
# ============================================================

def find_circle_bounds(alpha):

    visible = alpha > 0

    ys, xs = np.where(visible)

    if len(xs) == 0:
        return None

    left = xs.min()
    right = xs.max()

    top = ys.min()
    bottom = ys.max()

    return left, top, right, bottom


# ============================================================
# RECOLOR ICON
# ============================================================

def recolor_icon(
    input_path,
    output_path,
    class_count,
    class_colors
):

    image = Image.open(input_path).convert("RGBA")

    pixels = np.array(image)

    height, width = pixels.shape[:2]

    alpha = pixels[:, :, 3]

    # --------------------------------------------------------
    # Find all transparent pixels
    # --------------------------------------------------------

    transparent = alpha == 0

    if not np.any(transparent):
        raise ValueError(
            "The image contains no transparent pixels."
        )

    # --------------------------------------------------------
    # Find the center of the icon
    # --------------------------------------------------------
    #
    # Use the bounding box of all visible pixels.
    # This allows the icon to be positioned anywhere
    # within the PNG.
    # --------------------------------------------------------

    visible = alpha > 0

    ys, xs = np.where(visible)

    left = xs.min()
    right = xs.max()
    top = ys.min()
    bottom = ys.max()

    center_x = (left + right) / 2.0
    center_y = (top + bottom) / 2.0

    # --------------------------------------------------------
    # Generate coordinates for every pixel
    # --------------------------------------------------------

    y, x = np.indices(
        (height, width)
    )

    dx = x - center_x
    dy = y - center_y

    # --------------------------------------------------------
    # Calculate angle around the icon
    # --------------------------------------------------------

    angles = np.degrees(
        np.arctan2(dy, dx)
    )

    # Start at the top of the icon
    relative_angle = (
        angles - START_ANGLE
    ) % 360

    # --------------------------------------------------------
    # Divide the circle evenly
    # --------------------------------------------------------

    section_size = (
        360.0 / class_count
    )

    sections = np.floor(
        relative_angle / section_size
    ).astype(int)

    sections = np.clip(
        sections,
        0,
        class_count - 1
    )

    # --------------------------------------------------------
    # Only modify transparent pixels
    # --------------------------------------------------------

    for section_number in range(
        class_count
    ):

        mask = (
            transparent &
            (sections == section_number)
        )

        color = class_colors[
            section_number
        ]

        pixels[mask, 0] = color[0]
        pixels[mask, 1] = color[1]
        pixels[mask, 2] = color[2]

        pixels[mask, 3] = 255

    # --------------------------------------------------------
    # Save
    # --------------------------------------------------------

    result = Image.fromarray(
        pixels,
        "RGBA"
    )

    result.save(
        output_path
    )


# ============================================================
# GUI
# ============================================================

class HeroIconEditor:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "Hero Icon Editor"
        )

        self.root.geometry(
            "500x600"
        )

        self.root.resizable(
            False,
            False
        )

        self.input_path = ""

        self.color_variables = []

        # ====================================================
        # TITLE
        # ====================================================

        tk.Label(
            root,
            text="Hero Icon Editor",
            font=("Arial", 18, "bold")
        ).pack(
            pady=(20, 10)
        )

        # ====================================================
        # SELECT PNG
        # ====================================================

        tk.Label(
            root,
            text="Select Hero Icon",
            font=("Arial", 10, "bold")
        ).pack()

        self.file_label = tk.Label(
            root,
            text="No PNG selected",
            width=60
        )

        self.file_label.pack(
            pady=5
        )

        tk.Button(
            root,
            text="SELECT PNG",
            command=self.select_png,
            width=20
        ).pack(
            pady=5
        )

        # ====================================================
        # CLASS COUNT
        # ====================================================

        tk.Label(
            root,
            text="How many Classes does the Hero have?",
            font=("Arial", 10, "bold")
        ).pack(
            pady=(20, 5)
        )

        self.class_var = tk.StringVar(
            value="2 Classes"
        )

        class_options = [
            "1 Class",
            "2 Classes",
            "3 Classes",
            "4 Classes",
            "5 Classes"
        ]

        self.class_menu = tk.OptionMenu(
            root,
            self.class_var,
            *class_options,
            command=self.class_count_changed
        )

        self.class_menu.config(
            width=15
        )

        self.class_menu.pack()

        # ====================================================
        # COLOR SELECTION AREA
        # ====================================================

        self.color_frame = tk.Frame(
            root
        )

        self.color_frame.pack(
            pady=20
        )

        self.create_color_selectors()

        # ====================================================
        # RECOLOR BUTTON
        # ====================================================

        tk.Button(
            root,
            text="RECOLOR ICON",
            command=self.run,
            width=25,
            height=2,
            font=("Arial", 10, "bold")
        ).pack(
            pady=20
        )

    # ========================================================
    # SELECT PNG
    # ========================================================

    def select_png(self):

        path = filedialog.askopenfilename(
            title="Select Hero Icon",
            filetypes=[
                ("PNG Images", "*.png"),
                ("All Files", "*.*")
            ]
        )

        if path:

            self.input_path = path

            self.file_label.config(
                text=path
            )

    # ========================================================
    # GET CLASS COUNT
    # ========================================================

    def get_class_count(self):

        text = self.class_var.get()

        return int(
            text.split()[0]
        )

    # ========================================================
    # CLASS COUNT CHANGED
    # ========================================================

    def class_count_changed(self, value):

        self.create_color_selectors()

    # ========================================================
    # CREATE COLOR DROPDOWNS
    # ========================================================

    def create_color_selectors(self):

        # Remove previous widgets
        for widget in self.color_frame.winfo_children():
            widget.destroy()

        self.color_variables = []

        class_count = self.get_class_count()

        color_names = list(
            COLORS.keys()
        )

        tk.Label(
            self.color_frame,
            text="Section Colors",
            font=("Arial", 11, "bold")
        ).grid(
            row=0,
            column=0,
            columnspan=2,
            pady=(0, 10)
        )

        for i in range(class_count):

            # Class label
            tk.Label(
                self.color_frame,
                text=f"Class {i + 1}:",
                font=("Arial", 10, "bold")
            ).grid(
                row=i + 1,
                column=0,
                padx=10,
                pady=5,
                sticky="e"
            )

            # Default colors cycle through the list
            default_color = color_names[
                i % len(color_names)
            ]

            variable = tk.StringVar(
                value=default_color
            )

            self.color_variables.append(
                variable
            )

            menu = tk.OptionMenu(
                self.color_frame,
                variable,
                *color_names
            )

            menu.config(
                width=15
            )

            menu.grid(
                row=i + 1,
                column=1,
                padx=10,
                pady=5
            )

    # ========================================================
    # RUN
    # ========================================================

    def run(self):

        # ----------------------------------------------------
        # Make sure a PNG was selected
        # ----------------------------------------------------

        if not self.input_path:

            messagebox.showerror(
                "Error",
                "Please select a PNG image first."
            )

            return

        # ----------------------------------------------------
        # Class count
        # ----------------------------------------------------

        class_count = self.get_class_count()

        # ----------------------------------------------------
        # Selected colors
        # ----------------------------------------------------

        class_colors = []

        selected_names = []

        for variable in self.color_variables:

            name = variable.get()

            selected_names.append(
                name
            )

            class_colors.append(
                COLORS[name]
            )

        # ----------------------------------------------------
        # Ask where to save
        # ----------------------------------------------------

        original_name = os.path.basename(
            self.input_path
        )

        filename_without_extension = os.path.splitext(
            original_name
        )[0]

        suggested_name = (
            filename_without_extension +
            "_colored.png"
        )

        output_path = filedialog.asksaveasfilename(
            title="Save Recolored Icon",
            defaultextension=".png",
            initialfile=suggested_name,
            filetypes=[
                ("PNG Images", "*.png")
            ]
        )

        if not output_path:
            return

        # ----------------------------------------------------
        # Process
        # ----------------------------------------------------

        try:

            recolor_icon(
                self.input_path,
                output_path,
                class_count,
                class_colors
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"Could not recolor the image:\n\n{e}"
            )

            return

        # ----------------------------------------------------
        # Finished
        # ----------------------------------------------------

        color_text = "\n".join(
            f"Class {i + 1}: {name}"
            for i, name in enumerate(
                selected_names
            )
        )

        messagebox.showinfo(
            "Finished",
            f"Icon recolored successfully!\n\n"
            f"Classes: {class_count}\n\n"
            f"{color_text}\n\n"
            f"Saved to:\n{output_path}"
        )


# ============================================================
# START
# ============================================================

if __name__ == "__main__":

    import os

    root = tk.Tk()

    app = HeroIconEditor(root)

    root.mainloop()