import cv2
import numpy as np

url_camera = "http://192.168.0.241:8080/video"

cap = cv2.VideoCapture(url_camera)

while(cap.isOpened()):
    camera, frame = cap.read()
    if frame is not None:
        cv2.imshow("Frame",frame)
    
    q = cv2.waitKey(1)
    if q == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()