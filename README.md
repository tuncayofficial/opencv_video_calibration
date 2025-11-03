# OpenCV Video Calibration

A real-time video processing system that applies computer vision techniques and psychedelic effects using mathematical transformations. Transform your webcam feed into a trippy visual experience! 🌈✨

## 🌟 Features

• 🎥 Real-time Video Processing - Live webcam feed manipulation
• ⚡ Auto-calibration - Dynamic threshold detection based on scene complexity
• 🌊 Psychedelic Effects - Mathematical transformations for trippy visuals
• 🧩 Modular Architecture - Easy to extend with new effects

## 🧮 Mathematical Foundations

## Complexity Calculation
```python
def calculate_complexity(self, frame):
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    return np.var(gray) # Variation method
```

Mathematical Basis: Uses variance (σ²) to measure how "busy" a scene is:

Low variance = Flat, uniform areas (simple effects)

High variance = Detailed, textured areas (complex effects)

Dynamic Thresholding
```python
self.threshold = np.median(self.complexities)
```
Statistical Method: Uses median of recent frame complexities to adapt to different lighting conditions without being affected by outliers.

## 🚀 Installation
In order to use the library, you need to clone the repository :

```bash
# Clone the repository
git clone https://github.com/tuncayofficial/opencv_video_calibration.git

# Navigate to project directory
cd opencv_video_calibration

# Install dependencies
pip install -r requirements.txt
```

## 🎯 Quick Start
### Real-Time Video Processing 🎥
```bash
python main.py -rtm enable
```
_Process video files with live preview and real-time effects!_

### Video Rendering & Export 🎬
```bash
python main.py -render enable
```
_Render video files with mathematical transformations and export results_

## 🔮 Coming Soon
• Webcam Support - Live camera feed processing

• More Effects - Expanded mathematical transformations

• Audio Integration - Enhanced audio-video synchronization
