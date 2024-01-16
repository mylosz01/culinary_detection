import time
import threading
import cv2
import tracker as tr
import config
from ultralytics import YOLO

class VideoCaptureThreading:
    def __init__(self, src=0, width=640, height=480):
        self.src = src
        self.cap = cv2.VideoCapture(self.src)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.FRAME_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.FRAME_HEIGHT)
        self.cap.set(cv2.CAP_PROP_FPS,config.FPS)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE,10)
        self.grabbed, self.frame = self.cap.read()
        self.started = False
        self.read_lock = threading.Lock()

    def set(self, var1, var2):
        self.cap.set(var1, var2)

    def start(self):
        if self.started:
            print('[!] Thread is used.')
            return None
        self.started = True
        self.thread = threading.Thread(target=self.update, args=())
        self.thread.start()
        return self

    def update(self):
        while self.started:
            self.grabbed, self.frame = self.cap.read()
            """with self.read_lock:
                self.grabbed = grabbed
                self.frame = frame"""

    def read(self):
        """with self.read_lock:
            frame = self.frame.copy()
            grabbed = self.grabbed"""
        return self.grabbed, self.frame

    def stop(self):
        self.started = False
        self.thread.join()

    def __exit__(self):
        self.cap.release()