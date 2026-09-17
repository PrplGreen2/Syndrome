import json
import os
import shutil
import re

# Paths
json_file = "filtered.json"
autotagged_dir = r"C:\Users\vasik\Desktop\Prepatch Tag"
output_dir = "Cards"

os.makedirs(output_dir, exist_ok=True)

# --- Build index ONLY for *_1 files ---
file_index = {}

for root, _, files in os.walk(autotagged_dir):
    for file in files:
        if not file.endswith("_1"):
            continue

        base_id = file[:-2]  # removes "_1"
        full_path = os.path.join(root, file)

        file_index[base_id] = full_path

print(f"Indexed {len(file_index)} card files (_1 only).")

# --- Load JSON ---
with open(json_file, "r", encoding="utf-8") as f:
    data = json.load(f)

assets = data["BundleNamesByAssetPath"]

count = 0
missing = []

for asset_path, info in assets.items():
    raw_name = os.path.basename(asset_path)
    card_name = re.sub(r'[^\w\- ]', '_', raw_name)

    bn = info.get("Bn", "")
    if not bn.startswith("autotagged/"):
        continue

    file_id = bn.split("/")[-1]

    found_file = file_index.get(file_id)

    if not found_file:
        missing.append((card_name, file_id))
        continue

    # Create folder
    card_folder = os.path.join(output_dir, card_name)
    os.makedirs(card_folder, exist_ok=True)

    # Copy file
    dst = os.path.join(card_folder, os.path.basename(found_file))
    shutil.copy2(found_file, dst)

    count += 1

print(f"\n✅ Cards processed: {count}")
print(f"❌ Missing: {len(missing)}")

# Debug missing (optional)
for name, fid in missing[:10]:
    print(f"Missing: {name} ({fid})")