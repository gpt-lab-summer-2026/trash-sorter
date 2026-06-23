import cv2
# draws bounding boxes etc

def visualizer(frame, detections):
    # 
    if not detections:
        cv2.putText(frame, "Place item in front of camera",
                    (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.0,
                    (255, 255, 255),
                    2)
        return frame
        
    for detection in detections:
        frame_drawn = cv2.putText(frame, f"{detection['label']} {detection['confidence']:.0%} -> {detection['bin']}", 
            (30, 50),           # position just above the box
            cv2.FONT_HERSHEY_SIMPLEX, # font
            0.6,                      # font scale
            (255, 0, 0),              # color
            2)  

    return frame_drawn
