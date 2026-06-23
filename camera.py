# capture frames
from config import *
import cv2

# TO-DO: add return for function, what goes to main
def get_frame(camera_object):
    ret, frame = camera_object.read()
    if not ret:
        return None
    frame = cv2.resize(frame, (DIM_WIDTH, DIM_HEIGHT))
    return frame
            
