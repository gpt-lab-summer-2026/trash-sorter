# code for the info screen
import csv
from config import (
    LCD_RS_PIN, LCD_EN_PIN, LCD_D4_PIN, LCD_D5_PIN, LCD_D6_PIN, LCD_D7_PIN,
    LCD_COLS, LCD_ROWS,
)

# the LCD is only reachable when wired to a Pi's GPIO pins -- fall back to
# printing so this still runs on a dev machine without the hardware attached
try:
    import board
    import digitalio
    import adafruit_character_lcd.character_lcd as characterlcd

    _lcd = characterlcd.Character_LCD_Mono(
        digitalio.DigitalInOut(getattr(board, LCD_RS_PIN)),
        digitalio.DigitalInOut(getattr(board, LCD_EN_PIN)),
        digitalio.DigitalInOut(getattr(board, LCD_D4_PIN)),
        digitalio.DigitalInOut(getattr(board, LCD_D5_PIN)),
        digitalio.DigitalInOut(getattr(board, LCD_D6_PIN)),
        digitalio.DigitalInOut(getattr(board, LCD_D7_PIN)),
        LCD_COLS, LCD_ROWS,
    )
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
    # push text to the physical 16x2 LCD
    lines = [line[:LCD_COLS] for line in text.split("\n")[:LCD_ROWS]]
    if _lcd is not None:
        _lcd.message = "\n".join(lines)
    else:
        print("[LCD]", " | ".join(lines))

def clear_screen():
    _lcd.clear()
