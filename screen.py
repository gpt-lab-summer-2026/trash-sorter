# code for the info screen

def fetch_data():
    # fetch the data from the sorted.json file
    try:
        with open("sorted.json", "r") as f:
            lines = f.readlines()
            return lines
    except FileNotFoundError:
        return []

def show_info_screen():
    detection_amount = len(fetch_data())
    text = f"Sorted items: {detection_amount}"
    return text
