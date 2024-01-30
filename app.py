from ultralytics import YOLO
import cv2
import tracker as tr
import config
import time
from camera import VideoCaptureThreading

#IP CAMERA
URL_CAMERA = 'https://10.128.122.199:8080/video'

#camera thread object
camera = VideoCaptureThreading(src = URL_CAMERA, width=config.FRAME_WIDTH, height= config.FRAME_HEIGHT)

#check available camera
if camera is None or not camera.cap.isOpened():
    print('Error: camera is not available')

#read the trained model
culinaryDetector = YOLO(config.MODEL_NAME)
tracker = tr.Tracker()

#start camera thread
print('START...')
camera.start()
frame_count = 0
start_time = time.time()

#main loop
while camera.cap.isOpened():
    
    #read frame from capture
    ret, frame = camera.read()

    if ret:
        img = cv2.resize(frame,(config.FRAME_WIDTH,config.FRAME_HEIGHT))
        
        #detect objects from single frame
        results = culinaryDetector.predict(img,imgsz=(1664,1280), device=0, conf=0.70, verbose=False, stream_buffer=True)

        #add detection line zone
        #cv2.line(img,(config.FRAME_WIDTH // 2 + tracker.zone_width,0),(config.FRAME_WIDTH//2 + tracker.zone_width,config.FRAME_HEIGHT),(122,233,54),3)
        cv2.line(img,(config.FRAME_WIDTH // 2,0),(config.FRAME_WIDTH//2,config.FRAME_HEIGHT),(0,255,255),8)
        #cv2.line(img,(config.FRAME_WIDTH // 2 - tracker.zone_width,0),(config.FRAME_WIDTH//2 - tracker.zone_width,config.FRAME_HEIGHT),(122,32,10),3)

        #update position of objects
        tracker.update(results)

        #annote detected objects
        img = tracker.annotate_objects(img)

        #show statistics
        tracker.show_stats(img)

        #display final frame
        cv2.imshow('Culinary detect app',img)
        
        #fetch one frame per press
        """key = cv2.waitKey(0) & 0XFF
        if key == ord('q'):
            break"""
        
        #reset statistic
        if cv2.waitKey(1) == ord('r'):
            tracker.reset_stats()

    frame_count += 1

    #exit loop
    if cv2.waitKey(1) == ord("q"):
       break
    

#close all objects
camera.stop()
print(f'FPS: {(frame_count / (time.time() - start_time)):.2f}')
print('STOP...')
camera.cap.release()
cv2.destroyAllWindows()