from ultralytics import YOLO

from config import *
from labels import *

# load model
model = YOLO(MODEL_PATH, task="classify") 

def detector(frame):
    # TO-DO: compare current frame to base frame to detect movement ( aka new object has been placed )
    detections = model.predict(source=frame, conf=CONFIDENCE_THRESHOLD)
    results = []
    for r in detections: # r is result object of the whole frame
        if float(r.probs.top1conf) < CONFIDENCE_THRESHOLD:
            return []  # not confident enough, show nothing
        
        probs = r.probs.data.tolist()
        sorted_probs = sorted(probs, reverse=True)
        margin = sorted_probs[0] - sorted_probs[1]

        if margin < 0.25:
            return []  # model is uncertain, reject
        
        label = model.names[int(r.probs.top1)]
        bin_name = BIN_MAPPING.get(label, DEFAULT_BIN)
        
        result = {
            "label" : label,
            "confidence" : float(r.probs.top1conf),
            "bin" : bin_name,
        }
        results.append(result)
        print(f"Label: {label}, Confidence: {float(r.probs.top1conf):.2f}")

    return results