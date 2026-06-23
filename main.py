# imports
import cv2
#import config
from camera import *
from config import *
from detector import *
from visualizer import *


def main():
    # camera is open all the time so this probably in the main loop ??
    # Open the default camera
    cam = cv2.VideoCapture(CAMERA_INDEX)

    while True:
        # get frame and detections to it
        frame = get_frame(cam)
        if frame is None:
            continue
        detections = detector(frame)
        visualization = visualizer(frame, detections)
        #if visualization is None:
         #   continue
        cv2.imshow("Trash Detector", visualization)
        # Press 'q' to exit the loop
        if cv2.waitKey(1) == ord('q'):
            break
    # Release the capture and writer objects
    cam.release()
    cv2.destroyAllWindows()

# run program
if __name__=="__main__":
    main()