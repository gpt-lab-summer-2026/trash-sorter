
# settings etc all configs lol, in one place -> easy to change
MODEL_PATH = "models/best.onnx"  

CONFIDENCE_THRESHOLD = 0.5
MOTION_THRESHOLD = 6000        # for detecting item placement
COOLDOWN_THRESHOLD = 25000 

CAMERA_INDEX = 0  # 0 = iPhone (Continuity Camera), 1 = macbook camera
FRAME_TIME = 3 

# images resized to 384 x 512
DIM_HEIGHT = 600
DIM_WIDTH = 600

# ESP32-C6 serial connection (spherical actuator joint)
SERIAL_PORT = "/dev/ttyACM0"   # check Device Manager for the actual port
BAUD_RATE = 115200
SERIAL_TIMEOUT = 1

# servo joint limits -- must match esp32c6.ino
SERVO_BASE_US = 1300
SERVO_DEFLECT_US = 700
SERVO_ABS_MIN_US = 400
SERVO_ABS_MAX_US = 2600

# QAPASS 1602A LCD, wired directly to the Pi's GPIO pins (parallel interface,
# compatible with all Pi versions as of Jan. 2019, v1 - v3B+)
LCD_RS_PIN = "D22"
LCD_EN_PIN = "D17"
LCD_D4_PIN = "D25"
LCD_D5_PIN = "D24"
LCD_D6_PIN = "D23"
LCD_D7_PIN = "D18"
LCD_COLS = 16
LCD_ROWS = 2
