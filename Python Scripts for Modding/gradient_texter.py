def gradient_text_from_image(text, gradient_image_path):
    from PIL import Image

    # Filter out spaces to calculate gradient size
    visible_chars = [char for char in text if char != " "]

    # Load and resize the gradient image to match non-space characters
    gradient = Image.open(gradient_image_path).convert("RGB")
    gradient = gradient.resize((len(visible_chars), 1))  # One pixel per non-space character

    result = ""
    color_index = 0
    for char in text:
        if char == " ":
            result += " "
        else:
            r, g, b = gradient.getpixel((color_index, 0))
            hex_color = "#{:02X}{:02X}{:02X}".format(r, g, b)
            result += f"<color={hex_color}>{char}</color>"
            color_index += 1

    return result


if __name__ == "__main__":
    import tkinter as tk
    from tkinter import filedialog

    # Hide main tkinter window
    root = tk.Tk()
    root.withdraw()

    # Let the user pick an image
    gradient_path = filedialog.askopenfilename(
        title="Select Gradient Image",
        filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif"), ("All files", "*.*")]
    )

    if not gradient_path:
        print("No image selected. Exiting...")
        exit()

    user_input = input("Enter the text you want to gradient-color: ")
    colored_output = gradient_text_from_image(user_input, gradient_path)

    print("\nGradient-colored text:\n")
    print(colored_output)

