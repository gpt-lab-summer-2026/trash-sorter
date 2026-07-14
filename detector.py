from ultralytics import YOLO

from config import *
from labels import *

# ---------------------------------------------------------------------------
# Load model
# ---------------------------------------------------------------------------
model = YOLO(MODEL_PATH, task="classify")


def detector(frame):
    detections = model.predict(source=frame, conf=CONFIDENCE_THRESHOLD, verbose=False)

    for r in detections:  # r is the result object for the whole frame
        top1_conf = float(r.probs.top1conf)
        if top1_conf < CONFIDENCE_THRESHOLD:
            return []  # not confident enough, show nothing

        label = model.names[int(r.probs.top1)]
        bin_name = BIN_MAPPING.get(label, DEFAULT_BIN)

        result = {
            "label": label,
            "confidence": top1_conf,
            "bin": bin_name,
        }

        print(f"Label: {label}, Confidence: {top1_conf:.2f}")

        return [result]

    return []