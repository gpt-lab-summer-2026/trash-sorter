# imports
import cv2
import time
import sys

from camera import *
from config import *
from detector import *
from visualizer import *
from connect_esp import *
from sorter import *
from screen import *
from buttons import *

STATE_WAITING   = "waiting"
STATE_DETECTING = "detecting"
STATE_ACTION    = "action"
STATE_COOLDOWN  = "cooldown"

def main():
    # set up esp32 connection
    esp = connect_esp()
    reset_to_base(esp)
    # empty the csv file
    f = open("sorted.csv", "w")
    f.truncate()
    f.close()

    detection_amount = 0
    # Open the default camera
    cam = cv2.VideoCapture(CAMERA_INDEX)

    # wait for user to calibrate before starting the program
    reference_frame = None
    while reference_frame is None:
        frame = get_frame(cam)
        if frame is None:
            continue
        update_screen("Press the        \ncalibrate button")
        if SHOW_DISPLAY:
            msg = "Press the calibrate button"
            cv2.putText(frame, msg, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            cv2.imshow("Trash Detector", frame)
            cv2.waitKey(1)
        if calibrate_pressed():
            reference_frame = calibrate(cam)
        elif quit_pressed():
            sys.exit()

    screen = show_info_screen()
    update_screen(screen)
    
    state = STATE_WAITING
    state_start_time = None
    last_detections = []

    while True:
        # get frame and detections to it
        frame = get_frame(cam)
        if frame is None:
            continue

        if state == STATE_WAITING:
            print("STATE: WAITING") #debug
            update_screen(f"\nPlace item      ")
            if detect_motion(current_frame=frame, reference_frame=reference_frame): # check if motion
                time.sleep(1)
                state = STATE_DETECTING
                state_start_time = time.time()

        elif state == STATE_DETECTING:
            print("STATE: DETECTING") #debug
            update_screen(f"\nDetecting         ")
            # wait for item to settle before classifying
            if time.time() - state_start_time > 2.0:
                print(time)
                if detect_motion(frame, reference_frame):  # compares current frame to reference and detedts if item still in frame (true if item still in frame)
                    last_detections = detector(frame)
                    print(f"last detections: {last_detections}")
                    # TO-DO: if item not detected it should try it again couple times
                    if not last_detections:
                        # model was uncertain — default to general bin
                        last_detections = [{
                            "label": "unknown",
                            "confidence": 0.0,
                            "bin": DEFAULT_BIN
                        }]
                    state = STATE_ACTION
                    state_start_time = time.time()
                else:
                    # motion stopped before settle time — false trigger, go back
                    state = STATE_WAITING
            detection_amount += 1
                
        elif state == STATE_ACTION:
            print("STATE: ACTION") #debug
            # sort according to bin, send signal to esp to move to the correct position
            screen = show_current_item(last_detections) # show current item on screen
            update_screen(screen)
            sort_trash(last_detections, esp) # do the action of physically sorting

            if time.time() - state_start_time > 1.0:  # show result for 3 seconds
                state = STATE_COOLDOWN
                state_start_time = time.time() 
        
        elif state == STATE_COOLDOWN:
            print("STATE: COOLDOWN") #debug
            # wait for item to be removed
            time_in_cooldown = time.time() - state_start_time

            if (time_in_cooldown > 1.5):
                reference_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # just update reference silently
                state = STATE_WAITING
                last_detections = []
                screen = show_info_screen()  # update screen with new sorted item count
                update_screen(screen)
            
        if SHOW_DISPLAY:
            visualization = visualizer(frame, last_detections, state)
            cv2.imshow("Trash Detector", visualization)
            cv2.waitKey(1)

        if calibrate_pressed():
            time.sleep(5)
            reference_frame = calibrate(cam)
            state = STATE_WAITING
            last_detections = []
            state_start_time = None
            screen = show_info_screen()
            update_screen(screen)
        # press the quit button to stop the whole program
        if quit_pressed():
            clear_screen()
            break

    # Release the capture and writer objects
    cam.release()
    if SHOW_DISPLAY:
        cv2.destroyAllWindows()

# run program
if __name__=="__main__":
    main()
