import numpy as np
from PIL import Image
 
try:
    import tflite_runtime.interpreter as tflite
except ImportError:
    import tensorflow.lite as tflite
 
from config import *
from labels import *
 
# ---------------------------------------------------------------------------
# Load model
# ---------------------------------------------------------------------------
interpreter = tflite.Interpreter(model_path=MODEL_PATH)
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
 
INPUT_HEIGHT = input_details[0]["shape"][1]
INPUT_WIDTH = input_details[0]["shape"][2]
INPUT_SCALE, INPUT_ZERO_POINT = input_details[0]["quantization"]
OUTPUT_SCALE, OUTPUT_ZERO_POINT = output_details[0]["quantization"]
 
# labels.txt order must match the order the model was trained on
#with open(LABELS_PATH, "r") as f:
 #   CLASS_NAMES = [line.strip() for line in f if line.strip()]
 
 
def preprocess(frame):
    """frame: BGR numpy array from OpenCV (or RGB — adjust below if needed).
    Resizes + quantizes to match the int8 model's expected input.
    """
    # If your camera frame is BGR (typical OpenCV), convert to RGB first.
    # If you're already capturing in RGB (e.g. via picamera2), remove this line.
    frame_rgb = frame[:, :, ::-1] if frame.shape[-1] == 3 else frame
 
    image = Image.fromarray(frame_rgb).resize((INPUT_WIDTH, INPUT_HEIGHT))
    arr = np.array(image, dtype=np.float32)  # EfficientNetV2B0 expects [0,255] range
 
    # Quantize to int8: int8_value = float_value / scale + zero_point
    arr = arr / INPUT_SCALE + INPUT_ZERO_POINT
    arr = np.clip(arr, -128, 127).astype(np.int8)
    return np.expand_dims(arr, axis=0)
 
 

def detector(frame):

    input_data = preprocess(frame)
    interpreter.set_tensor(input_details[0]["index"], input_data)
    interpreter.invoke()
 
    output_data = interpreter.get_tensor(output_details[0]["index"])[0]
    # Dequantize output back to real probabilities
    probs = (output_data.astype(np.float32) - OUTPUT_ZERO_POINT) * OUTPUT_SCALE
 
    top1_idx = int(np.argmax(probs))
    top1_conf = float(probs[top1_idx])
 
    if top1_conf < CONFIDENCE_THRESHOLD:
        return []  # not confident enough, show nothing
 
    sorted_probs = sorted(probs, reverse=True)
    margin = sorted_probs[0] - sorted_probs[1]

    if margin < 0.25:
        return []  # model is uncertain, reject
    
    label = CLASSES[top1_idx]
    bin_name = BIN_MAPPING.get(label, DEFAULT_BIN)
    
    result = {
        "label" : label,
        "confidence" : float(top1_conf),
        "bin" : bin_name,
    }

    print(f"Label: {label}, Confidence: {float(top1_conf):.2f}")

    return [result]