import os
import shutil
import tkinter as tk
from tkinter import filedialog, scrolledtext


# ----------------------------------------------------------
# Parse filenames with rules:
#   - Must contain: something_something_NUMBER
#   - NUMBER is 1–3 digits
#   - No file extensions used
# ----------------------------------------------------------
def parse_filename(filename):
    parts = filename.split("_")
    last = parts[-1]

    if last.isdigit() and 1 <= len(last) <= 3:
        base = "_".join(parts[:-1])
        return base, last

    return None, None


# ----------------------------------------------------------
# GUI Application
# ----------------------------------------------------------
class RenameApp:
    def __init__(self, root):
        self.root = root
        root.title("PvZ Heroes Filename Updater")

        # Directory selection variables
        self.dirA = tk.StringVar()
        self.dirB = tk.StringVar()
        self.log_unmodified = tk.BooleanVar(value=False)

        # -------- Directory A --------
        tk.Label(root, text="Directory A (source filenames):").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        tk.Entry(root, textvariable=self.dirA, width=60).grid(row=0, column=1, sticky="ew", padx=5)
        tk.Button(root, text="Browse", command=self.browseA).grid(row=0, column=2, padx=5)

        # -------- Directory B --------
        tk.Label(root, text="Directory B (filenames to change):").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        tk.Entry(root, textvariable=self.dirB, width=60).grid(row=1, column=1, sticky="ew", padx=5)
        tk.Button(root, text="Browse", command=self.browseB).grid(row=1, column=2, padx=5)

        # -------- Checkbox for logging unmodified --------
        tk.Checkbutton(root, text="Log unmodified files", variable=self.log_unmodified).grid(row=2, column=1, sticky="w", padx=5)

        # -------- Run Button --------
        tk.Button(root, text="Update Filenames", command=self.run_process,
                  bg="#00FF00", fg="black", padx=10, pady=5).grid(row=3, column=1, pady=10)

        # -------- Output Log --------
        tk.Label(root, text="Output Log:").grid(row=4, column=0, sticky="nw", padx=5)

        self.output = scrolledtext.ScrolledText(root, wrap=tk.WORD)
        self.output.grid(row=4, column=1, columnspan=2, sticky="nsew", padx=5, pady=5)

        # Allow log window to expand
        root.rowconfigure(4, weight=1)
        root.columnconfigure(1, weight=1)
        root.columnconfigure(2, weight=0)

    def browseA(self):
        directory = filedialog.askdirectory()
        if directory:
            self.dirA.set(directory)

    def browseB(self):
        directory = filedialog.askdirectory()
        if directory:
            self.dirB.set(directory)

    def log(self, text):
        self.output.insert(tk.END, text + "\n")
        self.output.see(tk.END)
        self.root.update_idletasks()

    # ----------------------------------------------------------
    # Main rename logic
    # ----------------------------------------------------------
    def run_process(self):
        dirA = self.dirA.get()
        dirB = self.dirB.get()

        if not dirA or not dirB:
            self.log("[ERROR] Both directories must be selected.\n")
            return

        self.log(f"Directory A: {dirA}")
        self.log(f"Directory B: {dirB}")
        self.log("\nBuilding filename pattern map from Directory A...\n")

        # Build pattern map from Directory A
        pattern_map = {}

        for root, dirs, files in os.walk(dirA):
            for file in files:
                base, number = parse_filename(file)
                if base is not None:
                    pattern_map[base] = file

        self.log(f"Found {len(pattern_map)} valid patterns in Directory A.\n")

        # Track unmodified files
        unmodified = []

        self.log("Processing Directory B...\n")

        for root, dirs, files in os.walk(dirB):
            for file in files:
                base, number = parse_filename(file)
                full_path = os.path.join(root, file)

                if base is None:
                    unmodified.append(os.path.relpath(full_path, dirB))
                    continue

                if base in pattern_map:
                    correct_name = pattern_map[base]
                    new_path = os.path.join(root, correct_name)

                    if file == correct_name:
                        continue

                    if os.path.exists(new_path):
                        self.log(f"[SKIP] {new_path} already exists.")
                        continue

                    self.log(f"Renaming:\n  {full_path}\n→ {new_path}\n")
                    shutil.move(full_path, new_path)
                else:
                    unmodified.append(os.path.relpath(full_path, dirB))

        # Summary (conditional)
        if self.log_unmodified.get() and unmodified:
            self.log("\n[WARNING] The following files in Directory B were NOT modified:")
            for u in unmodified:
                self.log(" - " + u)
        elif not unmodified:
            self.log("\nAll eligible files in Directory B were renamed successfully!")

        self.log("\nDone.\n")


# ----------------------------------------------------------
# Start GUI
# ----------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    root.state("zoomed")  # Open the window maximized (Windows)
    app = RenameApp(root)
    root.mainloop()