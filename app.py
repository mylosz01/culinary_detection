from ultralytics import YOLO
import cv2
import tracker as tr
import config
import time
from camera import VideoCaptureThreading

#camera thread object
camera = VideoCaptureThreading(src = 'test_2.mp4', width=config.FRAME_WIDTH, height= config.FRAME_HEIGHT)

#check camera
if camera is None or not camera.cap.isOpened():
    print('Error: camera is not available')

#read the model
culinaryDetector = YOLO(config.MODEL_NAME)
tracker = tr.Tracker()

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
        #imgsz=(1088,736)
        #detect objects from single frame
        results = culinaryDetector.predict(img,imgsz=(640,480), device=0, conf=0.75, verbose=False,stream_buffer=True)

        #add detection line zone
        cv2.line(img,(config.FRAME_WIDTH // 2,0),(config.FRAME_WIDTH//2,config.FRAME_HEIGHT),(0,255,255),8)

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
    frame_count += 1

    #exit loop
    if cv2.waitKey(1) == ord("q"):
       break

#close objects
camera.stop()
print(f'FPS: {(frame_count / (time.time() - start_time)):.2f}')
print('STOP...')
camera.cap.release()
cv2.destroyAllWindows()