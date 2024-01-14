from ultralytics import YOLO
import cv2
import tracker as tr

class CulinaryDetector:

    def __init__(self,model_name = 'yolov8s.pt') -> None:
        self.model = YOLO(model_name)

#camera url
URL_CAMERA = 'test_2.mp4'#"http://192.168.0.241:8080/video"

# set video parameters
FRAME_WIDTH = 1280
FRAME_HEIGHT = 720
FPS = 240


cap = cv2.VideoCapture(URL_CAMERA)
if cap is None or not cap.isOpened():
    print('Error: camera is not available')


cap.set(cv2.CAP_PROP_FRAME_WIDTH,FRAME_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,FRAME_HEIGHT)
cap.set(cv2.CAP_PROP_FPS,FPS)

frame_count = 0

#read the model
culinaryDetector = CulinaryDetector('best_50.pt')
tracker = tr.Tracker()

print('START...')

while cap.isOpened():
    
    ret, frame = cap.read()

    if ret is not None:
        frame_count = cap.get(cv2.CAP_PROP_POS_FRAMES)
        frame = cv2.resize(frame,(FRAME_WIDTH,FRAME_HEIGHT))

        results = culinaryDetector.model.predict(frame,imgsz=(1088,736), device=0, conf=0.7, verbose=False)

        img = frame.copy()

        #add detection line zone
        cv2.line(img,(FRAME_WIDTH // 2,0),(FRAME_WIDTH//2,FRAME_HEIGHT),(0,255,255),8)

        print('NEW FRAME...\n')
        tracker.update(results)

        img = tracker.annotate_objects(img)

        tracker.show_stats(img)
        cv2.imshow('TEst',cv2.resize(img,(FRAME_WIDTH,FRAME_HEIGHT)))
        
        key = cv2.waitKey(0) & 0XFF
        if key == ord('q'):
            break

        """if cv2.waitKey(1) == ord('q'):
            break"""

    else:
        #return frame
        print("Lose frame...")
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_count - 1)
        cv2.waitKey(5)
        
    if cv2.waitKey(1) == ord("q"):
        break


print('STOP...')
cap.release()
cv2.destroyAllWindows()