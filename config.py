
# settings etc all configs lol, in one place -> easy to change
MODEL_PATH = "models/trash_classifier_int8.tflite"  #
LABELS_PATH = "models/labels.txt"

CONFIDENCE_THRESHOLD = 0.75
MOTION_THRESHOLD = 9000        # for detecting item placement
COOLDOWN_THRESHOLD = 25000 

CAMERA_INDEX = 1  # 0 = iPhone (Continuity Camera), 1 = built-in FaceTime
FRAME_TIME = 3 

# images resized to 384 x 512
DIM_HEIGHT = 720
DIM_WIDTH = 1280
