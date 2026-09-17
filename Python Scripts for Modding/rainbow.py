import os
import random
import numpy as np
from PIL import Image, ImageOps
from scipy.spatial import Delaunay

# === CONFIGURATION ===
INPUT_FOLDER = "C:/Users/vasik/Desktop/PvZ Heroes Syndrome/.TEXTURES/.HEROES/Heliodor Flare/Body/Python"
OUTPUT_FOLDER = "C:/Users/vasik/Desktop/PvZ Heroes Syndrome/.TEXTURES/.HEROES/Heliodor Flare/Body/Python/Pythonized"
PIXELATION_PERCENT = 0.05  # 5% triangular pixelation

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def hue_shift(image, shift):
    """Shift hue of an RGBA image by 'shift' in degrees."""
    img = image.convert("RGBA")
    arr = np.array(img)
    
    # Separate alpha channel
    alpha = arr[..., 3]

    # Convert to HSV
    rgb = arr[..., :3] / 255.0
    hsv = np.zeros_like(rgb)
    cmax = rgb.max(axis=2)
    cmin = rgb.min(axis=2)
    delta = cmax - cmin

    # Hue calculation
    hue = np.zeros_like(cmax)
    mask = delta != 0
    idx = (cmax == rgb[..., 0]) & mask
    hue[idx] = ((rgb[..., 1][idx] - rgb[..., 2][idx]) / delta[idx]) % 6
    idx = (cmax == rgb[..., 1]) & mask
    hue[idx] = ((rgb[..., 2][idx] - rgb[..., 0][idx]) / delta[idx]) + 2
    idx = (cmax == rgb[..., 2]) & mask
    hue[idx] = ((rgb[..., 0][idx] - rgb[..., 1][idx]) / delta[idx]) + 4
    hue = (hue / 6.0) % 1.0

    # Saturation
    sat = np.zeros_like(cmax)
    sat[cmax != 0] = delta[cmax != 0] / cmax[cmax != 0]

    val = cmax

    # Shift hue
    hue = (hue + shift / 360.0) % 1.0

    # Convert back to RGB
    c = val * sat
    x = c * (1 - np.abs((hue * 6) % 2 - 1))
    m = val - c

    rgb_out = np.zeros_like(rgb)
    h_idx = (hue * 6).astype(int)

    zeros = np.zeros_like(c)
    for i in range(6):
        mask = h_idx == i
        if i == 0: rgb_out[mask] = np.stack([c, x, zeros], axis=-1)[mask]
        elif i == 1: rgb_out[mask] = np.stack([x, c, zeros], axis=-1)[mask]
        elif i == 2: rgb_out[mask] = np.stack([zeros, c, x], axis=-1)[mask]
        elif i == 3: rgb_out[mask] = np.stack([zeros, x, c], axis=-1)[mask]
        elif i == 4: rgb_out[mask] = np.stack([x, zeros, c], axis=-1)[mask]
        elif i == 5: rgb_out[mask] = np.stack([c, zeros, x], axis=-1)[mask]


    rgb_out = (rgb_out + m[..., None]) * 255
    rgb_out = np.clip(rgb_out, 0, 255).astype(np.uint8)

    # Reattach alpha
    result = np.dstack([rgb_out, alpha])
    return Image.fromarray(result, "RGBA")

def triangular_pixelation(image, percent):
    """Apply a triangular pixelation (low-poly) effect."""
    img = image.convert("RGBA")
    w, h = img.size
    num_points = int(w * h * percent)

    arr = np.array(img)
    points = np.column_stack((
        np.random.randint(0, w, num_points),
        np.random.randint(0, h, num_points)
    ))

    # Add corner points to avoid black triangles at edges
    points = np.vstack([
        points,
        [[0, 0], [w - 1, 0], [0, h - 1], [w - 1, h - 1]]
    ])

    tri = Delaunay(points)
    output = np.zeros_like(arr)

    for simplex in tri.simplices:
        pts = points[simplex]
        mask = np.zeros((h, w), dtype=np.uint8)
        rr, cc = np.meshgrid(np.arange(w), np.arange(h))
        rrcc = np.stack((rr, cc), axis=-1)
        from matplotlib.path import Path
        path = Path(pts)
        mask[path.contains_points(rrcc.reshape(-1, 2)).reshape(h, w)] = 1

        mean_color = arr[mask == 1].mean(axis=0).astype(np.uint8)
        output[mask == 1] = mean_color

    return Image.fromarray(output, "RGBA")

for filename in os.listdir(INPUT_FOLDER):
    if filename.lower().endswith(".png"):
        img_path = os.path.join(INPUT_FOLDER, filename)

        # Load and convert to grayscale (preserving alpha)
        img = Image.open(img_path).convert("RGBA")
        gray = ImageOps.grayscale(img)
        gray_rgba = Image.merge("RGBA", [gray, gray, gray, img.split()[3]])

        # Apply random hue shift
        hue_val = random.randint(0, 360)
        hue_img = hue_shift(gray_rgba, hue_val)

        # Apply triangular pixelation
        pixelated_img = triangular_pixelation(hue_img, PIXELATION_PERCENT)

        # Save output
        output_path = os.path.join(OUTPUT_FOLDER, filename)
        pixelated_img.save(output_path, "PNG")

        print(f"Processed {filename} with hue shift {hue_val}°")

print("✅ All PNGs processed!")