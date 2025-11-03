import cv2 as cv
import numpy as np
import time
import math
import random

class Calibrator:
    def __init__(self):
        self.frames = []
        self.processed_frames = []
        self.complexities = []
        self.threshold = None
        self.start_time = time.time()

    def add_frame(self, frame):
        self.frames.append(frame)
        complexity = self.calculate_complexity(frame)
        self.complexities.append(complexity)

        if len(self.complexities) > 10 and self.threshold == None:
            self.threshold = np.median(self.complexities)
            print("Current Calibrator threshold has set to " + str(self.threshold))

    def calculate_complexity(self, frame):
        small = cv.resize(frame, (160, 90))
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        return np.var(gray)

    def process_current_frame(self, frame):
        if self.threshold is None:  
            cv.putText(frame, "CALIBRATING...", (50, 50), 
                  cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            return frame 

        self.processed_frames.append(frame)  
        complexity = self.calculate_complexity(frame)
        
        if complexity > self.threshold:
            return self._complex_frame_effect(frame, complexity)
        else:
            return self._simple_frame_effect(frame, complexity)

    def _complex_frame_effect(self, frame, complexity):
        edges = cv.Canny(frame, 100, 200)
        edges_bgr = cv.cvtColor(edges, cv.COLOR_GRAY2BGR)
        return cv.addWeighted(frame, 0.5, edges_bgr, 0.5, 0)
    
    def _simple_frame_effect(self, frame, complexity):
        stylized = cv.stylization(frame, sigma_s=100, sigma_r=0.8) 
        return stylized
