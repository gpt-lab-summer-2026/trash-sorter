import os
import random
import shutil

DATASET_DIR = "data/dataset-resized"
OUTPUT_DIR = "data"
SPLITS = {"train": 0.80, "val": 0.15, "test": 0.05}
SEED = 42

# Edit this list to control which folders are included and their class index.
# Order here determines the class index (0, 1, 2, ...).
CLASSES = [
    "battery",
    "cans",
    "cardboard",
    "glass",
    "metal",
    "organic_waste",
    "paper",
    "plastic",
    "plastic_bottles",
    "trash",
]


def split_data():
    random.seed(SEED)

    # Create output folders: data/train/class_name/, data/val/class_name/, etc.
    for split_name in SPLITS:
        for class_name in CLASSES:
            os.makedirs(os.path.join(OUTPUT_DIR, split_name, class_name), exist_ok=True)

    totals = {name: 0 for name in SPLITS}

    for class_idx, class_name in enumerate(CLASSES):
        src_folder = os.path.join(DATASET_DIR, class_name)
        if not os.path.isdir(src_folder):
            print(f"WARNING: folder not found, skipping: {src_folder}")
            continue

        images = sorted([
            f for f in os.listdir(src_folder)
            if f.lower().endswith((".jpg", ".jpeg", ".png"))
        ])
        random.shuffle(images)

        n = len(images)
        n_train = round(n * SPLITS["train"])
        n_val = round(n * SPLITS["val"])

        assignment = (
            [("train", img) for img in images[:n_train]] +
            [("val",   img) for img in images[n_train:n_train + n_val]] +
            [("test",  img) for img in images[n_train + n_val:]]
        )

        for split_name, img in assignment:
            src = os.path.join(src_folder, img)
            dst = os.path.join(OUTPUT_DIR, split_name, class_name, img)
            shutil.move(src, dst)
            totals[split_name] += 1

        n_test = n - n_train - n_val
        print(f"  {class_name:20s} (class {class_idx}): {n} total -> "
              f"{n_train} train, {n_val} val, {n_test} test")

    print(f"\nDone: {totals['train']} train, {totals['val']} val, {totals['test']} test")


if __name__ == "__main__":
    split_data()
