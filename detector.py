from ultralytics import YOLO

from config import *
from labels import *
# loads model, runs inference, returns detections

# TO-DO: load models once when starting program 
#model = config.model_path
# load model
model = YOLO(MODEL_PATH, task="classify") 

def detector(frame):
    detections = model.predict(source=frame, conf=CONFIDENCE_THRESHOLD)
    results = []
    for r in detections: # r is result object of the whole frame
        for box in r.boxes: 
            label = model.names[int(box.cls)]
            bin_name = BIN_MAPPING.get(label, DEFAULT_BIN)
            
            result = {
                "label" : label,
                "confidence" : float(box.conf),
                "bin" : bin_name,
                "box" : box.xyxy[0].tolist()
            }
            results.append(result)

    return results