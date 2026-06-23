from ultralytics import YOLO

from config import *
from labels import *
# loads model, runs inference, returns detections

# TO-DO: load models once when starting program 
#model = config.model_path
# load model
model = YOLO(MODEL_PATH, task="classify") 

def detector(frame):
    # TO-DO: run inference on the frame -> return results (list of tuples: (label, confidence, bounding_box))
    detections = model.predict(source=frame, conf=CONFIDENCE_THRESHOLD)
    results = []
    for r in detections: # r is result object of the whole frame

        label = model.names[int(r.probs.top1)]
        bin_name = BIN_MAPPING.get(label, DEFAULT_BIN)
        
        result = {
            "label" : label,
            "confidence" : float(r.probs.top1conf),
            "bin" : bin_name,
        }
        results.append(result)

    return results