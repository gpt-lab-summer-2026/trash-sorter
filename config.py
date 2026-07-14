
# settings etc all configs lol, in one place -> easy to change
MODEL_PATH = "models/trash_classifier_int8.tflite"  #
LABELS_PATH = "models/labels.txt"

CONFIDENCE_THRESHOLD = 0.75
MOTION_THRESHOLD = 9000        # for detecting item placement
COOLDOWN_THRESHOLD = 25000 

CAMERA_INDEX = 0  # 0 = iPhone (Continuity Camera), 1 = built-in FaceTime
FRAME_TIME = 3 

# images resized to 384 x 512
DIM_HEIGHT = 720
DIM_WIDTH = 1280

# ESP32-C6 serial connection (spherical actuator joint)
SERIAL_PORT = "/dev/cu.usbmodem11401"   # check Device Manager for the actual port
BAUD_RATE = 115200
SERIAL_TIMEOUT = 1

# servo joint limits -- must match esp32c6.ino
SERVO_BASE_US = 1300
SERVO_DEFLECT_US = 700
SERVO_ABS_MIN_US = 400
SERVO_ABS_MAX_US = 2600
