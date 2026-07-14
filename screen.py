# code for the info screen
import csv
from config import LCD_I2C_ADDRESS, LCD_EXPANDER, LCD_COLS, LCD_ROWS

# the LCD is only reachable when wired to a Pi's I2C bus -- fall back to
# printing so this still runs on a dev machine without the hardware attached
try:
    from RPLCD.i2c import CharLCD
    _lcd = CharLCD(LCD_EXPANDER, LCD_I2C_ADDRESS, cols=LCD_COLS, rows=LCD_ROWS)
except Exception:
    _lcd = None

def fetch_data():
    # fetch the data from the sorted.csv file
    try:
        with open("sorted.csv", "r", newline="") as f:
            return list(csv.reader(f))
    except FileNotFoundError:
        return []

def show_info_screen():
    number = len(fetch_data())
    text = f"Sorted items: {number}"
    return text

def show_current_item(last_detections):
    if not last_detections:
        return "Nothing detected yet."
    top_detection = last_detections[0]
    confidence = top_detection["confidence"]
    bin = top_detection["bin"]
    text = f"{bin}\nConfidence: {confidence:.2f}"
    return text

def update_screen(text):
    # push text to the physical 16x2 LCD, one line at a time
    lines = text.split("\n")[:LCD_ROWS]
    if _lcd is not None:
        _lcd.clear()
        for row, line in enumerate(lines):
            _lcd.cursor_pos = (row, 0)
            _lcd.write_string(line[:LCD_COLS])
    else:
        print("[LCD]", " | ".join(lines))
