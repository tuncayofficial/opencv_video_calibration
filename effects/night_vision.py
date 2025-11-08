import cv2 as cv
import numpy as np
import random
import time

class NightVision:
    def __init__(self):
        self.name = "NightVision Effect"

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
            self.threshold = np.mean(self.complexities)
            print("Current Tracker threshold has set to " + str(self.threshold))

    def calculate_complexity(self, frame):
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        variance = np.var(gray)

        return np.log1p(variance)

    def process_current_frame(self, frame, complexity):
        if self.threshold is None:  
            cv.putText(frame, "CALIBRATING...", (50, 50), 
                  cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            return frame 
        
        if complexity > self.threshold:
            return self._apply_night_vision(frame)
        else:
            return self._apply_night_vision(frame)

    def _night_vision_overlay(self, frame):
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        gray = cv.GaussianBlur(gray, (3, 3), 0)
        gray = cv.equalizeHist(gray)

        night_vision = cv.cvtColor(gray, cv.COLOR_GRAY2BGR)

        night_vision[:, :, 0] = 0
        night_vision[:, :, 2] = 0

        h, w = night_vision.shape[:2]
        kernel_x = cv.getGaussianKernel(w, w/3)
        kernel_y = cv.getGaussianKernel(h, h/3)
        kernel = kernel_y * kernel_x.T
        mask = kernel / kernel.max()

        night_vision = night_vision.astype(np.float32)
        night_vision *= mask[..., np.newaxis]
        night_vision = np.clip(night_vision, 0, 255).astype(np.uint8)

        return night_vision
    
    def _scan_lines(self, frame):
        result_frame = frame.copy().astype(np.float32)

        result_frame[::3, :, 0] *= 1.5
        result_frame[::3, :] *= 0.7
        
        return np.clip(result_frame.astype(np.uint8), 0, 255)
    
    def _apply_night_vision(self, frame):
        frame = self._night_vision_overlay(frame)
        #frame = self._scan_lines(frame)

        return frame