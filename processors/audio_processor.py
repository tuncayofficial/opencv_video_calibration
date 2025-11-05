import cv2 as cv
import math
import numpy as np
import time

class AudioProcessor:
    
    def __init__(self, audio_path):
        self.audio_path = audio_path

        self.tempo = 0
        self.beat_timestamps = []
        self.energy_history = []

        self.frequency_bands = {}
        self.spectral_centroid = 0

        self.effect_multipliers = {
            'color_blast': 1.0,
            'hue_shift': 1.0, 
            'distortion': 1.0
        }