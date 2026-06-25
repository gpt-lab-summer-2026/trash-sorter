# class list
# remove some classes, maybe 3-4 would be good amount 
CLASSES = [
    "cans",
    "cardboard",
    "glass",
    "metal",
    "organic_waste",
    "paper",
    "plastic",
    "plastic_bottles",
    "trash",
    "electronics"
]

# test version, update to correct when getting correct model for this one
BIN_MAPPING = {
    "cans" : "Cans and bottles",
    "cardboard" : "Cardboard bin",
    "glass" : "Glass bin",
    "metal" : "Metal bin",
    "organic_waste" : "Bio bin",
    "paper" : "Paper bin",
    "plastic" : "Plastic bin",
    "plastic_bottles" : "Cans and bottles",
    "trash": "General bin",
    "electronics" : "Electronics bin"
}
DEFAULT_BIN = "General bin"

import os

for split in ["train", "val", "test"]:
    print(f"\n{split}:")
    path = f"data/{split}"
    for cls in sorted(os.listdir(path)):
        cls_path = os.path.join(path, cls)
        if os.path.isdir(cls_path):
            print(f"  {cls}: {len(os.listdir(cls_path))} images")