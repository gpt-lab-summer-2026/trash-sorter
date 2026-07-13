# handle the physical sorting of the trash; motors and signals to them etc whatever is needed
import time
from connect_esp import *
from config import *

def sort_trash(last_detections, esp):
    # sort according to bin, send signal to esp to move to the correct position
    if not last_detections:
        return  # no detections, nothing to sort

    # get the label of the top detection
    top_detection = last_detections[0]
    bin = top_detection["bin"]

    # determine the servo angles based on the label
    if bin == "Cans and bottles":
        deg1, deg2 = 30, -30  # example angles for plastic bin
    elif bin == "Cardboard bin":
        deg1, deg2 = -30, 30  # example angles for metal bin
    elif bin == "Plastic bin":
        deg1, deg2 = -50, -50     # example angles for paper bin
    else:
        deg1, deg2 = 50, 30     # default angles for general bin

    # Set the servo angles
    set_angle(esp, deg1, deg2)
    time.sleep(1)  # wait for the servo to move
    reset_to_base(esp)


# testing the sorting function
# if __name__ == "__main__":
#     esp = connect_esp()
#     print(read_response(esp))       # boot + ledcAttach messages
#     last_detections = [{
#         "label": "plastic_bottles",
#         "confidence": 0.9,
#         "bin": "Cans and bottles"
#     }]
#     print("Sorting trash based on last detections...")
#     sort_trash(last_detections, esp)
#     time.sleep(2)
#     last_detections = [{
#         "label": "cardboard",
#         "confidence": 0.85,
#         "bin": "Cardboard bin"
#     }]
#     print("Sorting trash based on last detections...")
#     sort_trash(last_detections, esp)
#     time.sleep(1)
#     close_esp(esp)
