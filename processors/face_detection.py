import cv2 as cv
import time

class FaceDetector:
    
    def __init__(self):
        self.frames = []
        self.start_time = time.time()
        self.cv_haar_path = cv.data.haarcascades
        self.face_cascade = cv.CascadeClassifier(self.cv_haar_path + 'haarcascade_frontalface_alt2.xml')
        self.eye_cascade = cv.CascadeClassifier(self.cv_haar_path + 'haarcascade_eye.xml')

    def detect_face(self, frame):
        faces = self.face_cascade.detectMultiScale(frame, 1.1, 10, minSize=(60, 60))

        return faces
    
    def detect_eyes(self, frame):
        eyes = self.eye_cascade.detectMultiScale(frame, 1.1, 10, minSize=(20, 20))

        return eyes