# keys must match the YOLO model's own class names (model.names), which come
# from the training folder names in data/new_data -- check with model.names
BIN_MAPPING = {
    "cardboard_and_paper": "cardboard and paper bin",
    "electronics" : "electronics bin",
    "general_trash" : "general bin",
    "plastic" : "plastic bin"
}
DEFAULT_BIN = "general bin"

