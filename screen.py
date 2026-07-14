# code for the info screen
import csv

def fetch_data():
    # fetch the data from the sorted.csv file
    try:
        with open("sorted.csv", "r", newline="") as f:
            return list(csv.reader(f))
    except FileNotFoundError:
        return []

def show_info_screen():
    detection_amount = len(fetch_data())
    text = f"Sorted items: {detection_amount}"
    return text

def show_current_item(last_detections):
    if not last_detections:
        return "Nothing detected yet."
    top_detection = last_detections[0]
    confidence = top_detection["confidence"]
    bin = top_detection["bin"]
    text = f"Current item: {bin} (Confidence: {confidence:.2f})"
    return text
