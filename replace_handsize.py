import os
import re
from tkinter import Tk, filedialog, simpledialog, messagebox

def main():
    # Hide Tk window
    root = Tk()
    root.withdraw()

    # Select directory
    folder = filedialog.askdirectory(title="Select folder containing files to modify")
    if not folder:
        messagebox.showinfo("Cancelled", "No folder selected.")
        return

    # Ask for new MaxHandSize value
    new_value = simpledialog.askinteger("MaxHandSize Value",
                                        "Enter new MaxHandSize value:",
                                        minvalue=0)
    if new_value is None:
        messagebox.showinfo("Cancelled", "No value entered.")
        return

    pattern = re.compile(r'"MaxHandSize"\s*:\s*\d+')
    replacement = f'"MaxHandSize": {new_value}'

    edited = 0

    # Loop through files
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)

        # Skip folders
        if not os.path.isfile(file_path):
            continue

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Replace occurrences
            new_content = pattern.sub(replacement, content)

            # Only write if changed
            if new_content != content:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                edited += 1

        except Exception as e:
            print(f"Error processing {filename}: {e}")

    messagebox.showinfo("Done", f"Updated MaxHandSize in {edited} files.")

if __name__ == "__main__":
    main()