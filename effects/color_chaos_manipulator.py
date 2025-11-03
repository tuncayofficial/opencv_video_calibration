import cv2 as cv
import sys
import random
import numpy as np

class ColorChaosManipulator:
    def __init__(self):
        self.frames = []
        self.processed_frames = []
        self.complexities = []
        self.threshold = None
        self.color_palettes = []
        self.effect_history = []
        self._generate_color_palettes()

    def _generate_color_palettes(self):
        self.color_palettes = [
            # Neon palette
            [(0, 255, 255), (255, 0, 255), (255, 255, 0), (0, 255, 0)],
            # Warm palette  
            [(255, 100, 0), (255, 200, 0), (255, 50, 50), (200, 100, 0)],
            # Cool palette
            [(0, 100, 255), (100, 0, 255), (0, 200, 255), (50, 50, 255)],
            # Psychedelic palette
            [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) 
             for _ in range(4)],
            # Monochrome madness
            [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))] * 4
        ]

    def calculate_complexity(self, frame):
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        return np.var(gray)
    
    def add_frame(self, frame):
        self.frames.append(frame)
        complexity = self.calculate_complexity(frame)
        self.complexities.append(complexity)

        if len(self.complexities) > 10 and self.threshold == None:
            self.threshold = np.median(self.complexities)
            print("Current ColorChaosManipulator threshold has set to " + str(self.threshold))

    def process_current_frame(self, frame, complexity):
        if self.threshold is None:  
            cv.putText(frame, "CALIBRATING...", (50, 50), 
                  cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            return frame 
        
        
        complexity = self.calculate_complexity(frame)
        self.processed_frames.append(frame)  
        
        if complexity > self.threshold:
            return self._color_blast(frame, complexity)
        else:
            return self._channel_swap(frame)
        
    def _complex_frame_effect(self, frame, complexity):
        """
        effect_type = random.choice([
            'channel_swap', 'color_blast', 'neon_edges', 
            'hue_shift', 'rgb_split', 'psychedelic'
        ])
        """

        effect_type = "color_blast"

        match effect_type:
            case "channel_swap":
                return self._channel_swap(frame)
            case "color_blast":
                return self._color_blast(frame, complexity)
            case "neon_edges":
                return self._neon_edges(frame)
            case "hue_shift":
                return self._hue_shift(frame)
            case "rgb_split":
                return self._rgb_split(frame)
            case "psychedelic":
                return self._psychedelic(frame)
    
    def _channel_swap(self, frame):
        b, g, r = cv.split(frame)
        channels = [b, g, r]
        swapped_channels = random.shuffle(channels)
        return swapped_channels
    
    def _color_blast(self, frame, complexity):
        intensity = min(0.8, complexity / (self.threshold * 2))

        color = [random.randint(0, 255) for _ in range(3)]
        overlay = np.full_like(frame, color)

        print("Applying color blast...")

        return cv.addWeighted(frame, 1 - intensity, overlay, intensity, 0)