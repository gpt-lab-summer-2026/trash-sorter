# capture frames
from config import *
import cv2
import numpy as np

def calibrate(cam):
    frames = []
    for i in range(20):
        frame = get_frame(cam)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
        frames.append(gray.astype(np.float32))
    ref = np.mean(frames, axis=0).astype(np.uint8)
    return ref

def detect_motion(current_frame, reference_frame):
    #cv2.waitKey(500)  # wait 500ms for item to settle
    movement = False
    # convert frames to grayscale
    current_gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
    # reference_frame is already grayscale (from calibrate)
    difference = cv2.absdiff(reference_frame, current_gray)
    _, thresh = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)
    # test print
    count = cv2.countNonZero(thresh)
    print(f"Changed pixels: {count}")   

    if cv2.countNonZero(thresh) > 8000:
        movement = True
    return movement

# TO-DO: add return for function, what goes to main
def get_frame(camera_object):
    ret, frame = camera_object.read()
    if not ret:
        return None
    frame = cv2.resize(frame, (DIM_WIDTH, DIM_HEIGHT))
    return frame
            
